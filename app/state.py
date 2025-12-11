
# app/state.py
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class RefactorState:
    raw_code: str
    parsed_code: Dict[str, Any] = field(default_factory=dict)
    domain_model: Dict[str, Any] = field(default_factory=dict)
    bedrock_response_raw: Optional[str] = None
    structured_plan: Dict[str, Any] = field(default_factory=dict)
    cloud_factory_mapping: Dict[str, Any] = field(default_factory=dict)
    enriched_plan: Dict[str, Any] = field(default_factory=dict)
    deployment_blueprint: Optional[str] = None
    repo_zip: Optional[str] = None
    error: Optional[str] = None
