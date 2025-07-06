import psycopg2
import json
from src.database import get_db_connection

class DataManager:
    def __init__(self):
        pass

    # --- User Profile Management ---

    def create_user_profile(self, user_id: int, display_name: str, profile_picture_url: str = None, preferences: dict = None):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO user_profiles (user_id, display_name, profile_picture_url, preferences) VALUES (%s, %s, %s, %s)",
                (user_id, display_name, profile_picture_url, json.dumps(preferences) if preferences else None)
            )
            conn.commit()
            cur.close()
            return True
        except psycopg2.Error as e:
            print(f"Error creating user profile: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn: conn.close()

    def get_user_profile(self, user_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT user_id, display_name, profile_picture_url, preferences, created_at, updated_at FROM user_profiles WHERE user_id = %s", (user_id,))
            profile = cur.fetchone()
            cur.close()
            if profile:
                return {
                    "user_id": profile[0],
                    "display_name": profile[1],
                    "profile_picture_url": profile[2],
                    "preferences": profile[3] if profile[3] else None,
                    "created_at": profile[4],
                    "updated_at": profile[5]
                }
            return None
        except psycopg2.Error as e:
            print(f"Error getting user profile: {e}")
            return None
        finally:
            if conn: conn.close()

    def update_user_profile(self, user_id: int, display_name: str = None, profile_picture_url: str = None, preferences: dict = None):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            updates = []
            params = []
            if display_name is not None:
                updates.append("display_name = %s")
                params.append(display_name)
            if profile_picture_url is not None:
                updates.append("profile_picture_url = %s")
                params.append(profile_picture_url)
            if preferences is not None:
                updates.append("preferences = %s")
                params.append(json.dumps(preferences))
            
            if not updates:
                return False # No updates to perform

            params.append(user_id)
            cur.execute(
                f"UPDATE user_profiles SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE user_id = %s",
                params
            )
            conn.commit()
            cur.close()
            return cur.rowcount > 0
        except psycopg2.Error as e:
            print(f"Error updating user profile: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn: conn.close()

    def delete_user_profile(self, user_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM user_profiles WHERE user_id = %s", (user_id,))
            conn.commit()
            cur.close()
            return cur.rowcount > 0
        except psycopg2.Error as e:
            print(f"Error deleting user profile: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn: conn.close()

    # --- Encrypted Data Store Management ---

    def store_encrypted_data(self, user_id: int, data_type: str, encrypted_content: bytes, encryption_metadata: dict):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO encrypted_data_store (user_id, data_type, encrypted_content, encryption_metadata) VALUES (%s, %s, %s, %s) RETURNING data_id",
                (user_id, data_type, encrypted_content, json.dumps(encryption_metadata))
            )
            data_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            return str(data_id)
        except psycopg2.Error as e:
            print(f"Error storing encrypted data: {e}")
            if conn: conn.rollback()
            return None
        finally:
            if conn: conn.close()

    def retrieve_encrypted_data(self, data_id: str):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT data_id, user_id, data_type, encrypted_content, encryption_metadata, created_at, updated_at FROM encrypted_data_store WHERE data_id = %s", (data_id,))
            data = cur.fetchone()
            cur.close()
            if data:
                return {
                    "data_id": str(data[0]),
                    "user_id": data[1],
                    "data_type": data[2],
                    "encrypted_content": data[3],
                    "encryption_metadata": data[4],
                    "created_at": data[5],
                    "updated_at": data[6]
                }
            return None
        except psycopg2.Error as e:
            print(f"Error retrieving encrypted data: {e}")
            return None
        finally:
            if conn: conn.close()

    def delete_encrypted_data(self, data_id: str):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM encrypted_data_store WHERE data_id = %s", (data_id,))
            conn.commit()
            cur.close()
            return cur.rowcount > 0
        except psycopg2.Error as e:
            print(f"Error deleting encrypted data: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn: conn.close()

    def list_encrypted_data_by_user(self, user_id: int, data_type: str = None):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            if data_type:
                cur.execute("SELECT data_id, data_type, created_at FROM encrypted_data_store WHERE user_id = %s AND data_type = %s", (user_id, data_type))
            else:
                cur.execute("SELECT data_id, data_type, created_at FROM encrypted_data_store WHERE user_id = %s", (user_id,))
            
            data_list = []
            for row in cur.fetchall():
                data_list.append({"data_id": str(row[0]), "data_type": row[1], "created_at": row[2]})
            cur.close()
            return data_list
        except psycopg2.Error as e:
            print(f"Error listing encrypted data: {e}")
            return []
        finally:
            if conn: conn.close()
