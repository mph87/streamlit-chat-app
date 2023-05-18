"""Code showing example of how to use Supabase to store messages."""

import streamlit as st
from supabase import create_client

class Database:

    def __init__(self):
        url = st.secrets.supabase.url # CHANGE THIS
        api_key = st.secrets.supabase.api_key # CHANGE THIS

        self.db = create_client(url, api_key)

    def create_conversation(self, user):
        data = {
            "user": user,
        }
        response = self.db.table('conversations').insert(data).execute()
        convo_id = response.data[0]['id']
        return convo_id


    def add_message(self, message, user=None, convo_id=None):

        if convo_id is None:
            convo_id = self.create_conversation(user)

        dataload = {
            "message": message['content'],
            "role": message['role'],
            "conversation": convo_id,
        }

        self.db.table('messages').insert(dataload).execute()
        return convo_id

def test_db():
    """Script that tests the database"""

    db = Database()
    user = "Carl"

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, I'm looking for a restaurant in the center of town."},
        {"role": "assistant", "content": "Sure, what kind of food would you like?"},
        {"role": "user", "content": "I would like a Chinese restaurant."},
        {"role": "assistant", "content": "Great, I found a few restaurants for you: ..."}
    ]

    convo_id = None
    for message in messages:
        convo_id = db.add_message(message, user, convo_id)


if __name__ == "__main__":
    test_db()