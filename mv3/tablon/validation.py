CATEGORIAS = ("Mantenimiento", "Incidencia", "Seguridad", "General")
PRIORIDADES = ("Baja", "Media", "Alta", "Crítica")
FIELDS = ("titulo", "descripcion", "categoria", "prioridad")
REQUIRED = FIELDS
MAX_LENGTHS = {"titulo": 120, "descripcion": 2000, "categoria": 30, "prioridad": 20}


def clean_aviso_payload(source, partial=False):
    data = {}
    errors = {}
    for field in FIELDS:
        if field not in source:
            continue
        value = source.get(field)
        value = value.strip() if isinstance(value, str) else value
        data[field] = value or None

    if not partial:
        for field in REQUIRED:
            if not data.get(field):
                errors[field] = "Este campo es obligatorio."
    else:
        for field in REQUIRED:
            if field in data and not data[field]:
                errors[field] = "Este campo no puede quedar vacío."

    for field, value in data.items():
        if value and len(str(value)) > MAX_LENGTHS[field]:
            errors[field] = f"Máximo {MAX_LENGTHS[field]} caracteres."
    if data.get("categoria") and data["categoria"] not in CATEGORIAS:
        errors["categoria"] = "Categoría no válida."
    if data.get("prioridad") and data["prioridad"] not in PRIORIDADES:
        errors["prioridad"] = "Prioridad no válida."
    return data, errors
