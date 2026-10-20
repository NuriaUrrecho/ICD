from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from .validation import ESTADOS, TIPOS


def valid_ip(_form, field):
    if not field.data:
        return
    from ipaddress import ip_address
    try:
        ip_address(field.data)
    except ValueError as exc:
        raise ValidationError("Introduce una dirección IPv4 o IPv6 válida.") from exc


class EquipoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=120)])
    tipo = SelectField("Tipo", choices=[(x, x) for x in TIPOS], validators=[DataRequired()])
    marca = StringField("Marca", validators=[DataRequired(), Length(max=80)])
    modelo = StringField("Modelo", validators=[DataRequired(), Length(max=120)])
    numero_serie = StringField("Número de serie", validators=[Optional(), Length(max=120)])
    estado = SelectField("Estado", choices=[(x, x) for x in ESTADOS], validators=[DataRequired()])
    ubicacion = StringField("Ubicación", validators=[DataRequired(), Length(max=120)])
    ip_address = StringField("Dirección IP", validators=[Optional(), Length(max=45), valid_ip])
    submit = SubmitField("Guardar equipo")

