import streamlit as st
from pyairtable import Table

class AirtableDatabase:
    def __init__(self):
        self.api_key = st.secrets.airtable.api_key # Change this
        self.base_id = st.secrets.airtable.base_id # Change this

    def create_conversation(self, user):
        conversations_table = Table(self.api_key, self.base_id, 'conversations')
        convo = conversations_table.create({'user': user})

        record_id = convo['id']

        breakpoint()
        return record_id

    def get_messages(self):
        messages_table = Table(self.api_key, self.base_id, 'messages')
        messages = messages_table.all(view='Grid view')
        return messages


    def create_message(self, message, user=None, order=None, convo_id=None):

        if convo_id is None:
            convo_id = self.create_conversation(user)

        messages_table = Table(self.api_key, self.base_id, 'messages')
        result = messages_table.create({'message': message['content'], # The message content
                                        'role': message['role'], # One of [user, assistant, system]
                                        'order': order, # 0, 1, 2, 3, 4 (which index is the message in the conversation)
                                        'conversation': [convo_id]}) # We link to one conversation
        return convo_id

def test_airtable():

    db = AirtableDatabase()
    user = "Carl"

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, I'm looking for a restaurant in the center of town."},
        {"role": "assistant", "content": "Sure, what kind of food would you like?"},
        {"role": "user", "content": "I would like a Chinese restaurant."},
        {"role": "assistant", "content": "Great, I found a few restaurants for you: ..."}
    ]

    convo_id = None
    for order, message in enumerate(messages):
        convo_id = db.create_message(message, user, order, convo_id)

if __name__ == "__main__":
    test_airtable()