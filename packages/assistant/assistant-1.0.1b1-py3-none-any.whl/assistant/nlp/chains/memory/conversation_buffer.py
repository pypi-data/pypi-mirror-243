from langchain.memory import ConversationBufferMemory
from assistant.nlp.chains.schema.memory import get_buffer_string


class AssistantConversationBufferMemory(ConversationBufferMemory):
    """A memory that stores a conversation buffer."""

    @property
    def buffer_as_str(self) -> str:
        """Exposes the buffer as a string in case return_messages is True."""
        return get_buffer_string(
            self.chat_memory.messages,
            human_prefix=self.human_prefix,
            ai_prefix=self.ai_prefix,
        )
