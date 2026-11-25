from fastapi import FastAPI, HTTPException
import psycopg

app = FastAPI(
    title="MediTriage Académico",
    description="Prototipo para trabajar únicamente con datos ficticios.",
    version="0.1.0"
)

DATABASE_URL = (
    "postgresql://meditriage:demo_local@postgres:5432/meditriage"
)


@app.get("/")
def inicio():
    return {
        "proyecto": "MediTriage",
        "mensaje": "Backend académico funcionando",
        "modo": "Solo datos ficticios"
    }


@app.get("/salud")
def comprobar_salud():
    try:
        with psycopg.connect(DATABASE_URL) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

        return {
            "backend": "funcionando",
            "base_de_datos": "conectada",
            "modo": "academico"
        }

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar con PostgreSQL"
        )
# Funciones para pacientes ficticios

from pydantic import BaseModel, Field
from psycopg.rows import dict_row


class PacienteNuevo(BaseModel):
    identificador: str = Field(min_length=3, max_length=40)
    nombre: str = Field(min_length=2, max_length=100)


@app.post("/pacientes", status_code=201)
def registrar_paciente(paciente: PacienteNuevo):
    identificador = paciente.identificador.strip().upper()
    nombre = paciente.nombre.strip()

    if len(identificador) < 3 or len(nombre) < 2:
        raise HTTPException(
            status_code=422,
            detail="Completa el identificador y el nombre ficticio."
        )

    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO pacientes (identificador, nombre)
                    VALUES (%s, %s)
                    RETURNING id, identificador, nombre, fecha_registro
                    """,
                    (identificador, nombre)
                )

                resultado = cursor.fetchone()

        return resultado

    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un paciente con ese identificador."
        )

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo guardar el paciente."
        )


@app.get("/pacientes")
def listar_pacientes():
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, identificador, nombre, fecha_registro
                    FROM pacientes
                    ORDER BY id
                    """
                )

                pacientes = cursor.fetchall()

        return pacientes

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudieron consultar los pacientes."
        )
# Funciones para atenciones ficticias

class AtencionNueva(BaseModel):
    paciente_id: int = Field(gt=0)
    sintomas: str = Field(min_length=2, max_length=1000)
    pulsaciones: int = Field(ge=1, le=250)

    presion_arterial: str = Field(
        pattern=r"^[0-9]{2,3}/[0-9]{2,3}$"
    )

    # Campos opcionales mientras completamos el formulario.
    # Esta primera version esta orientada a adultos.
    edad_anos: int | None = Field(default=None, ge=18, le=120)

    frecuencia_respiratoria: int | None = Field(
        default=None,
        ge=1,
        le=100
    )

    saturacion_oxigeno: int | None = Field(
        default=None,
        ge=1,
        le=100
    )

    temperatura: float | None = Field(
        default=None,
        ge=25,
        le=45
    )

    intervencion_inmediata: bool | None = None
    situacion_alto_riesgo: bool | None = None
    alteracion_conciencia_nueva: bool | None = None
    dolor_o_malestar_intenso: bool | None = None

    # 0 = ninguno, 1 = uno, 2 = dos o mas.
    # None significa que aun no se ha registrado.
    recursos_previstos: int | None = Field(
        default=None,
        ge=0,
        le=2
    )


