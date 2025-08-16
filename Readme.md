
# NLP Text Classification & Web Scraping Project

## Overview
This project automates web scraping, text preprocessing, and linguistic analysis for a set of articles. It combines Natural Language Processing (NLP) techniques and readability metrics to generate structured insights in an Excel report.

### Key Features
- Automated scraping of article content from URLs
- Text cleaning and tokenization
- Sentiment analysis (positive, negative, polarity, subjectivity)
- Readability metrics (average sentence length, fog index, percentage of complex words)
- Lexical and grammatical features (word count, syllable per word, personal pronouns, average word length)
- Outputs a comprehensive report in `Output.xlsx`

---

## Getting Started

### 1. Install Dependencies
Open a terminal in the project directory and run:
```bash
pip install pandas requests beautifulsoup4 nltk openpyxl
```

### 2. Prepare Input Files
- Place `Input.xlsx` in the same folder as `main.py`.
- Ensure the folders `MasterDictionary/` and `StopWords/` are present in the project directory.

### 3. Run the Script
```bash
python main.py
```

### 4. Output
- Scraped articles are saved in the `articles/` folder.
- Final processed report is generated as `Output.xlsx`.

---

## Dependencies
- **pandas**: Data manipulation
- **requests**: HTTP requests
- **beautifulsoup4**: HTML parsing & scraping
- **nltk**: Text preprocessing, tokenization, sentiment resources
- **openpyxl**: Excel report generation

## Deliverables
- Scraped articles (raw text)
- Processed metrics (sentiment + readability)
- Final report (`Output.xlsx`)

## Highlights
- End-to-end NLP pipeline: scraping → preprocessing → analysis → reporting
- Uses lexical dictionaries for sentiment classification
- Implements Fog Index and other linguistic complexity metrics
- Provides actionable insights for large-scale textual datasets
