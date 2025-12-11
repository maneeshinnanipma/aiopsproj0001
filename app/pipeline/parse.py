
# app/pipeline/parse.py
from state import RefactorState
from utils.python_parser import parse_python_code

def node_parse(state: RefactorState) -> RefactorState:
    state.parsed_code = parse_python_code(state.raw_code)
    return state  # ← IMPORTANT
