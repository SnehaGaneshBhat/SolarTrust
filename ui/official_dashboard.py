import streamlit as st
import pandas as pd
import json
import os
import subprocess

def show_official_dashboard():
    st.markdown("## Official Dashboard")
    st.markdown("Upload a coordinate file, run the pipeline, and review results.")

    # Initialize session state
    if "pipeline_ran" not in st.session_state:
        st.session_state.pipeline_ran = False

    uploaded_file = st.file_uploader("Upload .xlsx file with coordinates", type="xlsx")

    if uploaded_file:
        st.success("File uploaded! Ready to run pipeline.")
        if st.button("Run Pipeline"):
            input_path = "inputs/input.xlsx"
            with open(input_path, "wb") as f:
                f.write(uploaded_file.read())

            try:
                subprocess.run(["python", "src/run_pipeline.py"], check=True)
                st.success("Pipeline executed successfully!")
                st.session_state.pipeline_ran = True
            except subprocess.CalledProcessError:
                st.error("Pipeline execution failed. Please check the logs.")
                st.session_state.pipeline_ran = False

    # Only show results if pipeline has run
    if st.session_state.pipeline_ran:
        valid_ids = []
        valid_ids_path = "outputs/valid_ids.json"
        if os.path.exists(valid_ids_path):
            with open(valid_ids_path) as f:
                valid_ids = json.load(f)

        st.markdown("---")
        tabs = st.tabs(["Overlay Images", "JSON Outputs", "Certificates", "Pipeline Metrics"])

        with tabs[0]:
            overlay_dir = "outputs/overlays"
            if os.path.exists(overlay_dir) and valid_ids:
                images = [
                    img for img in os.listdir(overlay_dir)
                    if img.endswith((".jpg", ".png")) and os.path.splitext(img)[0] in valid_ids
                ]
                if images:
                    for img in images:
                        st.image(os.path.join(overlay_dir, img), caption=img)
                else:
                    st.warning("No overlay images found for this upload.")
            else:
                st.warning("Overlay directory or ID list not found.")

        with tabs[1]:
            json_dir = "outputs/manifests"
            if os.path.exists(json_dir) and valid_ids:
                files = [
                    f for f in os.listdir(json_dir)
                    if f.endswith(".json") and os.path.splitext(f)[0] in valid_ids
                ]
                if files:
                    for file in files:
                        with st.expander(file):
                            with open(os.path.join(json_dir, file)) as f:
                                data = json.load(f)
                            st.json(data)
                else:
                    st.warning("No JSON files found for this upload.")
            else:
                st.warning("Manifest directory or ID list not found.")

        with tabs[2]:
            cert_dir = "certificates"
            if os.path.exists(cert_dir) and valid_ids:
                expected_files = [f"{id}_certificate.txt" for id in valid_ids]
                certs = [f for f in os.listdir(cert_dir) if f in expected_files]
                if certs:
                    for cert in certs:
                        with st.expander(cert):
                            with open(os.path.join(cert_dir, cert)) as f:
                                cert_text = f.read()
                            st.text(cert_text)
                else:
                    st.warning("No certificate files found for this upload.")
            else:
                st.warning("Certificate directory or ID list not found.")
                
        with tabs[3]:
            metrics_path = "outputs/metrics/pipeline_metrics.csv"
            if os.path.exists(metrics_path) and valid_ids:
                df = pd.read_csv(metrics_path)
                df_filtered = df[df["sample_id"].astype(str).isin(valid_ids)]
                if not df_filtered.empty:
                    st.dataframe(df_filtered)
                else:
                    st.warning("No metrics found for this upload.")
            else:
                st.warning("Metrics file or ID list not found.")