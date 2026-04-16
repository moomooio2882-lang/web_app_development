# 路由與頁面設計文件 (ROUTES) - 食譜收藏夾系統

本文件由 `/api-design` skill 自動產生，彙整了根據 FLOWCHART 與 DB_DESIGN 設計的所有 URL 路由對照與介面模板規劃。

## 1. 路由總覽表格

| 功能區塊 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁與瀏覽** | GET | `/` | `templates/recipe/index.html` | 顯示所有公開食譜（首頁）。 |
| **關鍵字搜尋** | GET | `/search` | `templates/recipe/search_results.html` | 顯示依食譜標題/簡介搜尋結果。 |
| **食材過濾搜尋**| GET | `/search/ingredients` | `templates/recipe/ingredient_search.html` | 顯示擁有指定多樣食材組合的食譜。 |
| **食譜詳情** | GET | `/recipe/<id>` | `templates/recipe/detail.html` | 顯示單一食譜內容與製作步驟。 |
| **註冊頁面** | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單。 |
| **送出註冊** | POST | `/auth/register` | — | 接收表單並建立 User，成功後重導向登入。 |
| **登入頁面** | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單。 |
| **送出登入** | POST | `/auth/login` | — | 校驗資料並建立 session，成功後重導向首頁。 |
| **會員登出** | GET | `/auth/logout` | — | 清除 session，重導向首頁。 |
| **我的食譜** | GET | `/recipe/my` | `templates/recipe/my_recipes.html` | 列出該登入會員建立的所有食譜。 |
| **新增食譜頁面**| GET | `/recipe/new` | `templates/recipe/new.html` | 顯示建立食譜與食材輸入表單。 |
| **送出新增食譜**| POST | `/recipe/new` | — | 儲存至 DB 並建立多對多關聯，重導向至詳情頁。|
| **編輯食譜頁面**| GET | `/recipe/<id>/edit`| `templates/recipe/edit.html` | 取出原始庫存資料，顯示編輯表單。 |
| **送出編輯食譜**| POST | `/recipe/<id>/edit`| — | 更新食譜資料與食材清單，重導向至詳情頁。 |
| **刪除食譜** | POST | `/recipe/<id>/delete`| — | 刪除自己名單下的食譜，重導向我的食譜頁。 |
| **後台總覽** | GET | `/admin` | `templates/admin/dashboard.html` | 唯有 Admin 權限可進入，檢視全站資料。 |
| **管理員刪除** | POST | `/admin/recipe/<id>/delete`| — | 強制刪除違規資料，重導向至後台總覽。 |

## 2. 路由詳細說明

### Auth (會員模組)
* **`GET, POST /auth/register`**:
  * 輸入：表單欄位 (`username`, `email`, `password`, `confirm_password`)。
  * 邏輯：檢查欄位必填與密碼一致性。檢查信箱是否重複 (`User.get_by_email`)。實作密碼雜湊，調用 `User.create`。
  * 輸出/錯誤：發生錯誤 `flash` 並重繪 `register.html`；成功重導向 `/auth/login`。
* **`GET, POST /auth/login`**:
  * 輸入：表單欄位 (`email`, `password`)。
  * 邏輯：以信箱取得會員，並驗證 `password_hash`。通過則賦予 `session['user_id']`。
  * 輸出/錯誤：失敗 `flash` 錯誤，成功重導向 `/` 或指定的 `next` 網址。
* **`GET /auth/logout`**:
  * 邏輯：呼叫 `session.clear()` 移除登入狀態並重導向首頁。

### Recipe (食譜核心模組)
* **`GET /` (index)**:
  * 邏輯：呼叫 `Recipe.get_all(public_only=True)` 取得全站公開食譜。渲染 `index.html`。
* **`GET /search`**:
  * 輸入：URL Query Parameter `?q=xxx`。
  * 邏輯：呼叫 `Recipe.search_by_keyword(q)` 執行關鍵字模糊查詢。
* **`GET /search/ingredients`**:
  * 輸入：URL Query Parameter `?items=蛋,番茄`。
  * 邏輯：字串切分為陣列，呼叫 `RecipeIngredientMap.search_recipes_by_ingredients(items)`。
* **`GET, POST /recipe/new`**:
  * 輸入：表單 (`title`, `description`, `steps`, `ingredients`, `is_public`)。
  * 邏輯：需驗證身份(`@login_required`)。建立食譜獲取 `recipe_id`，再結合 `ingredients` 更新多對多關聯 (`RecipeIngredientMap.add_ingredients_to_recipe`)。如果驗證失敗返回表單。
* **`GET, POST /recipe/<id>/edit`**:
  * 邏輯：需登入且校驗 `recipe.user_id == current_user.id`。POST 時同步變更食譜本體與關聯食材單。若非本人嘗試修改需回傳 403 Forbidden。
* **`POST /recipe/<id>/delete`**:
  * 邏輯：驗證為本人所有，呼叫 `Recipe.delete(id)`，重導向我的食譜頁面。
* **`GET /recipe/my`**:
  * 邏輯：需登入，調用 `Recipe.get_by_user_id(current_user.id)` 獲取個人清單。

### Admin (管理員模組)
* **`GET /admin`**:
  * 邏輯：需檢驗當中使用者角色是否具備 `admin` 身份，抓取所需全站數量清單資料，並渲染 `dashboard.html`。
* **`POST /admin/recipe/<id>/delete`**:
  * 邏輯：系統管理員高權限強制下架違規食譜內容。

## 3. Jinja2 模板清單

所有的模板檔案存放於 `app/templates/`。

共用外觀：
- `base.html` (定義 Navbar, Flash 訊息區塊, 引入 Vanilla CSS 手寫樣式、Footer)

各自繼承 `{% extends "base.html" %}` 的子模板：
1. **認證相關 (`auth/`)**
   - `register.html`: 註冊介面
   - `login.html`: 登入介面
2. **食譜檢視 (`recipe/`)**
   - `index.html`: 首頁主瀑布流設計
   - `search_results.html`: 一般搜尋字面與結果列表
   - `ingredient_search.html`: 現有食材過濾檢索與結果 (核心功能)
   - `detail.html`: 單一食譜詳細圖文與配料步驟說明
   - `my_recipes.html`: 表列展示個人擁有清單與快速編輯入口
3. **食譜寫入 (`recipe/`)**
   - `new.html`: 輸入表單與多項食材組合輸入器
   - `edit.html`: 沿用新建的版型配置，載入舊資料變數
4. **管理員 (`admin/`)**
   - `dashboard.html`: 全站資料總覽與管制操作清單
