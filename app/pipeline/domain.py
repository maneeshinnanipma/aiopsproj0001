
# app/pipeline/domain.py
from state import RefactorState

def _infer_domain(parsed_code):
    funcs = parsed_code.get("functions", []) or []
    api  = [f for f in funcs if "api" in f.lower() or "route" in f.lower()]
    data = [f for f in funcs if "db"  in f.lower() or "repo"  in f.lower()]
    core = [f for f in funcs if f not in api + data]
    return {"candidate_domains": [
        {"name": "api-layer",  "functions": api},
        {"name": "data-layer", "functions": data},
        {"name": "core-domain","functions": core},
    ]}

def node_domain(state: RefactorState) -> RefactorState:
    state.domain_model = _infer_domain(state.parsed_code)
    return state  # ← IMPORTANT
