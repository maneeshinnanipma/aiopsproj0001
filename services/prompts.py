
import json

def mk_refactor_plan_prompt(raw_code: str, parsed: dict, domain: dict) -> str:
    return (
        "Generate JSON migration plan for AWS-native architecture.\n"
        "Keys: current_diagnostic, target_architecture, phased_roadmap, "
        "readiness_scores, cloud_factory_mapping, deployment_blueprint.\n"
        "Code snippet:\n" + raw_code + "\nParsed:\n" +
        json.dumps(parsed, indent=2) + "\nDomain:\n" +
        json.dumps(domain, indent=2)
    )
