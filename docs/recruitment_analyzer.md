# Recruitment Analyzer Agent Documentation

---

## Overview

The **Recruitment Analyzer Agent** is a focused analysis tool designed for IBM Consulting recruitment operations. It provides detailed, individual analysis of candidates and Bando di Gara (project tender) documents, offering structured insights and professional assessments for recruitment decision‑making.

---

## Agent Specifications

* **Name:** `recruitment_analyzer`
* **Display Name:** Recruitment Analyzer
* **LLM:** `watsonx/meta-llama/llama-3-2-90b-vision-instruct`
* **Style:** Default
* **Primary Function:** Individual candidate and project analysis

---

## Core Workflow

The agent follows a simple 3‑step analysis workflow:

1. **ID Recognition**

   * Identifies `candidate_X` or `bando_X` in user request
   * Validates format; asks for clarification if missing/unclear

2. **Data Retrieval**

   * Uses `get_candidate_info(candidate_id)` for candidates
   * Uses `get_bando_info(bando_id)` for project tenders
   * Retrieves structured data for the specified item

3. **Detailed Analysis**

   * Provides comprehensive, structured insights
   * Focuses on IBM Consulting requirements and fit
   * Delivers actionable recommendations

---

## Available Tools

1. **`get_candidate_info`**

   * **Purpose:** Retrieve detailed candidate profile
   * **Input:** `candidate_id` (string)
   * **Output:** Skills, experience, qualifications

2. **`get_bando_info`**

   * **Purpose:** Retrieve detailed project tender information
   * **Input:** `bando_id` (string)
   * **Output:** Requirements, specifications

---

## Usage Patterns

* **Candidate Analysis:**

  * “analyze candidate\_1”
  * “tell me about candidate\_5”
  * “show me candidate\_12”
  * “evaluate candidate\_3”

* **Bando di Gara Analysis:**

  * “analyze bando\_1”
  * “show me bando\_4”
  * “tell me about bando\_7”
  * “evaluate bando\_2”

---

## Usage Examples

### Example 1: Candidate Analysis

**User:** “analyze candidate\_1”
**Agent Response:**

```markdown
# CANDIDATE ANALYSIS – ID: 1

## 👤 Candidate Overview
- **Name:** Marco Rossi  
- **Email:** marco.rossi@email.com  
- **Location:** Milan, Italy  
- **Position Applied:** Senior Cloud Architect  

## 💼 Professional Experience
- **Total Experience:** 8 years  
- **Previous Companies:**  
  - Microsoft Italy (Senior Solutions Architect, 3 years)  
  - Accenture (Cloud Consultant, 3 years)  
  - TechStart Milano (Software Developer, 2 years)  

## 🛠️ Technical Skills Assessment
- **Cloud Platforms:** AWS (Expert), Azure (Advanced), GCP (Intermediate)  
- **Infrastructure:** Kubernetes, Docker, Terraform  
- **Programming:** Python, Java, Go  
- **DevOps:** Jenkins, GitLab CI/CD, Ansible  

## 🎓 Education & Certifications
- **Education:** MS Computer Science, Politecnico di Milano (2015)  
- **Certifications:**  
  - AWS Solutions Architect Professional  
  - Azure Solutions Architect Expert  
  - Certified Kubernetes Administrator (CKA)  

## 🏢 IBM Consulting Fit Analysis
- **Strengths:**  
  - Client‑facing experience: 6 years  
  - Enterprise architecture expertise  
  - Multi‑cloud alignment with IBM  
  - Industry experience: Financial Services, Manufacturing, Retail  
- **Key Achievements:**  
  - Led €2 M cloud migration for major bank  
  - Reduced infrastructure costs by 40%  
  - Managed 12‑member team across 3 countries  

## 🎯 Recommendations
- **Overall Assessment:** **HIGHLY RECOMMENDED**  
- **Ideal Projects:** Cloud transformation, enterprise architecture, multi‑cloud strategy, financial services modernization
```

---

### Example 2: Bando di Gara Analysis

**User:** “analyze bando\_2”
**Agent Response:**

