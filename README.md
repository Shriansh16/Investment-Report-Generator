# 📈 FinWise AI - Investment Report Generator

FinWise AI is an AI-powered investment research assistant built using [Streamlit](https://streamlit.io/), [CrewAI](https://docs.crewai.com/), and [LangChain](https://www.langchain.com/). It enables users to generate detailed 5-page investment reports by simply entering a financial query — such as comparing multiple companies on valuation, growth, or profitability metrics.

---

## 🚀 Features

- **Natural Language Input**: Users can simply type a query like  
  `Compare Infosys, TCS, and Wipro on growth and valuation metrics`
- **Dynamic Financial Analysis**: Financial analysts are assigned per company using LLM agents.
- **Real-Time Data Integration**: Uses [Serper.dev](https://serper.dev) search tool to pull up-to-date financial data.
- **Structured Report Generation**: Outputs a well-organized, human-readable 5-page report in Markdown format.
- **Agent-Based Task Division**: Follows a multi-agent system design using CrewAI for modular reasoning.

---

## 🧠 Tech Stack

| Component        | Tech Used                      |
|------------------|-------------------------------|
| Frontend         | Streamlit                      |
| LLM Integration  | OpenAI GPT-4o (via LangChain)  |
| Agent Framework  | CrewAI                         |
| Data Retrieval   | Serper.dev Search API          |
| Backend Language | Python                         |

---

## 📄 Sample Output Structure

The report generated is divided into 5 pages:

1. **Executive Summary and Recommendation**
2. **Company Profiles**
3. **Financial Metrics Table and Visual Comparison**
4. **Analysis & Interpretation**
5. **Conclusion and Market Outlook**

---