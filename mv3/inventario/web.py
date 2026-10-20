from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from . import db
from .forms import EquipoForm
from .models import Equipo

web_bp = Blueprint("web", __name__)


@web_bp.get("/")
def index():
    query = request.args.get("q", "").strip()
    statement = db.select(Equipo).order_by(Equipo.id.desc())
    if query:
        term = f"%{query}%"
        statement = statement.where(or_(
            Equipo.nombre.ilike(term), Equipo.tipo.ilike(term), Equipo.marca.ilike(term),
            Equipo.modelo.ilike(term), Equipo.numero_serie.ilike(term),
            Equipo.ubicacion.ilike(term), Equipo.ip_address.ilike(term),
        ))
    equipos = db.session.execute(statement).scalars().all()
    return render_template(
        "index.html", equipos=equipos, query=query,
        student=current_app.config["STUDENT_NAME"], server_ip=current_app.config["SERVER_IP"],
    )


@web_bp.route("/equipos/nuevo", methods=["GET", "POST"])
def crear_equipo():
    form = EquipoForm()
    if form.validate_on_submit():
        equipo = Equipo()
        form.populate_obj(equipo)
        equipo.numero_serie = equipo.numero_serie or None
        equipo.ip_address = equipo.ip_address or None
        db.session.add(equipo)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            form.numero_serie.errors.append("Ese número de serie ya existe.")
        else:
            flash("Equipo registrado correctamente.", "success")
            return redirect(url_for("web.index"))
    return render_template("form.html", form=form, title="Nuevo equipo")


@web_bp.route("/equipos/<int:equipo_id>/editar", methods=["GET", "POST"])
def editar_equipo(equipo_id):
    equipo = db.session.get(Equipo, equipo_id) or abort(404)
    form = EquipoForm(obj=equipo)
    if form.validate_on_submit():
        form.populate_obj(equipo)
        equipo.numero_serie = equipo.numero_serie or None
        equipo.ip_address = equipo.ip_address or None
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            form.numero_serie.errors.append("Ese número de serie ya existe.")
        else:
            flash("Equipo actualizado.", "success")
            return redirect(url_for("web.index"))
    return render_template("form.html", form=form, title="Editar equipo")


@web_bp.post("/equipos/<int:equipo_id>/eliminar")
def eliminar_equipo(equipo_id):
    equipo = db.session.get(Equipo, equipo_id) or abort(404)
    db.session.delete(equipo)
    db.session.commit()
    flash("Equipo eliminado.", "success")
    return redirect(url_for("web.index"))

