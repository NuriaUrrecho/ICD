from flask import Blueprint, jsonify, request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from . import db
from .models import Aviso
from .validation import CATEGORIAS, PRIORIDADES, clean_aviso_payload

api_bp = Blueprint("api", __name__)


def error(message, status, details=None):
    payload = {"error": message}
    if details:
        payload["details"] = details
    return jsonify(payload), status


@api_bp.get("/avisos")
def listar_avisos():
    categoria = request.args.get("categoria", "").strip()
    prioridad = request.args.get("prioridad", "").strip()
    statement = db.select(Aviso).order_by(Aviso.fecha_publicacion.desc(), Aviso.id.desc())
    if categoria:
        if categoria not in CATEGORIAS:
            return error("Categoría no válida.", 400)
        statement = statement.where(Aviso.categoria == categoria)
    if prioridad:
        if prioridad not in PRIORIDADES:
            return error("Prioridad no válida.", 400)
        statement = statement.where(Aviso.prioridad == prioridad)
    avisos = db.session.execute(statement).scalars().all()
    return jsonify({"items": [aviso.to_dict() for aviso in avisos], "total": len(avisos)})


@api_bp.post("/avisos")
def crear_aviso():
    if not request.is_json:
        return error("Se requiere Content-Type application/json.", 415)
    data, errors = clean_aviso_payload(request.get_json(silent=True) or {})
    if errors:
        return error("Datos no válidos.", 400, errors)
    aviso = Aviso(**data)
    db.session.add(aviso)
    db.session.commit()
    return jsonify(aviso.to_dict()), 201


@api_bp.get("/avisos/<int:aviso_id>")
def obtener_aviso(aviso_id):
    aviso = db.session.get(Aviso, aviso_id)
    return jsonify(aviso.to_dict()) if aviso else error("Aviso no encontrado.", 404)


@api_bp.route("/avisos/<int:aviso_id>", methods=["PUT", "PATCH"])
def actualizar_aviso(aviso_id):
    aviso = db.session.get(Aviso, aviso_id)
    if not aviso:
        return error("Aviso no encontrado.", 404)
    if not request.is_json:
        return error("Se requiere Content-Type application/json.", 415)
    partial = request.method == "PATCH"
    data, errors = clean_aviso_payload(request.get_json(silent=True) or {}, partial=partial)
    if errors:
        return error("Datos no válidos.", 400, errors)
    if not data:
        return error("No se proporcionaron campos válidos.", 400)
    for field, value in data.items():
        setattr(aviso, field, value)
    db.session.commit()
    return jsonify(aviso.to_dict())


@api_bp.delete("/avisos/<int:aviso_id>")
def eliminar_aviso(aviso_id):
    aviso = db.session.get(Aviso, aviso_id)
    if not aviso:
        return error("Aviso no encontrado.", 404)
    db.session.delete(aviso)
    db.session.commit()
    return "", 204


@api_bp.get("/health")
def api_health():
    return health_response()


def health_response():
    try:
        version_sql = "SELECT sqlite_version()" if db.engine.dialect.name == "sqlite" else "SELECT VERSION()"
        version = db.session.execute(text(version_sql))
        database_version = str(version.scalar_one())
        total = db.session.execute(db.select(db.func.count(Aviso.id))).scalar_one()
        return jsonify(
            status="ok",
            database="connected",
            database_version=database_version,
            avisos=total,
        )
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(status="error", database="unavailable"), 503


