import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os, re 
import nltk

nltk.download('punkt')

def load_word_list(filepath):
    with open(filepath, "r", encoding="latin-1") as f:  # or encoding="ISO-8859-1"
        return set(w.strip().lower() for w in f if w.strip() and not w.startswith(";"))

    
positive_words = load_word_list("MasterDictionary/positive-words.txt")
negative_words = load_word_list("MasterDictionary/negative-words.txt")
    
stopwords = set()

stopwords_dir = "stopwords"
for fname in os.listdir(stopwords_dir):
    with open(os.path.join(stopwords_dir, fname), "r", encoding="utf-8", errors="ignore") as f:
        stopwords.update(w.strip().lower() for w in f if w.strip())

def syllable_count(word):
    word = word.lower()
    count = len(re.findall(r'[aeiouy]+', word))  # Count vowel groups
    if word.endswith(("es", "ed")):
        count -= 1
    return max(1, count)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def scrape_article(url):
    try:
        html = requests.get(url,timeout=10).text
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find("h1")
        title_text = title.get_text(strip=True)if title else ""
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        article_text= title_text + "\n" + "\n".join(paragraphs)
        return clean_text(article_text)
    except Exception as e:
        print(f"Error scraping article: {e}")
        return ""
    
def analyze_text(text):
    sentences = nltk.sent_tokenize(text)
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    meaningful_words = [w for w in words if w.lower() not in stopwords]
    
    # Positive/Negative score
    pos_score = sum(1 for w in meaningful_words if w.lower() in positive_words)
    neg_score = sum(1 for w in meaningful_words if w.lower() in negative_words)
    
    polarity = (pos_score - neg_score) / ((pos_score + neg_score) + 1e-6)
    subjectivity = (pos_score + neg_score) / (len(meaningful_words) + 1e-6)
    
    avg_sentence_len = len(meaningful_words) / max(1, len(sentences))
    complex_words = [w for w in meaningful_words if syllable_count(w) >= 3]
    perc_complex = len(complex_words) / max(1, len(meaningful_words))
    fog_index = 0.4 * (avg_sentence_len + perc_complex)
    total_words = sum(len(nltk.word_tokenize(s)) for s in sentences)
    avg_words_per_sentence = total_words / max(1, len(sentences))
    
    syll_per_word = sum(syllable_count(w) for w in meaningful_words) / max(1, len(meaningful_words))
    pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, flags=re.I))
    avg_word_len = sum(len(w) for w in meaningful_words) / max(1, len(meaningful_words))
    
    return [
        pos_score, neg_score, polarity, subjectivity,
        avg_sentence_len, perc_complex, fog_index,
        avg_words_per_sentence, len(complex_words), len(meaningful_words),
        syll_per_word, pronouns, avg_word_len
    ]

def main():
    df = pd.read_excel("Input.xlsx")
    os.makedirs("articles", exist_ok=True)
    
    results = []
    
    for idx, row in df.iterrows():
        url_id = row["URL_ID"]
        url = row["URL"]
        
        text = scrape_article(url)
        if text:
            with open(f"articles/{url_id}.txt", "w", encoding="utf-8") as f:
                f.write(text)
            
            metrics = analyze_text(text)
            results.append(list(row) + metrics)
        else:
            results.append(list(row) + [None]*14)
    
    # Create output DataFrame
    col_names = list(df.columns) + [
        "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE", "SUBJECTIVITY SCORE",
        "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS", "FOG INDEX",
        "AVG NUMBER OF WORDS PER SENTENCE", "COMPLEX WORD COUNT", "WORD COUNT",
        "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH"
    ]
    out_df = pd.DataFrame(results, columns=col_names)
    out_df.to_excel("Output.xlsx", index=False)
    print("✅ Output.xlsx generated successfully.")

if __name__ == "__main__":
    main()
