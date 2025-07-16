**Recruitment Document Manager Agent Documentation**

---

## Overview

The **Recruitment Document Manager Agent** is an intelligent document processing system designed for IBM Consulting recruitment operations. It serves as a central orchestrator that automatically processes uploaded CV and Bando di Gara documents, routes them for structured data extraction, and manages the complete workflow from document upload to database storage.

---

## Agent Specifications

* **Name:** `recruitment_manager`
* **Display Name:** Recruitment Document Manager
* **LLM:** `watsonx/meta-llama/llama-3-2-90b-vision-instruct`
* **Style:** React
* **Primary Function:** Document processing orchestration and database management

---

## Core Workflow

The agent follows a comprehensive 5‑step document management workflow:

1. **Document Upload Detection**

   * Detects uploads (PDF, Word, Excel)
   * Acknowledges each upload by filename
   * Supports batch uploads

2. **Document Routing to Processor**

   * Routes to the **processor** collaborator agent
   * Manages the collaboration protocol and message exchange

3. **Data Validation**

   * Receives and validates the extracted JSON
   * Ensures schema integrity before database operations
   * Handles errors gracefully

4. **Database Operations**

   * Formats and saves data via `format_and_save_processed_data`
   * Assigns unique IDs
   * Maintains data integrity and relationships

5. **Comprehensive Feedback**

   * Provides detailed feedback with assigned IDs and summaries
   * Suggests next steps and available actions

---

## Collaboration Architecture

**Processor Agent Integration**

* **Processor Agent Role:** Document analysis & structured extraction
* **Manager Agent Role:** Workflow orchestration, data validation, database management
* **Protocol:** JSON-based exchange with error handling

**End-to-End Flow**

```
User Upload → Manager Agent → Processor Agent → Manager Agent → Database → User Feedback
```

---

## Available Tools

1. **`format_and_save_processed_data`**

   * **Purpose:** Save extracted JSON to recruitment database
   * **Input:** Structured JSON
   * **Output:** Confirmation with assigned ID

2. **`get_all_candidates`**

   * **Purpose:** Retrieve all candidates
   * **Output:** List of candidates

3. **`get_all_bandos`**

   * **Purpose:** Retrieve all Bando di Gara projects
   * **Output:** List of projects

4. **`get_candidate_by_id`**

   * **Purpose:** Retrieve candidate details by ID
   * **Input:** Candidate ID
   * **Output:** Candidate information

5. **`clear_thread_files`**

   * **Purpose:** Clear uploaded file info in current thread
   * **Output:** Confirmation

---

## Document Processing Capabilities

* **Supported Types:**

  * CV/Resume (personal profiles, skills, experience)
  * Bando di Gara (project tenders, requirements, specs)
  * Excel (.xlsx)
  * PDFs, Word, other formats

* **Processing Rules:**

  * Individual processing per document
  * No merging across files
  * Graceful error handling
  * Real-time status updates

---

## Chat with Documents Feature

* **Configuration:**

  * Enabled for uploads & processing
  * Citations: Up to 3 source references
  * Response length: Moderate
  * Custom messages for delays or connectivity

* **Vector Index Settings:**

  * Chunk Size: 400 chars
  * Overlap: 50 chars
  * Result Limit: 10
  * Confidence Threshold: Low

---

## Usage Examples

### Example 1: Single CV Upload and Processing

**User:** Uploads `maria_garcia_cv.pdf`

**Agent Response:**

```markdown
📄 **Document Upload Detected**
I've received your CV: "maria_garcia_cv.pdf"

🔄 **Processing Status:** Routing to document processor...
⏳ **Please wait:** Document analysis in progress (10–30 sec)...

✅ **Processing Complete**

**Document Type:** CV  
**Candidate Name:** Maria Garcia  
**Email:** maria.garcia@email.com  
**Position Applied:** Senior Data Scientist  
**Experience:** 7 years  

💾 **Database Status:** Saved successfully  
**Assigned ID:** 15  
**Source File:** maria_garcia_cv.pdf  
**Saved At:** 2025-01-16T14:30:00  

🎯 **Next Steps:**  
- View all candidates: `"Show me all candidates"`  
- Get candidate details: `"Show me candidate 15"`  
- Upload more documents: Ready for next upload  
```

---

### Example 2: Bando di Gara Processing

**User:** Uploads `cloud_migration_tender.pdf`

**Agent Response:**

