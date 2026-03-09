from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os

app = Flask(__name__, static_folder=os.path.dirname(os.path.abspath(__file__)))
CORS(app)

# Conexão via variáveis de ambiente do Railway
DB_USER = os.environ.get("MYSQLUSER", "root")
DB_PASS = os.environ.get("MYSQLPASSWORD", "janeiro2002")
DB_HOST = os.environ.get("MYSQLHOST", "localhost")
DB_PORT = os.environ.get("MYSQLPORT", "3306")
DB_NAME = os.environ.get("MYSQLDATABASE", "churn_project")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Arquivos estáticos ───────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/style.css")
def style():
    return send_from_directory(BASE_DIR, "style.css")

@app.route("/script.js")
def script():
    return send_from_directory(BASE_DIR, "script.js")

# ── Endpoints de dados ───────────────────────────────────────
@app.route("/clientes_total")
def clientes_total():
    with engine.connect() as con:
        result = con.execute(text("SELECT COUNT(*) AS total_clientes FROM customers_churn"))
        return jsonify([dict(row._mapping) for row in result])

@app.route("/churn_rate")
def churn_rate():
    with engine.connect() as con:
        result = con.execute(text("""
            SELECT
                SUM(churn) AS total_churn,
                COUNT(*) AS total_clientes,
                ROUND(SUM(churn) / COUNT(*) * 100, 2) AS churn_rate
            FROM customers_churn
        """))
        return jsonify([dict(row._mapping) for row in result])

@app.route("/churn")
def churn():
    with engine.connect() as con:
        result = con.execute(text("""
            SELECT churn, COUNT(*) AS total
            FROM customers_churn
            GROUP BY churn
        """))
        return jsonify([dict(row._mapping) for row in result])

@app.route("/receita_media")
def receita_media():
    with engine.connect() as con:
        result = con.execute(text("SELECT ROUND(AVG(total_revenue), 2) AS receita_media FROM customers_churn"))
        return jsonify([dict(row._mapping) for row in result])

@app.route("/ticket_medio")
def ticket_medio():
    with engine.connect() as con:
        result = con.execute(text("SELECT ROUND(AVG(average_ticket), 2) AS ticket_medio FROM customers_churn"))
        return jsonify([dict(row._mapping) for row in result])

@app.route("/segmento")
def segmento():
    with engine.connect() as con:
        result = con.execute(text("""
            SELECT
                CASE
                    WHEN total_revenue >= 500 THEN 'Premium'
                    WHEN total_revenue >= 200 THEN 'Intermediario'
                    WHEN churn = 1 AND total_revenue < 200 THEN 'Inativo'
                    ELSE 'Basico'
                END AS segmento,
                COUNT(*) AS total,
                SUM(churn) AS total_churn,
                ROUND(SUM(churn) / COUNT(*) * 100, 2) AS taxa_churn
            FROM customers_churn
            GROUP BY segmento
        """))
        return jsonify([dict(row._mapping) for row in result])

@app.route("/distribuicao_dias")
def distribuicao_dias():
    with engine.connect() as con:
        result = con.execute(text("""
            SELECT
                CASE
                    WHEN days_since_last_purchase <= 30  THEN '0-30'
                    WHEN days_since_last_purchase <= 60  THEN '31-60'
                    WHEN days_since_last_purchase <= 90  THEN '61-90'
                    WHEN days_since_last_purchase <= 120 THEN '91-120'
                    ELSE '120+'
                END AS faixa,
                COUNT(*) AS total
            FROM customers_churn
            GROUP BY faixa
            ORDER BY MIN(days_since_last_purchase)
        """))
        return jsonify([dict(row._mapping) for row in result])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)