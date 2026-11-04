"""Validación aislada: SQLite temporal y transporte HTTP simulado, sin hardware."""
import ast
import gc
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

# Permite ejecutar la validación aun sin instalar requests en este intérprete.
try:
    import requests
except ImportError:
    requests = types.ModuleType('requests')
    requests.RequestException = type('RequestException', (Exception,), {})
    requests.Response = object
    requests.get = Mock()
    requests.post = Mock()
    sys.modules['requests'] = requests

from core import database
from core.lista_negra_local import bloqueo_local
from core.seguridad import migrar_passwords, verificar_password, hashear_password
from models.alta_model import AltaModel
from models.cancelar_model import CancelarModel
from models.recarga_model import RecargaModel
from models.sustituir_model import SustituirModel
from services.sync_service import SyncService


def respuesta(data):
    return Mock(json=Mock(return_value=data), raise_for_status=Mock())


class OfflineTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        folder = Path(self.temp.name)
        self.patches = [
            patch.object(database, 'DATABASE_DIR', folder),
            patch.object(database, 'DATABASE_PATH', folder / 'temporal.db'),
            patch('services.sync_service.DATABASE_DIR', folder),
            patch.object(requests, 'get', side_effect=requests.RequestException('offline')),
            patch.object(requests, 'post', side_effect=requests.RequestException('offline')),
        ]
        for item in self.patches:
            item.start()
        database.initialize_database()
        with database.get_connection() as c:
            c.execute("INSERT INTO usuarios(username,password,role_id) VALUES ('prueba','anterior',1)")
            migrar_passwords(c)

    def tearDown(self):
        for item in reversed(self.patches):
            item.stop()
        gc.collect()
        self.temp.cleanup()

    def filas(self, sql, params=()):
        with database.get_connection() as c:
            return [dict(row) for row in c.execute(sql, params)]

    def alta(self, uid='AABBCCDD', tipo='NO'):
        AltaModel().guardar_alta_local(uid, 'Nombre original á', tipo, '311230120000', curp=uid)

    def test_altas_operador_recarga_y_rollback(self):
        self.alta()
        self.alta('11223344', 'KI')
        self.assertEqual(len(self.filas('SELECT * FROM pasajeros')), 1)
        self.assertEqual(len(self.filas('SELECT * FROM operadores')), 1)
        self.assertIsNone(self.filas("SELECT * FROM tarjetas WHERE uid='11223344'")[0]['pasajero_id'])
        self.assertNotIn('pasajero_id', [r['name'] for r in self.filas('PRAGMA table_info(operadores)')])
        for monto in (5, -5):
            with self.assertRaises(ValueError):
                RecargaModel().guardar_recarga_flexible('11223344', 'prueba', monto, 5)
        RecargaModel().guardar_recarga_flexible('AABBCCDD', 'prueba', 25, 25)
        self.assertEqual(len(self.filas('SELECT * FROM sync_queue')), 3)
        for module, action in (
            ('models.alta_model', lambda: self.alta('FFFFFFFF')),
            ('models.recarga_model', lambda: RecargaModel().guardar_recarga_flexible('AABBCCDD', 'prueba', 5, 30)),
            ('models.cancelar_model', lambda: CancelarModel().cancelar_tarjeta_flexible('AABBCCDD')),
            ('models.sustituir_model', lambda: SustituirModel().guardar_sustitucion_local(
                uid_anterior='AABBCCDD', uid_nueva='EEEEEEEE', nueva_vigencia='311230120000')),
        ):
            before = {t: self.filas('SELECT * FROM ' + t) for t in
                      ('tarjetas', 'pasajeros', 'operadores', 'recargas', 'sustituciones', 'sync_queue')}
            with patch(module + '.enqueue_sync_event', side_effect=RuntimeError('fallo cola')):
                with self.assertRaises(RuntimeError):
                    action()
            self.assertEqual(before, {t: self.filas('SELECT * FROM ' + t) for t in before})

    def test_sustitucion_y_lista_negra_local(self):
        self.alta()
        self.alta('11223344', 'KI')
        RecargaModel().guardar_recarga_flexible('AABBCCDD', 'prueba', 25, 25)
        for old, new, tipo in [('AABBCCDD', 'AABBCCEE', 'NO'), ('11223344', '11223355', 'KI')]:
            datos = self.filas('SELECT * FROM v_tarjetas_locales WHERE uid=?', (old,))[0]
            SustituirModel().guardar_sustitucion_local(uid_anterior=old, uid_nueva=new,
                nueva_vigencia='311230120000', tipo_codigo_local=tipo, datos_original=datos)
            nueva = self.filas('SELECT * FROM v_tarjetas_locales WHERE uid=?', (new,))[0]
            self.assertEqual(nueva['nombre_pasajero'], datos['nombre_pasajero'])
            self.assertEqual(nueva['curp'], datos['curp'])
            self.assertEqual(nueva['tipo_tarjeta'], datos['tipo_tarjeta'])
            self.assertEqual(nueva['saldo'], 0 if tipo == 'KI' else 25)
            self.assertTrue(bloqueo_local(old))
        cancelar = CancelarModel()
        cancelar.cancelar_tarjeta_flexible('AABBCCEE')
        self.assertTrue(bloqueo_local('aabbccee'))
        with database.get_connection() as c:
            c.execute("INSERT INTO lista_negra(uid) VALUES ('AABBCCEE')")
        cancelar.cancelar_tarjeta_flexible('AABBCCEE', en_lista_negra=False)
        self.assertIsNone(bloqueo_local('AABBCCEE'))
        self.assertFalse(cancelar.obtener_tarjeta_por_uid('AABBCCEE')['en_lista_negra'])
        self.assertFalse(RecargaModel().obtener_tarjeta_por_uid('AABBCCEE')['en_lista_negra'])

    def test_sync_uuid_orden_offline_y_compatibilidad(self):
        self.alta()
        self.alta('11223344', 'KI')
        service = SyncService()
        before = self.filas('SELECT * FROM sync_queue ORDER BY id')
        self.assertEqual(service.sync_pending_once()['state'], 'offline')
        self.assertEqual(before, self.filas('SELECT * FROM sync_queue ORDER BY id'))
        with patch.object(service, '_ping_data', return_value={'ok': True}):
            service.sync_pending_once()
            self.assertEqual(before, self.filas('SELECT * FROM sync_queue ORDER BY id'))
        with patch.object(service, '_ping_data', return_value={'ok': True, 'capabilities': ['operadores_offline_v1']}), \
             patch.object(service, '_refresh_blacklist'):
            for results in ([], [{'operation_uuid': 'ajeno', 'status': 'ok'}],
                            [{'operation_uuid': before[0]['operation_uuid'], 'status': 'error'}]):
                with patch.object(requests, 'post', return_value=respuesta({'results': results})) as post:
                    service.sync_pending_once()
                    sent = post.call_args.kwargs['json']['operations']
                    self.assertEqual([r['operation_uuid'] for r in sent], [before[0]['operation_uuid']])
                    self.assertEqual(service.count_pending(), 2)
            with patch.object(requests, 'post', return_value=respuesta({'results': [
                    {'operation_uuid': before[0]['operation_uuid'], 'status': 'already_synced'}]})):
                service.sync_pending_once()
            self.assertEqual(self.filas('SELECT * FROM sync_queue')[0]['operation_uuid'], before[1]['operation_uuid'])

    def test_lista_negra_descarga_incompleta_y_prioridad(self):
        self.alta()
        CancelarModel().cancelar_tarjeta_flexible('AABBCCDD')
        with database.get_connection() as c:
            c.execute("INSERT INTO lista_negra(uid) VALUES ('ANTERIOR')")
        service = SyncService()
        with patch.object(requests, 'get', side_effect=[respuesta({'ok': True, 'items': [
                {'uid': 'NUEVA'}], 'next_after_id': 10}), requests.RequestException('corte')]):
            with self.assertRaises(requests.RequestException):
                service._refresh_blacklist()
        self.assertEqual(self.filas('SELECT uid FROM lista_negra'), [{'uid': 'ANTERIOR'}])
        with patch.object(requests, 'get', return_value=respuesta({'ok': True, 'items': [], 'next_after_id': None})):
            service._refresh_blacklist()
        self.assertTrue(bloqueo_local('AABBCCDD'))

    def test_passwords_y_mantenimiento(self):
        password = self.filas('SELECT password FROM usuarios')[0]['password']
        self.assertNotEqual(password, 'anterior')
        self.assertTrue(verificar_password('anterior', password))
        self.assertFalse(verificar_password('incorrecta', password))
        self.assertNotEqual(hashear_password('anterior'), password)
        folder = database.DATABASE_DIR / 'fotos'
        folder.mkdir()
        pending, uploaded, original = (folder / ('a' * 32 + '.jpg'), folder / ('b' * 32 + '.jpg'), database.DATABASE_DIR / 'original.jpg')
        orphan = folder / 'sin_referencias.png'
        for path in (pending, uploaded, original, orphan):
            path.write_bytes(b'foto simulada')
        self.alta()
        RecargaModel().guardar_recarga_flexible('AABBCCDD', 'prueba', 25, 25)
        with database.get_connection() as c:
            c.execute("UPDATE sync_queue SET payload_json=?", (json.dumps({'datos_original': {'foto': str(pending)}}),))
            for path in (pending, uploaded, original):
                c.execute('INSERT INTO uploaded_photos VALUES (?, ?)', (str(path), 'pasajeros/foto.jpg'))
            c.execute("INSERT INTO sustituciones(uid_anterior,uid_nueva,saldo_transferido,sincronizada,synced_at) VALUES ('1','2',0,1,datetime('now','-31 days'))")
            c.execute("INSERT INTO sustituciones(uid_anterior,uid_nueva,saldo_transferido) VALUES ('3','4',0)")
            c.execute("UPDATE recargas SET sincronizada=1, synced_at=datetime('now','-31 days')")
        SyncService()._maintenance()
        self.assertEqual(SyncService().limpiar_tarjetas_locales_ya_subidas(), 0)
        self.assertTrue(pending.exists())
        self.assertTrue(original.exists())
        self.assertTrue(uploaded.exists())
        self.assertTrue(orphan.exists())
        self.assertEqual(len(self.filas('SELECT * FROM sustituciones')), 2)
        self.assertEqual(len(self.filas('SELECT * FROM recargas')), 1)
        self.assertEqual(len(self.filas('SELECT * FROM sync_queue')), 2)

    def test_confirmacion_retira_cola_y_conserva_historial(self):
        self.alta()
        RecargaModel().guardar_recarga_flexible('AABBCCDD', 'prueba', 25, 25)
        SustituirModel().guardar_sustitucion_local(uid_anterior='AABBCCDD',
            uid_nueva='AABBCCEE', nueva_vigencia='311230120000')
        service = SyncService()
        with patch.object(service, '_ping_data', return_value={'ok': True, 'capabilities': ['operadores_offline_v1', 'sustituciones_offline_v1']}), \
             patch.object(service, '_refresh_blacklist'):
            while service.count_pending():
                operation = self.filas('SELECT * FROM sync_queue ORDER BY id')[0]
                with patch.object(requests, 'post', return_value=respuesta({'results': [
                        {'operation_uuid': operation['operation_uuid'], 'status': 'ok'}]})):
                    self.assertEqual(service.sync_pending_once()['synced_count'], 1)
        for table in ('recargas', 'sustituciones'):
            self.assertEqual(len(self.filas('SELECT * FROM ' + table)), 1)
            self.assertEqual(self.filas('SELECT * FROM ' + table)[0]['sincronizada'], 1)

    def test_foto_ruta_original_y_envio_simulado(self):
        # Se ejecuta el método real con UI simulada, sin cargar Qt.
        tree = ast.parse(Path('controllers/app_controller.py').read_text(encoding='utf-8'))
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'AppController')
        method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == '_seleccionar_foto_alta')
        module = ast.Module(body=[ast.ClassDef(name='Controller', bases=[], keywords=[], body=[method], decorator_list=[])], type_ignores=[])
        original = database.DATABASE_DIR / 'seleccionada.PNG'
        contenido = b'archivo original sin conversion\x00\xff'
        original.write_bytes(contenido)
        class UI:
            fotoimagen = Mock()
        namespace = {'Path': Path, 'QFileDialog': Mock(),
                     'QMessageBox': Mock(), 'QPixmap': Mock(), 'AltaWindow': UI,
                     'Ui_AltaOWindow': type('OperadorUI', (), {}),
                     '__file__': str(database.DATABASE_DIR / 'controllers' / 'app_controller.py')}
        namespace['QFileDialog'].getOpenFileName.return_value = (str(original), '')
        exec(compile(ast.fix_missing_locations(module), '<seleccion real>', 'exec'), namespace)
        controller = namespace['Controller']()
        controller.current_ui = UI()
        controller.current_window = None
        controller._seleccionar_foto_alta()
        self.assertEqual(Path(controller.foto_alta_path), original)
        self.assertFalse((database.DATABASE_DIR / 'data' / 'fotos').exists())
        self.assertEqual(original.read_bytes(), contenido)
        namespace['QMessageBox'].warning.assert_not_called()
        AltaModel().guardar_alta_local('AABBCCDD', 'Foto', 'NO', '311230120000',
                                      curp='FOTO', foto=str(original))
        self.assertEqual(self.filas('SELECT foto FROM pasajeros')[0]['foto'], str(original))
        row = self.filas('SELECT * FROM sync_queue')[0]
        operation = dict(row, payload=json.loads(row['payload_json']))
        with self.assertRaises(requests.RequestException):
            SyncService()._prepare_photo(operation)
        self.assertEqual(json.loads(self.filas('SELECT * FROM sync_queue')[0]['payload_json'])['foto'], str(original))
        def subir(*args, **kwargs):
            self.assertEqual(kwargs['files']['foto'][1].read(), contenido)
            return respuesta({'ok': True, 'path': 'pasajeros/foto.PNG'})
        with patch.object(requests, 'post', side_effect=subir):
            SyncService()._prepare_photo(operation)
        self.assertEqual(operation['payload']['foto'], 'pasajeros/foto.PNG')
        self.assertEqual(json.loads(self.filas('SELECT * FROM sync_queue')[0]['payload_json'])['foto'], 'pasajeros/foto.PNG')
        # Solo la confirmación del UUID retira el alta y actualiza al titular.
        service = SyncService()
        with patch.object(service, '_ping_data', return_value={'ok': True, 'capabilities': ['operadores_offline_v1']}), \
             patch.object(service, '_refresh_blacklist'), \
             patch.object(requests, 'post', return_value=respuesta({'results': [
                 {'operation_uuid': row['operation_uuid'], 'status': 'ok'}]})):
            self.assertEqual(service.sync_pending_once()['synced_count'], 1)
        self.assertEqual(self.filas('SELECT foto FROM pasajeros')[0]['foto'], 'pasajeros/foto.PNG')
        self.assertFalse(self.filas('SELECT * FROM sync_queue'))
        service._maintenance()
        self.assertEqual(original.read_bytes(), contenido)

    def test_controlador_saldo_sin_recarga_duplicada(self):
        # Ejecuta los métodos reales con serial, temporizador y UI simulados.
        source = Path('controllers/app_controller.py').read_text(encoding='utf-8')
        tree = ast.parse(source)
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'AppController')
        names = {'_continuar_sustitucion_con_saldo', '_procesar_saldo_para_sustitucion',
                 '_verificar_saldo_sustitucion', '_finalizar_sustitucion_local', '_guardar_sustitucion_confirmada',
                 '_procesar_confirmacion_saldo_sustitucion'}
        methods = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name in names]
        self.assertEqual(len(methods), len(names))
        module = ast.Module(body=[ast.ClassDef(name='Controller', bases=[], keywords=[], body=methods, decorator_list=[])], type_ignores=[])
        namespace = {'QTimer': Mock(), 'QMessageBox': Mock(), 'traceback': Mock()}
        exec(compile(ast.fix_missing_locations(module), '<controller real>', 'exec'), namespace)
        controller = namespace['Controller']()
        controller.arduino = Mock()
        controller.current_window = None
        controller.sustituir_model = SustituirModel()
        controller._sincronizar_pendientes = Mock()
        controller._limpiar_formulario_sustituir = Mock()
        controller._normalizar_uid = lambda uid: uid.strip().upper()
        self.alta()
        RecargaModel().guardar_recarga_flexible('AABBCCDD', 'prueba', 25, 25)
        datos = self.filas('SELECT * FROM v_tarjetas_locales')[0]
        controller.sustituir_pendiente = dict(uid_anterior='AABBCCDD', uid_nueva='AABBCCEE',
            nueva_vigencia='311230120000', nombre_pasajero='Alias corto', tipo_codigo_local='NO',
            datos_original=datos, saldo_objetivo_centavos=2500, fase='esperando_nombre')
        controller._continuar_sustitucion_con_saldo()
        self.assertFalse(self.filas('SELECT * FROM sustituciones'))
        controller._procesar_saldo_para_sustitucion(5423)
        controller.arduino.enviar_linea.assert_not_called()
        self.assertFalse(self.filas('SELECT * FROM sustituciones'))
        avisar = namespace['QTimer'].singleShot.call_args.args[1]
        avisar()
        mensaje = namespace['QMessageBox'].warning.call_args.args[2]
        self.assertIn('$54.23', mensaje)
        self.assertIn('$25.00', mensaje)
        controller._procesar_saldo_para_sustitucion(0)
        controller.arduino.enviar_linea.assert_called_once_with('rc,AABBCCEE,2500')
        controller._verificar_saldo_sustitucion()
        controller._procesar_saldo_para_sustitucion(0)
        controller.arduino.enviar_linea.assert_called_once()
        self.assertFalse(self.filas('SELECT * FROM sustituciones'))
        for trama in ('ok,AABBCCFF,2500,123', 'ok,AABBCCEE,0,123',
                      'ok,AABBCCEE,invalido,123', 'ok,AABBCCEE'):
            controller._procesar_confirmacion_saldo_sustitucion(trama)
        self.assertFalse(self.filas('SELECT * FROM sustituciones'))
        controller._procesar_confirmacion_saldo_sustitucion('ok,AABBCCEE,2500,123')
        self.assertEqual(len(self.filas('SELECT * FROM sustituciones')), 1)
        pendientes = self.filas("SELECT * FROM sync_queue WHERE event_type='sustitucion_tarjeta'")
        self.assertEqual(len(pendientes), 1)
        self.assertEqual(pendientes[0]['status'], 'pending')
        controller._procesar_confirmacion_saldo_sustitucion('ok,AABBCCEE,2500,123')
        self.assertEqual(len(self.filas('SELECT * FROM sustituciones')), 1)
        self.assertEqual(self.filas("SELECT * FROM v_tarjetas_locales WHERE uid='AABBCCEE'")[0]['nombre_pasajero'], 'Nombre original á')
        self.alta('11223344', 'KI')
        controller.sustituir_pendiente = dict(uid_anterior='11223344', uid_nueva='11223355',
            nueva_vigencia='311230120000', nombre_pasajero='Operador', tipo_codigo_local='KI',
            datos_original=self.filas("SELECT * FROM v_tarjetas_locales WHERE uid='11223344'")[0],
            saldo_objetivo_centavos=0, fase='esperando_nombre')
        controller._continuar_sustitucion_con_saldo()
        controller.arduino.enviar_linea.assert_called_once()
        self.assertEqual(len(self.filas('SELECT * FROM sustituciones')), 2)

    def test_recarga_respuesta_perdida_y_confirmacion_duplicada(self):
        tree = ast.parse(Path('controllers/app_controller.py').read_text(encoding='utf-8'))
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'AppController')
        methods = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name in
                   {'_procesar_saldo_recarga', '_procesar_respuesta_recarga', '_ejecutar_recarga'}]
        module = ast.Module(body=[ast.ClassDef(name='Controller', bases=[], keywords=[], body=methods, decorator_list=[])], type_ignores=[])
        namespace = {'QTimer': Mock(), 'QMessageBox': Mock()}
        exec(compile(ast.fix_missing_locations(module), '<controller real>', 'exec'), namespace)
        controller = namespace['Controller']()
        controller.current_ui = Mock()
        controller.current_window = None
        controller.current_username = 'prueba'
        controller.uid_actual = 'AABBCCDD'
        controller.recarga_model = RecargaModel()
        controller.arduino = Mock()
        controller._normalizar_uid = lambda uid: uid.upper()
        controller._fallo_recarga = Mock()
        controller._sincronizar_pendientes = Mock()
        controller._limpiar_mensaje_recarga_exitosa = Mock()
        controller._campo_monto_recarga = Mock()
        controller._actualizar_estado_vencimiento_tarjeta = Mock()
        controller._parsear_trama_saldo = Mock(return_value={
            'uid': 'AABBCCDD', 'saldo_centavos': 2500})
        self.alta()
        controller._recarga_en_curso = dict(uid='AABBCCDD', objetivo=2500, monto=2500,
                                          nombre='Nombre original á', oficina='Prueba')
        controller._ejecutar_recarga()
        controller.arduino.enviar_linea.assert_not_called()
        controller._procesar_saldo_recarga('sldo,AABBCCDD,2500,Nombre')
        controller._fallo_recarga.assert_not_called()
        self.assertIsNone(controller._recarga_en_curso)
        self.assertEqual(len(self.filas('SELECT * FROM recargas')), 1)
        controller._procesar_respuesta_recarga('ok,AABBCCDD,2500,123')
        self.assertEqual(len(self.filas('SELECT * FROM recargas')), 1)

    def test_migracion_operador_existente_conserva_cola_y_usuario(self):
        from core.operadores_local import migrar_operadores
        respaldo = database.DATABASE_DIR / 'matehuala_antes_operadores_separados.db'
        self.assertFalse(respaldo.exists())
        respaldo.write_bytes(b'respaldo existente')
        self.alta('11223344', 'KI')
        before = self.filas('SELECT * FROM sync_queue')
        with database.get_connection() as c:
            c.execute('ALTER TABLE operadores ADD COLUMN pasajero_id INTEGER')
            pasajero_id = c.execute("INSERT INTO pasajeros(nombre,documento,curp) VALUES ('Legado','-','LEGADO')").lastrowid
            c.execute('UPDATE operadores SET pasajero_id=?', (pasajero_id,))
            c.execute('UPDATE tarjetas SET pasajero_id=?', (pasajero_id,))
            c.execute("DELETE FROM local_migrations WHERE nombre='operadores_separados_v1'")
        migrar_operadores()
        self.assertEqual(respaldo.read_bytes(), b'respaldo existente')
        self.assertEqual(before, self.filas('SELECT * FROM sync_queue'))
        self.assertEqual(len(self.filas('SELECT * FROM operadores')), 1)
        self.assertFalse(self.filas('SELECT * FROM pasajeros'))
        self.assertIsNone(self.filas('SELECT * FROM tarjetas')[0]['pasajero_id'])
        self.assertTrue(verificar_password('anterior', self.filas('SELECT password FROM usuarios')[0]['password']))
        self.assertFalse(self.filas('PRAGMA foreign_key_check'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
