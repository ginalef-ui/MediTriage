import unittest

from esi_investigacion import evaluar_etapas_iniciales


class PruebasAlcanceAdulto(unittest.TestCase):

    def test_edad_ausente_no_asigna_prioridad(self):
        resultado = evaluar_etapas_iniciales({
            "edad_anos": None,
            "intervencion_inmediata": True
        })

        self.assertEqual(resultado["estado"], "informacion_insuficiente")
        self.assertIsNone(resultado["prioridad"])

    def test_menor_de_edad_no_asigna_prioridad(self):
        resultado = evaluar_etapas_iniciales({
            "edad_anos": 17,
            "intervencion_inmediata": True
        })

        self.assertEqual(
            resultado["estado"],
            "fuera_de_alcance_o_datos_invalidos"
        )
        self.assertIsNone(resultado["prioridad"])

    def test_adulto_puede_continuar_a_primera_etapa(self):
        resultado = evaluar_etapas_iniciales({
            "edad_anos": 18,
            "intervencion_inmediata": True
        })

        self.assertEqual(resultado["estado"], "resultado_parcial")
        self.assertEqual(resultado["prioridad"], 1)

    def test_booleano_no_es_una_edad_valida(self):
        resultado = evaluar_etapas_iniciales({
            "edad_anos": True,
            "intervencion_inmediata": True
        })

        self.assertEqual(
            resultado["estado"],
            "fuera_de_alcance_o_datos_invalidos"
        )
        self.assertIsNone(resultado["prioridad"])


if __name__ == "__main__":
    unittest.main(verbosity=2)