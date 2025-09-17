from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "change-this-in-production")

# filtro customizado para mostrar data em UTC formatada
@app.template_filter('isoutc')
def isoutc(dt: datetime):
    return dt.strftime("%B %d, %Y %I:%M %p")


# rota principal (home)
@app.route("/", methods=["GET", "POST"])
def index():
    nome = ""
    sobrenome = ""
    instituicao = ""
    disciplina = ""

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        sobrenome = request.form.get("sobrenome", "").strip()
        instituicao = request.form.get("instituicao", "").strip()
        disciplina = request.form.get("disciplina", "").strip()

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


# rota de login
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "").strip()

        if usuario and senha:
            session["usuario"] = usuario
            return redirect(url_for("dados"))
        else:
            msg = "Usuário ou senha inválidos"

    return render_template("login.html", mensagem=msg, agora=datetime.utcnow())



# rota dados do acesso (após login)
@app.route("/dados")
def dados():
    usuario = session.get("usuario", "desconhecido")
    agora = datetime.utcnow()
    return render_template("dados.html", usuario=usuario, agora=agora)


# rota logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
