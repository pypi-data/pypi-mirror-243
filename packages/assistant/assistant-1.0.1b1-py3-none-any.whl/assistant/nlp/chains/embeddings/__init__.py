from assistant.nlp.chains.embeddings.assistant import AssistantEmbeddings

def get_embeddings(model_name="intfloat/e5-large-v2"):
    return AssistantEmbeddings(model_name=model_name)
