from flask import Blueprint

order_bp=Blueprint("order",__name__)

@order_bp.route("/",methods=["GET"])
def order():
    return "Order Route Working"