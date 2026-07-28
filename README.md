CyberShield AI: Vendor Due Diligence Engine

A high-performance, intelligent automation framework for vendor risk assessment and compliance. CyberShield AI leverages the power of Generative AI to process non-structured data and provide actionable executive insights for supply chain and financial risk management.

🚀 Overview

CyberShield AI automates the Vendor Due Diligence process, traditionally a time-consuming manual task. By integrating public data sources with the Gemini API, the engine performs automated risk profiling of potential suppliers and generates structured, professional executive PDF reports.

Built with a modular architecture, this project demonstrates advanced skills in RPA governance, API orchestration, and LLM implementation.

🏗️ Architecture

Collector Module: Aggregates data from public APIs and professional search engines.

Threat Analyzer: Utilizes Gemini LLM to process non-structured data, analyze compliance risks (Financial, Regulatory, Reputational), and calculate a definitive Risk Score.

Reporter Engine: Generates high-quality, professional executive PDF summaries using ReportLab.

🛠️ Tech Stack

Language: Python 3.11+

AI/LLM: Google GenAI (Gemini API)

Automation: Web Scraping, API Integration

Report Generation: ReportLab

Infrastructure: PostgreSQL (Telemetry Governance ready)

⚙️ Configuration & Setup

1. Prerequisites

Ensure you have Python 3.11+ installed. Clone the repository and set up your virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt


2. Environment Variables

To run the engine, you need to provide your Gemini API Key and Model. Create a .env file in the root directory:

GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=model-gemini


Note: Never commit your .env file to version control. The repository includes a .gitignore to prevent this.

📈 Key Engineering Highlights

Structured Output: Leverages LLM prompting to extract deterministic data for reliable reporting.

Scalability: Modular design allows for the addition of new data collectors or alternative LLM models.

Professional Output: Automates executive-level PDF generation, ready for direct stakeholder presentation.

Developed by Marcos Paulo Macedo | Intelligent Automation Lead & RPA Architect
