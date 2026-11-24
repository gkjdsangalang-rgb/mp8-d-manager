import os
import pymysql
from dotenv import load_dotenv
load_dotenv()
cluster_config = {
    "active_node": "Default Node",
}
class DBManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_connection(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )

    # ==========================================
    # USER QUERY HELPERS (API & GUI)
    # ==========================================
    def get_user_by_email(self, email: str):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                return cursor.fetchone()
        finally:
            connection.close()

    def get_user_by_id(self, user_id: int):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
                return cursor.fetchone()
        finally:
            connection.close()

    def get_all_users(self):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, email FROM users")
                return cursor.fetchall()
        finally:
            connection.close()

    def insert_user(self, name: str, email: str, hashed_pw: str):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, email, hashed_pw))
                connection.commit()
                return cursor.lastrowid
        finally:
            connection.close()

    def update_user_name_by_id(self, user_id: int, new_name: str):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                query = "UPDATE users SET name = %s WHERE id = %s"
                cursor.execute(query, (new_name, user_id))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            connection.close()

    def delete_user_by_id(self, user_id: int):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                query = "DELETE FROM users WHERE id = %s"
                cursor.execute(query, (user_id,))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            connection.close()

    # ==========================================
    # INVENTORY QUERY HELPERS
    # ==========================================
    def get_all_items(self):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM inventory_items")
                return cursor.fetchall()
        finally:
            connection.close()

    def get_item_by_id(self, item_id: int):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM inventory_items WHERE item_id = %s", (item_id,))
                return cursor.fetchone()
        finally:
            connection.close()

    def add_item(self, name: str, qty: int, price: float, fragile: int, date: str):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO inventory_items (item_name, quantity, price, is_fragile, date_added) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, qty, price, fragile, date))
                connection.commit()
                return {"message": "Item added successfully!", "item_id": cursor.lastrowid}
        finally:
            connection.close()

    def update_stock(self, item_id: int, new_qty: int):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE inventory_items SET quantity = %s WHERE item_id = %s"
                cursor.execute(sql, (new_qty, item_id))
                connection.commit()
                return {"message": "Item stock updated successfully!"}
        finally:
            connection.close()

    def remove_item(self, item_id: int):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM inventory_items WHERE item_id = %s"
                cursor.execute(sql, (item_id,))
                connection.commit()
                return {"message": "Item deleted successfully!"}
        finally:
            connection.close()