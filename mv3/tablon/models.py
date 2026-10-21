from datetime import datetime, timezone

from . import db


class Aviso(db.Model):
    __tablename__ = "avisos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False, index=True)
    descripcion = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(30), nullable=False, index=True)
    prioridad = db.Column(db.String(20), nullable=False, index=True)
    fecha_publicacion = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "prioridad": self.prioridad,
            "fecha_publicacion": (
                self.fecha_publicacion.isoformat() if self.fecha_publicacion else None
            ),
        }
