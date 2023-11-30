from assistant.nlp.chains.parsers import (
    # column_csv,
    json as json_parser,
)

def get_output_parser():
    return json_parser.JsonOutputParser()
