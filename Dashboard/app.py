from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=BASE_DIR, static_folder=BASE_DIR)
CORS(app)

# ── SQLAlchemy engine (resolve o warning do pandas) ──────────
engine = create_engine(
    "mysql+mysqlconnector://root:janeiro2002@localhost/churn_project"
)

def query(sql):
    """Executa uma query e retorna lista de dicts."""
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        cols = result.keys()
        return [dict(zip(cols, row)) for row in result.fetchall()]


# ── Serve o front-end ─────────────────────────────────────────
@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/style.css")
def css():
    return app.send_static_file("style.css")

@app.route("/script.js")
def js():
    return app.send_static_file("script.js")


# ── Total de clientes ─────────────────────────────────────────
@app.route("/clientes_total")
def clientes_total():
    return jsonify(query("SELECT COUNT(*) AS total_clientes FROM customers_churn"))


# ── Churn rate ────────────────────────────────────────────────
@app.route("/churn_rate")
def churn_rate():
    return jsonify(query("""
        SELECT
            SUM(CASE WHEN churn = 1 THEN 1 ELSE 0 END)          AS total_churn,
            COUNT(*)                                              AS total_clientes,
            ROUND(
                SUM(CASE WHEN churn = 1 THEN 1 ELSE 0 END)
                * 100.0 / COUNT(*), 2
            )                                                    AS churn_rate
        FROM customers_churn
    """))


# ── Ativo vs Churn ────────────────────────────────────────────
@app.route("/churn")
def churn():
    return jsonify(query("""
        SELECT churn, COUNT(*) AS total
        FROM customers_churn
        GROUP BY churn
    """))


# ── Receita média ─────────────────────────────────────────────
@app.route("/receita_media")
def receita_media():
    return jsonify(query("""
        SELECT ROUND(AVG(total_revenue), 2) AS receita_media
        FROM customers_churn
    """))


# ── Ticket médio ──────────────────────────────────────────────
@app.route("/ticket_medio")
def ticket_medio():
    return jsonify(query("""
        SELECT ROUND(AVG(average_ticket), 2) AS ticket_medio
        FROM customers_churn
    """))


# ── Segmento (criado via CASE WHEN — sem coluna extra) ────────
#   Regra de negócio:
#   Premium      → receita total >= 500
#   Intermediário → receita total >= 200
#   Inativo      → churn = 1 e receita < 200
#   Básico       → demais
@app.route("/segmento")
def segmento():
    return jsonify(query("""
        SELECT
            segmento,
            COUNT(*)                                 AS total,
            SUM(churn)                               AS total_churn,
            ROUND(SUM(churn) * 100.0 / COUNT(*), 1) AS taxa_churn
        FROM (
            SELECT
                churn,
                CASE
                    WHEN total_revenue >= 500               THEN 'Premium'
                    WHEN total_revenue >= 200               THEN 'Intermediário'
                    WHEN churn = 1 AND total_revenue < 200  THEN 'Inativo'
                    ELSE 'Básico'
                END AS segmento
            FROM customers_churn
        ) t
        GROUP BY segmento
        ORDER BY taxa_churn DESC
    """))


# ── Distribuição por dias sem compra ──────────────────────────
@app.route("/distribuicao_dias")
def distribuicao_dias():
    return jsonify(query("""
        SELECT
            CASE
                WHEN days_since_last_purchase <= 30  THEN '0-30 dias'
                WHEN days_since_last_purchase <= 60  THEN '31-60 dias'
                WHEN days_since_last_purchase <= 90  THEN '61-90 dias'
                WHEN days_since_last_purchase <= 120 THEN '91-120 dias'
                ELSE '120+ dias'
            END AS faixa,
            COUNT(*) AS total
        FROM customers_churn
        GROUP BY faixa
        ORDER BY MIN(days_since_last_purchase)
    """))


# ── Entry point ───────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)