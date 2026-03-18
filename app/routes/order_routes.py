from flask import Blueprint

order_bp=Blueprint("order",__name__)

@order_bp.route("test",methods=["GET"])
def test():
    return "Test Route Working"