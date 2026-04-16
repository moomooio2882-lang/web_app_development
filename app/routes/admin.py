from flask import Blueprint, render_template, request, redirect, url_for, flash

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET'])
def dashboard():
    """
    GET: 系統後台總覽頁面。檢查當前 Session 使用者角色是否為 `admin`，並呈現全站相關資訊統計至 dashboard.html。
    """
    pass

@admin_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def admin_delete_recipe(id):
    """
    POST: 強制刪除機制。僅有系統管理員能夠發動，將違反規範的內容下架。
    重導向回管理員儀表板 (Dashboard)。
    """
    pass
