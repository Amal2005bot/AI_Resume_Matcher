import streamlit as st
import pandas as pd
import os
from utils import extract_text_from_pdf, clean_text, get_matching_skills, get_missing_skills
from engine import calculate_match_score

# --- Page Config ---
st.set_page_config(page_title="AI Resume Matcher", page_icon="📄")

st.title(" AI Resume–Job Description Matcher")
st.sidebar.info("This AI uses TF-IDF and Cosine Similarity to rank resumes.")
st.markdown("Upload multiple resumes to see who fits the job description best.")

# --- Layout ---
col1, col2 = st.columns(2)

with col1:
    st.header("1. Job Description")
    job_text = st.text_area("Paste the job description here:", height=300)

with col2:
    st.header("2. Upload Resumes")
    # Accept multiple files at once
    uploaded_files = st.file_uploader("Upload PDF resumes", type="pdf", accept_multiple_files=True)

# --- Analysis Logic ---
if st.button("Rank Candidates"):
    if uploaded_files and job_text:
        results = [] # To store data for our table
        
        with st.spinner(f'Analyzing {len(uploaded_files)} resumes...'):
            for uploaded_file in uploaded_files:
                # 1. Save and Read
                with open("temp.pdf", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                raw_resume = extract_text_from_pdf("temp.pdf")
                c_resume = clean_text(raw_resume)
                c_job = clean_text(job_text)
                
                # 2. Calculate
                score = calculate_match_score(c_resume, c_job)
                skills = get_matching_skills(c_resume, c_job)
                
                # 3. Store results in a list of dictionaries
                results.append({
                    "Candidate Name": uploaded_file.name,
                    "Match Score (%)": score,
                    "Top Skills": ", ".join(skills[:5])
                })
                
                os.remove("temp.pdf") 

            # --- Process Results ---
            df = pd.DataFrame(results)
            
            # Check if we actually got any results before displaying
            if not df.empty:
                df = df.sort_values(by="Match Score (%)", ascending=False)
                
                # --- Display Leaderboard ---
                st.divider()
                st.header("Candidate Ranking Report") # Professional version
                
                # Show the winner
                winner = df.iloc[0]["Candidate Name"]
                st.success(f"**Top Candidate Identified:** {winner}")
                
                # Display the table
                st.dataframe(df, use_container_width=True)
                
                # --- Download Button ---
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Export Results (CSV)",
                    data=csv,
                    file_name='candidate_ranking.csv',
                    mime='text/csv',
                )
            else:
                st.error("No resumes were successfully processed. Please check your files.")
