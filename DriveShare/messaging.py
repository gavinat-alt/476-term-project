from database import connect
from session_manager import SessionManager


class MessageService:

    @staticmethod
    def send_message(receiver_id, message_text):

        session = SessionManager()
        user = session.get_current_user()

        if not user:
            return False, "Not logged in"

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO messages
            (sender_id, receiver_id, message_text)
            VALUES (?, ?, ?)
        """, (
            user.userID,
            receiver_id,
            message_text
        ))

        conn.commit()
        conn.close()

        return True, "Message sent"

    @staticmethod
    def get_my_messages():

        session = SessionManager()
        user = session.get_current_user()

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT sender_id,
                   message_text,
                   sent_date
            FROM messages
            WHERE receiver_id = ?
            ORDER BY sent_date DESC
        """, (user.userID,))

        messages = cursor.fetchall()

        conn.close()

        return messages