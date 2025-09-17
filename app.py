from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "change-this-in-production")

@app.template_filter('isoutc')
def isoutc(dt: datetime):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

@app.route("/", methods=["GET", "POST"])
def index():
    # Valores padrão para o formulário
    nome = ""
    sobrenome = ""
    instituicao = ""
    disciplina = ""

    # Se o formulário for enviado por POST, captura os valores
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        sobrenome = request.form.get("sobrenome", "").strip()
        instituicao = request.form.get("instituicao", "").strip()
        disciplina = request.form.get("disciplina", "").strip()

    # Tentativas de obter IP e host do cliente (podem vir como None em alguns ambientes)
    ip_remoto = request.remote_addr or None
    host_app = request.host or None

    agora = datetime.utcnow()

    return render_template(
        "index.html",
        nome=nome,
        sobrenome=sobrenome,
        instituicao=instituicao,
        disciplina=disciplina,
        ip_remoto=ip_remoto,
        host_app=host_app,
        agora=agora
    )

@app.route("/login", methods=["GET","POST"])
def login():
    msg = ""
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        senha = request.form.get("senha", "")
        # Implementação simples de exemplo — NÃO usar assim em produção
        if usuario == "admin" and senha == "admin":
            return redirect(url_for("index"))
        else:
            msg = "Usuário ou senha inválidos"
    return render_template("login.html", mensagem=msg)

if __name__ == "__main__":
    app.run(debug=True)
