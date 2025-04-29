import time
import datetime

class ConversationManager:
    def __init__(self):
        self.conversations = {}
    
    def create_conversation(self, user_id):
        conversation_id = f"conv_{user_id}_{int(time.time())}"
        self.conversations[conversation_id] = {
            "messages": [],
            "state": {},
            "created_at": datetime.now()
        }
        return conversation_id
    
    def add_message(self, conversation_id, message):
        if conversation_id in self.conversations:
            self.conversations[conversation_id]["messages"].append(message)
    
    def get_conversation_messages(self, conversation_id):
        if conversation_id in self.conversations:
            return self.conversations[conversation_id]["messages"]
        return []
    
    def update_state(self, conversation_id, state_updates):
        if conversation_id in self.conversations:
            self.conversations[conversation_id]["state"].update(state_updates)