from pathlib import Path
from typing import List
from langchain.docstore.document import Document
from langchain.schema.vectorstore import VectorStoreRetriever
# from langchain.pydantic_v1 import Field
from langchain.vectorstores import Chroma

from assistant.utils import say

try:
    from datasets import load_dataset
except ImportError as exce:
    raise ImportError("Please install the datasets library with: pip install datasets") from exce

from assistant import ASSISTANT_PATH

class AGIRetriever(VectorStoreRetriever):
    '''
    Augmented Generation Interface Retriever
    Returns a guide for the best action to take to answer the query given similarity with intent examples
    
    For example:
        Query -> Action
        Hey give me the time please -> Tell Local Time
        What date is it? -> Tell Local Date
        List my files -> Print files and directories
        Where are we? -> Tell Local Time
        assistant -> Addressing the User by Name
        the screen should be cleaned. -> Clearing the Screen or Starting Anew

        Each action returns a guide as document like so:
        Action: Tell Local Time
        Guide: # Tell Local Time
        
        When the user inquires about local time, use either `python` or the `shell` to easely grab a shapshot of the time (i.e. using `date +%T` or `datetime.datetime.now().time()`). Then (once you observed the time), in your final answer, let the user know. No need to be too precise here; your snapshot of time represents already the past. Give your answer using natural language.
        
        
        Return a list of only one Document
    '''
    vectorstore: VectorStoreRetriever
    search_type: str = "similarity"
    search_kwargs: dict = {} #Field(default_factory=dict)

    def _get_relevant_documents(self, query: str) -> List[Document]:
        """
        Retrieves relevant documents based on the given query.

        Args:
            query (str): The query string.

        Returns:
            List[Document]: A list of relevant documents.
        """
        
        results = self.vectorstore.get_relevant_documents(query=query)
        # return a set of unique guides
        r = {}
        for result in results:
            #r[result.metadata['action']] = result.metadata['guide']
                return [
                    Document(
                        page_content=result.metadata['guide'],
                        metadata={'action': result.metadata['action']},
                    )
                    #for intent_example, guide in r.items()
                ]

def split_markdown_guide(md: str):
    action, guide, examples = [md.split("\n")[0].lstrip("# ")] + [x.strip() for x in md.split("## Intent Examples")]
    return action, guide, examples

def get_guides_intent_examples(guidebook):
    actions, guides, intent_examples = [], [], []
    for x in guidebook['guide']:
        action, guide, intent_example = split_markdown_guide(x)
        actions.append(action)
        guides.append(guide)
        intent_examples.append(intent_example)
    return actions, guides, intent_examples

def get_guidebook_docs():
    guidebook = load_dataset("wasertech/AGI", split="train")
    actions, guides, intent_examples = get_guides_intent_examples(guidebook)
    guidebook_docs = {}
    for action, guide, intents in zip(actions, guides, intent_examples):
        guidebook_docs[action] = {
            "guide": guide,
            "intent_examples": [i.replace('"', "").replace("- ", "").strip() for i in intents.split("\n")],
        }
    return guidebook_docs

def get_guides_intent_examples_docs(guidebook_docs):  
    for action, doc in guidebook_docs.items():
        for intent_example in doc['intent_examples']:
            yield Document(page_content=intent_example, metadata={'action': action, 'guide': doc['guide']})

def get_or_ingest_vectorstore(embeddings, vectorstore_path="vectorstore"):
    if Path(vectorstore_path).exists():
        vectorstore = Chroma(persist_directory=vectorstore_path, embedding_function=embeddings)
    else:
        say("Ingesting vectorstore...")
        guidebook_docs = get_guidebook_docs()
        intent_examples_sources = list(get_guides_intent_examples_docs(guidebook_docs))
        vectorstore = Chroma.from_documents(intent_examples_sources, embeddings, persist_directory=vectorstore_path)
    return vectorstore

def get_agi_retriever(embeddings, search_type="mmr", search_kwargs={"k": 1}, vectorstore_path=f"{ASSISTANT_PATH}/vectorstore/guidebook"):   
    # guidebook_docs = get_guidebook_docs()
    # intent_examples_sources = list(get_guides_intent_examples_docs(guidebook_docs))
    # vectorstore = Chroma.from_documents(intent_examples_sources, embeddings)
    vectorstore = get_or_ingest_vectorstore(embeddings, vectorstore_path=vectorstore_path)
    retriever = vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs,
    )
    return AGIRetriever(vectorstore=retriever, search_type=search_type, search_kwargs=search_kwargs)
