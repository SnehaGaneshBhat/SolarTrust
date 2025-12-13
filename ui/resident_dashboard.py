import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt

def show_resident_dashboard():
    st.markdown("## Resident Dashboard")
    
    # --- Carousel-style Info Section ---
    st.markdown("### Updates & Announcements")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div style='background-color:#f0f2f6; padding:20px; border-radius:10px;'>
                <h4 style='margin-bottom:10px;'>📢 New Policy</h4>
                <p style='font-size:14px;'>Subsidy eligibility now includes buildings with ≥ 1000 sqft solar area.</p>
            </div>
            """, unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style='background-color:#f0f2f6; padding:20px; border-radius:10px;'>
                <h4 style='margin-bottom:10px;'>📅 Inspection Schedule</h4>
                <p style='font-size:14px;'>Next round of verifications begins Dec 10th in South Bengaluru.</p>
            </div>
            """, unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div style='background-color:#f0f2f6; padding:20px; border-radius:10px;'>
                <h4 style='margin-bottom:10px;'>✅ Verified Count</h4>
                <p style='font-size:14px;'>Over 1,200 rooftops verified and certified this month.</p>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("---")

    # --- Tabbed Navigation ---
    tabs = st.tabs(["Home", "View Progress", "Download Certificate", "Savings Calculator"])

    # --- Home Tab ---
    with tabs[0]:
        st.markdown("### About the Platform")
        st.markdown(
            """
            <div style='font-size:16px; line-height:1.6;'>
                <p>
                This platform empowers residents and officials to collaborate on accelerating rooftop solar adoption.
                Officials can verify solar installations using AI-powered satellite analysis, while residents can track
                the status of their building and access official certification for subsidy eligibility.
                </p>
                <p>
                Our mission is to streamline solar verification, ensure transparency, and support India's clean energy goals.
                </p>
            </div>
            """, unsafe_allow_html=True
        )

    # --- View Progress Tab ---
    with tabs[1]:
        st.markdown("### Check Your Building's Status")
        sample_id = st.text_input("Enter your building's Sample ID")

        if sample_id:
            manifest_path = f"outputs/manifests/{sample_id}.json"
            if os.path.exists(manifest_path):
                with open(manifest_path) as f:
                    data = json.load(f)

                st.success("Your building has been processed.")
                st.markdown(f"**QC Status:** {data['qc_status']}")
                st.markdown(f"**Solar Panels Detected:** {'Yes' if data['has_solar'] else 'No'}")
                st.markdown(f"**Estimated Solar Area:** {data['pv_area_sqm_est']} sqm")
                st.markdown(f"**Verification Date:** {data['image_metadata']['capture_date']}")

                if data["qc_status"] == "VERIFIABLE":
                    st.markdown("<span style='color:green; font-weight:bold;'>You are eligible for certification.</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color:red; font-weight:bold;'>Your rooftop did not meet the verification criteria.</span>", unsafe_allow_html=True)
            else:
                st.warning("No record found for this Sample ID. Please check and try again.")

    # --- Download Certificate Tab ---
    with tabs[2]:
        st.markdown("### Download Your Certificate")
        cert_id = st.text_input("Enter your Sample ID to retrieve your certificate")

        if cert_id:
            cert_path = f"certificates/{cert_id}_certificate.txt"
            if os.path.exists(cert_path):
                with open(cert_path, "r", encoding="utf-8") as f:
                    cert_text = f.read()

                st.text_area("Preview", cert_text, height=300)

                st.download_button(
                    label="📄 Download Certificate",
                    data=cert_text,
                    file_name=f"{cert_id}_certificate.txt",
                    mime="text/plain"
                )
            else:
                st.warning("Certificate not found. It may not have been issued yet.")

    # --- Savings Calculator Tab ---
    with tabs[3]:
        st.markdown("### Interactive Savings Calculator")

        house_id = st.text_input("Enter your House ID (Sample ID)")
        monthly_usage = st.number_input("Enter your monthly electricity usage (kWh)", min_value=0, step=10)

        if house_id and monthly_usage > 0:
            manifest_path = f"outputs/manifests/{house_id}.json"
            try:
                if os.path.exists(manifest_path):
                    with open(manifest_path) as f:
                        data = json.load(f)

                    # Safely fetch rooftop area
                    pv_area = data.get("pv_area_sqm_est")
                    if pv_area is None or pv_area == 0:
                        st.warning("This house hasn't been certified by an official yet. Please wait for verification.")
                    else:
                        # Auto-calculate system size from rooftop area
                        system_size = round(pv_area / 10, 1)  # assume ~10 sqm per kW
                        st.info(f"Detected System Size: {system_size} kW (based on rooftop area)")

                        # Assumptions
                        cost_per_kWh = 8  # ₹ per kWh
                        generation_per_kW = 120  # kWh/month per kW system
                        co2_per_kWh = 0.82  # kg CO₂ avoided per kWh
                        cost_per_kW = 40000  # ₹ per kW installation cost

                        monthly_generation = system_size * generation_per_kW
                        savings = min(monthly_generation, monthly_usage) * cost_per_kWh
                        payback_years = (system_size * cost_per_kW) / (savings * 12)
                        co2_reduction = monthly_generation * co2_per_kWh / 1000  # tons per month

                        # Results
                        st.success(f"Estimated Monthly Savings: ₹{savings:,.0f}")
                        st.info(f"Estimated Payback Period: {payback_years:.1f} years")
                        st.success(f"CO₂ Reduction: {co2_reduction:.2f} tons per month")

                        # --- Visual Bar Chart ---
                        chart_data = pd.DataFrame({
                            "Category": ["Monthly Usage", "Solar Generation"],
                            "kWh": [monthly_usage, monthly_generation]
                        })
                        st.bar_chart(chart_data.set_index("Category"))

                else:
                    st.warning("No record found for this House ID. It may not have been certified yet.")

            except Exception as e:
                st.error("⚠️ Something went wrong while retrieving data. Please try again later.")
                st.caption(f"Technical details: {e}")