from flask import Blueprint

menu_bp=Blueprint("menu",__name__)

@menu_bp.route("test",methods=["GET"])
def test():
    return "Test Route Working"