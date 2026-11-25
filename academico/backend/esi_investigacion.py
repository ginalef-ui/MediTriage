"""
Motor parcial de investigacion basado en ESI version 4.

SOLO PARA CASOS FICTICIOS Y PRUEBAS.
No es una implementacion completa ni validada para uso clinico.
"""


def evaluar_etapas_iniciales(datos):
    """
    Evalua las etapas iniciales usando respuestas registradas
    por una persona. None significa no evaluado.

    No interpreta texto ni determina por si mismo si una situacion
    es de alto riesgo.
    """

    # comprobar_alcance_adulto_al_inicio
    # Esta comprobacion delimita la prueba; no reemplaza una
    # evaluacion profesional ni debe retrasar una atencion real.
    edad = datos.get("edad_anos")

    if edad is None:
        return {
            "estado": "informacion_insuficiente",
            "prioridad": None,
            "detalle": "Falta registrar la edad para verificar el alcance adulto."
        }

    if type(edad) is not int or edad < 18 or edad > 120:
        return {
            "estado": "fuera_de_alcance_o_datos_invalidos",
            "prioridad": None,
            "detalle": "Esta prueba solo considera adultos de 18 a 120 anos."
        }

    intervencion = datos.get("intervencion_inmediata")

    # No avanzar a una categoria menor si la primera etapa
    # no ha sido evaluada.
    if intervencion is None:
        return {
            "estado": "informacion_insuficiente",
            "prioridad": None,
            "detalle": "Falta evaluar intervencion inmediata."
        }

    if intervencion is True:
        return {
            "estado": "resultado_parcial",
            "prioridad": 1,
            "detalle": (
                "Etapa inicial: se registro que requiere "
                "una intervencion inmediata."
            )
        }

    if intervencion is not False:
        return {
            "estado": "datos_invalidos",
            "prioridad": None,
            "detalle": "La respuesta de intervencion debe ser si, no o no evaluado."
        }

    campos_riesgo = [
        "situacion_alto_riesgo",
        "alteracion_conciencia_nueva",
        "dolor_o_malestar_intenso"
    ]

    respuestas = [datos.get(campo) for campo in campos_riesgo]

    # Validar valores antes de continuar.
    if any(valor is not None and valor is not True and valor is not False
           for valor in respuestas):
        return {
            "estado": "datos_invalidos",
            "prioridad": None,
            "detalle": "Las evaluaciones deben ser si, no o no evaluado."
        }

    # Si hay al menos una respuesta positiva, se identifica
    # la rama de alto riesgo del algoritmo de referencia.
    if any(valor is True for valor in respuestas):
        return {
            "estado": "resultado_parcial",
            "prioridad": 2,
            "detalle": (
                "Etapa inicial: se registro al menos una "
                "evaluacion positiva de alto riesgo."
            )
        }

    faltantes = [
        campo for campo in campos_riesgo
        if datos.get(campo) is None
    ]

    if faltantes:
        return {
            "estado": "informacion_insuficiente",
            "prioridad": None,
            "detalle": "Faltan evaluaciones de alto riesgo.",
            "campos_no_registrados": faltantes
        }

    # Etapa de recursos: respuesta registrada por una persona.
    recursos = datos.get("recursos_previstos")

    if recursos is None:
        return {
            "estado": "informacion_insuficiente",
            "prioridad": None,
            "detalle": "Falta registrar los recursos previstos."
        }

    # bool es una subclase de int en Python; por eso se exige
    # que el tipo sea exactamente int.
    if type(recursos) is not int or recursos not in (0, 1, 2):
        return {
            "estado": "datos_invalidos",
            "prioridad": None,
            "detalle": "Los recursos deben ser 0, 1 o 2."
        }

    if recursos == 0:
        return {
            "estado": "resultado_parcial",
            "prioridad": 5,
            "detalle": "Se registraron cero recursos previstos."
        }

    if recursos == 1:
        return {
            "estado": "resultado_parcial",
            "prioridad": 4,
            "detalle": "Se registro un recurso previsto."
        }

    # revision_inicial_signos_adultos
    # Esta etapa es experimental y solo para casos ficticios.
    edad = datos.get("edad_anos")

    if edad is None:
        return {
            "estado": "evaluacion_incompleta",
            "prioridad": None,
            "detalle": "Falta registrar la edad para verificar el alcance adulto."
        }

    if type(edad) is not int or edad < 18 or edad > 120:
        return {
            "estado": "fuera_de_alcance_o_datos_invalidos",
            "prioridad": None,
            "detalle": "Esta prueba solo considera adultos de 18 a 120 anos."
        }

    signos = {
        "pulsaciones": datos.get("pulsaciones"),
        "frecuencia_respiratoria": datos.get("frecuencia_respiratoria"),
        "saturacion_oxigeno": datos.get("saturacion_oxigeno")
    }

    limites_tecnicos = {
        "pulsaciones": (1, 250),
        "frecuencia_respiratoria": (1, 100),
        "saturacion_oxigeno": (1, 100)
    }

    for nombre, valor in signos.items():
        if valor is not None:
            minimo, maximo = limites_tecnicos[nombre]

            if type(valor) is not int or not minimo <= valor <= maximo:
                return {
                    "estado": "datos_invalidos",
                    "prioridad": None,
                    "detalle": "Hay un valor invalido en: " + nombre
                }

    indicadores = []

    if signos["pulsaciones"] is not None and signos["pulsaciones"] > 100:
        indicadores.append("pulsaciones")

    if (
        signos["frecuencia_respiratoria"] is not None
        and signos["frecuencia_respiratoria"] > 20
    ):
        indicadores.append("frecuencia_respiratoria")

    if (
        signos["saturacion_oxigeno"] is not None
        and signos["saturacion_oxigeno"] < 92
    ):
        indicadores.append("saturacion_oxigeno")

    faltantes = [
        nombre for nombre, valor in signos.items()
        if valor is None
    ]

    # La referencia indica considerar una prioridad mayor;
    # no se asigna automaticamente.
    if indicadores:
        return {
            "estado": "revision_profesional",
            "prioridad": None,
            "detalle": (
                "Hay indicadores que requieren revision profesional. "
                "El motor no asigna automaticamente una prioridad."
            ),
            "indicadores": indicadores,
            "campos_no_registrados": faltantes
        }

    if faltantes:
        return {
            "estado": "evaluacion_incompleta",
            "prioridad": None,
            "detalle": "Faltan signos vitales para esta etapa.",
            "campos_no_registrados": faltantes
        }

    return {
        "estado": "resultado_parcial",
        "prioridad": 3,
        "detalle": (
            "Resultado parcial del algoritmo de investigacion. "
            "Requiere revision y validacion profesional."
        )
    }