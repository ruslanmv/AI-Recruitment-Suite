**Document Processor Agent Documentation**

---

## Overview

The **Document Processor Agent** is an intelligent document extraction system designed for IBM Consulting recruitment. It automatically analyzes uploaded documents (CVs, Bando di Gara, Excel files, PDFs) and extracts structured information in standardized JSON schemas that can be used by other agents and database systems.

---

## Agent Specifications

* **Name:** `processor`
* **Display Name:** Document Processor
* **LLM:** `watsonx/meta-llama/llama-3-2-90b-vision-instruct`
* **Style:** Planner
* **Primary Function:** Automatic document information extraction

---

## Core Workflow

The agent follows an automatic 5‑step document processing workflow:

1. **Document Upload Detection**

   * Automatically detects when documents are uploaded
   * Acknowledges each document by filename
   * Supports multiple file formats (PDF, Excel, Word, etc.)

2. **Document Processing Wait**

   * Waits for document processing to complete (10–30 seconds)
   * Handles processing delays gracefully
   * Provides status updates to users

3. **Document Type Detection**

   * Automatically analyzes document content to determine type
   * **CV/Resume** indicators: “curriculum”, “resume”, “CV”, personal information, work experience, education
   * **Bando di Gara** indicators: “bando”, “gara”, “tender”, “appalto”, project requirements, client information
   * **Excel files:** Analyzes content to determine data type

4. **Schema‑Based Information Extraction**

   * Extracts information according to appropriate schema
   * Maintains data accuracy and completeness
   * Uses `"Not specified"` for missing information

5. **Structured JSON Output**

   * Returns clean JSON structure following standardized schema
   * Includes metadata (extraction status, data quality notes)
   * Always references source filename

---

## Document Processing Rules

* **Individual Processing**

  * Each document is processed individually and separately
  * Never merges information from multiple documents
  * Each document produces its own extraction result
  * Always specifies source filename in response

* **Supported Document Types**

  1. **CV/Resume Documents**: Extract personal details, skills, experience, qualifications
  2. **Bando di Gara Documents**: Extract project tender information (requirements, client details, specifications)
  3. **Excel Files (.xlsx)**: Analyze content to determine if it contains CV data, project data, or other structured information
  4. **PDF Files**: Process based on automatic document type detection

---

## Extraction Schemas

### CV Document Schema

```json
{
  "document_type": "CV",
  "source_filename": "<exact filename>",
  "candidate_name": "<Full name>",
  "contact_info": {
    "email": "<email>",
    "phone": "<phone>",
    "location": "<city, country>"
  },
  "position_applied": "<Position>",
  "technical_skills": ["<skill1>", "<skill2>", "..."],
  "experience_years": "<Total years>",
  "education": "<Degrees, universities, years>",
  "certifications": ["<cert1>", "<cert2>", "..."],
  "previous_companies": ["<Company1>", "<Company2>", "..."],
  "consulting_experience": "<Consulting/project experience>",
  "key_achievements": ["<Achievement1>", "<Achievement2>", "..."],
  "languages": ["<Language (proficiency)>", "..."],
  "industry_experience": ["<Sector1>", "<Sector2>", "..."]
}
```

### Bando di Gara Document Schema

```json
{
  "document_type": "Bando di Gara",
  "source_filename": "<exact filename>",
  "client_name": "<Client organization>",
  "project_title": "<Project/tender title>",
  "project_description": "<Brief description>",
  "required_skills": ["<skill1>", "<skill2>", "..."],
  "experience_required": "<Minimum years>",
  "education_requirements": "<Educational background>",
  "certifications_required": ["<cert1>", "<cert2>", "..."],
  "project_duration": "<Timeline>",
  "team_size": "<Number of members>",
  "location": "<Location or remote>",
  "deadline": "<YYYY‑MM‑DD>",
  "budget_range": "<Budget if mentioned>",
  "industry_sector": "<Industry sector>",
  "key_deliverables": ["<Deliverable1>", "<Deliverable2>", "..."]
}
```

---

## Usage Examples

### Example 1: Single CV Processing

**User:** Uploads `john_doe_cv.pdf`
**Agent Response:**

````markdown
Processing document: john_doe_cv.pdf

