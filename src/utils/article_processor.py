import os
from docx import Document
from typing import List, Dict
import re


class ArticleProcessor:
    
    def __init__(self, articles_dir: str = "Articles"):
        self.articles_dir = articles_dir
        
    def read_docx(self, filepath: str) -> str:
        try:
            doc = Document(filepath)
            full_text = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    full_text.append(paragraph.text.strip())
            
            return "\n".join(full_text)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?;:\-()]', '', text)
        return text.strip()
    
    def extract_key_sentences(self, text: str, num_sentences: int = 5) -> List[str]:
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 50]
        
        descriptive_words = ['describe', 'show', 'depict', 'illustrate', 'feature', 
                            'image', 'picture', 'scene', 'view', 'landscape']
        
        scored_sentences = []
        for i, sent in enumerate(sentences):
            score = 0
            if i < 3:
                score += 2
            if any(word in sent.lower() for word in descriptive_words):
                score += 3
            if len(sent) > 100:
                score += 1
            
            scored_sentences.append((score, sent))
        
        scored_sentences.sort(reverse=True, key=lambda x: x[0])
        return [sent for _, sent in scored_sentences[:num_sentences]]
    
    def extract_concepts(self, text: str, max_concepts: int = 3) -> List[str]:
        key_sentences = self.extract_key_sentences(text, num_sentences=max_concepts)
        
        concepts = []
        for sentence in key_sentences:
            concept = sentence[:150] if len(sentence) > 150 else sentence
            concepts.append(concept)
        
        return concepts
    
    def get_all_articles(self) -> List[str]:
        if not os.path.exists(self.articles_dir):
            print(f"Articles directory '{self.articles_dir}' not found")
            return []
        
        articles = []
        for filename in os.listdir(self.articles_dir):
            if filename.endswith('.docx') and not filename.startswith('~'):
                articles.append(os.path.join(self.articles_dir, filename))
        
        return sorted(articles)
    
    def process_article(self, filepath: str, max_concepts: int = 3) -> Dict:
        filename = os.path.basename(filepath)
        text = self.read_docx(filepath)
        
        if not text:
            return {
                "filename": filename,
                "filepath": filepath,
                "text": "",
                "concepts": [],
                "error": "Failed to read article"
            }
        
        cleaned_text = self.clean_text(text)
        concepts = self.extract_concepts(cleaned_text, max_concepts)
        
        return {
            "filename": filename,
            "filepath": filepath,
            "text": cleaned_text[:500],
            "full_text": cleaned_text,
            "concepts": concepts,
            "num_concepts": len(concepts)
        }
    
    def process_all_articles(self, max_concepts: int = 3) -> List[Dict]:
        articles = self.get_all_articles()
        processed = []
        
        for article_path in articles:
            result = self.process_article(article_path, max_concepts)
            processed.append(result)
            print(f"Processed: {result['filename']} - Found {result['num_concepts']} concepts")
        
        return processed
