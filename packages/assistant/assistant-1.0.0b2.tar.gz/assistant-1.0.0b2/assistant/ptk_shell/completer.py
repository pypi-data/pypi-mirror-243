import requests
import json

from typing import List
from prompt_toolkit.completion import Completion, Completer
from prompt_toolkit.document import Document


class AssistantCompleter(Completer):
    def format_query(self, query):
        formatted_query = f"""<|im_start|>system
You are to complete/finish given sentence(s), phrase(s) or command(s) with the most appropriate word(s) or phrase(s) that best fits the context. Do not answer the query yet.<|im_end|>
<|im_start|>user
{query}"""

        return formatted_query

    def send_request(
        self,
        query,
        host="localhost",
        port="5085",
        n: int = 5,
        max_tokens: int = 3,
        stream: bool = False,
        stop: List[str] | None = ["<|im_end|>", "<|im_start|>"],
    ):
        try:
            headers = {"User-Agent": "completer"}
            payload = {
                "prompt": query,
                "use_beam_search": True,
                "n": n,
                "temperature": 0,
                "max_tokens": max_tokens,
                "stream": stream,
                "stop": stop,
            }
            r = requests.post(
                f"http://{host}:{port}/generate", json=payload, headers=headers,
                timeout=2
            )
            if r.status_code == 200:
                rj = r.json()  # json.loads(r.content)
                if rj:
                    return self.format_completions(rj.get("text", []))
            else:
                raise Exception(r)
        except ConnectionError as e:
            return []
        except Exception as e:
            return []

    def format_completion(self, completion: str):
        formatted_completion = completion
        formatted_completion = formatted_completion.split("</s>")[0]
        formatted_completion = formatted_completion.split("[/INST]")[0]
        formatted_completion = formatted_completion.strip()
        return formatted_completion

    def format_completions(self, completions: List[str]):
        return [self.format_completion(completion) for completion in completions]

    def predict_next_words(self, current_words, host="localhost", port="5085", n=5):
        query = self.format_query(current_words)
        return self.send_request(query, host, port, n=n)

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        word_before_cursor = document.get_word_before_cursor()
        preds = list(
			set(
				[
					pred.split()[0] if pred.split() else pred
					for pred in self.predict_next_words(text_before_cursor)
				]
			)
		)
        for pred in preds:
            word = word_before_cursor + pred
            yield Completion(word, start_position=-len(word_before_cursor), display_meta="🔮")


if __name__ == "__main__":
    from prompt_toolkit import PromptSession

    session = PromptSession()
    completer = AssistantCompleter()
    while True:
        try:
            text = session.prompt(
                ">>> ",
                completer=completer,
                complete_while_typing=True,
                complete_in_thread=True,
                complete_style="readline",
            )
            print(f"You entered: {text}")
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
