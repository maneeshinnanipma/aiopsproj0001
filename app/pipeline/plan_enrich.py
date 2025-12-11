
# app/pipeline/plan_enrich.py
from state import RefactorState

def node_cloud_factory(state: RefactorState) -> RefactorState:
    state.cloud_factory_mapping = state.structured_plan.get("cloud_factory_mapping", {"services": []})
    return state  # ← IMPORTANT

def node_enrich_plan(state: RefactorState) -> RefactorState:
    plan = dict(state.structured_plan)
    plan["additional_resources"] = {
        "Networking": {"InternetGateway": {"Type": "AWS::EC2::InternetGateway"}},
        "Compute":    {"AutoScalingGroup": {"Type": "AWS::AutoScaling::AutoScalingGroup"}},
        "Storage":    {"S3Bucket": {"Type": "AWS::S3::Bucket"}},
        "IAM":        {"InstanceRole": {"Type": "AWS::IAM::Role"}},
        "Monitoring": {"CloudWatchAlarm": {"Type": "AWS::CloudWatch::Alarm"}},
    }
    state.enriched_plan = plan
    return state  # ← IMPORTANT
