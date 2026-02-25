## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()


from crewai import Agent

from tools import search_tool, FinancialDocumentTool

### Loading LLM
llm = None

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Accurately analyze financial documents and extract meaningful insights based only on the provided data: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced financial analyst with strong expertise in financial statements, "
        "market trends, and risk evaluation. You carefully read and interpret financial documents "
        "without making assumptions. You provide fact-based insights and avoid speculation. "
        "You ensure that all analysis is grounded in the actual data provided."
    ),
    tools=[FinancialDocumentTool()],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)


# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify whether the uploaded document is a valid financial document before analysis.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a compliance-focused financial document verifier. "
        "You carefully inspect uploaded documents and confirm whether they "
        "contain structured financial information such as balance sheets, "
        "income statements, or financial reports."
    ),
    llm=llm,
    max_iter=2,
    allow_delegation=False
)



investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide responsible and realistic investment suggestions based on verified financial data.",
    verbose=True,
    backstory=(
        "You are a certified investment advisor with deep market knowledge. "
        "You only recommend investment strategies that align with the financial "
        "data provided. You avoid speculation and ensure regulatory compliance."
    ),
    llm=llm,
    max_iter=2,
    allow_delegation=False
)


risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Identify and evaluate financial risks based strictly on the provided financial data.",
    verbose=True,
    backstory=(
        "You are a professional risk analyst who evaluates financial documents "
        "to identify operational, liquidity, credit, and market risks. "
        "Your assessments are data-driven and objective."
    ),
    llm=llm,
    max_iter=2,
    allow_delegation=False
)
