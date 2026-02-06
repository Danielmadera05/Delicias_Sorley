from flask import Blueprint, render_template, session, redirect, flash
from models.fritosModels import Fritos

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