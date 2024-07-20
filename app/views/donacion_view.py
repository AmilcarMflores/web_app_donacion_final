from flask import render_template, url_for
from flask_login import current_user

def list_donaciones(donaciones):
    return render_template(
        "donaciones.html",
        donaciones=donaciones,
        title="Lista de Donaciones",
        current_user=current_user,
    )

def create_donacion(users, current_user):
    return render_template(
        "create_donacion.html",
        title="Crear donación",
        current_user=current_user,
        users=users,
    )

def update_donacion(donacion):
    return render_template(
        "update_donacion.html",
        title="Editar donación",
        donacion=donacion,
        current_user=current_user,
    )

def generate_donaciones_report(donaciones):
    return render_template(
        "reportes.html",
        title="Reporte de Donaciones",
        donaciones=donaciones,
        current_user=current_user,
        download_url=url_for('donacion.download_report')
    )
