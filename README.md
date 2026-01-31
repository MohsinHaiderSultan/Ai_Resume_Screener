<p align="center">
  <img src="https://img.icons8.com/fluency/120/artificial-intelligence.png" width="120" />
</p>

<h1 align="center">💠 TalentPulse AI</h1>

<p align="center">
  <strong>Next-Gen Recruitment Intelligence Platform</strong><br>
  Enterprise-grade AI Resume Screening & Candidate Ranking System
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/NLP-TF--IDF%20%7C%20Cosine-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" />
</p>

---

## 📸 Screenshots

| Dashboard | Candidate Comparsion | Pool Analytics | Final Selection |
|------------|-----------|----------------|----------------|
| <img src="assets/Screenshot (36).png" alt="Login Page" width="300"/> | <img src="assets/Screenshot (37).png" alt="Dashboard" width="300"/> | <img src="assets/Screenshot (38).png" alt="Anomaly Report" width="300"/> |<img src="assets/Screenshot (39).png" alt="Threat Intel" width="300"/> |


---

---

## 🚀 Overview

**TalentPulse AI** is a high-performance, enterprise-grade **AI Resume Screening and Candidate Ranking System**.  
Built using modern **Human-Computer Interaction (HCI)** principles, it leverages advanced **Natural Language Processing (NLP)** to:

- Automate the recruitment pipeline
- Reduce unconscious hiring bias
- Identify top-tier talent with semantic precision

This platform moves beyond traditional keyword filtering by **understanding context, relevance, and intent**.

---

## ✨ Core Features

### 🧠 Intelligent Semantic Ranking
- TF-IDF Vectorization with Cosine Similarity
- Context-aware matching of resumes to Job Descriptions
- Eliminates shallow keyword dependency

### 🎨 Multi-Theme Enterprise UI
A premium dashboard with three professional environments:

- 🌞 **Light Mode** – Clean, high-contrast corporate layout  
- 🌑 **Dark Mode** – Midnight theme for focused workflows  
- ⚡ **SOC Neon Mode** – Cyber-inspired UI for data-heavy analysis  

### 🛡️ Dynamic Bias Mitigation
- **Blind Hiring Mode** – One-click anonymization of candidate identifiers
- **Weighted Scoring Engine** – Adjust importance of:
  - Technical Skills
  - Experience
  - Education

### 📊 Advanced Talent Analytics
- **Gap Analysis** – Detects missing competencies per JD
- **Side-by-Side Comparison** – Compare two candidates simultaneously
- **Visual Insights** – Real-time Plotly charts for:
  - Score distribution
  - Talent seniority
  - Ranking spread

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|-----------|
| Frontend | Streamlit (Custom CSS / JS Injection) |
| NLP Engine | Scikit-learn (TF-IDF, Cosine Similarity) |
| Parsing | pdfminer.six (PDF), python-docx (DOCX) |
| Visualization | Plotly Express |
| Styling | Modern CSS3 (Glassmorphism & Fluid Typography) |

---

## 📂 Project Structure

```bash
ai_resume_screener/
├── app.py              # Main Streamlit Dashboard (UI / UX Logic)
├── requirements.txt    # Python Dependencies
├── assets/
│   └── style.css       # Enterprise Theme Engine (Light / Dark / SOC)
├── core/
│   ├── parser.py       # Resume Parsing Logic (PDF / DOCX)
│   ├── analyzer.py     # Weighted NLP Ranking Engine
│   └── utils.py        # Text Cleaning & Preprocessing
└──  data/
      └── uploads/        # Temporary Storage for Batch Processing
```
---

## ⚙️ Installation & Setup
- 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/talentpulse-ai.git
cd talentpulse-ai
```

- 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

- 3️⃣ Run the Application
```bash
streamlit run app.py
```
---

## 📋 Usage Guide

### 1️⃣ Configure Campaign
- Paste the **Job Description** into the provided input area
- Adjust **scoring weights** (Skills, Experience, Education) from the sidebar

### 2️⃣ Upload Resumes
- Drag & drop candidate resumes in **PDF** or **DOCX** format
- Supports **batch processing** for multiple candidates

### 3️⃣ Analyze
- Click **“Initiate Smart Scan”**
- The NLP engine processes resumes **in real time** and computes semantic scores

### 4️⃣ Shortlist
- View the **ranked leaderboard** of candidates
- Deep-dive into **individual candidate insights**
- **Compare candidates side-by-side** for informed decision-making

### 5️⃣ Export
- Download the **executive summary** and rankings as a **CSV file**

---

## 🧩 Architecture & Design Philosophy

This system is designed following **Human-Computer Interaction (HCI)** best practices:

- **Visibility**  
  Real-time progress indicators during resume processing

- **Recognition over Recall**  
  Clear highlighting of matched skills versus identified gaps

- **Minimalist Aesthetic**  
  High information density managed through intuitive workspace tabs

- **Enterprise Readability**  
  Clean typography with contrast-safe color palettes for professional use

---

## 👤 Author

**Mohsin Haider Sultan**  
*Lead Systems Architect & AI Specialist*

---

