from flask import Blueprint
from .auth import auth_bp
from .recipe import recipe_bp
from .admin import admin_bp

def register_blueprints(app):
    """將各領域的 Controller Router 註冊至主程式中"""
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    # Recipe 包含首頁與主要邏輯，不用前綴
    app.register_blueprint(recipe_bp)
