"""Búsquedas por sección con SQLite temporal y respuestas HTTP simuladas."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import test_offline as offline
from core import database
from models.sustituir_model import SustituirModel


class BusquedaTest(unittest.TestCase):
    setUp = offline.OfflineTest.setUp
    tearDown = offline.OfflineTest.tearDown
    filas = offline.OfflineTest.filas
    alta = offline.OfflineTest.alta

    def respuesta(self, items):
        response = offline.respuesta({'items': items})
        response.status_code = 200
        return response

    def test_local_separa_tipos_sin_clasificar_por_nombre(self):
        for uid, tipo in [('00000001', 'NO'), ('00000002', 'EU'),
                          ('00000003', 'KI'), ('00000004', 'DE')]:
            self.alta(uid, tipo)
        with database.get_connection() as c:
            c.execute("UPDATE pasajeros SET nombre='Operador Despachador'")
            c.execute("UPDATE operadores SET nombre='Normal'")
            c.execute("UPDATE despachadores SET nombre='Preferencial'")
        modelo = SustituirModel()
        self.assertEqual({r['tipo_codigo_local'] for r in modelo.buscar_tarjetas_locales(seccion='pasajeros')},
                         {'NO', 'EU'})
        self.assertEqual({r['tipo_codigo_local'] for r in modelo.buscar_tarjetas_locales(seccion='personal')},
                         {'KI', 'DE'})

    def test_filtro_local_antes_del_limite(self):
        for i in range(6):
            self.alta(f'{i + 1:08X}', 'KI')
        self.alta('00112233', 'NO')
        with database.get_connection() as c:
            c.execute("UPDATE operadores SET nombre='AAA'")
            c.execute("UPDATE pasajeros SET nombre='ZZZ'")
        resultado = SustituirModel().buscar_tarjetas_locales(limite=1, seccion='pasajeros')
        self.assertEqual([r['uid'] for r in resultado], ['00112233'])

    def test_filtro_remoto_antes_del_limite_final(self):
        items = [dict(uid=f'{i + 1:08X}', tipo_tarjeta=tipo, nombre_pasajero='Mismo nombre')
                 for i, tipo in enumerate(('KI', 'DE', 'NO', 'EU'))]
        modelo = SustituirModel()
        with patch.object(offline.requests, 'get', return_value=self.respuesta(items)) as get:
            pasajeros = modelo.buscar_tarjetas_por_nombre('Mismo', limite=1, seccion='pasajeros')
            personal = modelo.buscar_tarjetas_por_nombre('Mismo', limite=1, seccion='personal')
        self.assertEqual([r['uid'] for r in pasajeros], ['00000003'])
        self.assertEqual([r['uid'] for r in personal], ['00000001'])
        self.assertGreaterEqual(get.call_args.kwargs['params']['limite'], 50)

    def test_uid_normalizada_prioriza_local_y_conserva_ceros(self):
        self.alta('00AABBCC', 'NO')
        with database.get_connection() as c:
            c.execute("UPDATE tarjetas SET uid=' 00aabbcc '")
        items = [dict(uid='00AABBCC', tipo_tarjeta='EU', nombre_pasajero='Dato del servidor'),
                 dict(uid=' 00aabbcc ', tipo_tarjeta='NO', nombre_pasajero='Otra copia'),
                 dict(uid='0000000a', tipo_tarjeta='NO', nombre_pasajero='Otra tarjeta')]
        with patch.object(offline.requests, 'get', return_value=self.respuesta(items)):
            resultado = SustituirModel().buscar_tarjetas_por_nombre('', seccion='pasajeros')
        self.assertEqual([r['uid'] for r in resultado], ['00AABBCC', '0000000A'])
        self.assertEqual(resultado[0]['tipo_codigo_local'], 'NO')
        self.assertNotEqual(resultado[0]['nombre_pasajero'], 'Dato del servidor')
        self.assertEqual(self.filas('SELECT uid FROM tarjetas')[0]['uid'], ' 00aabbcc ')

    def test_nombres_iguales_no_eliminan_tarjetas_diferentes(self):
        self.alta('00000001', 'NO')
        self.alta('00000002', 'EU')
        nombre = self.filas('SELECT nombre FROM pasajeros LIMIT 1')[0]['nombre']
        items = [dict(uid='00000003', tipo_tarjeta='NO', nombre_pasajero=nombre),
                 dict(uid='00000004', tipo_tarjeta='EU', nombre_pasajero=nombre),
                 dict(uid=' 00000003 ', tipo_tarjeta='NO', nombre_pasajero=nombre)]
        with patch.object(offline.requests, 'get', return_value=self.respuesta(items)):
            resultado = SustituirModel().buscar_tarjetas_por_nombre('', seccion='pasajeros')
        self.assertEqual({r['uid'] for r in resultado}, {'00000001', '00000002', '00000003', '00000004'})

    def test_duplicados_locales_no_consumen_el_limite(self):
        self.alta('AABBCCDD', 'NO')
        self.alta('11223344', 'EU')
        with database.get_connection() as c:
            c.execute("""
                INSERT INTO tarjetas(uid,saldo,tipo_tarjeta_id,pasajero_id,vigencia)
                SELECT ' aabbccdd ',saldo,tipo_tarjeta_id,pasajero_id,vigencia
                FROM tarjetas WHERE uid='AABBCCDD'
            """)
        resultado = SustituirModel().buscar_tarjetas_locales(limite=2, seccion='pasajeros')
        self.assertEqual({r['uid'] for r in resultado}, {'AABBCCDD', '11223344'})

    def test_uid_invalidas_se_reportan_sin_reconstruir_ni_borrar(self):
        self.alta('UID_INVALIDA', 'NO')
        self.alta('0000000A', 'NO')
        tablas = ('tarjetas', 'pasajeros', 'operadores', 'despachadores', 'sync_queue')
        antes = {t: self.filas('SELECT * FROM ' + t) for t in tablas}
        invalidas = ('GG112233', '0011 2233', '0x112233', '12.5E+03',
                     12345678, 'AABBCCD', 'AA' * 11)
        items = [dict(uid=uid, tipo_tarjeta='NO') for uid in invalidas]
        modelo = SustituirModel()
        with self.assertLogs('models.sustituir_model', level='WARNING') as logs, \
             patch.object(offline.requests, 'get', return_value=self.respuesta(items)):
            resultado = modelo.buscar_tarjetas_por_nombre('', limite=1, seccion='pasajeros')
        self.assertEqual([r['uid'] for r in resultado], ['0000000A'])
        self.assertEqual(len(modelo.incidencias_busqueda), len(invalidas) + 1)
        self.assertTrue(any('UID_INVALIDA' in linea for linea in logs.output))
        self.assertEqual(antes, {t: self.filas('SELECT * FROM ' + t) for t in tablas})

    def test_desconocidos_o_contradictorios_no_son_normal(self):
        items = [dict(uid='00000001', nombre_pasajero='Normal'),
                 dict(uid='00000002', tipo_tarjeta_id=1),
                 dict(uid='00000003', tipo_tarjeta='Especial'),
                 dict(uid='00000004', tipo_tarjeta='NO', tipo_codigo_local='DE')]
        modelo = SustituirModel()
        self.assertEqual(modelo._normalizar_item_busqueda(items[0])['tipo_tarjeta'], 'Desconocido')
        for seccion in ('pasajeros', 'personal'):
            with self.assertLogs('models.sustituir_model', level='WARNING'), \
                 patch.object(offline.requests, 'get', return_value=self.respuesta(items)):
                self.assertEqual(modelo.buscar_tarjetas_por_nombre('', seccion=seccion), [])

    def test_tipo_anidado_y_aliases_reales(self):
        items = [dict(uid='00000001', tipo_tarjeta={'id': 22, 'clave': 'NOR', 'descripcion': 'Normal'}),
                 dict(uid='00000002', tipo={'clave': 'PRE', 'descripcion': 'Preferencial'}),
                 dict(uid='00000003', tipo_codigo_local='KI'),
                 dict(uid='00000004', tipo_descripcion='Despachador')]
        with patch.object(offline.requests, 'get', return_value=self.respuesta(items)):
            modelo = SustituirModel()
            self.assertEqual({r['tipo_codigo_local'] for r in modelo.buscar_tarjetas_por_nombre(seccion='pasajeros')},
                             {'NO', 'EU'})
            self.assertEqual({r['tipo_codigo_local'] for r in modelo.buscar_tarjetas_por_nombre(seccion='personal')},
                             {'KI', 'DE'})

    def test_servidor_no_reintroduce_uid_local_bloqueada_o_de_otra_seccion(self):
        self.alta('00000001', 'KI')
        self.alta('00000002', 'NO')
        with database.get_connection() as c:
            c.execute("UPDATE tarjetas SET en_lista_negra=1 WHERE uid='00000002'")
        items = [dict(uid=' 00000001 ', tipo_tarjeta='NO', en_lista_negra=0),
                 dict(uid='00000002', tipo_tarjeta='NO', en_lista_negra=0)]
        with patch.object(offline.requests, 'get', return_value=self.respuesta(items)):
            self.assertEqual(SustituirModel().buscar_tarjetas_por_nombre(seccion='pasajeros'), [])

    def test_prioridad_local_incluso_si_solo_coincide_el_nombre_remoto(self):
        self.alta('00000001', 'NO')
        with patch.object(offline.requests, 'get', return_value=self.respuesta([
                dict(uid='00000001', tipo_tarjeta='NO', nombre_pasajero='Nombre remoto actualizado')])):
            resultado = SustituirModel().buscar_tarjetas_por_nombre('actualizado', seccion='pasajeros')
        self.assertEqual(len(resultado), 1)
        self.assertNotEqual(resultado[0]['nombre_pasajero'], 'Nombre remoto actualizado')

    def test_sin_internet_y_cambio_de_seccion_en_controlador(self):
        for uid, tipo in [('00000001', 'NO'), ('00000002', 'EU'),
                          ('00000003', 'KI'), ('00000004', 'DE')]:
            self.alta(uid, tipo)
        fuente = Path('controllers/app_controller.py').read_text(encoding='utf-8')
        clase = next(n for n in ast.parse(fuente).body if isinstance(n, ast.ClassDef))
        metodos = [n for n in clase.body if isinstance(n, ast.FunctionDef)
                   and n.name in ('show_sustituir_window', '_buscar_pasajeros_sustituir')]
        class Vista:
            pass
        namespace = dict(SustituirWindow=Vista, QTableWidgetItem=Mock(),
                         Qt=SimpleNamespace(UserRole=1, AlignVCenter=2, AlignLeft=4))
        modulo = ast.Module(body=[ast.ClassDef(name='Controller', bases=[], keywords=[],
            body=metodos, decorator_list=[])], type_ignores=[])
        exec(compile(ast.fix_missing_locations(modulo), '<busqueda real>', 'exec'), namespace)
        c = namespace['Controller']()
        c.current_ui = Vista()
        c._show_port_window = Mock()
        c._configurar_sustituir_window = Mock()
        c._crear_popup_resultados_sustituir = Mock()
        c._formatear_fecha_simple_sustituir = Mock(return_value='')
        c._formatear_vigencia_sustituir = Mock(return_value='')
        c.popup_resultados_sustituir = Mock()
        c.popup_resultados_sustituir.columnWidth.return_value = 50
        c.popup_resultados_sustituir.rowCount.return_value = 2
        c.sustituir_model = SustituirModel()
        # setUp bloquea todas las llamadas HTTP reales con RequestException.
        for seccion, tipos in [('pasajeros', {'NO', 'EU'}), ('personal', {'KI', 'DE'}),
                               ('pasajeros', {'NO', 'EU'})]:
            c.show_sustituir_window(seccion=seccion)
            c._buscar_pasajeros_sustituir('')
            self.assertEqual({r['tipo_codigo_local'] for r in c.resultados_sustituir}, tipos)

    def test_seccion_invalida_no_hace_busqueda_sin_filtro(self):
        modelo = SustituirModel()
        with self.assertRaises(ValueError):
            modelo.buscar_tarjetas_locales(seccion='todas')
        with self.assertRaises(ValueError):
            modelo.buscar_tarjetas_por_nombre(seccion='todas')


if __name__ == '__main__':
    unittest.main(verbosity=2)
