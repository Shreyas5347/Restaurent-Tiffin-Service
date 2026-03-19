from flask import Blueprint

payment_bp=Blueprint("payment",__name__)

@payment_bp.route("/",methods=["GET"])
def payment():
    return "Payment Route Working"