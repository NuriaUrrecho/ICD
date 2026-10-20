from flask import Blueprint, jsonify, request
from sqlalchemy import or_, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from . import db
from .models import Equipo
from .validation import clean_equipo_payload

api_bp = Blueprint("api", __name__)


def error(message, status, details=None):
    payload = {"error": message}
    if details:
        payload["details"] = details
    return jsonify(payload), status


@api_bp.get("/health")
def health():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "ok", "database": "connected"})
    except SQLAlchemyError:
        return jsonify({"status": "error", "database": "unavailable"}), 503


@api_bp.get("/equipos")
def listar():
    query = request.args.get("q", "").strip()
    statement = db.select(Equipo).order_by(Equipo.id.desc())
    if query:
        term = f"%{query}%"
        statement = statement.where(or_(
            Equipo.nombre.ilike(term), Equipo.tipo.ilike(term), Equipo.marca.ilike(term),
            Equipo.modelo.ilike(term), Equipo.numero_serie.ilike(term), Equipo.ubicacion.ilike(term),
        ))
    items = db.session.execute(statement).scalars().all()
    return jsonify({"items": [item.to_dict() for item in items], "total": len(items)})


@api_bp.post("/equipos")
def crear():
    if not request.is_json:
        return error("Se requiere Content-Type application/json.", 415)
    data, errors = clean_equipo_payload(request.get_json(silent=True) or {})
    if errors:
        return error("Datos no válidos.", 400, errors)
    equipo = Equipo(**data)
    db.session.add(equipo)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error("El número de serie ya existe.", 409)
    return jsonify(equipo.to_dict()), 201


@api_bp.get("/equipos/<int:equipo_id>")
def obtener(equipo_id):
    equipo = db.session.get(Equipo, equipo_id)
    return jsonify(equipo.to_dict()) if equipo else error("Equipo no encontrado.", 404)


@api_bp.route("/equipos/<int:equipo_id>", methods=["PUT", "PATCH"])
def actualizar(equipo_id):
    equipo = db.session.get(Equipo, equipo_id)
    if not equipo:
        return error("Equipo no encontrado.", 404)
    if not request.is_json:
        return error("Se requiere Content-Type application/json.", 415)
    partial = request.method == "PATCH"
    data, errors = clean_equipo_payload(request.get_json(silent=True) or {}, partial=partial)
    if errors:
        return error("Datos no válidos.", 400, errors)
    if not data:
        return error("No se proporcionaron campos válidos.", 400)
    for key, value in data.items():
        setattr(equipo, key, value)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error("El número de serie ya existe.", 409)
    return jsonify(equipo.to_dict())


@api_bp.delete("/equipos/<int:equipo_id>")
def eliminar(equipo_id):
    equipo = db.session.get(Equipo, equipo_id)
    if not equipo:
        return error("Equipo no encontrado.", 404)
    db.session.delete(equipo)
    db.session.commit()
    return "", 204
