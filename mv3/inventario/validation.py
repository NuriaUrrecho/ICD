from ipaddress import ip_address

TIPOS = ("Sobremesa", "Portátil", "Servidor", "Impresora", "Red", "Otro")
ESTADOS = ("Operativo", "Mantenimiento", "Retirado")
FIELDS = ("nombre", "tipo", "marca", "modelo", "numero_serie", "estado", "ubicacion", "ip_address")
REQUIRED = ("nombre", "tipo", "marca", "modelo", "estado", "ubicacion")
MAX_LENGTHS = {
    "nombre": 120,
    "tipo": 50,
    "marca": 80,
    "modelo": 120,
    "numero_serie": 120,
    "estado": 30,
    "ubicacion": 120,
    "ip_address": 45,
}


def clean_equipo_payload(source, partial=False):
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
    if data.get("tipo") and data["tipo"] not in TIPOS:
        errors["tipo"] = "Tipo no válido."
    if data.get("estado") and data["estado"] not in ESTADOS:
        errors["estado"] = "Estado no válido."
    if data.get("ip_address"):
        try:
            ip_address(data["ip_address"])
        except ValueError:
            errors["ip_address"] = "Introduce una dirección IPv4 o IPv6 válida."
    return data, errors

