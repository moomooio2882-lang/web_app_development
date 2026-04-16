from flask import Blueprint, render_template, request, redirect, url_for, flash

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/', methods=['GET'])
def index():
    """
    GET: 首頁。呼叫 Model 取得所有公開的食譜，並呈現於 index.html。
    """
    pass

@recipe_bp.route('/search', methods=['GET'])
def search():
    """
    GET: 關鍵字搜尋功能。藉由 `?q=xxx` 獲取參數，回傳匹配的食譜至 search_results.html。
    """
    pass

@recipe_bp.route('/search/ingredients', methods=['GET'])
def ingredient_search():
    """
    GET: 食材組合搜尋功能。接收 `?items=蛋,番茄`，切分後至 DB 過濾出完全包含該些食材的食譜，呈現於 ingredient_search.html。
    """
    pass

@recipe_bp.route('/recipe/<int:id>', methods=['GET'])
def detail(id):
    """
    GET: 單一食譜詳情頁面。根據食譜 ID 取得細節、步驟與配料，呈現於 detail.html，若找不到回傳 404。
    """
    pass

@recipe_bp.route('/recipe/my', methods=['GET'])
def my_recipes():
    """
    GET: 專門列出登入用戶自己建立的食譜列表以供管理。需要驗證登入權限。呈現於 my_recipes.html。
    """
    pass

@recipe_bp.route('/recipe/new', methods=['GET', 'POST'])
def new_recipe():
    """
    GET: 顯示新增食譜的表單 (new.html)。
    POST: 接收食譜資料與食材清單，寫入資料庫並建立多對多關聯。
    需要驗證登入權限。
    """
    pass

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    """
    GET: 顯示編輯食譜表單 (edit.html)，並預留當前食譜內容變數。
    POST: 接收編輯後的新資料與食材異動並儲存。
    需要驗證登入權限，並且限制僅有食譜建立者 (user_id) 可見與修改。失敗拋錯 403 Forbidden。
    """
    pass

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    POST: 刪除指定的食譜。需再三確保為本人操作。刪除後預設連鎖會移除多對多食材關聯表內對應資料。
    重導向至我的食譜列表首頁。
    """
    pass
