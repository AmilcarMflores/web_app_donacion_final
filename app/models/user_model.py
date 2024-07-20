from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Date

class User(db.Model, UserMixin):
  __tablename__ = 'donantes'
  
  id = db.Column(db.Integer, primary_key=True)
  nombre = db.Column(db.String(100), nullable=False)
  apellido = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), nullable=False, unique=True)
  telefono = db.Column(db.String(100), nullable=False)
  direccion = db.Column(db.String(100), nullable=False)
  fecha_registro = db.Column(db.Date, nullable=False)
  username = db.Column(db.String(100), nullable=False, unique=True)
  password_hash = db.Column(db.String(128), nullable=False)
  role = db.Column(db.String(100), nullable=False, default="donante")
  
  def __init__(self, nombre, apellido, email, telefono, direccion, fecha_registro, username, password, role="donante"):
    self.nombre = nombre
    self.apellido = apellido
    self.email = email
    self.telefono = telefono
    self.direccion = direccion
    self.fecha_registro = fecha_registro
    self.username = username
    self.set_password(password)
    self.role = role
    
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
  
  def save(self):
    db.session.add(self)
    db.session.commit()
    
  @staticmethod
  def get_all():
    return User.query.all()
  
  @staticmethod
  def get_by_id(id):
    return User.query.get(id)
  
  def update(self):
    db.session.commit()
    
  def delete(self):
    db.session.delete(self)
    db.session.commit()
    
  @staticmethod
  
  def get_user_by_username(username):
    return User.query.filter_by(username=username).first()
  
  def has_role(self, role):
    return self.role == role
  

  
