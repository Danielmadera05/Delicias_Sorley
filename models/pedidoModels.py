from extensions import db

class Pedido(db.Model):
    __tablename__ = "pedido"

    ped_id = db.Column(db.Integer, primary_key=True)
    cli_id = db.Column(db.Integer, db.ForeignKey("cliente.cli_id"))
    ped_total = db.Column(db.Float(10,2))
    ped_fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    ped_estado = db.Column(db.String(50))

class PedidoDetalle(db.Model):
    __tablename__ = "pedido_detalle"

    det_id = db.Column(db.Integer, primary_key=True)
    ped_id = db.Column(db.Integer, db.ForeignKey("pedido.ped_id"))
    fri_id = db.Column(db.Integer, db.ForeignKey("fritos.fri_id"))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float(10,2))