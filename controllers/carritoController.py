from flask import Blueprint, render_template, session, redirect, flash
from models.fritosModels import Fritos
from models.pedidoModels import Pedido
from models.detalleModels import PedidoDetalle
from extensions import db

cart_bp = Blueprint("carrito", __name__)

#Add product to cart 
@cart_bp.route("/add-cart/<int:id>", methods=["POST"])
def add_cart(id):

    # 🔒 Validar sesión
    if not session.get("cliente_id"):
        flash("Debes iniciar sesión para agregar productos al carrito", "warning")
        return redirect("/login")

    producto = Fritos.query.get(id)

    # Verificar si el carrito ya existe en la sesión
    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]

    # Agregar o actualizar el producto en el carrito
    if str(id) in cart:
        cart[str(id)]["cantidad"] += 1
    else:
        cart[str(id)] = {
            "nombre": producto.fri_nombre,
            "precio": producto.fri_precio,
            "cantidad": 1
        }

    session["cart"] = cart
    flash("Producto agregado al carrito 🛒", "success") # Notificacion por mensaje
    return redirect("/")

#View cart
@cart_bp.route("/cart")
def cart():
    carrito = session.get("cart", {})
    return render_template("carrito.html", carrito=carrito)

#Remove product from cart
@cart_bp.route("/remove_from_cart/<int:producto_id>")
def remove_from_cart(producto_id):
    if "cart" in session:
        session["cart"].pop(str(producto_id), None)
        session.modified = True
    return redirect("/cart")

# Increase product quantity in cart
@cart_bp.route("/increase/<int:producto_id>")
def increase(producto_id):
    if "cart" in session:
        if str(producto_id) in session["cart"]:
            session["cart"][str(producto_id)]["cantidad"] += 1
            session.modified = True
    return redirect("/cart")

# Decrease product quantity in cart
@cart_bp.route("/decrease/<int:producto_id>")
def decrease(producto_id):
    if "cart" in session:
        if str(producto_id) in session["cart"]:
            if session["cart"][str(producto_id)]["cantidad"] > 1:
                session["cart"][str(producto_id)]["cantidad"] -= 1
            else:
                session["cart"].pop(str(producto_id), None)
            session.modified = True
    return redirect("/cart")

# Checkout and create order
@cart_bp.route("/checkout")
def checkout():

    # Si el cliente no ha iniciado sesión, redirigir al login
    if "cliente_id" not in session:
        return redirect("/login")

    # Si el carrito está vacío, redirigir al carrito
    if "cart" not in session or len(session["cart"]) == 0:
        return redirect("/cart")

    total = 0

    for item in session["cart"].values():
        total += item["precio"] * item["cantidad"]

    pedido = Pedido(
        cli_id=session["cliente_id"],
        ped_total=total,
        ped_estado="Solicitado"
    )
    db.session.add(pedido)
    db.session.commit()

    # Crear detalles del pedido
    for id, item in session["cart"].items():
        detalle = PedidoDetalle(
            ped_id=pedido.ped_id,
            fri_id=id,
            cantidad=item["cantidad"],
            precio=item["precio"]
        )
        db.session.add(detalle)

    db.session.commit()

    session.pop("cart")
    flash("Puede revisar sus pedidos en la sección de MIS COMPRAS 🧾", "success") # Notificacion por mensaje
    return render_template("confirmacion.html", pedido_id=pedido.ped_id)
