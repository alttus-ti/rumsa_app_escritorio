"""DE en SQLite temporal, controlador simulado y HTTP bloqueado/simulado."""
import ast
import json
from pathlib import Path
import re
import unittest
import uuid
from unittest.mock import Mock, patch

import test_offline as offline
from test_offline import requests, respuesta
from core import database
from core.sync_queue import enqueue_sync_event
from models.alta_model import AltaModel
from models.cancelar_model import CancelarModel
from models.recarga_model import RecargaModel
from models.sustituir_model import SustituirModel
from services.sync_service import SyncService


class UI:
    def __init__(self):
        for nombre in (
            'texto1', 'texto2', 'texto4', 'texto5', 'texto6', 'texto7',
            'botonrecargar', 'lineEdit', 'textonombre', 'textocurp',
            'textofechanacimiento', 'calendario', 'normal', 'textomotivo', 'listanegra',
        ):
            setattr(self, nombre, Mock())
        self.calendario.selectedDate.return_value.toString.return_value = '311230'
        self.textonombre.toPlainText.return_value = 'Nombre de prueba'
        self.textocurp.toPlainText.return_value = 'CURPPRUEBADE'
        self.textofechanacimiento.toPlainText.return_value = '01-01-1990'
        self.texto7.property.return_value = 'info'


class PersonalUI(UI):
    pass


