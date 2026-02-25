# Financial Document Analyzer – Debug Challenge Submission

## 📌 Overview

This project is a CrewAI-based financial document analysis system designed to process corporate financial PDFs and generate structured investment insights.

The original codebase contained multiple deterministic bugs, dependency conflicts, architectural issues, and inefficient prompt designs. These have been identified, debugged, refactored, and resolved.

The system is now fully functional and includes SQLite database persistence as a bonus feature.

---

## 🚀 Features

- Upload financial documents (PDF)
- Structured financial analysis
- Revenue & profit detection
- Risk factor identification
- Investment considerations
- SQLite database persistence
- Analysis history endpoint (`/history`)

---

# 🐛 Bugs Identified & Fixed

## 1️⃣ Dependency Conflicts

### Problem:
The original `requirements.txt` contained incompatible pinned versions (`onnxruntime`, `opentelemetry`, etc.) which caused installation failures and dependency resolution errors.

### Fix:
- Simplified dependency list
- Removed conflicting pinned versions
- Aligned versions compatible with CrewAI
- Ensured clean installation using Python 3.10

---

## 2️⃣ CrewAI Import Errors

### Problem:
Outdated imports such as:

```python
from crewai.agents import Agent
```

caused runtime import failures due to API changes in newer CrewAI versions.

### Fix:
Updated to current API usage:

```python
from crewai import Agent
```

---

## 3️⃣ Undefined LLM Initialization

### Problem:
Code contained invalid statement:

```python
llm = llm
```

This resulted in a `NameError`.

### Fix:
- Refactored LLM initialization
- Added support for mock execution mode
- Ensured system runs even without external API billing

---

## 4️⃣ Incorrect Tool Architecture

### Problem:
Tools:
- Did not inherit from `BaseTool`
- Were incorrectly registered
- Used incompatible async structure

This caused Pydantic validation errors and runtime failures.

### Fix:
Refactored tools to properly inherit from `BaseTool` and implemented `_run()` method.

---

## 5️⃣ Task & Endpoint Naming Collision

### Problem:
The task object and FastAPI endpoint shared the same name (`analyze_financial_document`), causing the task reference to be overridden at runtime.

### Fix:
- Renamed task object
- Updated all references
- Eliminated namespace collision

---

## 6️⃣ Hardcoded File Path Bug

### Problem:
The system always attempted to read:

```
data/sample.pdf
```

Instead of processing the uploaded file dynamically.

### Fix:
Implemented dynamic file path handling:

```python
result = run_crew(query=query.strip(), file_path=file_path)
```

---

## 7️⃣ FastAPI Multipart Dependency Missing

### Problem:
File upload failed due to missing dependency:

```
python-multipart
```

### Fix:
Installed required package:

```bash
pip install python-multipart
```

---

## 8️⃣ Inefficient / Unsafe Prompt Design

### Problem:
Original task prompt:
- Encouraged hallucination
- Allowed fabricated URLs
- Suggested unsafe financial advice
- Was non-deterministic

### Fix:
Rewrote task instructions to:
- Use only document content
- Avoid fabrication
- Provide structured output
- Ensure deterministic and reliable responses

---

# ⭐ Bonus Feature: Database Integration

Implemented SQLite database persistence using SQLAlchemy.

### Stored Fields:
- File name
- Query
- Analysis result
- Timestamp

### Database File:
```
analysis.db
```

---

## 📡 Additional Endpoint

### GET `/history`

Returns all past financial analyses stored in the database.

Example response:

```json
[
  {
    "id": 1,
    "file_name": "TSLA-Q2-2025-Update.pdf",
    "query": "Analyze revenue and risk factors",
    "result": "...",
    "created_at": "2026-02-25T15:56:31"
  }
]
```

---

# ⚙️ Setup Instructions

```bash
git clone <your-repo-url>
cd financial-document-analyzer-debug

python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt
uvicorn main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# 📡 API Endpoints

## POST `/analyze`

Upload a financial PDF and provide a query.

Form-data:
- `file` (PDF)
- `query` (string)

Returns structured financial analysis in JSON format.

---

## GET `/history`

Retrieve stored analysis records.

---

# 🔐 LLM Configuration

The system supports OpenAI via environment variable:

```
OPENAI_API_KEY
```

For demo/debug mode, a mock execution path is implemented to allow the system to run without requiring external billing.

To enable real LLM execution:

1. Create a `.env` file
2. Add:

```
OPENAI_API_KEY=your_api_key_here
```

---

# 🏗 Architecture Overview

User  
→ FastAPI  
→ Analysis Layer  
→ PDF Parser  
→ Structured JSON  
→ SQLite Database  

---

# 📌 Conclusion

The system has been fully stabilized, refactored, and enhanced to ensure:

- Deterministic execution
- Clean architecture
- Reliable prompt behavior
- Structured API responses
- Persistent storage

The debugging process addressed both deterministic bugs and inefficient prompt issues, fulfilling all assignment requirements and implementing a bonus feature.
