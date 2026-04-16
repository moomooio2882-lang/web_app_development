import sqlite3
import os
from flask import g

# 指定資料庫檔案路徑，擺放在 instance 目錄中
DB_PATH = os.path.join(os.getcwd(), 'instance', 'database.db')

def get_db():
    """取得當前 Request 的資料庫連線，並使用 fetchall 時可利用欄位名稱存取字典 (Row)"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        
        # 啟動外鍵支持，避免 ON DELETE CASCADE 不發生作用
        db.execute("PRAGMA foreign_keys = ON")
    return db

def close_db(exception=None):
    """關閉資料庫連線，會在 Request 結束時自動被 Flask 呼叫"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db(app):
    """初始化資料庫工具，載入 schema 建立資料表 (通常藉由 CLI 工具觸發)"""
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    with app.app_context():
        db = get_db()
        # 讀取 database 資料夾底下的 schema.sql 檔案
        schema_path = os.path.join(os.getcwd(), 'database', 'schema.sql')
        with open(schema_path, mode='r', encoding='utf-8') as f:
            db.cursor().executescript(f.read())
        db.commit()

def init_app(app):
    """與 app 初始化做掛載配置"""
    app.teardown_appcontext(close_db)
