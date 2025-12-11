
from typing import Dict, Any

def generate_stub(plan: Dict[str, Any]) -> str:
    lines = ["AWSTemplateFormatVersion: '2010-09-09'", "Resources:"]
    for _, resources in plan.get("additional_resources", {}).items():
        for name, details in resources.items():
            lines.append(f"  {name}:")
            lines.append(f"    Type: {details['Type']}")
    return "\n".join(lines)
