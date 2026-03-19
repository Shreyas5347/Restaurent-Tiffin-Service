from flask import Blueprint

auth_bp=Blueprint("auth",__name__)

@auth_bp.route("/",methods=["GET"])
def auth():
    return "Auth Route Working"