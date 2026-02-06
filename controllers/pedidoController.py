from flask import Blueprint, render_template, session, redirect
from models.pedidoModels import Pedido

pedido_bp = Blueprint("pedido", __name__)

# Ruta para ver las compras realizadas por el cliente
@pedido_bp.route("/mis-compras")
def mis_compras():

    if not session.get("cliente_id"):
        return redirect("/login")

    pedidos = Pedido.query.filter_by(
        cli_id=session["cliente_id"]
    ).all()

    return render_template("mis_compras.html",pedidos=pedidos)