@app.post("/atenciones", status_code=201)
def registrar_atencion(atencion: AtencionNueva):
    sintomas = atencion.sintomas.strip()

    if len(sintomas) < 2:
        raise HTTPException(
            status_code=422,
            detail="Ingresa los sintomas ficticios."
        )

    try:
        with psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row
        ) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO atenciones (
                        paciente_id,
                        sintomas,
                        pulsaciones,
                        presion_arterial,
                        edad_anos,
                        frecuencia_respiratoria,
                        saturacion_oxigeno,
                        temperatura,
                        intervencion_inmediata,
                        situacion_alto_riesgo,
                        alteracion_conciencia_nueva,
                        dolor_o_malestar_intenso,
                        recursos_previstos
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING *
                    """,
                    (
                        atencion.paciente_id,
                        sintomas,
                        atencion.pulsaciones,
                        atencion.presion_arterial,
                        atencion.edad_anos,
                        atencion.frecuencia_respiratoria,
                        atencion.saturacion_oxigeno,
                        atencion.temperatura,
                        atencion.intervencion_inmediata,
                        atencion.situacion_alto_riesgo,
                        atencion.alteracion_conciencia_nueva,
                        atencion.dolor_o_malestar_intenso,
                        atencion.recursos_previstos
                    )
                )

                resultado = cursor.fetchone()

        return resultado

    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(
            status_code=404,
            detail="El paciente indicado no existe."
        )

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo registrar la atencion."
        )

@app.get("/atenciones")
def listar_atenciones():
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        a.id,
                        a.paciente_id,
                        p.identificador,
                        p.nombre,
                        a.sintomas,
                        a.pulsaciones,
                        a.presion_arterial,
                        a.edad_anos,
                        a.frecuencia_respiratoria,
                        a.saturacion_oxigeno,
                        a.temperatura,
                        a.intervencion_inmediata,
                        a.situacion_alto_riesgo,
                        a.alteracion_conciencia_nueva,
                        a.dolor_o_malestar_intenso,
                        a.recursos_previstos,
                        a.prioridad_confirmada,
                        a.estado,
                        a.fecha_registro
                    FROM atenciones AS a
                    JOIN pacientes AS p ON p.id = a.paciente_id
                    ORDER BY a.fecha_registro DESC, a.id DESC
                    """
                )

                atenciones = cursor.fetchall()

        return atenciones

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudieron consultar las atenciones."
        )
# Confirmacion de prioridad y cola de espera

from fastapi import Request


class ConfirmacionPrioridad(BaseModel):
    prioridad: int = Field(ge=1, le=5)
    motivo: str = Field(default="", max_length=500)
    sugerencia_id: int | None = Field(default=None, gt=0)


@app.post("/atenciones/{atencion_id}/confirmar")
def confirmar_prioridad(
    atencion_id: int,
    confirmacion: ConfirmacionPrioridad,
    request: Request
):
    motivo = confirmacion.motivo.strip()

    try:
        with psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row
        ) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, estado
                    FROM atenciones
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (atencion_id,)
                )

                atencion = cursor.fetchone()

                if atencion is None:
                    raise HTTPException(
                        status_code=404,
                        detail="La atencion no existe."
                    )

                if atencion["estado"] != "pendiente":
                    raise HTTPException(
                        status_code=409,
                        detail="La atencion ya no esta pendiente."
                    )

                # validar_sugerencia_existente
                cursor.execute(
                    """
                    SELECT EXISTS (
                        SELECT 1
                        FROM sugerencias_ia
                        WHERE atencion_id = %s
                    ) AS existe
                    """,
                    (atencion_id,)
                )

                hay_sugerencias = cursor.fetchone()["existe"]


                if confirmacion.sugerencia_id is not None:
                    cursor.execute(
                        """
                        SELECT id, prioridad_sugerida
                        FROM sugerencias_ia
                        WHERE id = %s AND atencion_id = %s
                        """,
                        (
                            confirmacion.sugerencia_id,
                            atencion_id
                        )
                    )

                    sugerencia = cursor.fetchone()

                    if sugerencia is None:
                        raise HTTPException(
                            status_code=422,
                            detail=(
                                "La sugerencia no existe o "
                                "no pertenece a esta atencion."
                            )
                        )

                    if (
                        confirmacion.prioridad
                        != sugerencia["prioridad_sugerida"]
                        and not motivo
                    ):
                        raise HTTPException(
                            status_code=422,
                            detail=(
                                "Indica un motivo cuando la prioridad "
                                "sea distinta de la sugerencia de IA."
                            )
                        )

                cursor.execute(
                    """
                    UPDATE atenciones
                    SET prioridad_confirmada = %s,
                        motivo_cambio = %s,
                        confirmado_por = %s,
                        sugerencia_utilizada_id = %s,
                        estado = 'esperando',
                        fecha_confirmacion = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING *
                    """,
                    (
                        confirmacion.prioridad,
                        motivo,
                        request.state.usuario["id"],
                        confirmacion.sugerencia_id,
                        atencion_id
                    )
                )

                resultado = cursor.fetchone()

        return resultado

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo confirmar la prioridad."
        )

