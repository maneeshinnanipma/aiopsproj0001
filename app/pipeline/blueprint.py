
# app/pipeline/blueprint.py
import json
from state import RefactorState

def node_blueprint(state: RefactorState) -> RefactorState:
    state.deployment_blueprint = f"# Deployment Blueprint\n\n{json.dumps(state.enriched_plan, indent=2)}"
    return state  # ← IMPORTANT
