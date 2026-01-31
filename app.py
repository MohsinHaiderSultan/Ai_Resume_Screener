import streamlit as st
import pandas as pd
import time
import plotly.express as px
from core.parser import extract_text
from core.analyzer import rank_candidates
from core.utils import clean_text

# 1. Page Configuration
st.set_page_config(
    page_title="TalentPulse AI | Premium Recruitment Suite",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Load External Stylesheet
def load_styles():
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback if file is missing in local environment
        pass

load_styles()

# 3. State Management
if 'shortlist' not in st.session_state:
    st.session_state.shortlist = []
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

def main():
    # Modern Executive Header
    st.markdown("""
        <div style='display: flex; align-items: center; justify-content: space-between; padding: 1.5rem 0; border-bottom: 1px solid var(--card-border); margin-bottom: 2rem;'>
            <div style='display: flex; align-items: center;'>
                <div style='background: #1d4ed8; width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 18px; box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3);'>
                    <span style='font-size: 24px; color: white;'>💠</span>
                </div>
                <div>
                    <h1 style='margin: 0; font-size: 1.8rem; font-weight: 800; color: var(--text-primary); letter-spacing: -0.02em;'>TalentPulse <span style='color: #1d4ed8;'>AI</span></h1>
                    <p style='margin: 0; color: var(--text-secondary); font-size: 0.9rem; font-weight: 500;'>Advanced Recruitment Intelligence</p>
                </div>
            </div>
            <div style='display: flex; gap: 12px;'>
                <div style='background: var(--metric-bg); padding: 10px 20px; border-radius: 10px; border: 1px solid var(--card-border); display: flex; align-items: center;'>
                    <span style='width: 8px; height: 8px; background: #10b981; border-radius: 50%; margin-right: 8px;'></span>
                    <span style='color: var(--text-primary); font-size: 0.85rem; font-weight: 700;'>SYSTEM ACTIVE</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar: Campaign Management
    with st.sidebar:
        st.markdown("<h3 style='color: var(--text-primary);'>Campaign Configuration</h3>", unsafe_allow_html=True)
        job_title = st.text_input("Job Role", "Senior Full-Stack Engineer")
        
        with st.expander("⚖️ Weighted Scoring", expanded=False):
            skill_weight = st.slider("Technical Skills", 0, 100, 50)
            exp_weight = st.slider("Experience Level", 0, 100, 30)
            edu_weight = st.slider("Education Value", 0, 100, 20)
        
        jd_text = st.text_area("Requirements Description", height=200, placeholder="Paste job details here...")
        
        uploaded_resumes = st.file_uploader(
            "Resumes (PDF/DOCX)", 
            type=["pdf", "docx"], 
            accept_multiple_files=True
        )
        
        st.divider()
        blind_mode = st.toggle("Blind Screening Mode")
        
        if st.button("🚀 Analyze Talent Pool", use_container_width=True, type="primary"):
            if jd_text and uploaded_resumes:
                with st.spinner("Analyzing candidate data..."):
                    all_results = []
                    progress = st.progress(0)
                    for idx, file in enumerate(uploaded_resumes):
                        progress.progress((idx + 1) / len(uploaded_resumes))
                        text = extract_text(file)
                        if text:
                            # Process analysis using the weights provided
                            analysis = rank_candidates(text, jd_text, weights=(skill_weight, exp_weight, edu_weight))
                            all_results.append({
                                "ID": f"C-{1000 + idx}",
                                "Name": "Candidate (Hidden)" if blind_mode else file.name,
                                "RawName": file.name,
                                "Score": analysis['score'],
                                "Skills": analysis['skills'],
                                "Missing": analysis['missing_skills'],
                                "Experience": analysis['experience_match'],
                                "Level": analysis['seniority_level'],
                                "Summary": analysis['summary']
                            })
                    st.session_state.analysis_results = pd.DataFrame(all_results).sort_values(by="Score", ascending=False)
                    st.toast("Analysis complete.", icon="📊")
            else:
                st.warning("Please upload resumes and paste a job description.")

        # Developer Attribution
        st.markdown("---")
        st.markdown(f"""
            <div style='padding: 20px; border-radius: 12px; background: var(--card-bg); border: 1px solid var(--card-border); text-align: center;'>
                <p style='margin: 0; font-size: 0.75rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase;'>Architected By</p>
                <p style='margin: 4px 0 0 0; font-size: 1.1rem; color: var(--text-primary); font-weight: 800;'>Mohsin Haider Sultan</p>
                <div style='display: flex; justify-content: center; gap: 8px; margin-top: 10px;'>
                    <span style='background: #1d4ed8; color: white; padding: 2px 10px; border-radius: 6px; font-size: 0.7rem; font-weight: 700;'>AI Specialist</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Dashboard Rendering
    if st.session_state.analysis_results is not None:
        df = st.session_state.analysis_results
        
        # Dashboard Overview Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Pipeline Size", f"{len(df)} Profiles")
        col2.metric("Shortlisted", f"{len(st.session_state.shortlist)} Candidates")
        col3.metric("Avg. Match", f"{round(df['Score'].mean(), 1)}%")
        col4.metric("Top Fit ID", df['ID'].iloc[0])

        st.markdown("<br>", unsafe_allow_html=True)

        # Main Interface Tabs
        tab_list, tab_compare, tab_analytics, tab_shortlist = st.tabs([
            "📋 Ranking Leaderboard", "🆚 Candidate Comparison", "🧠 Pool Analytics", "⭐ Final Selection"
        ])

        with tab_list:
            st.markdown("### Talent Match Leaderboard")
            st.dataframe(
                df[["ID", "Name", "Score", "Experience", "Level"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Score": st.column_config.ProgressColumn("Fit Confidence", format="%d%%", min_value=0, max_value=100),
                    "Level": "Seniority Class"
                }
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            selected_id = st.selectbox("Select Candidate for Deep Insight", df["ID"])
            row = df[df["ID"] == selected_id].iloc[0]
            
            p_col1, p_col2 = st.columns([2, 1])
            with p_col1:
                # Pill logic for Strengths and Gaps
                skills_html = "".join([f"<span class='pill pill-success'>{s}</span>" for s in row['Skills']])
                missing_html = "".join([f"<span class='pill pill-danger'>{s}</span>" for s in row['Missing']])

                st.markdown(f"""
                    <div class='talent-card'>
                        <h4 style='margin-top:0; color: var(--text-primary); border-bottom: 2px solid var(--card-border); padding-bottom: 10px;'>Analysis: {row['Name']}</h4>
                        <p style='font-size: 1rem; line-height: 1.6; color: var(--text-secondary); padding-top: 10px;'>{row['Summary']}</p>
                        
                        <div style='margin-top: 25px;'>
                            <p style='font-weight: 700; color: var(--text-primary); margin-bottom: 12px; font-size: 0.9rem;'>✅ IDENTIFIED STRENGTHS</p>
                            <div style='display: flex; flex-wrap: wrap; gap: 8px;'>
                                {skills_html if skills_html else "<span style='color: var(--text-muted); font-style: italic;'>No major matches found</span>"}
                            </div>
                        </div>
                        
                        <div style='margin-top: 20px;'>
                            <p style='font-weight: 700; color: var(--danger-text); margin-bottom: 12px; font-size: 0.9rem;'>⚠️ COMPETENCY GAPS</p>
                            <div style='display: flex; flex-wrap: wrap; gap: 8px;'>
                                {missing_html if missing_html else "<span style='color: var(--text-muted); font-style: italic;'>No significant gaps identified</span>"}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            with p_col2:
                st.markdown(f"""
                    <div class='talent-card' style='text-align: center;'>
                        <h1 style='color: var(--accent-primary); font-size: 3rem; margin: 0;'>{row['Score']}%</h1>
                        <p style='color: var(--text-muted); font-weight: 600;'>MATCH PROBABILITY</p>
                        <div style='margin-top: 15px;'>
                            <span class='pill pill-success' style='width: 100%; box-sizing: border-box;'>{row['Level']}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"⭐ Shortlist {row['ID']}", use_container_width=True):
                    if row['ID'] not in st.session_state.shortlist:
                        st.session_state.shortlist.append(row['ID'])
                        st.success("Shortlisted Successfully")
                    else:
                        st.info("Candidate already in shortlist")

        with tab_compare:
            st.markdown("### Talent Comparison Matrix")
            col_a, col_b = st.columns(2)
            with col_a:
                c1_id = st.selectbox("Subject A", df["ID"], key="ca_1")
                c1 = df[df["ID"] == c1_id].iloc[0]
                st.markdown(f"""
                    <div class='talent-card'>
                        <h2 style='color: var(--accent-primary); margin: 0;'>{c1['Score']}%</h2>
                        <p style='color: var(--text-secondary); font-weight: 700;'>{c1['Level']}</p>
                        <hr style='border: 0; border-top: 1px solid var(--card-border); margin: 15px 0;'>
                        <p style='color: var(--text-primary); line-height: 1.5;'>{c1['Experience']}</p>
                    </div>
                """, unsafe_allow_html=True)
            with col_b:
                c2_id = st.selectbox("Subject B", df["ID"], key="ca_2", index=min(1, len(df)-1))
                c2 = df[df["ID"] == c2_id].iloc[0]
                st.markdown(f"""
                    <div class='talent-card'>
                        <h2 style='color: var(--accent-primary); margin: 0;'>{c2['Score']}%</h2>
                        <p style='color: var(--text-secondary); font-weight: 700;'>{c2['Level']}</p>
                        <hr style='border: 0; border-top: 1px solid var(--card-border); margin: 15px 0;'>
                        <p style='color: var(--text-primary); line-height: 1.5;'>{c2['Experience']}</p>
                    </div>
                """, unsafe_allow_html=True)

        with tab_analytics:
            st.markdown("### Recruitment Data Insights")
            a_col1, a_col2 = st.columns(2)
            with a_col1:
                fig1 = px.histogram(df, x="Score", nbins=10, title="Match Distribution", 
                                   color_discrete_sequence=['#1d4ed8'], template="plotly_white")
                fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig1, use_container_width=True)
            with a_col2:
                fig2 = px.pie(df, names="Level", title="Experience Composition", hole=.4, 
                             color_discrete_sequence=px.colors.qualitative.Bold)
                fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig2, use_container_width=True)

        with tab_shortlist:
            if st.session_state.shortlist:
                s_df = df[df["ID"].isin(st.session_state.shortlist)]
                st.markdown("### Executive Talent Selection")
                st.dataframe(s_df[["ID", "Name", "Score", "Level"]], use_container_width=True, hide_index=True)
                
                if st.button("🗑️ Clear Shortlist", type="secondary"):
                    st.session_state.shortlist = []
                    st.rerun()
                
                csv = s_df.to_csv(index=False).encode('utf-8')
                st.download_button("📂 Export Detailed CSV", csv, "Shortlisted_Talent.csv", 
                                 "text/csv", use_container_width=True)
            else:
                st.info("No candidates selected yet. Review the Ranking Matrix to build your pool.")

    else:
        # Professional Hero Section for Empty State
        st.markdown(f"""
            <div style='background: var(--bg-color); border: 1px solid var(--card-border); padding: 80px 40px; border-radius: 24px; text-align: center; margin-top: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);'>
                <h1 style='color: var(--text-primary) !important; font-size: 3rem; margin-bottom: 20px; font-weight: 800; letter-spacing: -0.03em;'>Intelligent Talent Acquisition</h1>
                <p style='font-size: 1.2rem; max-width: 800px; margin: 0 auto 40px auto; color: var(--text-secondary); line-height: 1.7;'>
                    TalentPulse AI bridges the gap between massive resume pools and your ideal hire. 
                    Upload your candidate data to begin the automated semantic screening process.
                </p>
                <div style='display: flex; justify-content: center; gap: 30px; border-top: 1px solid var(--card-border); padding-top: 40px;'>
                    <div style='text-align: center;'>
                        <h3 style='margin:0; color: var(--accent-primary); font-size: 1.5rem;'>Semantic</h3>
                        <p style='margin:0; font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;'>Ranking Engine</p>
                    </div>
                    <div style='border-left: 1px solid var(--card-border); padding-left: 30px; text-align: center;'>
                        <h3 style='margin:0; color: var(--accent-primary); font-size: 1.5rem;'>Neural</h3>
                        <p style='margin:0; font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;'>Skill Analysis</p>
                    </div>
                    <div style='border-left: 1px solid var(--card-border); padding-left: 30px; text-align: center;'>
                        <h3 style='margin:0; color: var(--accent-primary); font-size: 1.5rem;'>Secure</h3>
                        <p style='margin:0; font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;'>Blind Screening</p>
                    </div>
                </div>
            </div>
            <div style='text-align: center; margin-top: -25px;'>
                <span style='background: #1d4ed8; color: white; padding: 12px 35px; border-radius: 50px; font-weight: 700; font-size: 0.95rem; box-shadow: 0 8px 25px rgba(29, 78, 216, 0.4);'>
                    Enterprise-Grade AI Screening
                </span>
            </div>
        """, unsafe_allow_html=True)
        
    # Standard System Footer
    st.markdown("""
        <div style='text-align: center; margin-top: 100px; padding: 40px 0; border-top: 1px solid var(--card-border);'>
            <p style='color: var(--text-muted); font-size: 0.85rem; line-height: 1.8;'>
                TalentPulse AI Suite • Version 2.0.4<br>
                Engineered for Performance by <b>Mohsin Haider Sultan</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()