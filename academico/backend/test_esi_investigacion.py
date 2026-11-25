import unittest

from esi_investigacion import evaluar_etapas_iniciales


class PruebasEtapasIniciales(unittest.TestCase):

    def test_intervencion_no_evaluada_no_entrega_prioridad(self):
        resultado = evaluar_etapas_iniciales({
            "edad_anos": 35,
            "intervencion_inmediata": None,
            "situacion_alto_riesgo": True
        })

        self.assertEqual(resultado["estado"], "informacion_insuficiente")
        self.assertIsNone(resultado["prioridad"])

    def test_intervencion_positiva_no_exige_recursos(self):
        resultado = evaluar_etapas_iniciales({
            "edad_anos": 35,
            "intervencion_inmediata": True,
            "recursos_previstos": None
        })

        self.assertEqual(resultado["prioridad"], 1)

    def test_riesgo_positivo_con_intervencion_negativa(self):
        resultado = evaluar_etapas_iniciales({
            "edad_anos": 35,
            "intervencion_inmediata": False,
            "situacion_alto_riesgo": True,
            "alteracion_conciencia_nueva": None,
            "dolor_o_malestar_intenso": None
        })

        self.assertEqual(resultado["prioridad"], 2)

    def test_evaluacion_incompleta_no_inventa_prioridad(self):
        resultado = evaluar_etapas_iniciales({
            "edad_anos": 35,
            "intervencion_inmediata": False,
            "situacion_alto_riesgo": False,
            "alteracion_conciencia_nueva": None,
            "dolor_o_malestar_intenso": False
        })

        self.assertEqual(resultado["estado"], "informacion_insuficiente")
        self.assertIsNone(resultado["prioridad"])

    def test_etapas_negativas_no_inventan_resultado_final(self):
        resultado = evaluar_etapas_iniciales({
            "edad_anos": 35,
            "intervencion_inmediata": False,
            "situacion_alto_riesgo": False,
            "alteracion_conciencia_nueva": False,
            "dolor_o_malestar_intenso": False
        })

        self.assertEqual(resultado["estado"], "informacion_insuficiente")
        self.assertIsNone(resultado["prioridad"])

    def test_valor_invalido_no_entrega_prioridad(self):
        resultado = evaluar_etapas_iniciales({
            "edad_anos": 35,
            "intervencion_inmediata": False,
            "situacion_alto_riesgo": "no"
        })

        self.assertEqual(resultado["estado"], "datos_invalidos")
        self.assertIsNone(resultado["prioridad"])


if __name__ == "__main__":
    unittest.main(verbosity=2)