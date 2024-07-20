from flask import Blueprint, request, redirect, url_for, flash,Response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from utils.decorators import role_required
from views import user_view
from models.user_model import User
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

user_bp = Blueprint("user", __name__)

@user_bp.route("/")
def index():
  if current_user.is_authenticated:
    return redirect(url_for("user.profile", id=current_user.id))
  return redirect(url_for("user.login"))

@user_bp.route("/users")
@login_required
def list_users():
  users = User.get_all()
  return user_view.usuarios(users)

@user_bp.route("/users/create", methods=["GET", "POST"])
def create_user():
  if request.method == "POST":
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    direccion = request.form["direccion"]
    fecha_registro = request.form["fecha_registro"]
    fecha_registro = datetime.strptime(fecha_registro, "%Y-%m-%d")
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
      flash("El nombre de usuario ya está en uso.", "error")
      return redirect(url_for("user.create_user"))
    #nombre, apellido, email, telefono, direccion, fecha_registro, username, password, role="donante"):
    user = User(nombre, apellido, email, telefono, direccion, fecha_registro, username, password, role=role)
    user.set_password(password)
    user.save()
    flash("Usuario registrado con éxito.", "success")
    return redirect(url_for("user.list_users"))
  return user_view.registro()

@user_bp.route("/users/<int:id>/update", methods=["GET", "POST"])
@login_required
@role_required("admin")
def update_user(id):
  user = User.get_by_id(id)
  if not user:
    return "Usuario no encontrado", 404
  if request.method == "POST":
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]

    user.nombre = nombre
    user.apellido = apellido
    user.update()
    return redirect(url_for("user.list_users"))
  return user_view.actualizar(user)

@user_bp.route("/users/<int:id>/delete")
@login_required
@role_required("admin")
def delete_user(id):
  user = User.get_by_id(id)
  if not user:
    return "Usuario no encontrado", 404
  user.delete()
  return redirect(url_for("user.list_users"))

@user_bp.route("/login", methods=["GET", "POST"])
def login():
  # print post 
  print(request.form)
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    user = User.get_user_by_username(username)
    print(user)
    print(username)
    if user and check_password_hash(user.password_hash, password):
      login_user(user)
      flash("Inicio de sesión exitoso.", "success")
      if user.has_role("admin"):
        return redirect(url_for("user.list_users"))
      else:
        return redirect(url_for("user.profile", id=user.id))
    else:
      flash("Nombre de usuario o contraseña incorrectos", "error")
  return user_view.login()

# Ruta para cerrar sesión
@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("user.login"))


@user_bp.route("/profile/<int:id>")
@login_required
def profile(id):
    user = User.get_by_id(id)
    return user_view.perfil(user)


@user_bp.route("/users/report")
@login_required
def user_report():
    users = User.get_all()
    return user_view.generate_user_report(users)

# @user_bp.route("/reports/")
# @login_required
# @role_required("admin")
# def reports(id):
#     user = User.get_by_id(id)
#     return user_view.perfil(user)



@user_bp.route("/users/report/download")
@login_required
def download_report():
    users = User.get_all()

    # Crear un buffer de memoria para el archivo PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Crear un objeto para la página
    elements = []
    
    # Estilo para el título
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    
    # Agregar título al documento
    title = Paragraph("Reporte de Sistema de gestión de donaciones - donantes ", title_style)
    elements.append(title)
    
    # Espacio debajo del título
    elements.append(Paragraph("<br/>", styles['Normal']))
    
    # Definir los datos para la tabla
    data = [["Nombre", "Apellido", "Usuario", "Correo", "Dirección", "Teléfono", "Fecha de registro"]]
    for user in users:
        data.append([
            user.nombre,
            user.apellido,
            user.username,
            user.email,  # Usa `user.email` en lugar de `user.correo`
            user.direccion,
            user.telefono,
            user.fecha_registro.strftime("%Y-%m-%d")
        ])
    
    # Crear una tabla y definir el estilo
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#FFFFFF'),  # Color de fondo para el encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),    # Color del texto para el encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),         # Alineación del texto
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente del encabezado
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),        # Padding en la parte inferior del encabezado
        ('BACKGROUND', (0, 1), (-1, -1), '#FFFFFF'),  # Color de fondo para las filas
        ('GRID', (0, 0), (-1, -1), 1, '#000000')      # Cuadrícula alrededor de la tabla
    ]))
    
    # Agregar la tabla al documento
    elements.append(table)
    
    # Crear el documento PDF
    doc.build(elements)
    
    buffer.seek(0)
    return Response(buffer, mimetype='application/pdf', headers={"Content-Disposition": "attachment;filename=reportes_donantes.pdf"})
