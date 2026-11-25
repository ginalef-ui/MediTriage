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


@app.post("/atenciones", status_code=201)
def registrar_atencion(atencion: AtencionNueva):
    sintomas = atencion.sintomas.strip()

    if len(sintomas) < 2:
        raise HTTPException(
            status_code=422,
            detail="Ingresa los sintomas ficticios."
        )

    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO atenciones (
                        paciente_id,
                        sintomas,
                        pulsaciones,
                        presion_arterial
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING *
                    """,
                    (
                        atencion.paciente_id,
                        sintomas,
                        atencion.pulsaciones,
                        atencion.presion_arterial
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

class ConfirmacionPrioridad(BaseModel):
    prioridad: int = Field(ge=1, le=5)
    motivo: str = Field(default="", max_length=500)


@app.post("/atenciones/{atencion_id}/confirmar")
def confirmar_prioridad(
    atencion_id: int,
    confirmacion: ConfirmacionPrioridad
):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE atenciones
                    SET prioridad_confirmada = %s,
                        motivo_cambio = %s,
                        estado = 'esperando',
                        fecha_confirmacion = CURRENT_TIMESTAMP
                    WHERE id = %s AND estado = 'pendiente'
                    RETURNING *
                    """,
                    (
                        confirmacion.prioridad,
                        confirmacion.motivo.strip(),
                        atencion_id
                    )
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
                        detail="La atencion ya no esta pendiente."
                    )

        return atencion

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
                        prioridad_confirmada,
                        estado,
                        motivo_cambio,
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

        return {
            "paciente": paciente,
            "atenciones": atenciones
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