```markdown
📋 **Bando di Gara Upload Detected**
I've received your tender: "cloud_migration_tender.pdf"

🔄 **Processing Status:** Analyzing project requirements...

✅ **Processing Complete**

**Document Type:** Bando di Gara  
**Client:** Global Manufacturing Corp  
**Project:** Cloud Infrastructure Migration  
**Required Skills:** AWS, Kubernetes, DevOps, Python  
**Experience Required:** 5+ years cloud architecture  
**Location:** Milan (Hybrid)  
**Deadline:** 2025-03-15  

💾 **Database Status:** Saved successfully  
**Assigned ID:** 8  
**Source File:** cloud_migration_tender.pdf  
**Saved At:** 2025-01-16T14:35:00  

🎯 **Next Steps:**  
- View all projects: `"Show me all Bando di Gara"`  
- Find matching candidates: Ready for evaluation  
- Upload more tenders: Ready for next upload  
```

---

### Example 3: Multiple Document Batch Processing

**User:** Uploads `candidate_1.pdf`, `candidate_2.pdf`, `new_project.pdf`

**Agent Response:**

```markdown
📁 **Multiple Documents Detected**
Processing 3 documents:

📄 **Document 1:** candidate_1.pdf  
✅ **CV Processed:** John Smith – Software Engineer – ID: 16

📄 **Document 2:** candidate_2.pdf  
✅ **CV Processed:** Sarah Johnson – DevOps Specialist – ID: 17

📋 **Document 3:** new_project.pdf  
✅ **Bando Processed:** E‑commerce Platform – Client: TechStart Inc – ID: 9

💾 **Summary:**  
- 2 new candidates added  
- 1 new project added  
- All documents processed & saved

🎯 **Suggested Actions:**  
- `"Show me all candidates"`  
- `"Show me all projects"`  
- `"Evaluate candidate 16 for project 9"`
```

---

### Example 4: Error Handling

**User:** Uploads corrupted `damaged_cv.pdf`

**Agent Response:**

```markdown
⚠️ **Processing Issue Detected**
**Document:** damaged_cv.pdf  
**Status:** Unable to extract data

🔍 **Issue Details:** Corrupted or unsupported format

💡 **Suggested Solutions:**  
1. Re‑upload the document  
2. Ensure valid PDF/Word/Excel  
3. Check file size & integrity  
4. Convert to another supported format

🔄 **Ready for Retry:** Upload corrected document now.
```

---

### Example 5: Database Query Operations

**User:** “Show me all candidates in the database”

**Agent Response:**

```markdown
👥 **All Candidates in Database**
**Total:** 17

**Recent Additions:**

**ID: 17** – Sarah Johnson  
- **Email:** sarah.johnson@email.com  
- **Position:** DevOps Specialist  
- **Experience:** 5 years  
- **Source:** candidate_2.pdf  
- **Added:** 2025-01-16T14:40:00

**ID: 16** – John Smith  
- **Email:** john.smith@email.com  
- **Position:** Software Engineer  
- **Experience:** 3 years  
- **Source:** candidate_1.pdf  
- **Added:** 2025-01-16T14:38:00

**ID: 15** – Maria Garcia  
- **Email:** maria.garcia@email.com  
- **Position:** Senior Data Scientist  
- **Experience:** 7 years  
- **Source:** maria_garcia_cv.pdf  
- **Added:** 2025-01-16T14:30:00

[… additional candidates …]

🎯 **Available Actions:**  
- `"Show me candidate [ID]"`  
- `"Show me all projects"`  
- Upload more CVs for processing
```

---

## Starter Prompts

* 📄 **Process CV/Resume**
  *Subtitle:* “Upload a candidate’s CV for processing”
  *Action:* Initiates CV workflow

* 📋 **Process Bando di Gara**
  *Subtitle:* “Upload a project tender document”
  *Action:* Initiates tender workflow

* 👥 **View All Candidates**
  *Subtitle:* “See all processed candidates”

* 🏢 **View All Projects**
  *Subtitle:* “See all Bando di Gara projects”

---

## Response Format Guidelines

### Document Processing Responses

* **Immediate Acknowledgment**
* **Real‑time Status Updates**
* **Completion Summary**
* **Database Confirmation**
* **Next Steps Suggestions**

### Error Responses

* **Clear Problem Description**
* **Actionable Solutions**
* **Retry Instructions**

### Query Responses

* **Structured Data Display**
* **Visual Clarity (emojis, formatting)**
* **Action Suggestions**

---

## Key Features

* **Intelligent Orchestration:** Automatic routing & error recovery
* **Status Tracking:** Real‑time workflow monitoring
* **Database Integration:** Structured storage & unique IDs
* **Professional UX:** Clear communication, emojis, actionable guidance
* **Multi‑Format Support:** PDF, Word, Excel, batch processing

---

## Best Practices

* **File Naming:** Use descriptive, unique filenames
* **Document Quality:** Ensure clarity and readability
* **Batch Uploads:** Group related docs for efficiency
* **Error Resolution:** Follow suggested solutions
* **Database Queries:** Use specific IDs for detailed info
* **Workflow Completion:** Allow processing before new uploads

---

This agent provides a comprehensive solution for recruitment document management, combining intelligent processing with robust database operations and excellent user experience.
