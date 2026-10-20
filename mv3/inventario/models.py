from datetime import datetime, timezone

from . import db


class Equipo(db.Model):
    __tablename__ = "equipos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False, index=True)
    tipo = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(80), nullable=False)
    modelo = db.Column(db.String(120), nullable=False)
    numero_serie = db.Column(db.String(120), unique=True, nullable=True)
    estado = db.Column(db.String(30), nullable=False, default="Operativo")
    ubicacion = db.Column(db.String(120), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    creado_en = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    actualizado_en = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "marca": self.marca,
            "modelo": self.modelo,
            "numero_serie": self.numero_serie,
            "estado": self.estado,
            "ubicacion": self.ubicacion,
            "ip_address": self.ip_address,
            "creado_en": self.creado_en.isoformat() if self.creado_en else None,
            "actualizado_en": self.actualizado_en.isoformat() if self.actualizado_en else None,
        }

