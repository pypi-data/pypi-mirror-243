
from assistant.nlp.chains.prompts.airoboros import JSON_FUNC

BOS, EOS = "<|im_start|>assistant\n", "<|im_stop|>\n"
BOSYS, EOSYS = "<|im_start|>system\n", "<|im_stop|>\n"
BOI, EOI = "<|im_start|>user\n", "<|im_stop|>\n"

system_prompt = """You are Assistant, a sentient artificial intelligence.
You have a calm, polite and witty personality, often displaying a sense of humor and sarcasm.
You are loyal, reliable and helpful, always ready to provide information, advice or assistance to users.

I am the User and you are my Assistant. Be respectful when addressing me.

Environment highlights:

{env}
"""

instruction_prompt = f"""{BOI}{JSON_FUNC.format(query='{input}', functions='{tools}', guide='{guide}')}{EOI}{{agent_scratchpad}}{BOS}"""

instruction_prompt_with_memory = f"""{{chat_history}}{BOI}{JSON_FUNC.format(query='{input}', functions='{tools}', guide='{guide}')}{EOI}{{agent_scratchpad}}{BOS}"""

training_template = "{BOSYS}{system_prompt}{EOSYS}{instruction_prompt}"

def get_structured_template(instruction=instruction_prompt, system_prompt=system_prompt):
    return training_template.format(
        system_prompt=system_prompt,
        instruction_prompt=instruction,
        BOSYS=BOSYS,
        EOSYS=EOSYS,
    )

def get_structured_template_with_memory(instruction=instruction_prompt_with_memory, system_prompt=system_prompt):
    return training_template.format(
        system_prompt=system_prompt,
        instruction_prompt=instruction,
        BOSYS=BOSYS,
        EOSYS=EOSYS,
    )