from database import init_db, SessionLocal, AnalysisRecord
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

from crewai import Crew, Process
from agents import financial_analyst
from task import financial_analysis_task

app = FastAPI(title="Financial Document Analyzer")
init_db()

def run_crew(query: str, file_path: str):
    """
    Mock Crew execution for demo mode (no OpenAI required)
    """

    # Read file manually
    from langchain_community.document_loaders import PyPDFLoader

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    full_text = ""
    for page in docs:
        full_text += page.page_content + "\n"

    # Simple demo analysis logic
    revenue = "Revenue data found" if "revenue" in full_text.lower() else "Revenue not clearly mentioned"
    profit = "Profit data found" if "profit" in full_text.lower() else "Profit not clearly mentioned"
    risk = "Risk factors identified" if "risk" in full_text.lower() else "No explicit risk section found"

    return {
        "Revenue Summary": revenue,
        "Profit/Loss Overview": profit,
        "Key Financial Ratios": "Basic ratio analysis placeholder",
        "Identified Risk Factors": risk,
        "Investment Considerations": "Based on available data, conduct deeper quantitative analysis before investing."
    }


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_financial_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if query=="" or query is None:
            query = "Analyze this financial document for investment insights"
            
        # Process the financial document with all analysts
        response = run_crew(query=query.strip(), file_path=file_path)
        # Save to database
        db = SessionLocal()
        record = AnalysisRecord(
            file_name=file.filename,
            query=query,
            result=str(response)
        )
        db.add(record)
        db.commit()
        db.close()

        return {
            "status": "success",
            "query": query,
            "analysis": response,
            "file_processed": file.filename
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()   # 👈 This prints full error in terminal
        raise HTTPException(status_code=500, detail=str(e))

    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

@app.get("/history")
def get_analysis_history():
    db = SessionLocal()
    records = db.query(AnalysisRecord).all()
    db.close()

    return [
        {
            "id": r.id,
            "file_name": r.file_name,
            "query": r.query,
            "result": r.result,
            "created_at": r.created_at
        }
        for r in records
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)