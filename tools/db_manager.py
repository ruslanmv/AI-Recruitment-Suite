import json
import sqlite3
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# Initialize database
def init_db():
    conn = sqlite3.connect('recruitment.db')
    cursor = conn.cursor()
    
    # Create candidates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id TEXT PRIMARY KEY,
            candidate_name TEXT,
            email TEXT,
            phone TEXT,
            location TEXT,
            position_applied TEXT,
            technical_skills TEXT,
            experience_years TEXT,
            education TEXT,
            certifications TEXT,
            previous_companies TEXT,
            consulting_experience TEXT,
            key_achievements TEXT,
            languages TEXT,
            industry_experience TEXT,
            created_at TEXT
        )
    ''')
    
    # Create bando_di_gara table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bando_di_gara (
            id TEXT PRIMARY KEY,
            client_name TEXT,
            project_title TEXT,
            project_description TEXT,
            required_skills TEXT,
            experience_required TEXT,
            education_requirements TEXT,
            certifications_required TEXT,
            project_duration TEXT,
            team_size TEXT,
            location TEXT,
            deadline TEXT,
            budget_range TEXT,
            industry_sector TEXT,
            key_deliverables TEXT,
            created_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on import
init_db()

@tool
def save_candidate_data(extracted_data: str) -> str:
    """
    Save candidate CV data to database with unique ID
    
    :param extracted_data: JSON string containing extracted CV information
    :returns: Success message with candidate ID
    """
    try:
        data = json.loads(extracted_data)
        
        if data.get('document_type') != 'CV':
            return "Error: This is not CV data"
        
        # Generate unique candidate ID
        candidate_id = f"CAND_{uuid.uuid4().hex[:8].upper()}"
        
        conn = sqlite3.connect('recruitment.db')
        cursor = conn.cursor()
        
        # Extract contact info
        contact_info = data.get('contact_info', {})
        
        cursor.execute('''
            INSERT INTO candidates (
                id, candidate_name, email, phone, location, position_applied,
                technical_skills, experience_years, education, certifications,
                previous_companies, consulting_experience, key_achievements,
                languages, industry_experience, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            candidate_id,
            data.get('candidate_name', ''),
            contact_info.get('email', ''),
            contact_info.get('phone', ''),
            contact_info.get('location', ''),
            data.get('position_applied', ''),
            json.dumps(data.get('technical_skills', [])),
            data.get('experience_years', ''),
            data.get('education', ''),
            json.dumps(data.get('certifications', [])),
            json.dumps(data.get('previous_companies', [])),
            data.get('consulting_experience', ''),
            json.dumps(data.get('key_achievements', [])),
            json.dumps(data.get('languages', [])),
            json.dumps(data.get('industry_experience', [])),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return f"✅ Candidate saved successfully with ID: {candidate_id}"
        
    except Exception as e:
        return f"❌ Error saving candidate: {str(e)}"

@tool
def save_bando_data(extracted_data: str) -> str:
    """
    Save Bando di Gara data to database with unique ID
    
    :param extracted_data: JSON string containing extracted Bando di Gara information
    :returns: Success message with bando ID
    """
    try:
        data = json.loads(extracted_data)
        
        if data.get('document_type') != 'Bando di Gara':
            return "Error: This is not Bando di Gara data"
        
        # Generate unique bando ID
        bando_id = f"BANDO_{uuid.uuid4().hex[:8].upper()}"
        
        conn = sqlite3.connect('recruitment.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bando_di_gara (
                id, client_name, project_title, project_description, required_skills,
                experience_required, education_requirements, certifications_required,
                project_duration, team_size, location, deadline, budget_range,
                industry_sector, key_deliverables, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            bando_id,
            data.get('client_name', ''),
            data.get('project_title', ''),
            data.get('project_description', ''),
            json.dumps(data.get('required_skills', [])),
            data.get('experience_required', ''),
            json.dumps(data.get('education_requirements', [])),
            json.dumps(data.get('certifications_required', [])),
            data.get('project_duration', ''),
            data.get('team_size', ''),
            data.get('location', ''),
            data.get('deadline', ''),
            data.get('budget_range', ''),
            data.get('industry_sector', ''),
            json.dumps(data.get('key_deliverables', [])),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return f"✅ Bando di Gara saved successfully with ID: {bando_id}"
        
    except Exception as e:
        return f"❌ Error saving bando: {str(e)}"

