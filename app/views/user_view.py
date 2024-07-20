from flask import render_template, url_for
from flask_login import current_user

def usuarios(users):
  return render_template(
    "usuarios.html",
    users=users,
    title="Lista de donantes",
    current_user=current_user,
    )
  
def registro():
  return render_template(
    "registro.html",
    title="Registro de donantes",
    current_user=current_user,
    )
  
def actualizar(user):
  return render_template(
    "actualizar.html",
    title="Actualizar donante",
    user=user,
    current_user=current_user,
    )
  
def login():
  return render_template(
    "login.html",
    title="Inicio de sesión",
    current_user=current_user,
    )
  
def perfil(user):
  return render_template(
    "profile.html",
    title="Perfil de donante",
    current_user=current_user,
    user=user,
    )

def list_donadores(users):
    return render_template(
        "create_donacion.html",
        users=users,
        title="Registrar Donación",
        current_user=current_user,
    )

# def generate_user_report(users):
#   return render_template(
#     "reportes.html",
#     title="Reporte de donantes",
#     users=users,
#     current_user=current_user,
#     )



def generate_user_report(users):
    return render_template(
        "reportes.html",
        title="Reporte de donantes",
        users=users,
        current_user=current_user,
        download_url=url_for('user.download_report')  
    )
