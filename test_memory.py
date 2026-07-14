from core.memory import memory

memory.add("chat1", "user", "Hello")
memory.add("chat1", "assistant", "Hi!")

print(memory.get_history("chat1"))