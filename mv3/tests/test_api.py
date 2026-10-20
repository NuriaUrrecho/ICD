VALID = {
    "nombre": "Servidor de pruebas", "tipo": "Servidor", "marca": "Dell",
    "modelo": "PowerEdge", "numero_serie": "LAB-001", "estado": "Operativo",
    "ubicacion": "Rack A", "ip_address": "192.0.2.10",
}


def test_health_and_empty_list(client):
    assert client.get("/api/health").get_json()["database"] == "connected"
    response = client.get("/api/equipos")
    assert response.status_code == 200
    assert response.get_json()["total"] == 0


def test_crud_complete(client):
    created = client.post("/api/equipos", json=VALID)
    assert created.status_code == 201
    equipo_id = created.get_json()["id"]
    assert client.get(f"/api/equipos/{equipo_id}").get_json()["nombre"] == VALID["nombre"]
    updated = client.patch(f"/api/equipos/{equipo_id}", json={"estado": "Mantenimiento"})
    assert updated.status_code == 200
    assert updated.get_json()["estado"] == "Mantenimiento"
    assert client.get("/api/equipos?q=PowerEdge").get_json()["total"] == 1
    assert client.delete(f"/api/equipos/{equipo_id}").status_code == 204
    assert client.get(f"/api/equipos/{equipo_id}").status_code == 404


def test_validation_and_duplicate_serial(client):
    invalid = client.post("/api/equipos", json={"nombre": "", "ip_address": "999.1.1.1"})
    assert invalid.status_code == 400
    assert "nombre" in invalid.get_json()["details"]
    assert "ip_address" in invalid.get_json()["details"]
    assert client.post("/api/equipos", json=VALID).status_code == 201
    duplicate = {**VALID, "nombre": "Otro servidor"}
    assert client.post("/api/equipos", json=duplicate).status_code == 409


def test_web_pages(client):
    assert client.get("/").status_code == 200
    assert client.get("/equipos/nuevo").status_code == 200

