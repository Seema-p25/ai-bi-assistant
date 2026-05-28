# 📊 AI-Powered Business Intelligence Assistant

A live, end-to-end AI application that lets anyone upload a CSV dataset and instantly 
explore it using plain English questions, automatic charts, and data summaries — 
no SQL or coding knowledge required.

🔗 **Live App:** https://seema-p25-ai-bi-assistant-app-frrsql.streamlit.app/

---

## Features

- **AI Question Answering** — Ask questions about your data in plain English and get instant answers
- **Auto Chart Generator** — Select columns and chart type to visualise data instantly
- **AI Chart Suggestion** — Describe what you want to see and the AI builds the chart automatically
- **Automatic Data Summary** — Instant statistics, data types, and null value analysis on any uploaded dataset

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web interface |
| LangChain | AI agent framework |
| Groq LLM (Llama 3.3) | Natural language understanding |
| Pandas | Data processing |
| Plotly | Interactive charts |
| python-dotenv | Environment variable management |

---

## How to Run Locally

**1. Clone the repository**
```
git clone https://github.com/PariseneniSaiTeja/ai-bi-assistant.git
cd ai-bi-assistant/bi-assistant
```

**2. Install dependencies**
```
pip install -r requirements.txt
```

**3. Create a `.env` file in the `bi-assistant` folder**
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free Groq API key at https://console.groq.com

**4. Run the app**
```
streamlit run app.py
```

---

## Usage

1. Upload any CSV file using the Upload button
2. Ask questions in plain English — e.g. *"What is the average revenue?"*
3. Use the Auto Chart Generator to visualise your data
4. Describe a chart in plain English and let the AI build it
5. View automatic statistics and data summary below

---

## Project Structure

```
bi-assistant/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── .gitignore          # Excludes .env and data files
└── data/               # Local data folder (not pushed to GitHub)
```

---



