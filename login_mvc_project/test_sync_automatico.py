"""Contrato de sincronización: SQLite temporal y HTTP simulado, sin servidor real."""
import ast
import json
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

import test_offline as offline
from core import database
from models.cancelar_model import CancelarModel
from models.recarga_model import RecargaModel
from models.sustituir_model import SustituirModel
from services.sync_service import SyncService


class SincronizacionTest(unittest.TestCase):
    setUp = offline.OfflineTest.setUp
    tearDown = offline.OfflineTest.tearDown
    filas = offline.OfflineTest.filas
    alta = offline.OfflineTest.alta

    def servicio(self, capacidades=None):
        servicio = SyncService()
        servicio._ping_data = Mock(return_value={'ok': True, **(
            {'capabilities': capacidades} if capacidades is not None else {})})
        servicio._refresh_blacklist = Mock()
        return servicio

    def confirmar(self, *args, **kwargs):
        return offline.respuesta({'results': [
            {'operation_uuid': op['operation_uuid'], 'status': 'ok'}
            for op in kwargs['json']['operations']]})

    def test_ping_sin_capacidades_envia_no_y_eu(self):
        self.alta()
        self.alta('11223344', 'EU')
        with patch.object(offline.requests, 'post', side_effect=self.confirmar) as post:
            resultado = self.servicio().sync_pending_once()
        self.assertEqual(resultado['synced_count'], 2)
        self.assertEqual(post.call_count, 2)
        self.assertFalse(self.filas('SELECT * FROM sync_queue'))

    def test_personal_sin_soporte_no_bloquea_otras_tarjetas(self):
        self.alta('11223344', 'DE')
        self.alta('22334455', 'KI')
        self.alta('33445566', 'NO')
        antes = self.filas('SELECT * FROM sync_queue ORDER BY id')
        with patch.object(offline.requests, 'post', side_effect=self.confirmar) as post:
            resultado = self.servicio().sync_pending_once()
        self.assertEqual(resultado['synced_count'], 1)
        post.assert_called_once()
        self.assertEqual(post.call_args.kwargs['json']['operations'][0]['entity_uid'], '33445566')
        restantes = self.filas('SELECT * FROM sync_queue ORDER BY id')
        self.assertEqual(len(restantes), 2)
        for original, actual in zip(antes, restantes):
            self.assertEqual(actual['operation_uuid'], original['operation_uuid'])
            self.assertEqual(actual['payload_json'], original['payload_json'])
            self.assertEqual(actual['retries'], original['retries'])
            self.assertEqual(actual['status'], 'waiting_api')

    def test_capacidad_ki_no_implica_soporte_de(self):
        self.alta('11223344', 'DE')
        self.alta('22334455', 'KI')
        with patch.object(offline.requests, 'post', side_effect=self.confirmar) as post:
            resultado = self.servicio(['operadores_offline_v1']).sync_pending_once()
        self.assertEqual(resultado['synced_count'], 1)
        self.assertEqual(post.call_args.kwargs['json']['operations'][0]['payload']['tipo_codigo_local'], 'KI')
        self.assertEqual(self.filas('SELECT entity_uid FROM sync_queue')[0]['entity_uid'], '11223344')

    def test_soporte_confirmado_permite_reintentar_el_mismo_evento_de(self):
        self.alta(tipo='DE')
        uuid = self.filas('SELECT operation_uuid FROM sync_queue')[0]['operation_uuid']
        servicio = self.servicio()
        with patch.object(offline.requests, 'post', side_effect=self.confirmar) as post:
            servicio.sync_pending_once()
            post.assert_not_called()
            servicio._ping_data.return_value = {'ok': True, 'capabilities': ['despachadores_offline_v1']}
            resultado = servicio.sync_pending_once()
        enviado = post.call_args.kwargs['json']['operations'][0]
        self.assertEqual((enviado['operation_uuid'], enviado['payload']['entidad']), (uuid, 'despachador'))
        self.assertEqual(resultado['synced_count'], 1)

    def test_eventos_dependientes_no_adelantan_sustitucion_no_compatible(self):
        self.alta()
        SustituirModel().guardar_sustitucion_local(
            uid_anterior='AABBCCDD', uid_nueva='AABBCCEE', nueva_vigencia='311230120000')
        RecargaModel().guardar_recarga_flexible('AABBCCEE', 'prueba', 25, 25)
        self.alta('11223344', 'EU')
        with patch.object(offline.requests, 'post', side_effect=self.confirmar) as post:
            resultado = self.servicio().sync_pending_once()
        self.assertEqual(resultado['synced_count'], 2)
        enviados = [c.kwargs['json']['operations'][0]['entity_uid'] for c in post.call_args_list]
        self.assertEqual(enviados, ['AABBCCDD', '11223344'])
        self.assertEqual([r['event_type'] for r in self.filas('SELECT * FROM sync_queue ORDER BY id')],
                         ['sustitucion_tarjeta', 'recarga_tarjeta'])

    def test_recuperacion_de_conexion_envia_pendientes(self):
        self.alta()
        servicio = self.servicio()
        servicio._ping_data.side_effect = [offline.requests.RequestException('offline'), {'ok': True}]
        antes = self.filas('SELECT * FROM sync_queue')
        with patch.object(offline.requests, 'post', side_effect=self.confirmar) as post:
            self.assertEqual(servicio.sync_pending_once()['state'], 'offline')
            post.assert_not_called()
            self.assertEqual(self.filas('SELECT * FROM sync_queue'), antes)
            self.assertEqual(servicio.sync_pending_once()['synced_count'], 1)

    def test_respuesta_perdida_reintenta_uuid_sin_confirmar_localmente(self):
        self.alta()
        servicio = self.servicio()
        antes = self.filas('SELECT * FROM sync_queue')
        with patch.object(offline.requests, 'post', side_effect=offline.requests.RequestException('corte')):
            servicio.sync_pending_once()
        self.assertEqual(self.filas('SELECT * FROM sync_queue'), antes)
        with patch.object(offline.requests, 'post', side_effect=self.confirmar) as post:
            self.assertEqual(servicio.sync_pending_once()['synced_count'], 1)
        self.assertEqual(post.call_args.kwargs['json']['operations'][0]['operation_uuid'],
                         antes[0]['operation_uuid'])

    def test_confirmacion_debe_ser_unica_y_del_uuid_enviado(self):
        self.alta()
        uuid = self.filas('SELECT operation_uuid FROM sync_queue')[0]['operation_uuid']
        for resultado in (
            {'ok': True}, {'results': []}, {'results': {}},
            {'results': [{'operation_uuid': 'otro', 'status': 'ok'}]},
            {'results': [{'operation_uuid': uuid, 'status': 'ok'}] * 2},
            {'results': [{'operation_uuid': uuid, 'status': 'success'}]},
        ):
            with patch.object(offline.requests, 'post', return_value=offline.respuesta(resultado)):
                self.servicio().sync_pending_once()
            self.assertEqual(len(self.filas('SELECT * FROM sync_queue')), 1)

    def test_vaciado_por_limite_sin_perder_orden(self):
        for uid in ('AABBCCDD', '11223344', '22334455'):
            self.alta(uid)
        uuids = [r['operation_uuid'] for r in self.filas('SELECT * FROM sync_queue ORDER BY id')]
        servicio = self.servicio()
        with patch('services.sync_service.SYNC_BATCH_SIZE', 2), \
             patch.object(offline.requests, 'post', side_effect=self.confirmar) as post:
            self.assertEqual(servicio.sync_pending_once()['synced_count'], 2)
            self.assertEqual(servicio.sync_pending_once()['synced_count'], 1)
        self.assertEqual([c.kwargs['json']['operations'][0]['operation_uuid']
                          for c in post.call_args_list], uuids)


