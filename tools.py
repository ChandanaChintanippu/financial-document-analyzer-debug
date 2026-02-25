import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import BaseTool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader


# 🔎 Search Tool (External)
search_tool = SerperDevTool()


# 📄 Financial Document Reader Tool
class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = "Reads and extracts text from a financial PDF document."

    def _run(self, path: str) -> str:

        """The document path is provided as {path}"""

        loader = PyPDFLoader(path)
        docs = loader.load()

        full_report = ""

        for page in docs:
            content = page.page_content

            # Clean formatting
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")

            full_report += content + "\n"

        return full_report


# 📈 Investment Analysis Tool
class InvestmentTool(BaseTool):
    name: str = "Investment Analyzer"
    description: str = "Analyzes financial document data and provides investment insights."

    def _run(self, financial_document_data: str) -> str:
        # Placeholder logic
        cleaned_data = financial_document_data.replace("  ", " ")
        return "Investment analysis completed based on provided financial data."


# ⚠️ Risk Assessment Tool
class RiskTool(BaseTool):
    name: str = "Risk Assessment Tool"
    description: str = "Evaluates financial risks from document data."

    def _run(self, financial_document_data: str) -> str:
        return "Risk assessment completed based on provided financial data."
