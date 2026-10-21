VALID = {
    "titulo": "Aviso de prueba",
    "descripcion": "Comprobación automatizada del tablón.",
    "categoria": "Mantenimiento",
    "prioridad": "Media",
}


def test_health_and_empty_list(client):
    assert client.get("/health").get_json()["database"] == "connected"
    response = client.get("/api/avisos")
    assert response.status_code == 200
    assert response.get_json()["total"] == 0


def test_crud_complete(client):
    created = client.post("/api/avisos", json=VALID)
    assert created.status_code == 201
    aviso_id = created.get_json()["id"]
    assert client.get(f"/api/avisos/{aviso_id}").get_json()["titulo"] == VALID["titulo"]
    updated = client.patch(f"/api/avisos/{aviso_id}", json={"prioridad": "Alta"})
    assert updated.status_code == 200
    assert updated.get_json()["prioridad"] == "Alta"
    assert client.get("/api/avisos?prioridad=Alta").get_json()["total"] == 1
    assert client.delete(f"/api/avisos/{aviso_id}").status_code == 204
    assert client.get(f"/api/avisos/{aviso_id}").status_code == 404


def test_validation(client):
    invalid = client.post("/api/avisos", json={"titulo": "", "categoria": "Incorrecta"})
    assert invalid.status_code == 400
    assert "titulo" in invalid.get_json()["details"]
    assert "categoria" in invalid.get_json()["details"]
    assert "descripcion" in invalid.get_json()["details"]


def test_web_pages(client):
    assert client.get("/").status_code == 200
    created = client.post("/avisos", data=VALID, follow_redirects=True)
    assert created.status_code == 200
    assert "Aviso de prueba" in created.get_data(as_text=True)