class InicioTest(unittest.TestCase):
    def controlador(self):
        fuente = Path('controllers/app_controller.py').read_text(encoding='utf-8')
        clase = next(n for n in ast.parse(fuente).body if isinstance(n, ast.ClassDef))
        nombres = {'_sincronizar_pendientes', '_recibir_sincronizacion'}
        modulo = ast.Module(body=[ast.ClassDef(name='Controller', bases=[], keywords=[],
            body=[n for n in clase.body if isinstance(n, ast.FunctionDef) and n.name in nombres],
            decorator_list=[])], type_ignores=[])
        namespace = {'QTimer': Mock()}
        exec(compile(ast.fix_missing_locations(modulo), '<sincronizacion real>', 'exec'), namespace)
        c = namespace['Controller']()
        c.current_ui = None
        c.sync_service = Mock()
        c.sync_service.count_pending.return_value = 2
        c._sync_future = None
        c._sync_executor = Mock()
        c._sync_poll = Mock()
        c._actualizar_estado_sync_ui = Mock()
        return c, namespace['QTimer']

    def test_sincroniza_incluso_antes_de_autenticar_sin_trabajos_simultaneos(self):
        c, _ = self.controlador()
        c._sincronizar_pendientes()
        c._sincronizar_pendientes()
        c._sync_executor.submit.assert_called_once_with(c.sync_service.sync_pending_once)

    def test_continua_despues_de_un_lote_confirmado(self):
        c, timer = self.controlador()
        c._sync_future = Mock()
        c._sync_future.result.return_value = dict(state='connected', synced_count=50,
                                                 pending_after=2, error_count=0)
        c._recibir_sincronizacion()
        self.assertIsNone(c._sync_future)
        timer.singleShot.assert_called_once_with(0, c._sincronizar_pendientes)

    def test_fallo_no_crea_bucle_inmediato_y_permite_siguiente_intento(self):
        c, timer = self.controlador()
        c._sync_future = Mock()
        c._sync_future.result.side_effect = RuntimeError('offline')
        c._recibir_sincronizacion()
        self.assertIsNone(c._sync_future)
        timer.singleShot.assert_not_called()
        c._sincronizar_pendientes()
        c._sync_executor.submit.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)
