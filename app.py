import os, sqlite3
from flask import Flask, request, redirect, url_for, render_template, flash, abort

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "local-demo-secret"),
        DATABASE=os.environ.get("DATABASE", os.path.join(app.instance_path, "invoices.db")),
        APP_VERSION=os.environ.get("APP_VERSION", "v3").lower(),
    )
    if test_config:
        app.config.update(test_config)
    os.makedirs(os.path.dirname(app.config["DATABASE"]) or ".", exist_ok=True)

    def connect():
        db = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
        return db

    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS invoices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            invoice_date TEXT NOT NULL,
            amount REAL NOT NULL
        )""")

    version = app.config["APP_VERSION"]
    if version not in ("v1", "v2", "v3"):
        raise ValueError("APP_VERSION must be v1, v2, or v3")

    @app.context_processor
    def inject_version():
        return {"app_version": version}

    @app.get("/")
    def index():
        return redirect(url_for("invoices"))

    @app.get("/health")
    def health():
        return {"status": "healthy", "version": version}, 200

    @app.route("/invoices", methods=["GET", "POST"])
    def invoices():
        if request.method == "POST":
            number = request.form.get("invoice_number", "").strip()
            customer = request.form.get("customer_name", "").strip()
            date = request.form.get("invoice_date", "").strip()
            amount_text = request.form.get("amount", "").strip()
            try:
                amount = float(amount_text)
                if amount < 0: raise ValueError()
                if not all((number, customer, date)): raise ValueError()
                with connect() as db:
                    db.execute("INSERT INTO invoices(invoice_number,customer_name,invoice_date,amount) VALUES(?,?,?,?)",
                               (number, customer, date, amount))
                flash("Invoice created successfully.", "success")
            except sqlite3.IntegrityError:
                flash("Invoice number already exists.", "error")
            except ValueError:
                flash("Enter all fields and a valid non-negative amount.", "error")
            return redirect(url_for("invoices"))
        with connect() as db:
            rows = db.execute("SELECT * FROM invoices ORDER BY id DESC").fetchall()
        return render_template("invoices.html", invoices=rows)

    @app.route("/edit/<int:invoice_id>", methods=["GET", "POST"])
    def edit(invoice_id):
        if version == "v1": abort(404)
        with connect() as db:
            invoice = db.execute("SELECT * FROM invoices WHERE id=?", (invoice_id,)).fetchone()
            if invoice is None: abort(404)
            if request.method == "POST":
                customer = request.form.get("customer_name", "").strip()
                date = request.form.get("invoice_date", "").strip()
                try:
                    amount = float(request.form.get("amount", ""))
                    if not customer or not date or amount < 0: raise ValueError()
                    db.execute("UPDATE invoices SET customer_name=?, invoice_date=?, amount=? WHERE id=?",
                               (customer, date, amount, invoice_id))
                    flash("Invoice updated successfully.", "success")
                    return redirect(url_for("invoices"))
                except ValueError:
                    flash("Enter valid invoice details.", "error")
        return render_template("edit.html", invoice=invoice)

    @app.get("/view/<int:invoice_id>")
    def view(invoice_id):
        if version != "v3": abort(404)
        with connect() as db:
            invoice = db.execute("SELECT * FROM invoices WHERE id=?", (invoice_id,)).fetchone()
        if invoice is None: abort(404)
        return render_template("view.html", invoice=invoice)

    return app

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
