import unittest

from esi_investigacion import evaluar_etapas_iniciales


def caso_base():
    return {
        "intervencion_inmediata": False,
        "situacion_alto_riesgo": False,
        "alteracion_conciencia_nueva": False,
        "dolor_o_malestar_intenso": False,
        "recursos_previstos": 2,
        "edad_anos": 35,
        "pulsaciones": 100,
        "frecuencia_respiratoria": 20,
        "saturacion_oxigeno": 92
    }


class PruebasSignosAdultos(unittest.TestCase):

    def test_datos_completos_en_limites_de_referencia(self):
        resultado = evaluar_etapas_iniciales(caso_base())

        self.assertEqual(resultado["estado"], "resultado_parcial")
        self.assertEqual(resultado["prioridad"], 3)

    def test_pulso_sobre_referencia_pide_revision(self):
        datos = caso_base()
        datos["pulsaciones"] = 101

        resultado = evaluar_etapas_iniciales(datos)

        self.assertEqual(resultado["estado"], "revision_profesional")
        self.assertIsNone(resultado["prioridad"])
        self.assertIn("pulsaciones", resultado["indicadores"])

    def test_frecuencia_sobre_referencia_pide_revision(self):
        datos = caso_base()
        datos["frecuencia_respiratoria"] = 21

        resultado = evaluar_etapas_iniciales(datos)

        self.assertEqual(resultado["estado"], "revision_profesional")
        self.assertIsNone(resultado["prioridad"])

    def test_saturacion_bajo_referencia_pide_revision(self):
        datos = caso_base()
        datos["saturacion_oxigeno"] = 91

        resultado = evaluar_etapas_iniciales(datos)

        self.assertEqual(resultado["estado"], "revision_profesional")
        self.assertIsNone(resultado["prioridad"])

    def test_signo_faltante_no_inventa_prioridad(self):
        datos = caso_base()
        datos["saturacion_oxigeno"] = None

        resultado = evaluar_etapas_iniciales(datos)

        self.assertEqual(resultado["estado"], "evaluacion_incompleta")
        self.assertIsNone(resultado["prioridad"])
        self.assertIn("saturacion_oxigeno", resultado["campos_no_registrados"])

    def test_indicador_con_otro_dato_faltante_pide_revision(self):
        datos = caso_base()
        datos["pulsaciones"] = 101
        datos["saturacion_oxigeno"] = None

        resultado = evaluar_etapas_iniciales(datos)

        self.assertEqual(resultado["estado"], "revision_profesional")
        self.assertIsNone(resultado["prioridad"])

    def test_fuera_del_alcance_adulto(self):
        datos = caso_base()
        datos["edad_anos"] = 17

        resultado = evaluar_etapas_iniciales(datos)

        self.assertEqual(
            resultado["estado"],
            "fuera_de_alcance_o_datos_invalidos"
        )
        self.assertIsNone(resultado["prioridad"])

    def test_saturacion_invalida(self):
        datos = caso_base()
        datos["saturacion_oxigeno"] = 150

        resultado = evaluar_etapas_iniciales(datos)

        self.assertEqual(resultado["estado"], "datos_invalidos")
        self.assertIsNone(resultado["prioridad"])


if __name__ == "__main__":
    unittest.main(verbosity=2)