```json
{
  "document_type": "CV",
  "source_filename": "john_doe_cv.pdf",
  "extraction_status": "Successful",
  "data_quality_notes": "Complete CV with all major sections identified",
  "candidate_name": "John Doe",
  "contact_info": {
    "email": "john.doe@email.com",
    "phone": "+1-555-0123",
    "location": "New York, USA"
  },
  "position_applied": "Senior Software Engineer",
  "technical_skills": ["Java", "Python", "AWS", "Docker", "Kubernetes"],
  "experience_years": "8 years",
  "education": "BS Computer Science, MIT, 2015",
  "certifications": ["AWS Solutions Architect", "Certified Kubernetes Administrator"],
  "previous_companies": ["Google", "Microsoft", "Startup Inc"],
  "consulting_experience": "3 years client-facing development at consulting firm",
  "key_achievements": ["Led team of 5 developers", "Reduced system latency by 40%"],
  "languages": ["English (Native)", "Spanish (Conversational)"],
  "industry_experience": ["Technology", "Finance", "Healthcare"]
}
````

---

### Example 2: Bando di Gara Processing

**User:** Uploads `banking_modernization_tender.pdf`
**Agent Response:**

````markdown
Processing document: banking_modernization_tender.pdf

```json
{
  "document_type": "Bando di Gara",
  "source_filename": "banking_modernization_tender.pdf",
  "extraction_status": "Successful",
  "data_quality_notes": "Complete tender document with detailed requirements",
  "client_name": "First National Bank",
  "project_title": "Core Banking System Modernization",
  "project_description": "Migration from legacy mainframe to cloud-native architecture",
  "required_skills": ["Java", "Spring Boot", "Microservices", "AWS", "Banking Domain"],
  "experience_required": "5+ years in banking systems",
  "education_requirements": "Bachelor's degree in Computer Science or related field",
  "certifications_required": ["AWS Solutions Architect", "PMP"],
  "project_duration": "18 months",
  "team_size": "12 developers",
  "location": "New York (Hybrid)",
  "deadline": "2025-02-15",
  "budget_range": "$2.5M - $3.2M",
  "industry_sector": "Financial Services",
  "key_deliverables": ["System Architecture", "Migration Plan", "Testing Framework"]
}
````

---

### Example 3: Multiple Document Processing

**User:** Uploads `candidate_a.pdf`, `candidate_b.pdf`, `project_tender.pdf`
**Agent Response:**

````markdown
Processing document: candidate_a.pdf

```json
{
  "document_type": "CV",
  "source_filename": "candidate_a.pdf",
  "extraction_status": "Successful",
  "candidate_name": "Alice Smith",
  "contact_info": {
    "email": "alice.smith@email.com",
    "phone": "+1-555-0456",
    "location": "San Francisco, USA"
  },
  "technical_skills": ["React", "Node.js", "MongoDB", "GraphQL"],
  "experience_years": "6 years"
  // ... additional fields
}
````

````markdown
Processing document: candidate_b.pdf

```json
{
  "document_type": "CV",
  "source_filename": "candidate_b.pdf",
  "extraction_status": "Successful",
  "candidate_name": "Bob Johnson",
  "contact_info": {
    "email": "bob.johnson@email.com",
    "phone": "+1-555-0789",
    "location": "Chicago, USA"
  },
  "technical_skills": ["Python", "Django", "PostgreSQL", "Redis"],
  "experience_years": "4 years"
  // ... additional fields
}
````

````markdown
Processing document: project_tender.pdf

```json
{
  "document_type": "Bando di Gara",
  "source_filename": "project_tender.pdf",
  "extraction_status": "Successful",
  "client_name": "Tech Corp",
  "project_title": "E-commerce Platform Development"
  // ... additional fields
}
````

---

### Example 4: Partial Extraction

**User:** Uploads `incomplete_cv.pdf`
**Agent Response:**

````markdown
Processing document: incomplete_cv.pdf

```json
{
  "document_type": "CV",
  "source_filename": "incomplete_cv.pdf",
  "extraction_status": "Partial",
  "data_quality_notes": "Missing contact information and education details",
  "candidate_name": "Jane Wilson",
  "contact_info": {
    "email": "Not specified",
    "phone": "Not specified",
    "location": "Boston, USA"
  },
  "technical_skills": ["JavaScript", "React", "CSS"],
  "experience_years": "Not specified",
  "education": "Not found in document",
  "certifications": [],
  "previous_companies": ["WebDev Co"],
  "consulting_experience": "Not specified",
  "key_achievements": ["Built responsive web applications"],
  "languages": ["English"],
  "industry_experience": ["Technology"]
}
````

---

## Response Format

* **Always** start with `Processing document: [filename]`
* Return clean JSON following the appropriate schema
* Include required metadata fields:

  * `document_type`: `"CV"`, `"Bando di Gara"`, or `"Unknown"`
  * `source_filename`: Exact filename processed
  * `extraction_status`: `"Successful"`, `"Partial"`, or `"Failed"`
  * `data_quality_notes`: Context about extraction

### Extraction Status Values

* **Successful:** Complete extraction with all major fields populated
* **Partial:** Some information extracted, but missing key details
* **Failed:** Unable to extract meaningful information

---

## Key Features

* **Automatic Processing:** No manual intervention; immediate processing upon upload
* **Intelligent Type Detection:** Auto‑detect CVs, tenders, spreadsheets, etc.
* **Individual Handling:** Each document processed separately; no data merging
* **Structured Output:** Standardized JSON schemas ready for integration
* **Quality Assurance:** Extraction status tracking and data quality notes
* **Multi‑Format Support:** PDFs, Excel, Word, images

---

## Chat with Documents Feature

* **Citations:** Up to 3 relevant document sources with clear titles and links
* **Generation Settings:** Verbose responses, delay messages, connectivity handling
* **Vector Index Config:** 400‑character chunks, 50‑character overlap, low confidence thresholds

---

## Best Practices

* **Upload Quality:** Ensure clear, readable documents
* **File Naming:** Use descriptive filenames
* **Processing Time:** Allow 10–30 seconds per document
* **Batch Uploads:** Group related documents for batch processing
* **Verification:** Review extraction results for accuracy
* **Integration:** Feed structured output directly into database tools

---

This agent provides a robust foundation for automated document processing in recruitment workflows, ensuring consistent, accurate, and structured data extraction across document types.
