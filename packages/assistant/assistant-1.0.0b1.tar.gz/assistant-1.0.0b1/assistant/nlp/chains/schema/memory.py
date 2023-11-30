
from typing import Sequence

from langchain.schema.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, FunctionMessage, ChatMessage

def get_buffer_string(
    messages: Sequence[BaseMessage], human_prefix: str = "Human", ai_prefix: str = "AI"
) -> str:
    """Convert sequence of Messages to strings and concatenate them into one string.

    Args:
        messages: Messages to be converted to strings.
        human_prefix: The prefix to prepend to contents of HumanMessages.
        ai_prefix: The prefix to prepend to contents of AIMessages.

    Returns:
        A single string concatenation of all input messages.

    Example:
        .. code-block:: python

            from langchain.schema import AIMessage, HumanMessage

            messages = [
                HumanMessage(content="Hi, how are you?"),
                AIMessage(content="Good, how are you?"),
            ]
            get_buffer_string(messages)
    """
    user_message = None
    assistant_message = None
    string_messages = []
    for m in messages:
        if isinstance(m, HumanMessage):
            role = human_prefix
        elif isinstance(m, AIMessage):
            role = ai_prefix
        elif isinstance(m, SystemMessage):
            role = "System"
        elif isinstance(m, FunctionMessage):
            role = "Function"
        elif isinstance(m, ChatMessage):
            role = m.role
        else:
            raise ValueError(f"Got unsupported message type: {m}")
        if role == human_prefix:
            user_message = f"<|im_start|>user\n{m.content}<|im_stop|>"
        elif role == ai_prefix:
            assistant_message = f"<|im_start|>assistant\n{m.content}<|im_stop|>"
        #message = f"{role}: {m.content}"
        # if isinstance(m, AIMessage) and "function_call" in m.additional_kwargs:
        #     message += f"{m.additional_kwargs['function_call']}"
        if user_message and assistant_message:
            string_messages.append(f"{user_message}\n{assistant_message}")
            user_message = None
            assistant_message = None
        #string_messages.append(f"{message}")

    return str("\n".join(string_messages) + "\n") if string_messages else ""