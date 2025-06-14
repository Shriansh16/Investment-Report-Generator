import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from datetime import datetime
import os

# Load environment variables
llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

st.title("FinWise AI - Investment Report Generator")

with st.form("report_form"):
    user_query = st.text_area("Enter your investment query",
                              placeholder="e.g., Compare Infosys, TCS, and Wipro on growth and valuation metrics")
    submit = st.form_submit_button("Generate Report")

if submit and user_query.strip():
    with st.spinner("Generating Investment Report..."):

        
        executive_agent = Agent(
            role="Investment Strategist",
            goal="Generate comprehensive investment reports and strategic recommendations",
            backstory="You are a seasoned investment strategist who oversees report generation and final recommendations.",
            verbose=True,
            llm=llm,
            allow_delegation=True
        )

        # Extract company names (assumes query format like: Compare X, Y, Z on metrics)
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
                backstory=f"You are an expert financial analyst assigned to deeply evaluate {company}'s key metrics and risks.",
                verbose=True,
                llm=llm,
                allow_delegation=False
            )
            task = Task(
                description=f"""Perform a detailed financial analysis for {company}.
                Focus on:
                - Valuation: PE ratio, EPS
                - Profitability: ROE
                - Solvency: Debt-to-Equity
                - Growth: CAGR
                Identify major trends, risks, and red flags.""",
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
            description=f"""Using all company analyses, write a structured 5-page investment report in Markdown format.
Divide it as follows:
---
**Page 1: Executive Summary and Recommendation**  
Summarize the key findings and give a clear investment recommendation (buy/hold/sell).

**Page 2: Company Profiles**  
Write brief profiles (industry, business model, history) of each company.

**Page 3: Financial Metrics Table and Visual Comparison**  
Create a Markdown table comparing financial metrics (PE ratio, EPS, ROE, Debt-to-Equity, CAGR).  
Include descriptions of 2-3 visuals (e.g., bar charts, trend lines) even if you can’t embed them.

**Page 4: Analysis & Interpretation**  
Interpret what the numbers mean for investors. Discuss risks, trends, and competitive positioning.

**Page 5: Conclusion and Market Outlook**  
Summarize the long-term outlook for each company and overall industry trends.
""",
            agent=report_writer,
            expected_output="A well-structured Markdown investment report with sections, visualizations, and recommendations.",
            context=analyst_tasks
        )

        # Create Crew
        crew = Crew(
            agents=[executive_agent] + analyst_agents + [report_writer],
            tasks=analyst_tasks + [write_report_task],
            verbose=True,
            process=Process.sequential
        )

        # Execute
        result = crew.kickoff()
        st.markdown(result, unsafe_allow_html=True)

