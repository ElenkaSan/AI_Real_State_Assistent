from langchain.memory import ConversationBufferWindowMemory

user_memories = {}

def get_memory(user_id):
    if user_id not in user_memories:
        user_memories[user_id] = ConversationBufferWindowMemory(k=15, return_messages=True)
    return user_memories[user_id]

def reset_memory():
    user_memories.clear()