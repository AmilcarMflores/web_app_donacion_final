from database import db

class Donacion(db.Model):
  __tablename__ = 'donaciones'

# id, id_donante, monto, fecha_donacion, metodo_pago
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), nullable=False)
  #id_donante = db.Column(db.Integer, db.ForeignKey('donantes.id'), nullable=False)
  monto = db.Column(db.Float, nullable=False)
  fecha_donacion = db.Column(db.Date, nullable=False)
  metodo_pago = db.Column(db.String(50), nullable=False)
  
  def __init__(self,username,monto,fecha_donacion,metodo_pago):
    #self.id_donante = id_donante
    self.username = username
    self.monto = monto
    self.fecha_donacion = fecha_donacion
    self.metodo_pago = metodo_pago
    
  def save(self):
    db.session.add(self)
    db.session.commit()
    
  @staticmethod
  def get_all():
    return Donacion.query.all()
  
  @staticmethod
  def get_by_id(id):
    return Donacion.query.get(id)
  
  def update(self,username=None,monto=None,fecha_donacion=None,metodo_pago=None):
    if username is not None:
      self.username = username
    if monto is not None:
      self.monto = monto
    if fecha_donacion is not None:
      self.fecha_donacion = fecha_donacion
    if metodo_pago is not None:
      self.metodo_pago = metodo_pago
    db.session.commit()
    
  def delete(self):
    db.session.delete(self)
    db.session.commit()
    