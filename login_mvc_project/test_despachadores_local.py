"""Separación de titulares con SQLite temporal y transporte HTTP simulado."""
import json
import sqlite3
import unittest
from unittest.mock import patch

import test_offline as offline
from core import database
from core.despachadores_local import migrar_despachadores
from models.alta_model import AltaModel
from models.cancelar_model import CancelarModel
from models.sustituir_model import SustituirModel
from services.sync_service import SyncService


class SeparacionTest(unittest.TestCase):
    setUp = offline.OfflineTest.setUp
    tearDown = offline.OfflineTest.tearDown
    filas = offline.OfflineTest.filas
    alta = offline.OfflineTest.alta

    def legado(self):
        self.alta('AABBCCDD', 'DE')
        self.alta('11223344', 'KI')
        with database.get_connection() as c:
            c.execute("""
                UPDATE despachadores SET nombre='Personal DE', documento='DOC-DE',
                    curp='CURP-DE', foto='original.png', fecha_nacimiento='01-01-1990',
                    created_at='2020-01-02 03:04:05'
            """)
            c.execute("""
                INSERT INTO operadores (
                    id, tarjeta_id, nombre, documento, curp, foto, fecha_nacimiento, created_at
                ) SELECT 41, tarjeta_id, nombre, documento, curp, foto, fecha_nacimiento, created_at
                FROM despachadores
            """)
            c.execute('DELETE FROM despachadores')
            c.execute("DROP VIEW v_tarjetas_locales")
            c.execute("""
                CREATE VIEW v_tarjetas_locales AS
                SELECT t.*, tt.descripcion AS tipo_tarjeta,
                    COALESCE(o.nombre,p.nombre,'') AS nombre_pasajero,
                    COALESCE(o.documento,p.documento,'-') AS documento,
                    COALESCE(o.curp,p.curp,'') AS curp,
                    COALESCE(o.foto,p.foto,'') AS foto,
                    COALESCE(o.fecha_nacimiento,p.fecha_nacimiento,'') AS fecha_nacimiento,
                    CASE WHEN o.id IS NOT NULL THEN 'operador' ELSE 'pasajero' END AS entidad
                FROM tarjetas t JOIN tipo_tarjetas tt ON tt.id=t.tipo_tarjeta_id
                LEFT JOIN operadores o ON o.tarjeta_id=t.id
                LEFT JOIN pasajeros p ON p.id=t.pasajero_id
            """)
            fila = c.execute("SELECT * FROM sync_queue WHERE entity_uid='AABBCCDD'").fetchone()
            payload = json.loads(fila['payload_json'])
            payload['entidad'] = 'operador'
            payload['datos_original'] = {'tipo_tarjeta': 'Despachador', 'entidad': 'operador',
                                         'foto': 'original.png'}
            c.execute("""
                UPDATE sync_queue SET payload_json=?,status='error',retries=4,last_error='API antigua'
                WHERE id=?
            """, (json.dumps(payload), fila['id']))
        return self.filas('SELECT * FROM operadores WHERE id=41')[0]

    def test_migracion_preserva_datos_ki_relaciones_y_eventos(self):
        anterior = self.legado()
        ki = self.filas('SELECT * FROM operadores WHERE id<>41')
        tarjetas = self.filas('SELECT * FROM tarjetas')
        eventos = self.filas('SELECT * FROM sync_queue ORDER BY id')
        migrar_despachadores()
        self.assertEqual(self.filas('SELECT * FROM despachadores'), [anterior])
        self.assertEqual(self.filas('SELECT * FROM operadores'), ki)
        self.assertEqual(self.filas('SELECT * FROM tarjetas'), tarjetas)
        for viejo, nuevo in zip(eventos, self.filas('SELECT * FROM sync_queue ORDER BY id')):
            self.assertEqual({k: v for k, v in viejo.items() if k != 'payload_json'},
                             {k: v for k, v in nuevo.items() if k != 'payload_json'})
            payload = json.loads(nuevo['payload_json'])
            if viejo['entity_uid'] == 'AABBCCDD':
                self.assertEqual((payload['tipo_codigo_local'], payload['entidad']),
                                 ('DE', 'despachador'))
                self.assertEqual(payload['datos_original']['entidad'], 'despachador')
                self.assertEqual(payload['datos_original']['foto'], 'original.png')
            else:
                self.assertEqual(viejo, nuevo)
        vista = self.filas("SELECT * FROM v_tarjetas_locales WHERE uid='AABBCCDD'")[0]
        self.assertEqual((vista['entidad'], vista['curp'], vista['foto']),
                         ('despachador', 'CURP-DE', 'original.png'))
        self.assertFalse(self.filas('PRAGMA foreign_key_check'))

    def test_repetir_migracion_e_inicializacion_no_duplica_ni_pierde(self):
        self.legado()
        migrar_despachadores()
        tablas = ('tarjetas', 'operadores', 'despachadores', 'pasajeros', 'sync_queue', 'usuarios')
        antes = {t: self.filas('SELECT * FROM ' + t) for t in tablas}
        migrar_despachadores()
        database.initialize_database()
        self.assertEqual(antes, {t: self.filas('SELECT * FROM ' + t) for t in tablas})
        self.assertFalse(self.filas('PRAGMA foreign_key_check'))

    def test_inicializacion_ejecuta_migracion_sobre_esquema_anterior(self):
        anterior = self.legado()
        with database.get_connection() as c:
            c.execute('DROP TABLE despachadores')
            c.execute("DELETE FROM local_migrations WHERE nombre='despachadores_separados_v1'")
        database.initialize_database()
        self.assertEqual(self.filas('SELECT * FROM despachadores'), [anterior])
        self.assertEqual(len(self.filas('SELECT * FROM operadores')), 1)
        self.assertFalse(self.filas('PRAGMA foreign_key_check'))

    def test_curp_duplicada_considera_las_tres_tablas(self):
        modelo = AltaModel()
        for index, origen in enumerate(('NO', 'KI', 'DE')):
            uid = f'{index + 1:08X}'
            modelo.guardar_alta_local(uid, 'Titular', origen, '311230120000', curp=uid)
            self.assertEqual(modelo.buscar_curp_local(' ' + uid.lower() + ' ')['uid'], uid)
            for destino in ('NO', 'EU', 'KI', 'DE'):
                with self.assertRaisesRegex(ValueError, 'CURP'):
                    modelo.guardar_alta_local(f'{index + 10:08X}', 'Otro', destino,
                                             '311230120000', curp=uid)
        self.assertEqual([len(self.filas('SELECT * FROM ' + t)) for t in
                          ('pasajeros', 'operadores', 'despachadores')], [1, 1, 1])

    def test_de_consulta_cancela_y_sustituye_conservando_titular(self):
        self.legado()
        migrar_despachadores()
        anterior = self.filas('SELECT * FROM despachadores')[0]
        cancelar = CancelarModel()
        consulta = cancelar.obtener_tarjeta_por_uid('AABBCCDD')
        self.assertEqual(consulta['entidad'], 'despachador')
        cancelar.cancelar_tarjeta_flexible('AABBCCDD', motivo_baja='Prueba')
        cancelar.cancelar_tarjeta_flexible('AABBCCDD', en_lista_negra=False)
        self.assertEqual(self.filas('SELECT * FROM despachadores')[0], anterior)
        SustituirModel().guardar_sustitucion_local(
            uid_anterior='AABBCCDD', uid_nueva='AABBCCEE', nueva_vigencia='311230120000')
        nuevo = self.filas('SELECT * FROM despachadores')[0]
        self.assertEqual({k:v for k,v in anterior.items() if k != 'tarjeta_id'},
                         {k:v for k,v in nuevo.items() if k != 'tarjeta_id'})
        vista = self.filas("SELECT * FROM v_tarjetas_locales WHERE uid='AABBCCEE'")[0]
        self.assertEqual((vista['tipo_tarjeta'], vista['entidad'], vista['saldo']),
                         ('Despachador', 'despachador', 0))
        self.assertEqual(nuevo['tarjeta_id'], vista['id'])
        self.assertEqual(len(self.filas('SELECT * FROM operadores')), 1)
        self.assertFalse(self.filas('PRAGMA foreign_key_check'))

    def test_tarjeta_id_es_unico_y_tiene_clave_foranea(self):
        self.alta(tipo='DE')
        tarjeta = self.filas('SELECT tarjeta_id FROM despachadores')[0]['tarjeta_id']
        for tarjeta_id in (tarjeta, tarjeta + 999):
            with self.assertRaises(sqlite3.IntegrityError), database.get_connection() as c:
                c.execute("INSERT INTO despachadores(tarjeta_id,nombre) VALUES (?, 'Duplicado')",
                          (tarjeta_id,))
        self.assertEqual(len(self.filas('SELECT * FROM despachadores')), 1)
        self.assertFalse(self.filas('PRAGMA foreign_key_check'))

    def test_conflicto_no_sobrescribe_ni_borra_informacion(self):
        anterior = self.legado()
        with database.get_connection() as c:
            c.execute("""
                INSERT INTO despachadores SELECT * FROM operadores WHERE id=41
            """)
            c.execute("UPDATE despachadores SET nombre='Datos distintos'")
        antes = self.filas('SELECT * FROM despachadores')
        with self.assertRaisesRegex(RuntimeError, 'datos distintos'):
            migrar_despachadores()
        self.assertEqual(self.filas('SELECT * FROM operadores WHERE id=41'), [anterior])
        self.assertEqual(self.filas('SELECT * FROM despachadores'), antes)

    def test_error_de_cola_revierte_movimiento_y_creacion_de_tabla(self):
        anterior = self.legado()
        with database.get_connection() as c:
            c.execute('DROP TABLE despachadores')
            c.execute("UPDATE sync_queue SET payload_json='no es JSON' WHERE entity_uid='AABBCCDD'")
        sql = self.filas("SELECT sql FROM sqlite_master WHERE name='v_tarjetas_locales'")
        with self.assertRaises(json.JSONDecodeError):
            migrar_despachadores()
        self.assertEqual(self.filas('SELECT * FROM operadores WHERE id=41'), [anterior])
        self.assertFalse(self.filas("SELECT 1 FROM sqlite_master WHERE name='despachadores'"))
        self.assertEqual(self.filas("SELECT sql FROM sqlite_master WHERE name='v_tarjetas_locales'"), sql)

    def test_repara_pendientes_por_tipo_o_uid_sin_tocar_confirmados(self):
        self.alta(tipo='DE')
        with database.get_connection() as c:
            for index, (estado, payload) in enumerate([
                ('pending', {'tipo_codigo_local': 'DE', 'entidad': 'operador'}),
                ('error', {'tipo_codigo_local': 'DE', 'entidad': 'operador'}),
                ('waiting_api', {'datos_original': {'tipo_tarjeta': 'Despachador'}}),
                ('pending', {'uid_nueva': 'AABBCCDD', 'entidad': 'operador'}),
                ('synced', {'tipo_codigo_local': 'DE', 'entidad': 'operador'}),
            ]):
                c.execute("""
                    INSERT INTO sync_queue(operation_uuid,event_type,status,payload_json)
                    VALUES (?, 'sustitucion_tarjeta', ?, ?)
                """, (f'prueba-{index}', estado, json.dumps(payload)))
        antes = self.filas("SELECT * FROM sync_queue WHERE status='synced'")
        migrar_despachadores()
        self.assertEqual(self.filas("SELECT * FROM sync_queue WHERE status='synced'"), antes)
        for fila in self.filas("SELECT * FROM sync_queue WHERE status<>'synced'"):
            payload = json.loads(fila['payload_json'])
            self.assertEqual((payload['entidad'], payload['tipo_codigo_local']), ('despachador', 'DE'))

    def test_sincronizacion_de_fotos_usa_tabla_y_prefijo_despachadores(self):
        self.alta(tipo='DE')
        evento = self.filas('SELECT * FROM sync_queue')[0]
        local = database.DATABASE_DIR / 'original.png'
        local.write_bytes(b'archivo de prueba')
        payload = json.loads(evento['payload_json'])
        payload['foto'] = str(local)
        with database.get_connection() as c:
            c.execute('UPDATE despachadores SET foto=?', (str(local),))
            c.execute('UPDATE sync_queue SET payload_json=?', (json.dumps(payload),))
        servicio = SyncService()
        operacion = dict(evento, payload=payload)
        with patch.object(offline.requests, 'post', return_value=offline.respuesta({
                'ok': True, 'path': 'despachadores/foto.png'})) as post:
            servicio._prepare_photo(operacion)
            post.assert_called_once()
        with patch.object(offline.requests, 'post') as post:
            servicio._prepare_photo(operacion)
            post.assert_not_called()
        servicio._mark_synced(evento['operation_uuid'])
        self.assertEqual(self.filas('SELECT foto FROM despachadores')[0]['foto'],
                         'despachadores/foto.png')
        self.assertEqual(self.filas('SELECT * FROM uploaded_photos')[0]['local_path'], str(local))
        self.assertTrue(local.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
