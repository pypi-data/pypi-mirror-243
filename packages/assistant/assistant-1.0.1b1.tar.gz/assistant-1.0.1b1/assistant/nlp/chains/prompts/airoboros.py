"""
Airoboros prompt templates.
"""

JSON_FUNC_INSTRUCTIONS = """\
As my Assistant, \
please select the most suitable \
function and parameters \
from the list of available functions below, \
based on my input. \
Provide your response in JSON format.\
"""

JSON_FUNC = f"""\
{JSON_FUNC_INSTRUCTIONS}

Input: {{query}}

Available functions:
{{functions}}
final_answer:
    description: User only sees your final answers. Use this tool to talk with the User. Always consider the `$LANG` environment variable to make sure to answer in the User language.
        parameters:
            answer: Anything you want to say to the User.

Guidebook:
Use the following guide to anser only if relevant to the Input from the User.
{{guide}}
"""
