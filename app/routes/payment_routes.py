from flask import Blueprint

payment_bp=Blueprint("payment",__name__)

@payment_bp.route("test",methods=["GET"])
def test():
    return "Test Route Working"