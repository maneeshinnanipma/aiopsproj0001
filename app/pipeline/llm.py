
# app/pipeline/llm.py
import json
from typing import Optional
from state import RefactorState
from services.bedrock_client import get_bedrock_client
from services.prompts import mk_refactor_plan_prompt
from utils.json_utils import safe_json_loads

MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
ANTHROPIC_API_VERSION = "bedrock-2023-05-31"

def node_bedrock_haiku(state: RefactorState,
                       region: str="us-east-1",
                       aws_access_key_id: Optional[str]=None,
                       aws_secret_access_key: Optional[str]=None) -> RefactorState:
    client = get_bedrock_client(aws_access_key_id, aws_secret_access_key, region)
    body = {
        "anthropic_version": ANTHROPIC_API_VERSION,
        "max_tokens": 2000,
        "temperature": 0.2,
        "messages": [{"role": "user", "content": mk_refactor_plan_prompt(
            state.raw_code, state.parsed_code, state.domain_model)}]
    }
    try:
        response = client.invoke_model(
            modelId=MODEL_ID, contentType="application/json", accept="application/json",
            body=json.dumps(body)
        )
        raw = json.loads(response["body"].read().decode("utf-8"))
        text = raw["content"][0]["text"]
        state.bedrock_response_raw = text
        state.structured_plan = safe_json_loads(text)
    except Exception as e:
        state.error = str(e)
    return state  # ← IMPORTANT