@app.get("/cola")
def consultar_cola():
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        a.id AS atencion_id,
                        p.identificador,
                        p.nombre,
                        a.sintomas,
                        a.prioridad_confirmada,
                        a.estado,
                        a.fecha_confirmacion
                    FROM atenciones AS a
                    JOIN pacientes AS p ON p.id = a.paciente_id
                    WHERE a.estado = 'esperando'
                    ORDER BY
                        a.prioridad_confirmada ASC,
                        a.fecha_confirmacion ASC,
                        a.id ASC
                    """
                )

                cola = cursor.fetchall()

        return cola

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo consultar la cola."
        )


@app.post("/atenciones/{atencion_id}/atender")
def marcar_atendida(atencion_id: int):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE atenciones
                    SET estado = 'atendido',
                        fecha_atencion = CURRENT_TIMESTAMP
                    WHERE id = %s AND estado = 'esperando'
                    RETURNING *
                    """,
                    (atencion_id,)
                )

                atencion = cursor.fetchone()

                if atencion is None:
                    cursor.execute(
                        "SELECT id FROM atenciones WHERE id = %s",
                        (atencion_id,)
                    )

                    if cursor.fetchone() is None:
                        raise HTTPException(
                            status_code=404,
                            detail="La atencion no existe."
                        )

                    raise HTTPException(
                        status_code=409,
                        detail="La atencion no esta en espera."
                    )

        return atencion

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo actualizar la atencion."
        )
# Historial de atenciones por paciente ficticio

