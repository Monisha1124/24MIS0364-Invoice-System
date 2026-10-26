import pytest
from app import create_app

@pytest.fixture()
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db"), "APP_VERSION": "v3"})
    return app.test_client()

def test_home_redirects(client):
    response = client.get("/")
    assert response.status_code == 302

def test_create_invoice(client):
    response = client.post("/invoices", data={"invoice_number":"INV-101","customer_name":"Asha","invoice_date":"2026-10-26","amount":"1250"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"INV-101" in response.data

def test_duplicate_invoice_number(client):
    data={"invoice_number":"INV-102","customer_name":"Asha","invoice_date":"2026-10-26","amount":"500"}
    client.post("/invoices",data=data)
    response=client.post("/invoices",data=data,follow_redirects=True)
    assert b"already exists" in response.data

def test_edit_invoice(client):
    data={"invoice_number":"INV-103","customer_name":"Asha","invoice_date":"2026-10-26","amount":"500"}
    client.post("/invoices",data=data)
    with client.application.app_context():
        import sqlite3
        db=sqlite3.connect(client.application.config["DATABASE"])
        invoice_id=db.execute("SELECT id FROM invoices WHERE invoice_number='INV-103'").fetchone()[0]
        db.close()
    response=client.post(f"/edit/{invoice_id}",data={"customer_name":"Meena","invoice_date":"2026-10-27","amount":"750"},follow_redirects=True)
    assert b"Meena" in response.data

def test_view_invoice(client):
    data={"invoice_number":"INV-104","customer_name":"Ravi","invoice_date":"2026-10-26","amount":"999"}
    client.post("/invoices",data=data)
    with client.application.app_context():
        import sqlite3
        db=sqlite3.connect(client.application.config["DATABASE"])
        invoice_id=db.execute("SELECT id FROM invoices WHERE invoice_number='INV-104'").fetchone()[0]
        db.close()
    response=client.get(f"/view/{invoice_id}")
    assert response.status_code == 200
    assert b"Ravi" in response.data
