# MarketPulse 📊

MarketPulse is a Streamlit dashboard for analyzing customer reviews and comparing sentiment across competing companies.

The project processes Arabic, English, or mixed-language reviews and shows rating trends, sentiment breakdowns, and recurring customer themes. It can work offline using rating-based sentiment and keyword frequency, with an optional AI layer for deeper topic extraction using the Anthropic Claude API.

## Live Demo

The app is deployed on Streamlit Cloud:

https://marketpulse-sarabaj.streamlit.app

## Overview

Customer reviews can contain useful signals about product quality, user experience, pricing, support, and common customer pain points. MarketPulse helps organize these reviews into a simple dashboard that makes patterns easier to identify and compare.

The sample dataset includes synthetic reviews for three fintech competitors. Users can also upload their own CSV file through the sidebar.

## Features

- Upload and analyze customer review CSV files
- Support Arabic, English, and mixed-language reviews
- Calculate sentiment from star ratings
- Compare average rating by company
- Show sentiment breakdown by competitor
- Track rating trends over time
- Extract recurring review themes using AI when an API key is available
- Use offline keyword analysis when no API key is configured

## Tech Stack

| Layer | Technologies |
|---|---|
| Dashboard | Streamlit |
| Data Analysis | Python, pandas |
| Visualization | Plotly |
| AI Topic Extraction | Anthropic Claude API |
| Dataset | Synthetic CSV review data |
| Deployment | Streamlit Cloud |

## Project Structure

```text
MarketPulse/
├── app.py              # Streamlit dashboard
├── analysis.py         # Sentiment logic and topic extraction
├── generate_data.py    # Generates sample review data
├── data/
│   └── reviews.csv     # Sample dataset
├── requirements.txt
├── .gitignore
└── README.md
```

## Dataset Format

To upload your own file, the CSV should include these columns:

| Column | Description |
|---|---|
| `company` | Company or competitor name |
| `review_text` | Customer review text |
| `rating` | Numeric rating from 1 to 5 |
| `date` | Review date |

## How to Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate sample data

```bash
python generate_data.py
```

### 3. Optional: enable AI topic extraction

Set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY=your-key-here
```

For Windows PowerShell:

```powershell
$env:ANTHROPIC_API_KEY="your-key-here"
```

### 4. Run the dashboard

```bash
streamlit run app.py
```

The app will open locally, usually at:

```text
http://localhost:8501
```

## Deployment

This project is deployed using Streamlit Cloud.  
The deployment connects directly to the GitHub repository and runs the main Streamlit file:

```text
app.py
```

## Notes

The project works without an API key by using rating-based sentiment and keyword frequency analysis. The AI feature is optional and only used for extracting deeper recurring themes from review text.

No API keys are included in this repository.

## Future Improvements

- Add real review scraping from app stores or public review sources
- Add filters by date range and rating range
- Track recurring themes over time
- Export dashboard summaries as PDF or CSV
- Add comparison reports for selected competitors
- Improve bilingual theme extraction for Arabic and English reviews

## Purpose

This project was built to practice customer review analytics, sentiment analysis, bilingual text processing, dashboard development, cloud deployment, and AI-assisted market insight extraction.
