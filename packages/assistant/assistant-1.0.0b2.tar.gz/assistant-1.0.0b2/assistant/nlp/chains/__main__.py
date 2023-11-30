
from assistant.nlp.chains.session import SessionAssistant
from assistant.nlp.chains.callback_handlers import InputOutputAsyncCallbackHandler

if __name__ == "__main__":
    assistant = SessionAssistant(temperature=0.0, max_tokens=200, verbose=True, callbacks=[InputOutputAsyncCallbackHandler()])
    queries = [
        "", # query goes here
        ]
    for query in queries:
        print(assistant(query))
