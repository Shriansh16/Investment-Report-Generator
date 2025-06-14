import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
from datetime import datetime
import os

# Load environment variables
llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
os.environ['SERPER_API_KEY'] = SERPER_API_KEY

st.title("FinWise AI - Investment Report Generator")

with st.form("report_form"):
    user_query = st.text_area("Enter your investment query",
                              placeholder="e.g., Compare Infosys, TCS, and Wipro on growth and valuation metrics")
    submit = st.form_submit_button("Generate Report")

if submit and user_query.strip():
    with st.spinner("Generating Investment Report..."):

        # Get current date
        today = datetime.today().strftime('%B %d, %Y')

        executive_agent = Agent(
            role="Investment Strategist",
            goal="Generate comprehensive investment reports and strategic recommendations",
            backstory="You are a seasoned investment strategist who oversees report generation and final recommendations.",
            verbose=True,
            llm=llm,
            allow_delegation=True
        )

        # Extract company names
        try:
            company_names = [name.strip() for name in user_query.split("Compare")[1].split("on")[0].split(",")]
        except:
            st.error("Please follow the format: 'Compare Company1, Company2 on metric1, metric2'")
            st.stop()

        analyst_agents = []
        analyst_tasks = []

        for company in company_names:
            analyst = Agent(
                role=f"{company} Financial Analyst",
                goal=f"Analyze {company}'s financial performance and extract insights",
                backstory=f"You are an expert financial analyst assigned to deeply evaluate {company}'s key metrics and risks. You have access to real-time data using a search tool.",
                verbose=True,
                llm=llm,
                tools=[SerperDevTool()],
                allow_delegation=False
            )
            task = Task(
                description=f"""As of {today}, perform a detailed financial analysis of {company}.
Focus on:
- Valuation: PE ratio, EPS
- Profitability: ROE
- Solvency: Debt-to-Equity
- Growth: CAGR
Use the search tool to retrieve recent financial data, trends, and news headlines.
Identify key performance trends, risks, and any red flags from recent reports or news.""",
                agent=analyst,
                expected_output=f"A comprehensive summary of {company}'s financial health and strategic outlook."
            )
            analyst_agents.append(analyst)
            analyst_tasks.append(task)

        report_writer = Agent(
            role="Investment Report Writer",
            goal="Synthesize analysis into a structured, human-readable investment report with visualizations",
            backstory="You are an expert financial writer who creates professional reports with clear insights and compelling visuals.",
            verbose=True,
            llm=llm,
            allow_delegation=False
        )

        write_report_task = Task(
            description=f"""Based on the company analyses from {today}, write a structured 5-page investment report in Markdown format.
Divide it as follows:

**Page 1: Executive Summary and Recommendation**  
Summarize key findings and give a clear investment recommendation (buy/hold/sell).

**Page 2: Company Profiles**  
Brief company overviews (industry, business model, history).

**Page 3: Financial Metrics Table and Visual Comparison**  
Markdown table comparing metrics: PE ratio, EPS, ROE, Debt-to-Equity, CAGR.  
Include descriptions of 2-3 visuals (bar charts, trend lines) if charts can't be rendered.

**Page 4: Analysis & Interpretation**  
Interpret key financial signals, market trends, risks, and competitive advantages.

**Page 5: Conclusion and Market Outlook**  
Summarize long-term prospects and current market conditions.""",
            agent=report_writer,
            expected_output="A 5-page Markdown investment report with insights, comparisons, and recommendations.",
            context=analyst_tasks
        )

        # Create and run the Crew
        crew = Crew(
            agents=[executive_agent] + analyst_agents + [report_writer],
            tasks=analyst_tasks + [write_report_task],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        st.markdown(result, unsafe_allow_html=True)
