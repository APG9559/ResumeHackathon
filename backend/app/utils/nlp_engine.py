import re
from collections import Counter
import math

# Common English stop words
STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
    'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with',
    'the', 'this', 'but', 'they', 'have', 'had', 'what', 'when', 'where', 'who',
    'which', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now'
}

def preprocess_text(text):
    """Preprocess text: lowercase, remove special characters, tokenize"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text):
    """Tokenize text and remove stop words"""
    words = preprocess_text(text).split()
    return [w for w in words if w not in STOP_WORDS and len(w) > 2]

def calculate_tf(tokens):
    """Calculate term frequency"""
    tf_dict = {}
    total_tokens = len(tokens)
    token_counts = Counter(tokens)
    
    for token, count in token_counts.items():
        tf_dict[token] = count / total_tokens
    
    return tf_dict

def calculate_idf(documents):
    """Calculate inverse document frequency"""
    idf_dict = {}
    total_docs = len(documents)
    
    all_tokens = set()
    for doc in documents:
        all_tokens.update(set(doc))
    
    for token in all_tokens:
        doc_count = sum(1 for doc in documents if token in doc)
        idf_dict[token] = math.log(total_docs / (1 + doc_count))
    
    return idf_dict

def calculate_tfidf(tokens, idf_dict):
    """Calculate TF-IDF scores"""
    tf_dict = calculate_tf(tokens)
    tfidf_dict = {}
    
    for token, tf_value in tf_dict.items():
        tfidf_dict[token] = tf_value * idf_dict.get(token, 0)
    
    return tfidf_dict

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    all_tokens = set(vec1.keys()).union(set(vec2.keys()))
    
    dot_product = sum(vec1.get(token, 0) * vec2.get(token, 0) for token in all_tokens)
    
    magnitude1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
    magnitude2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

def calculate_fit_score(resume_text, job_text):
    """
    Calculate fit score between resume and job description using simple TF-IDF.
    Returns a score between 0 and 100.
    """
    if not resume_text or not job_text:
        return 0.0
    
    try:
        resume_tokens = tokenize(resume_text)
        job_tokens = tokenize(job_text)
        
        if not resume_tokens or not job_tokens:
            return 0.0
        
        documents = [job_tokens, resume_tokens]
        idf_dict = calculate_idf(documents)
        
        job_tfidf = calculate_tfidf(job_tokens, idf_dict)
        resume_tfidf = calculate_tfidf(resume_tokens, idf_dict)
        
        similarity = cosine_similarity(job_tfidf, resume_tfidf)
        
        fit_score = similarity * 100
        return round(fit_score, 2)
    except Exception as e:
        print(f"Error calculating fit score: {str(e)}")
        return 0.0

def extract_matching_keywords(resume_text, job_text, top_n=10):
    """
    Extract matching keywords between resume and job description.
    Returns a list of top matching keywords.
    """
    if not resume_text or not job_text:
        return []
    
    try:
        resume_tokens = set(tokenize(resume_text))
        job_tokens = tokenize(job_text)
        
        matching_tokens = resume_tokens.intersection(set(job_tokens))
        
        job_token_counts = Counter(job_tokens)
        
        scored_matches = []
        for token in matching_tokens:
            score = job_token_counts.get(token, 0)
            scored_matches.append((token, score))
        
        scored_matches.sort(key=lambda x: x[1], reverse=True)
        
        top_keywords = [kw for kw, score in scored_matches[:top_n]]
        
        return top_keywords
    except Exception as e:
        print(f"Error extracting keywords: {str(e)}")
        return []