class DespachadorTest(unittest.TestCase):
    # Reutiliza exclusivamente las utilidades de aislamiento, sin heredar sus tests.
    setUp = offline.OfflineTest.setUp
    tearDown = offline.OfflineTest.tearDown
    filas = offline.OfflineTest.filas
    alta = offline.OfflineTest.alta

    def eventos(self):
        return [dict(fila, payload=json.loads(fila['payload_json']))
                for fila in self.filas('SELECT * FROM sync_queue ORDER BY id')]

    def controlador(self):
        fuente = Path('controllers/app_controller.py').read_text(encoding='utf-8')
        clase = next(n for n in ast.parse(fuente).body if isinstance(n, ast.ClassDef))
        nombres = {
            '_normalizar_uid', '_parsear_trama_saldo', '_procesar_saldo_recarga',
            '_bloquear_recarga_operador', '_aplicar_bloqueo_lista_negra_recarga',
            '_ejecutar_recarga', '_ejecutar_alta', '_guardar_alta_local_confirmada',
            '_mostrar_datos_tarjeta_cancelar', '_ejecutar_cancelar',
            '_ejecutar_sustitucion', '_continuar_sustitucion_con_saldo',
            '_finalizar_sustitucion_local', '_guardar_sustitucion_confirmada',
        }
        metodos = [n for n in clase.body if isinstance(n, ast.FunctionDef) and n.name in nombres]
        modulo = ast.Module(body=[ast.ClassDef(name='Controller', bases=[], keywords=[],
                                              body=metodos, decorator_list=[])], type_ignores=[])
        namespace = dict(RecargaWindow=UI, CancelarWindow=UI, SustituirWindow=UI,
                         AltaWindow=UI, Ui_AltaOWindow=PersonalUI,
                         QMessageBox=Mock(), QTimer=Mock(), QDateTime=Mock(),
                         traceback=Mock(), re=re)
        namespace['QDateTime'].currentDateTime.return_value.toString.return_value = '120000'
        exec(compile(ast.fix_missing_locations(modulo), '<controlador real DE>', 'exec'), namespace)
        c = namespace['Controller']()
        c.UID_RE = re.compile(r'^[0-9A-F]{8,20}$')
        c.current_ui = UI()
        c.current_window = None
        c.current_username = 'prueba'
        c.arduino = Mock()
        c.tipo_actual = ''
        c.uid_actual = 'AABBCCDD'
        c.nombre_actual = 'Nombre de prueba'
        c.saldo_actual_centavos = 0
        c.monto_pendiente_centavos = 0
        c.tarjeta_bloqueada = False
        c.tarjeta_vencida = False
        c._recarga_en_curso = None
        c._campo_monto_recarga = Mock(return_value=c.current_ui.lineEdit)
        c._texto_monto_recarga = Mock(return_value='25')
        c._oficina_seleccionada_recarga = Mock(return_value='Oficina de prueba')
        c._actualizar_estado_vencimiento_tarjeta = Mock()
        c._fallo_recarga = Mock()
        c._preview_saldo_nuevo = Mock()
        c._sincronizar_pendientes = Mock()
        c._limpiar_formulario_sustituir = Mock()
        c._limpiar_forulario_alta = Mock()
        c._set_curp_status_alta = Mock()
        c._limpiar_alias_para_arduino = Mock(return_value='Nombre de prueba')
        c._ajustar_alias_para_comando_alta = Mock(return_value='Nombre de prueba')
        return c, namespace

    def test_catalogo_y_altas_conservan_los_cuatro_tipos(self):
        for uid, tipo in [('AABBCCDD', 'NO'), ('11223344', 'EU'),
                          ('22334455', 'KI'), ('33445566', 'DE')]:
            self.alta(uid, tipo)
        self.assertEqual(len(self.filas('SELECT * FROM pasajeros')), 2)
        self.assertEqual(len(self.filas('SELECT * FROM operadores')), 1)
        self.assertEqual(len(self.filas('SELECT * FROM despachadores')), 1)
        self.assertEqual([e['payload']['tipo_codigo_local'] for e in self.eventos()],
                         ['NO', 'EU', 'KI', 'DE'])
        de = self.filas("SELECT * FROM v_tarjetas_locales WHERE uid='33445566'")[0]
        self.assertEqual((de['tipo_tarjeta'], de['entidad'], de['saldo'], de['pasajero_id']),
                         ('Despachador', 'despachador', 0, None))
        database.initialize_database()
        self.assertEqual(len(self.filas("SELECT * FROM tipo_tarjetas WHERE clave='despachador'")), 1)
        self.assertEqual(len(self.filas('SELECT * FROM tarjetas')), 4)
        self.assertEqual(len(self.eventos()), 4)

    def test_recargas_y_descuentos_prohibidos_para_de_y_ki(self):
        for uid, tipo in [('AABBCCDD', 'DE'), ('11223344', 'KI')]:
            self.alta(uid, tipo)
            for monto in (25, -5):
                with self.assertRaisesRegex(ValueError, 'no admiten recargas'):
                    RecargaModel().guardar_recarga_flexible(uid, 'prueba', monto, 25)
        self.assertFalse(self.filas('SELECT * FROM recargas'))
        self.assertEqual(len(self.eventos()), 2)
        self.assertTrue(all(r['saldo'] == 0 for r in self.filas('SELECT * FROM tarjetas')))

    def test_no_y_eu_conservan_recarga_y_saldo_en_sustitucion(self):
        for uid, nueva, tipo, descripcion in [
            ('AABBCCDD', 'AABBCCEE', 'NO', 'Normal'),
            ('11223344', '11223355', 'EU', 'Preferencial'),
        ]:
            self.alta(uid, tipo)
            RecargaModel().guardar_recarga_flexible(uid, 'prueba', 35, 35)
            SustituirModel().guardar_sustitucion_local(
                uid_anterior=uid, uid_nueva=nueva, nueva_vigencia='311230120000',
                tipo_codigo_local=tipo)
            tarjeta = self.filas('SELECT * FROM v_tarjetas_locales WHERE uid=?', (nueva,))[0]
            self.assertEqual((tarjeta['tipo_tarjeta'], tarjeta['saldo'], tarjeta['entidad']),
                             (descripcion, 35, 'pasajero'))
            self.assertEqual(self.eventos()[-1]['payload']['tipo_codigo_local'], tipo)

    def test_cancelacion_y_reactivacion_de_conservan_tipo(self):
        self.alta(tipo='DE')
        modelo = CancelarModel()
        modelo.cancelar_tarjeta_flexible('AABBCCDD', motivo_baja='Prueba')
        self.assertTrue(self.filas('SELECT en_lista_negra FROM tarjetas')[0]['en_lista_negra'])
        modelo.cancelar_tarjeta_flexible('AABBCCDD', en_lista_negra=False)
        self.assertFalse(self.filas('SELECT en_lista_negra FROM tarjetas')[0]['en_lista_negra'])
        for evento in self.eventos():
            self.assertEqual(evento['payload']['tipo_codigo_local'], 'DE')
            self.assertEqual(evento['payload']['entidad'], 'despachador')
        self.assertEqual(len(self.filas('SELECT * FROM despachadores')), 1)
        self.assertFalse(self.filas('SELECT * FROM operadores'))
        self.assertFalse(self.filas('SELECT * FROM pasajeros'))

    def test_cancelacion_de_sin_registro_local_crea_operador(self):
        CancelarModel().cancelar_tarjeta_flexible('AABBCCDD', nombre_pasajero='Despachador',
                                                tipo_codigo_local='de')
        self.assertEqual(len(self.filas('SELECT * FROM despachadores')), 1)
        self.assertFalse(self.filas('SELECT * FROM operadores'))
        self.assertFalse(self.filas('SELECT * FROM pasajeros'))
        self.assertEqual(self.filas('SELECT tipo_tarjeta FROM v_tarjetas_locales')[0]['tipo_tarjeta'],
                         'Despachador')
        self.assertEqual(self.eventos()[0]['payload']['tipo_codigo_local'], 'DE')

    def test_sustitucion_local_de_infiere_tipo_y_no_transfiere_saldo(self):
        self.alta(tipo='DE')
        # Una lectura/importación inconsistente no habilita transferencias para DE.
        with database.get_connection() as c:
            c.execute('UPDATE tarjetas SET saldo=125')
        datos = self.filas('SELECT * FROM v_tarjetas_locales')[0]
        SustituirModel().guardar_sustitucion_local(uid_anterior='AABBCCDD', uid_nueva='11223344',
                                                  nueva_vigencia='311230120000', datos_original=datos)
        nueva = self.filas("SELECT * FROM v_tarjetas_locales WHERE uid='11223344'")[0]
        self.assertEqual((nueva['tipo_tarjeta'], nueva['entidad'], nueva['saldo']),
                         ('Despachador', 'despachador', 0))
        self.assertEqual((nueva['nombre_pasajero'], nueva['curp']),
                         (datos['nombre_pasajero'], datos['curp']))
        self.assertTrue(self.filas("SELECT en_lista_negra FROM tarjetas WHERE uid='AABBCCDD'")[0]['en_lista_negra'])
        self.assertEqual(self.eventos()[-1]['payload']['tipo_codigo_local'], 'DE')
        self.assertEqual(self.eventos()[-1]['payload']['saldo_transferido'], 0)
        self.assertFalse(self.filas('PRAGMA foreign_key_check'))

    def test_sustitucion_remota_de_no_se_convierte_en_no_o_ki(self):
        for index, tipo_erroneo in enumerate(('NO', 'KI')):
            vieja, nueva = f'{index + 1:08X}', f'{index + 11:08X}'
            datos = dict(tipo_tarjeta='Despachador', nombre_pasajero='Personal',
                         curp=f'CURP{index}', saldo=120, documento='-', foto='foto.png')
            SustituirModel().guardar_sustitucion_local(
                uid_anterior=vieja, uid_nueva=nueva, nueva_vigencia='311230120000',
                tipo_codigo_local=tipo_erroneo, datos_original=datos)
            nueva_fila = self.filas('SELECT * FROM v_tarjetas_locales WHERE uid=?', (nueva,))[0]
            self.assertEqual((nueva_fila['tipo_tarjeta'], nueva_fila['saldo']), ('Despachador', 0))
            self.assertEqual(self.eventos()[-1]['payload']['tipo_codigo_local'], 'DE')
        self.assertEqual(len(self.filas('SELECT * FROM despachadores')), 2)
        self.assertFalse(self.filas('SELECT * FROM operadores'))
        self.assertFalse(self.filas('SELECT * FROM pasajeros'))

    def test_cola_sin_titular_no_duplica_uuid_ni_pierde_de(self):
        payload = {'tipo_codigo_local': 'DE'}
        with database.get_connection() as c, patch('core.sync_queue.uuid.uuid4', wraps=uuid.uuid4) as nuevo:
            operation_uuid = enqueue_sync_event(c, event_type='alta_tarjeta',
                                                entity_uid='AABBCCDD', payload=payload)
            nuevo.assert_called_once()
            enqueue_sync_event(c, event_type='prueba', entity_uid=None, payload={})
        self.assertEqual(payload, {'tipo_codigo_local': 'DE'})
        evento = self.eventos()[0]
        self.assertEqual(evento['operation_uuid'], operation_uuid)
        self.assertEqual(evento['payload'], {'tipo_codigo_local': 'DE', 'entidad': 'despachador'})
        self.assertEqual(len(self.eventos()), 2)

    def test_rollback_de_conserva_datos_si_falla_la_cola(self):
        self.alta(tipo='DE')
        tablas = ('tarjetas', 'pasajeros', 'operadores', 'despachadores', 'sync_queue', 'sustituciones')
        for modulo, accion in (
            ('models.alta_model', lambda: self.alta('11223344', 'DE')),
            ('models.cancelar_model', lambda: CancelarModel().cancelar_tarjeta_flexible('AABBCCDD')),
            ('models.sustituir_model', lambda: SustituirModel().guardar_sustitucion_local(
                uid_anterior='AABBCCDD', uid_nueva='22334455', nueva_vigencia='311230120000')),
        ):
            antes = {t: self.filas('SELECT * FROM ' + t) for t in tablas}
            with patch(modulo + '.enqueue_sync_event', side_effect=RuntimeError('cola simulada')):
                with self.assertRaises(RuntimeError):
                    accion()
            self.assertEqual(antes, {t: self.filas('SELECT * FROM ' + t) for t in tablas})

    def test_respuestas_simuladas_reconocen_codigo_de(self):
        item = dict(uid='AABBCCDD', tipo_codigo_local='DE', tipo_tarjeta_id=17, nombre='Personal')
        recarga = RecargaModel()._normalizar_tarjeta_servidor(item)
        cancelar = CancelarModel()._normalizar_tarjeta_servidor(item)
        sustituir = SustituirModel()._normalizar_item_busqueda(item)
        self.assertEqual([x['tipo_tarjeta'] for x in (recarga, cancelar, sustituir)],
                         ['Despachador'] * 3)
        self.assertEqual(recarga['tipo_tarjeta_id'], 17)
        self.assertEqual(item['tipo_codigo_local'], 'DE')

    def test_lote_http_simulado_conserva_de(self):
        self.alta(tipo='DE')
        evento = self.eventos()[0]
        servicio = SyncService()
        with patch.object(servicio, '_ping_data', return_value={
                'ok': True, 'capabilities': ['despachadores_offline_v1']}), \
             patch.object(servicio, '_refresh_blacklist'), \
             patch.object(requests, 'post', return_value=respuesta({'results': [{
                 'operation_uuid': evento['operation_uuid'], 'status': 'ok'}]})) as post:
            resultado = servicio.sync_pending_once()
        enviado = post.call_args.kwargs['json']['operations'][0]
        self.assertEqual(enviado['payload']['tipo_codigo_local'], 'DE')
        self.assertEqual(enviado['payload']['entidad'], 'despachador')
        self.assertEqual(resultado['synced_count'], 1)

    def test_controlador_bloquea_de_fisico_y_consultado(self):
        for fisico, descripcion in [('DE', None), ('', 'Despachador'), ('', 'DE'), ('KI', None)]:
            c, _ = self.controlador()
            c.recarga_model = Mock()
            c.recarga_model.obtener_tarjeta_por_uid.return_value = (
                dict(tipo_tarjeta=descripcion, en_lista_negra=0) if descripcion else None)
            c._procesar_saldo_recarga(f'sldo,AABBCCDD,0,Nombre,{fisico}')
            esperado = 'KI' if fisico == 'KI' else 'DE'
            self.assertEqual(c.tipo_actual, esperado)
            c._ejecutar_recarga()
            c.arduino.enviar_linea.assert_not_called()
            c.current_ui.texto6.setText.assert_called_with('Operador' if esperado == 'KI' else 'Despachador')
            c._aplicar_bloqueo_lista_negra_recarga(False)
            c.current_ui.botonrecargar.setEnabled.assert_called_with(False)

    def test_controlador_restaura_lista_negra_y_conserva_recarga_no(self):
        for bloqueada in (1, 0):
            c, ns = self.controlador()
            c.tipo_actual = 'NO'
            c.recarga_model = Mock()
            c.recarga_model.obtener_tarjeta_por_uid.return_value = dict(
                tipo_tarjeta='Normal', en_lista_negra=bloqueada)
            c._ejecutar_recarga()
            if bloqueada:
                c.arduino.enviar_linea.assert_not_called()
                self.assertEqual(ns['QMessageBox'].warning.call_args.args[1], 'Tarjeta en lista negra')
            else:
                c.arduino.enviar_linea.assert_called_once_with('rc,AABBCCDD,2500')

    def test_controlador_alta_personal_de_y_ki_mantiene_codigo(self):
        for despachador in (True, False):
            c, _ = self.controlador()
            c.current_ui = PersonalUI()
            c.current_ui.normal.isChecked.return_value = despachador
            c.uid_alta_actual = 'AABBCCDD'
            c._leer_serial_alta = Mock()
            c.foto_alta_path = ''
            c.alta_model = Mock()
            c.alta_model.buscar_curp_local.return_value = None
            c.alta_model.buscar_curp_servidor.return_value = None
            c._ejecutar_alta()
            codigo = 'DE' if despachador else 'KI'
            self.assertEqual(c.arduino.enviar_linea.call_args.args[0].split(',')[3], codigo)
            self.assertEqual(c.alta_pendiente['tipo'], codigo)
            self.assertTrue(c._guardar_alta_local_confirmada())
            self.assertEqual(c.alta_model.guardar_alta_local.call_args.kwargs['tipo'], codigo)

    def test_controlador_cancelacion_identifica_de_desde_consulta(self):
        c, _ = self.controlador()
        c.tipo_cancelar_actual = ''
        c.uid_cancelar_actual = 'AABBCCDD'
        c.current_ui.textomotivo.toPlainText.return_value = 'Prueba'
        c._mostrar_datos_tarjeta_cancelar(dict(nombre_pasajero='Personal', motivo_baja='',
                                             en_lista_negra=0, tipo_tarjeta='Despachador'))
        self.assertEqual(c.tipo_cancelar_actual, 'DE')
        c.cancelar_model = CancelarModel()
        c._ejecutar_cancelar()
        self.assertEqual(self.eventos()[0]['payload']['tipo_codigo_local'], 'DE')
        self.assertFalse(self.filas('SELECT * FROM pasajeros'))

    def test_controlador_sustitucion_de_no_envia_recarga_ni_se_convierte(self):
        self.alta(tipo='DE')
        c, ns = self.controlador()
        c.sustituir_model = SustituirModel()
        c.sustituir_pendiente = None
        c.uid_sustituir_original = 'AABBCCDD'
        c.tarjeta_sustituir_seleccionada = self.filas('SELECT * FROM v_tarjetas_locales')[0]
        def leer(*args):
            c.uid_sustituir_nueva = '11223344'
        c._leer_serial_sustituir = Mock(side_effect=leer)
        c._ejecutar_sustitucion()
        self.assertEqual(c.sustituir_pendiente['tipo_codigo_local'], 'DE')
        self.assertEqual(c.sustituir_pendiente['saldo_objetivo_centavos'], 0)
        self.assertEqual(c.arduino.enviar_linea.call_args.args[0].split(',')[3], 'DE')
        c._continuar_sustitucion_con_saldo()
        c.arduino.enviar_linea.assert_called_once()
        self.assertIsNone(c.sustituir_pendiente)
        self.assertEqual(self.eventos()[-1]['payload']['tipo_codigo_local'], 'DE')
        self.assertEqual(self.filas("SELECT tipo_tarjeta FROM v_tarjetas_locales WHERE uid='11223344'")[0]['tipo_tarjeta'],
                         'Despachador')
        ns['QMessageBox'].critical.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)