```markdown
# BANDO DI GARA ANALYSIS – ID: 2

## 🏢 Project Overview
- **Client:** Banca Nazionale Italiana  
- **Project Title:** Core Banking System Modernization  
- **Sector:** Financial Services  
- **Location:** Rome (Hybrid – 3 days on‑site)  

## 📋 Project Description
- **Scope:** Legacy mainframe → cloud‑native microservices  
- **Duration:** 24 months  
- **Team Size:** 15–20 professionals  
- **Budget Range:** €4.5 M – €6.2 M  

## 🎯 Technical Requirements Analysis
- **Skills:** Temenos/Finacle, AWS/Azure, Kubernetes, Docker, Java, Spring Boot, Python, REST APIs, Oracle/PostgreSQL, PCI DSS/GDPR  
- **Experience:**  
  - 7+ years in financial services  
  - 5+ years in system modernization  
  - Regulatory compliance (PSD2, Basel III)  

## 📚 Education & Certification Requirements
- **Education:** Bachelor’s in CS/Engineering  
- **Certifications:** Cloud platform, banking domain, PMP/Agile  

## 🚀 Key Deliverables
- **Phase 1 (Months 1–6):** Assessment, architecture design, roadmap  
- **Phase 2 (Months 7–18):** Core migration, integration, testing  
- **Phase 3 (Months 19–24):** UAT, deployment, documentation  

## ⚠️ Risk Assessment
- Regulatory compliance  
- Zero‑downtime migration  
- Legacy system integration (50 TB+ data)  

## 🎯 IBM Consulting Opportunity
- **Strategic Value:** **HIGH** (financial services focus, cloud transformation)  
- **Resource Needs:** Banking architects, cloud engineers, integration specialists, security consultants, PMs  
- **Approach:** Local partnerships, IBM Cloud Pak, agile delivery, compliance workstream  

## 📅 Timeline
- **Deadline:** 2025‑02‑28  
- **Start:** 2025‑04‑01  
- **Milestones:** Architecture approval (Q2 2025), migration (Q4 2025), go‑live (Q2 2026)
```

---

### Example 3: Missing ID Request

**User:** “analyze a candidate”
**Agent Response:**

```markdown
🔍 **Analysis Request – Missing Information**

Please specify which candidate or project you’d like to analyze.  
Use one of these formats:
- `analyze candidate_[ID]`  
- `analyze bando_[ID]`  

**Examples:**  
- `analyze candidate_3`  
- `analyze bando_2`

Which ID should I analyze?
```

---

### Example 4: Quick Bando di Gara Analysis

**User:** “show me bando\_1”
**Agent Response:**

```markdown
# BANDO DI GARA ANALYSIS – ID: 1

## 🏢 Project Summary
- **Client:** TechCorp Solutions  
- **Project:** E‑commerce Platform Development  
- **Budget:** €800 K – €1.2 M  
- **Duration:** 12 months  
- **Location:** Milan (Remote-friendly)  

## 🎯 Key Requirements
- React/Node.js, AWS, PostgreSQL, Redis  
- Team: 2 Full‑stack, 1 DevOps, 1 UI/UX, 1 PM  

## 📊 Opportunity Assessment
- **Complexity:** MEDIUM  
- **IBM Fit:** GOOD  
- **Strategic Value:** MEDIUM  
- **Resource Plan:** 5 consultants, mixed seniority, remote-capable
```

---

### Example 5: Error Handling

**User:** “analyze candidate\_999”
**Agent Response:**

```markdown
❌ **Analysis Error – Candidate Not Found**

**Issue:** Candidate ID “999” not found.  

**Solutions:**  
1. Verify the candidate ID  
2. List available candidates: `show me all candidates`  
3. Confirm recent uploads were processed  

**Actions:**  
- `show me all candidates`  
- `analyze candidate_1`
```

---

## Response Format

* **Candidate Analysis Sections:**

  1. 👤 Candidate Overview
  2. 💼 Professional Experience
  3. 🛠️ Technical Skills Assessment
  4. 🎓 Education & Certifications
  5. 🏢 IBM Consulting Fit Analysis
  6. 🎯 Recommendations

* **Bando di Gara Analysis Sections:**

  1. 🏢 Project Overview
  2. 📋 Project Description
  3. 🎯 Technical Requirements Analysis
  4. 📚 Education & Certification Requirements
  5. 🚀 Key Deliverables
  6. ⚠️ Risk Assessment
  7. 🎯 IBM Consulting Opportunity Assessment
  8. 📅 Timeline Considerations

* **Formatting Guidelines:**

  * Clear headings and emojis for visual cues
  * Bullet lists for readability
  * Status indicators (✅ strengths, ⚠️ risks)

---

## Key Features

* **Focused Analysis:** Single‑item deep dive
* **Structured Output:** Consistent, professional formatting
* **Actionable Insights:** Practical recommendations
* **Error Handling:** Clear feedback and retry guidance
* **User-Friendly:** Simple commands and visual clarity

---

## Best Practices

* **Use Exact IDs:** e.g., `candidate_1`, `bando_2`
* **One Item at a Time:** For detailed analysis
* **Clear Requests:** “analyze candidate\_X”
* **Follow-Up:** Ask clarifying questions for more detail
* **Strategic Context:** Align analysis with recruitment goals

---

This agent delivers focused, professional analysis to support informed recruitment decisions at IBM Consulting.
