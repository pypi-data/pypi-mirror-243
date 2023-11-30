import requests
from typing import List
from langchain.embeddings.base import Embeddings

class AssistantEmbeddings(Embeddings):
    def __init__(self, model_name):
        self.assert_embeddings(model_name)

    def assert_embeddings(self, model_name):
        """Asserts served model is actually the requested model."""
        explained = """To ensure that the latent embedded space is consistent and meaningful, \
it is important to use only one embedding model throughout the process. \
Mixing different models can lead to \
incompatible or noisy representations that affect the quality of the downstream tasks. \
Therefore, you have two options: \
either rebuild your vectorstore using the new model that you have chosen, \
or stick to the current one that you have already used. \
Please do not attempt to combine or switch models without rebuilding the vectorstore, \
as this can cause errors and inconsistencies."""
        served_model_name = self.get_served_model_name()
        assert (
            model_name == served_model_name
        ), f"""Tried to initialize embeddings model {model_name} \
but model served is {served_model_name}.
{explained}"""
        self.model_name = model_name

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs."""
        return self.embed_sentences(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """Embed query text."""
        return self.embed_sentences(text)

    def embed_sentences(self, input_sentences: str or list):
        """Call Assistant API to get embeddings for sentences"""
        embed = self.send_request(
            "post", "embed", query=input_sentences
        )
        if isinstance(embed, dict) and "error" in embed:
            raise requests.RequestException(embed["error"])
        elif isinstance(embed, dict) and "embeddings" in embed:
            return embed["embeddings"]
        return embed

    def get_served_model_name(self):
        """Call Assistant API to get the name of the emmbedding model served"""
        r = self.send_request("get", "embeding/model/name")
        
        if isinstance(r, dict) and "model_name" in r:
            return r["model_name"]
        elif isinstance(r, dict) and "error" in r:
            raise requests.RequestException(r["error"])
        return r.decode("utf-8").strip()

    def send_request(
        self,
        rtype: str = "post" or "get",
        endpoint: str = "embed" or "embeding/model/name",
        query: str | list | None = None,
        host: str = "localhost",
        port: int = 5085,
        user_agent: str = "embedder",
        timeout: int = 2,
    ):
        """Send request to Assistant API (only for embedding models)"""
        try:
            headers = {"User-Agent": user_agent}
            payload = {}
            if query:
                payload["prompt"] = query
            if rtype == "post":
                r = requests.post(
                    f"http://{host}:{str(port)}/{endpoint}",
                    json=payload,
                    headers=headers,
                    timeout=timeout,
                )
            elif rtype == "get":
                r = requests.get(
                    f"http://{host}:{str(port)}/{endpoint}",
                    json=payload,
                    headers=headers,
                    timeout=timeout,
                )
            else:
                raise TypeError(
                    f"Request type is not supported.\n{rtype not in ['get', 'post']=}"
                )

            if r.status_code == 200:
                try:
                    rj = r.json()  # json.loads(r.content)
                    if rj:
                        return rj
                except requests.exceptions.JSONDecodeError:
                    pass
                return r.content
            raise requests.RequestException(
                f"""{r.status_code != 200=}\n{r.reason=}\n{r.content=}\n{r.json()=}\n{r=}"""
            )
        except (ConnectionError, requests.RequestException, TypeError) as ce:
            return {"error": str(ce)}
        except Exception as e:
            raise e


if __name__ == "__main__":
    embeddings = AssistantEmbeddings("intfloat/e5-large-v2")
    sentences = ["hello"]
    print(f"{embeddings.embed_sentences(sentences)=}")
