from extensions import db

class Pedido(db.Model):
    __tablename__ = "pedido"

    ped_id = db.Column(db.Integer, primary_key=True)
    cli_id = db.Column(db.Integer, db.ForeignKey("cliente.cli_id"))
    ped_total = db.Column(db.Float(10,2))
    ped_fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    ped_estado = db.Column(db.String(50))