@app.get("/pacientes/{paciente_id}/historial")
def consultar_historial(paciente_id: int):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, identificador, nombre, fecha_registro
                    FROM pacientes
                    WHERE id = %s
                    """,
                    (paciente_id,)
                )

                paciente = cursor.fetchone()

                if paciente is None:
                    raise HTTPException(
                        status_code=404,
                        detail="El paciente no existe."
                    )

                cursor.execute(
                    """
                    SELECT
                        id,
                        sintomas,
                        pulsaciones,
                        presion_arterial,
                        edad_anos,
                        frecuencia_respiratoria,
                        saturacion_oxigeno,
                        temperatura,
                        intervencion_inmediata,
                        situacion_alto_riesgo,
                        alteracion_conciencia_nueva,
                        dolor_o_malestar_intenso,
                        recursos_previstos,
                        prioridad_confirmada,
                        estado,
                        motivo_cambio,
                        confirmado_por,
                        sugerencia_utilizada_id,
                        (
                            SELECT nombre_mostrar
                            FROM usuarios
                            WHERE id = atenciones.confirmado_por
                        ) AS confirmado_por_nombre,
                        fecha_registro,
                        fecha_confirmacion,
                        fecha_atencion
                    FROM atenciones
                    WHERE paciente_id = %s
                    ORDER BY fecha_registro DESC, id DESC
                    """,
                    (paciente_id,)
                )

                atenciones = cursor.fetchall()

                cursor.execute(
                    """
                    SELECT
                        s.id,
                        s.atencion_id,
                        s.modelo,
                        s.prioridad_sugerida,
                        s.explicacion,
                        s.fecha_creacion,
                        u.nombre_mostrar AS solicitada_por
                    FROM sugerencias_ia AS s
                    JOIN atenciones AS a ON a.id = s.atencion_id
                    JOIN usuarios AS u ON u.id = s.usuario_id
                    WHERE a.paciente_id = %s
                    ORDER BY s.fecha_creacion DESC, s.id DESC
                    """,
                    (paciente_id,)
                )

                sugerencias_ia = cursor.fetchall()

        return {
            "paciente": paciente,
            "atenciones": atenciones,
            "sugerencias_ia": sugerencias_ia
        }

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo consultar el historial."
        )
# Autenticacion y roles para la version academica

import hashlib
import hmac
import re
import secrets

from fastapi import Request
from fastapi.responses import JSONResponse


class DatosLogin(BaseModel):
    usuario: str = Field(min_length=1, max_length=50)
    clave: str = Field(min_length=1, max_length=200)


def generar_hash_clave(clave, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    resultado = hashlib.pbkdf2_hmac(
        "sha256",
        clave.encode("utf-8"),
        bytes.fromhex(salt),
        210000
    )

    return salt + "$" + resultado.hex()


def comprobar_clave(clave, clave_hash):
    try:
        salt, _ = clave_hash.split("$", 1)
        calculado = generar_hash_clave(clave, salt)
        return hmac.compare_digest(calculado, clave_hash)
    except (ValueError, TypeError):
        return False


@app.on_event("startup")
def crear_usuarios_demo():
    cuentas = [
        ("admision", "Admision Demo", "admision"),
        ("triaje", "Profesional de Triaje Demo", "triaje"),
        ("medico", "Medico Demo", "medico"),
        ("admin", "Administrador Demo", "admin")
    ]

    with psycopg.connect(DATABASE_URL) as conexion:
        with conexion.cursor() as cursor:
            for usuario, nombre, rol in cuentas:
                cursor.execute(
                    """
                    SELECT id
                    FROM usuarios
                    WHERE nombre_usuario = %s
                    """,
                    (usuario,)
                )

                if cursor.fetchone() is None:
                    clave_hash = generar_hash_clave("Demo2026!")

                    cursor.execute(
                        """
                        INSERT INTO usuarios (
                            nombre_usuario,
                            nombre_mostrar,
                            rol,
                            clave_hash
                        )
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (nombre_usuario) DO NOTHING
                        """,
                        (usuario, nombre, rol, clave_hash)
                    )


@app.post("/login")
def iniciar_sesion(datos: DatosLogin):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, nombre_usuario, nombre_mostrar,
                           rol, clave_hash, activo
                    FROM usuarios
                    WHERE nombre_usuario = %s
                    """,
                    (datos.usuario.strip().lower(),)
                )

                usuario = cursor.fetchone()

                if (
                    usuario is None
                    or not usuario["activo"]
                    or not comprobar_clave(
                        datos.clave,
                        usuario["clave_hash"]
                    )
                ):
                    raise HTTPException(
                        status_code=401,
                        detail="Usuario o clave incorrectos."
                    )

                token = secrets.token_urlsafe(32)

                token_hash = hashlib.sha256(
                    token.encode("utf-8")
                ).hexdigest()

                cursor.execute(
                    """
                    INSERT INTO sesiones (
                        usuario_id,
                        token_hash,
                        fecha_expiracion
                    )
                    VALUES (
                        %s,
                        %s,
                        CURRENT_TIMESTAMP + INTERVAL '8 hours'
                    )
                    """,
                    (usuario["id"], token_hash)
                )

        return {
            "token": token,
            "tipo": "Bearer",
            "usuario": usuario["nombre_usuario"],
            "nombre": usuario["nombre_mostrar"],
            "rol": usuario["rol"]
        }

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo iniciar sesion."
        )


def roles_permitidos(metodo, ruta):
    if metodo == "GET" and ruta == "/pacientes":
        return {"admision", "triaje", "medico", "admin"}

    if metodo == "POST" and ruta == "/pacientes":
        return {"admision", "admin"}

    if metodo == "POST" and ruta == "/atenciones":
        return {"admision", "triaje", "admin"}

    if metodo == "GET" and ruta == "/atenciones":
        return {"triaje", "medico", "admin"}

    if metodo == "GET" and ruta == "/cola":
        return {"triaje", "medico", "admin"}

    if metodo == "GET" and re.fullmatch(
        r"/pacientes/[0-9]+/historial", ruta
    ):
        return {"triaje", "medico", "admin"}

    if metodo == "POST" and re.fullmatch(
        r"/atenciones/[0-9]+/confirmar", ruta
    ):
        return {"triaje", "admin"}

    if metodo == "POST" and re.fullmatch(
        r"/atenciones/[0-9]+/atender", ruta
    ):
        return {"triaje", "medico", "admin"}

    if metodo == "POST" and re.fullmatch(
        r"/atenciones/[0-9]+/sugerencia-ia", ruta
    ):
        return {"triaje", "admin"}

    if metodo == "GET" and re.fullmatch(
        r"/atenciones/[0-9]+/preparar-analisis", ruta
    ):
        return {"triaje", "admin"}

    if metodo == "POST" and ruta == "/investigacion/esi":
        return {"triaje", "admin"}

    if metodo == "POST" and ruta == "/investigacion/extraer-texto":
        return {"triaje", "admin"}

    return set()


