
# --- Robust path bootstrap: add project root to sys.path ---
import os, sys
# ROOT = parent folder of this file's directory (i.e., project root containing app/, infra/, services/, utils/, config/)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

#!/usr/bin/env python
# main.py

import streamlit as st

from state import RefactorState
from pipeline.parse import node_parse
from pipeline.domain import node_domain
from pipeline.llm import node_bedrock_haiku
from pipeline.plan_enrich import node_cloud_factory, node_enrich_plan
from pipeline.blueprint import node_blueprint
from pipeline.repo import node_generate_repo
from config import settings

def main():
    st.set_page_config(page_title="Cloud Refactor Planner", layout="wide")
    st.title("🏗️ Monolith → Cloud Factory Refactor Planner")

    # Optional AWS overrides — prefer provider chain; do not persist secrets
    st.sidebar.header("AWS (optional overrides)")
    region = st.sidebar.text_input("Region", value=(settings.AWS_REGION or "us-east-1"))
    use_explicit = st.sidebar.checkbox("Use explicit access keys (discouraged)", value=False)
    ak = st.sidebar.text_input("Access Key", value=(settings.AWS_ACCESS_KEY_ID or ""), type="default") if use_explicit else None
    sk = st.sidebar.text_input("Secret Key", value=(settings.AWS_SECRET_ACCESS_KEY or ""), type="password") if use_explicit else None

    code_text = st.text_area("Paste Monolith Code", height=300)

    if st.button("🚀 Generate Plan"):
        if not code_text.strip():
            st.error("Please provide code.")
            st.stop()

        progress = st.progress(0)
        state = RefactorState(raw_code=code_text)

        progress.progress(20, "Parsing...")
        state = node_parse(state)
        st.subheader("Parsed Code"); st.json(state.parsed_code)

        progress.progress(40, "Inferring domain...")
        state = node_domain(state)
        st.subheader("Domain Model"); st.json(state.domain_model)

        progress.progress(60, "Calling Claude Haiku on Bedrock...")
        state = node_bedrock_haiku(state, region=region, aws_access_key_id=ak, aws_secret_access_key=sk)
        if state.error:
            st.error(state.error); st.stop()
        st.subheader("Structured Plan (LLM)"); st.json(state.structured_plan)

        progress.progress(75, "Cloud Factory mapping...")
        state = node_cloud_factory(state)
        st.subheader("Cloud Factory Mapping"); st.json(state.cloud_factory_mapping)

        progress.progress(85, "Enriching plan...")
        state = node_enrich_plan(state)
        st.subheader("Enriched Plan"); st.json(state.enriched_plan)

        progress.progress(95, "Generating blueprint...")
        state = node_blueprint(state)
        st.subheader("Deployment Blueprint"); st.markdown(state.deployment_blueprint or "")

        progress.progress(100, "Creating GitHub repo...")
        state = node_generate_repo(state)
        st.success("✅ Repo ready!")
        if state.repo_zip:
            with open(state.repo_zip, "rb") as f:
                st.download_button("Download GitHub Repo ZIP", f, file_name=state.repo_zip)

if __name__ == "__main__":
    main()
