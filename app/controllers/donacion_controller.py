from flask import Blueprint, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from models.donacion_model import Donacion
from models.user_model import User
from views import donacion_view
from utils.decorators import role_required
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

donacion_bp = Blueprint("donacion", __name__)

@donacion_bp.route("/donaciones")
@login_required
def list_donaciones():
    donaciones = Donacion.get_all()
    return donacion_view.list_donaciones(donaciones)


@donacion_bp.route("/donaciones/create", methods=["GET", "POST"])
@login_required
def create_donacion():
    if request.method == "POST":
        username = request.form["username_donante"]
        monto = request.form["monto"]
        fecha_donacion = request.form["fecha_donacion"]
        fecha_donacion = datetime.strptime(fecha_donacion, "%Y-%m-%d").date()
        metodo_pago = request.form["metodo_pago"]
        
        donacion = Donacion(username=username, monto=monto, fecha_donacion=fecha_donacion, metodo_pago=metodo_pago)
        donacion.save()
        flash("Donación creada correctamente.", "success")
        return redirect(url_for("user.profile", id=current_user.id))
    
    users = User.get_all()
    return donacion_view.create_donacion(users, current_user)

@donacion_bp.route("/donaciones/<int:id>/update", methods=["GET", "POST"])
@login_required
@role_required("admin")
def update_donacion(id):
  donacion = Donacion.get_by_id(id)
  if request.method == "POST":
    username = request.form["username"]
    monto = float(request.form["monto"])
    fecha_donacion = request.form["fecha_donacion"]
    fecha_donacion = datetime.strptime(fecha_donacion, "%Y-%m-%d").date()
    metodo_pago = request.form["metodo_pago"]
    donacion.update(username=username, monto=monto, fecha_donacion=fecha_donacion, metodo_pago=metodo_pago)
    flash("Donación actualizada correctamente.", "success")
    return redirect(url_for("donacion.list_donaciones"))
  return donacion_view.update_donacion(donacion)

@donacion_bp.route("/donaciones/<int:id>/delete")
@login_required
@role_required("admin")
def delete_donacion(id):
  donacion = Donacion.get_by_id(id)
  if not donacion:
    return "Donacion no encontrada", 404
  donacion.delete()
  flash("Donación eliminada correctamente.", "success")
  return redirect(url_for("donacion.list_donaciones"))




@donacion_bp.route("/donaciones/report")
@login_required
def donaciones_report():
    donaciones = Donacion.get_all()
    return donacion_view.generate_donaciones_report(donaciones)



@donacion_bp.route("/donaciones/report/download")
@login_required
def download_report():
    donaciones = Donacion.get_all()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    elements = []
    
    # Estilo para el título
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    
    # Agregar título al documento
    title = Paragraph("Reporte de Donaciones", title_style)
    elements.append(title)
    
    # Espacio debajo del título
    elements.append(Paragraph("<br/>", styles['Normal']))
    
    # Definir los datos para la tabla
    data = [["Usuario", "Monto Donado", "Fecha de Donación", "Método de Pago"]]
    for donacion in donaciones:
        data.append([
            donacion.username,
            donacion.monto,
            donacion.fecha_donacion,
            donacion.metodo_pago,
        ])
    
    # Crear una tabla y definir el estilo
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#009688'),  # Color de fondo para el encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), '#FFFFFF'),    # Color del texto para el encabezado
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
    return Response(buffer, mimetype='application/pdf', headers={"Content-Disposition": "attachment;filename=reporte-donaciones.pdf"})