@app.middleware("http")
async def comprobar_sesion_y_rol(request: Request, call_next):
    ruta = request.url.path
    metodo = request.method

    rutas_publicas = {
        "/",
        "/salud",
        "/panel",
        "/docs",
        "/redoc",
        "/openapi.json"
    }

    if (
        (metodo == "GET" and ruta in rutas_publicas)
        or (metodo == "POST" and ruta == "/login")
    ):
        return await call_next(request)

    autorizacion = request.headers.get("Authorization", "")
    partes = autorizacion.split()

    if len(partes) != 2 or partes[0].lower() != "bearer":
        return JSONResponse(
            status_code=401,
            content={"detail": "Debes iniciar sesion."}
        )

    token_hash = hashlib.sha256(
        partes[1].encode("utf-8")
    ).hexdigest()

    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT u.id, u.nombre_usuario, u.rol
                    FROM sesiones AS s
                    JOIN usuarios AS u ON u.id = s.usuario_id
                    WHERE s.token_hash = %s
                      AND s.fecha_expiracion > CURRENT_TIMESTAMP
                      AND u.activo = TRUE
                    """,
                    (token_hash,)
                )

                usuario = cursor.fetchone()

    except psycopg.Error:
        return JSONResponse(
            status_code=503,
            content={"detail": "No se pudo comprobar la sesion."}
        )

    if usuario is None:
        return JSONResponse(
            status_code=401,
            content={"detail": "Sesion invalida o vencida."}
        )

    permitidos = roles_permitidos(metodo, ruta)

    if usuario["rol"] not in permitidos:
        return JSONResponse(
            status_code=403,
            content={"detail": "Tu rol no permite esta accion."}
        )

    request.state.usuario = usuario

    return await call_next(request)

# Pantalla del prototipo academico

from fastapi.responses import FileResponse

@app.get("/panel", include_in_schema=False)
def mostrar_panel():
    return FileResponse("panel.html")

# Integracion experimental con Ollama para casos ficticios

import json
import socket
import urllib.error
import urllib.request


@app.post("/atenciones/{atencion_id}/sugerencia-ia")
def sugerencia_ia_academica(atencion_id: int, request: Request):
    # pausa_ia_hasta_evaluacion
    raise HTTPException(
        status_code=503,
        detail=(
            "La sugerencia de IA esta temporalmente en evaluacion. "
            "Continua con la confirmacion manual."
        )
    )
    try:
        with psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row
        ) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, sintomas, pulsaciones,
                           presion_arterial, estado
                    FROM atenciones
                    WHERE id = %s
                    """,
                    (atencion_id,)
                )

                atencion = cursor.fetchone()

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo consultar la atencion."
        )

    if atencion is None:
        raise HTTPException(
            status_code=404,
            detail="La atencion no existe."
        )

    if atencion["estado"] != "pendiente":
        raise HTTPException(
            status_code=409,
            detail="La atencion ya no esta pendiente."
        )

    datos_ficticios = {
        "sintomas": atencion["sintomas"],
        "pulsaciones": atencion["pulsaciones"],
        "presion_arterial": atencion["presion_arterial"]
    }

    prompt = (
        "Eres parte de una DEMOSTRACION ACADEMICA con casos "
        "completamente ficticios. No estas realizando una "
        "evaluacion medica real. "
        "Para demostrar el intercambio de datos, devuelve SOLO "
        "un objeto JSON con dos claves: "
        "'prioridad', un numero entero del 1 al 5, y "
        "'explicacion', una frase breve en espanol que describa "
        "que es una sugerencia ficticia para la demostracion. "
        "No des instrucciones de tratamiento. "
        "Datos ficticios: "
        + json.dumps(datos_ficticios, ensure_ascii=False)
    )

    solicitud = {
        "model": "qwen2.5:1.5b-instruct",
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0,
            "num_predict": 160,
            "num_ctx": 2048
        }
    }

    peticion = urllib.request.Request(
        "http://host.docker.internal:11434/api/generate",
        data=json.dumps(solicitud).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(peticion, timeout=180) as respuesta:
            resultado = json.load(respuesta)

        contenido = json.loads(resultado.get("response", ""))

    except (
        urllib.error.URLError,
        socket.timeout,
        TimeoutError,
        json.JSONDecodeError
    ):
        raise HTTPException(
            status_code=503,
            detail=(
                "No se pudo obtener una respuesta valida de Ollama. "
                "La prioridad se puede seleccionar manualmente."
            )
        )

    if not isinstance(contenido, dict):
        raise HTTPException(
            status_code=502,
            detail="El modelo devolvio un formato inesperado."
        )

    prioridad = contenido.get("prioridad")
    explicacion = contenido.get("explicacion")

    if (
        type(prioridad) is not int
        or prioridad not in range(1, 6)
        or not isinstance(explicacion, str)
        or not explicacion.strip()
        or len(explicacion) > 600
    ):
        raise HTTPException(
            status_code=502,
            detail=(
                "El modelo no entrego una sugerencia valida. "
                "La prioridad se puede seleccionar manualmente."
            )
        )

    # Guardar la sugerencia solo si la atencion sigue pendiente.
    try:
        with psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row
        ) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT estado
                    FROM atenciones
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (atencion_id,)
                )

                estado_actual = cursor.fetchone()

                if estado_actual is None:
                    raise HTTPException(
                        status_code=404,
                        detail="La atencion ya no existe."
                    )

                if estado_actual["estado"] != "pendiente":
                    raise HTTPException(
                        status_code=409,
                        detail=(
                            "La atencion ya no esta pendiente. "
                            "No se guardo la sugerencia."
                        )
                    )

                cursor.execute(
                    """
                    INSERT INTO sugerencias_ia (
                        atencion_id,
                        usuario_id,
                        modelo,
                        prioridad_sugerida,
                        explicacion
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, fecha_creacion
                    """,
                    (
                        atencion_id,
                        request.state.usuario["id"],
                        "qwen2.5:1.5b-instruct",
                        prioridad,
                        explicacion.strip()
                    )
                )

                sugerencia_guardada = cursor.fetchone()

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo guardar la sugerencia de IA."
        )

    return {
        "sugerencia_id": sugerencia_guardada["id"],
        "fecha_creacion": sugerencia_guardada["fecha_creacion"],
        "atencion_id": atencion_id,
        "prioridad_sugerida": prioridad,
        "explicacion": explicacion.strip(),
        "modelo": "qwen2.5:1.5b-instruct",
        "advertencia": (
            "Sugerencia experimental para datos ficticios. "
            "No es una clasificacion clinica."
        )
    }

