🛡️ CyberShield AI: Multi-Layer Threat Analysis & Executive Security Report Framework

An end-to-end, open-source architecture for Cybersecurity Intelligence and Artificial Intelligence, designed to analyze threat vectors, evaluate risk severity levels, and generate structured executive security reports automatically.

This framework solves critical challenges in rapid incident triage and vulnerability assessment by combining modern prompt engineering with Google Gemini 2.5 Flash, a responsive web interface, and an automated PDF report engine powered by ReportLab.

🚀 Key Features & Pipeline Architecture

🔍 Intelligent Threat Analysis (threat_analyzer.py):

Ingests raw incident logs, vulnerability descriptions, or attack vectors.

Direct integration with Google Gemini API to classify severity levels (Low, Medium, High, Critical) and provide actionable remediation strategies.

📄 Automated PDF Report Engine (pdf_generator.py):

Converts AI technical diagnostics into executive-ready PDF security reports.

Leverages ReportLab canvas rendering for structured layouts, risk metrics, and mitigation checklists.

📊 Data Collector & Sanitizer (collector.py):

Validates and sanitizes incoming security payloads before LLM ingestion.

Ensures structured JSON data formatting for downstream processing.

🖥️ Web Audit Interface & Dashboard (app.py / static/index.html):

Lightweight Flask backend serving a responsive Tailwind CSS web UI.

Real-time threat submission, interactive diagnostic inspection, and instant PDF report generation & download.

⚙️ How to Run

1. Clone the Repository

git clone https://github.com/Marcos-Paulo-Macedo/cybershield-ai.git
cd cybershield-ai


2. Set Up Virtual Environment

# On Windows
python -m venv venv
venv\Scripts\activate

# On Linux/macOS
python3 -m venv venv
source venv/bin/activate


3. Install Dependencies

pip install -r requirements.txt


4. Configure Environment Variables

Create a .env file in the project root directory:

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash


5. Launch the Application

python app.py


Open your browser and navigate to http://127.0.0.1:5000 to access the CyberShield AI interface.
