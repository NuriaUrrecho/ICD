from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for

from . import db
from .models import Aviso
from .validation import CATEGORIAS, PRIORIDADES, clean_aviso_payload

web_bp = Blueprint("web", __name__)


@web_bp.get("/health")
def health():
    from .api import health_response

    return health_response()


@web_bp.get("/")
def index():
    categoria = request.args.get("categoria", "").strip()
    prioridad = request.args.get("prioridad", "").strip()
    statement = db.select(Aviso).order_by(Aviso.fecha_publicacion.desc(), Aviso.id.desc())
    if categoria in CATEGORIAS:
        statement = statement.where(Aviso.categoria == categoria)
    if prioridad in PRIORIDADES:
        statement = statement.where(Aviso.prioridad == prioridad)
    avisos = db.session.execute(statement).scalars().all()
    return render_template(
        "index.html",
        avisos=avisos,
        categorias=CATEGORIAS,
        prioridades=PRIORIDADES,
        categoria_actual=categoria,
        prioridad_actual=prioridad,
        student=current_app.config["STUDENT_NAME"],
        server_ip=current_app.config["SERVER_IP"],
    )


@web_bp.post("/avisos")
def crear_aviso():
    data, errors = clean_aviso_payload(request.form)
    if errors:
        flash("Revisa el formulario: todos los campos son obligatorios.", "error")
        return redirect(url_for("web.index"))
    db.session.add(Aviso(**data))
    db.session.commit()
    flash("Aviso publicado correctamente.", "success")
    return redirect(url_for("web.index"))


@web_bp.post("/avisos/<int:aviso_id>/eliminar")
def eliminar_aviso(aviso_id):
    aviso = db.session.get(Aviso, aviso_id) or abort(404)
    db.session.delete(aviso)
    db.session.commit()
    flash("Aviso eliminado.", "success")
    return redirect(url_for("web.index"))