# Preparacion de datos para investigacion de triaje.
# Esta ruta no asigna una categoria ESI.

@app.get("/atenciones/{atencion_id}/preparar-analisis")
def preparar_analisis_triaje(atencion_id: int):
    try:
        with psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row
        ) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        sintomas,
                        edad_anos,
                        pulsaciones,
                        presion_arterial,
                        frecuencia_respiratoria,
                        saturacion_oxigeno,
                        temperatura,
                        intervencion_inmediata,
                        situacion_alto_riesgo,
                        alteracion_conciencia_nueva,
                        dolor_o_malestar_intenso,
                        recursos_previstos,
                        estado
                    FROM atenciones
                    WHERE id = %s
                    """,
                    (atencion_id,)
                )

                atencion = cursor.fetchone()

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudieron consultar los datos de la atencion."
        )

    if atencion is None:
        raise HTTPException(
            status_code=404,
            detail="La atencion no existe."
        )

    campos_revisados = [
        "edad_anos",
        "frecuencia_respiratoria",
        "saturacion_oxigeno",
        "temperatura",
        "intervencion_inmediata",
        "situacion_alto_riesgo",
        "alteracion_conciencia_nueva",
        "dolor_o_malestar_intenso",
        "recursos_previstos"
    ]

    no_registrados = [
        campo for campo in campos_revisados
        if atencion[campo] is None
    ]

    return {
        "atencion_id": atencion["id"],
        "datos": atencion,
        "campos_no_registrados": no_registrados,
        "advertencia": (
            "Esta revision solo identifica campos sin registrar. "
            "No asigna prioridad ni valida el protocolo ESI."
        )
    }

# Ruta de investigacion: solo casos ficticios.
# No modifica atenciones ni confirma prioridades.

from typing import Literal
from pydantic import StrictBool, StrictInt
from esi_investigacion import evaluar_etapas_iniciales


class CasoInvestigacionESI(BaseModel):
    confirmo_caso_ficticio: Literal[True]

    edad_anos: StrictInt | None = None

    intervencion_inmediata: StrictBool | None = None
    situacion_alto_riesgo: StrictBool | None = None
    alteracion_conciencia_nueva: StrictBool | None = None
    dolor_o_malestar_intenso: StrictBool | None = None

    recursos_previstos: StrictInt | None = None

    pulsaciones: StrictInt | None = None
    frecuencia_respiratoria: StrictInt | None = None
    saturacion_oxigeno: StrictInt | None = None


@app.post("/investigacion/esi")
def probar_motor_investigacion(caso: CasoInvestigacionESI):
    datos = caso.model_dump()

    resultado = evaluar_etapas_iniciales(datos)

    return {
        "modo": "investigacion_con_casos_ficticios",
        "referencia": "ESI v4 - implementacion parcial",
        "resultado": resultado,
        "advertencia": (
            "Resultado no validado clinicamente. "
            "No usar para atender pacientes ni ordenar una cola real."
        )
    }

# Investigacion de extraccion con IA.
# No asigna prioridades ni modifica atenciones.

from typing import Literal
from pydantic import ValidationError


class TextoFicticioIA(BaseModel):
    confirmo_caso_ficticio: Literal[True]
    texto: str = Field(min_length=1, max_length=600)


class FragmentosIA(BaseModel):
    fragmentos: list[str] = Field(max_length=8)


@app.post("/investigacion/extraer-texto")
def extraer_texto_ficticio_ia(caso: TextoFicticioIA):
    texto = caso.texto.strip()

    if not texto:
        raise HTTPException(
            status_code=422,
            detail="Ingresa un texto ficticio."
        )

    esquema = FragmentosIA.model_json_schema()

    prompt = (
        "Esta es una prueba de software con texto completamente ficticio. "
        "Identifica fragmentos literales que describan sintomas mencionados "
        "en el texto. Conserva las negaciones si aparecen. "
        "No inventes datos, no diagnostiques y no asignes prioridad. "
        "Si no encuentras fragmentos, devuelve una lista vacia. "
        "Responde con el esquema JSON indicado. "
        "Esquema: " + json.dumps(esquema, ensure_ascii=False) +
        "\nTexto ficticio: " + json.dumps(texto, ensure_ascii=False)
    )

    solicitud = {
        "model": "qwen2.5:1.5b-instruct",
        "prompt": prompt,
        "stream": False,
        "format": esquema,
        "options": {
            "temperature": 0,
            "num_predict": 180,
            "num_ctx": 2048
        }
    }

    peticion = urllib.request.Request(
        "http://host.docker.internal:11434/api/generate",
        data=json.dumps(solicitud).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(peticion, timeout=180) as respuesta:
            resultado_modelo = json.load(respuesta)

        extraccion = FragmentosIA.model_validate_json(
            resultado_modelo.get("response", "")
        )

    except (
        urllib.error.URLError,
        socket.timeout,
        TimeoutError,
        json.JSONDecodeError,
        ValidationError
    ):
        raise HTTPException(
            status_code=503,
            detail="No se obtuvo una respuesta valida del modelo."
        )

    fragmentos = []

    for fragmento in extraccion.fragmentos:
        fragmento = fragmento.strip()

        if not fragmento or len(fragmento) > 200:
            raise HTTPException(
                status_code=502,
                detail="El modelo devolvio un fragmento invalido."
            )

        fragmentos.append({
            "texto": fragmento,
            "aparece_literalmente": fragmento.casefold() in texto.casefold()
        })

    return {
        "modo": "investigacion_con_texto_ficticio",
        "modelo": "qwen2.5:1.5b-instruct",
        "fragmentos_propuestos": fragmentos,
        "advertencia": (
            "Salida no validada. Revisar el texto original, las negaciones "
            "y el contexto. No usar para diagnostico ni triaje."
        )
    }