import unittest

from esi_investigacion import evaluar_etapas_iniciales


def caso_base():
    return {
        "edad_anos": 35,
        "intervencion_inmediata": False,
        "situacion_alto_riesgo": False,
        "alteracion_conciencia_nueva": False,
        "dolor_o_malestar_intenso": False
    }


class PruebasRecursos(unittest.TestCase):

    def test_recursos_no_registrados(self):
        resultado = evaluar_etapas_iniciales(caso_base())

        self.assertEqual(resultado["estado"], "informacion_insuficiente")
        self.assertIsNone(resultado["prioridad"])

    def test_sin_recursos(self):
        datos = caso_base()
        datos["recursos_previstos"] = 0

        resultado = evaluar_etapas_iniciales(datos)

        self.assertEqual(resultado["prioridad"], 5)

    def test_un_recurso(self):
        datos = caso_base()
        datos["recursos_previstos"] = 1

        resultado = evaluar_etapas_iniciales(datos)

        self.assertEqual(resultado["prioridad"], 4)

    def test_dos_o_mas_recursos_requiere_siguiente_etapa(self):
        datos = caso_base()
        datos["recursos_previstos"] = 2

        resultado = evaluar_etapas_iniciales(datos)

        self.assertEqual(resultado["estado"], "evaluacion_incompleta")
        self.assertIsNone(resultado["prioridad"])

    def test_valor_invalido(self):
        datos = caso_base()
        datos["recursos_previstos"] = 3

        resultado = evaluar_etapas_iniciales(datos)

        self.assertEqual(resultado["estado"], "datos_invalidos")
        self.assertIsNone(resultado["prioridad"])

    def test_booleano_no_es_cantidad_de_recursos(self):
        datos = caso_base()
        datos["recursos_previstos"] = True

        resultado = evaluar_etapas_iniciales(datos)

        self.assertEqual(resultado["estado"], "datos_invalidos")
        self.assertIsNone(resultado["prioridad"])


if __name__ == "__main__":
    unittest.main(verbosity=2)