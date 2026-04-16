from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: 顯示註冊表單 (templates/auth/register.html)。
    POST: 接收表單資料，驗證輸入是否合法、信箱是否重複，寫入資料庫並重新導向至登入頁面。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 顯示登入表單 (templates/auth/login.html)。
    POST: 接收表單並比對資料庫密碼，驗證成功後將使用者狀態存入 Session，將用戶導回首頁。
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    GET: 清除目前的 Session 登入狀態，重導向至首頁。
    """
    pass
