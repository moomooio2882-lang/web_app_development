from .database import get_db

class Recipe:
    @staticmethod
    def create(user_id, title, description, steps, is_public=True):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            '''INSERT INTO recipes (user_id, title, description, steps, is_public) 
               VALUES (?, ?, ?, ?, ?)''',
            (user_id, title, description, steps, int(is_public))
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get_by_id(recipe_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            SELECT r.*, u.username as author_name 
            FROM recipes r
            LEFT JOIN users u ON r.user_id = u.id
            WHERE r.id = ?
        ''', (recipe_id,))
        return cursor.fetchone()

    @staticmethod
    def get_all(public_only=True):
        db = get_db()
        cursor = db.cursor()
        if public_only:
            cursor.execute('''
                SELECT r.*, u.username as author_name 
                FROM recipes r
                LEFT JOIN users u ON r.user_id = u.id
                WHERE r.is_public = 1 
                ORDER BY r.created_at DESC
            ''')
        else:
            cursor.execute('''
                SELECT r.*, u.username as author_name 
                FROM recipes r
                LEFT JOIN users u ON r.user_id = u.id
                ORDER BY r.created_at DESC
            ''')
        return cursor.fetchall()

    @staticmethod
    def get_by_user_id(user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM recipes WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        return cursor.fetchall()

    @staticmethod
    def update(recipe_id, title, description, steps, is_public):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            '''UPDATE recipes 
               SET title = ?, description = ?, steps = ?, is_public = ?, updated_at = CURRENT_TIMESTAMP 
               WHERE id = ?''',
            (title, description, steps, int(is_public), recipe_id)
        )
        db.commit()

    @staticmethod
    def delete(recipe_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        db.commit()

    @staticmethod
    def search_by_keyword(keyword, public_only=True):
        db = get_db()
        cursor = db.cursor()
        query = '''
            SELECT r.*, u.username as author_name 
            FROM recipes r
            LEFT JOIN users u ON r.user_id = u.id
            WHERE (r.title LIKE ? OR r.description LIKE ?)
        '''
        if public_only:
            query += ' AND r.is_public = 1'
        query += ' ORDER BY r.created_at DESC'
        
        like_keyword = f'%{keyword}%'
        cursor.execute(query, (like_keyword, like_keyword))
        return cursor.fetchall()

class Ingredient:
    @staticmethod
    def get_or_create(name):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT id FROM ingredients WHERE name = ?', (name,))
        row = cursor.fetchone()
        if row:
            return row['id']
        cursor.execute('INSERT INTO ingredients (name) VALUES (?)', (name,))
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get_by_recipe(recipe_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            SELECT i.id, i.name FROM ingredients i
            JOIN recipe_ingredients ri ON i.id = ri.ingredient_id
            WHERE ri.recipe_id = ?
        ''', (recipe_id,))
        return cursor.fetchall()

class RecipeIngredientMap:
    @staticmethod
    def add_ingredients_to_recipe(recipe_id, ingredient_names):
        db = get_db()
        cursor = db.cursor()
        
        # 先清除現有該食譜的關聯
        cursor.execute('DELETE FROM recipe_ingredients WHERE recipe_id = ?', (recipe_id,))
        
        for name in ingredient_names:
            name = name.strip()
            if not name:
                continue
            # 取回或建立食材的 ID
            ingredient_id = Ingredient.get_or_create(name)
            cursor.execute('''
                INSERT INTO recipe_ingredients (recipe_id, ingredient_id)
                VALUES (?, ?)
            ''', (recipe_id, ingredient_id))
        db.commit()

    @staticmethod
    def search_recipes_by_ingredients(ingredient_names, public_only=True):
        if not ingredient_names:
            return []
            
        db = get_db()
        cursor = db.cursor()
        
        # 使用 IN 條件搜尋所有包含指定任意食材的食譜，
        # 並使用 GROUP BY 結合 HAVING 確保食譜包含的「指定食材數量」等於搜尋數量。
        placeholders = ','.join(['?'] * len(ingredient_names))
        
        query = f'''
            SELECT r.*, u.username as author_name, COUNT(ri.ingredient_id) as match_count
            FROM recipes r
            JOIN recipe_ingredients ri ON r.id = ri.recipe_id
            JOIN ingredients i ON ri.ingredient_id = i.id
            LEFT JOIN users u ON r.user_id = u.id
            WHERE i.name IN ({placeholders})
        '''
        if public_only:
            query += ' AND r.is_public = 1'
            
        query += f'''
            GROUP BY r.id
            HAVING match_count = {len(ingredient_names)}
            ORDER BY match_count DESC, r.created_at DESC
        '''
        
        # 執行搜尋 (這裡確保是同時包含所有搜尋指定的食材)
        cursor.execute(query, tuple(ingredient_names))
        return cursor.fetchall()
