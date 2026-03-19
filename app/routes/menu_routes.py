from flask import Blueprint

menu_bp=Blueprint("menu",__name__)



@menu_bp.route("/",methods=["GET"])
def menu():
    return "Menu Route Working"