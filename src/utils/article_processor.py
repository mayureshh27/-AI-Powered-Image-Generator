import os
from typing import List, Dict
from docx import Document
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class ArticleProcessor:
    
    def __init__(self, articles_dir: str = "Articles"):
        self.articles_dir = articles_dir
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in .env file")
        self.client = Groq(api_key=api_key)

    def read_docx(self, filepath: str) -> str:
        try:
            doc = Document(filepath)
            return "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return ""

    def process_article(self, filepath: str, max_concepts: int = 3) -> Dict:
        text = self.read_docx(filepath)
        filename = os.path.basename(filepath)
        
        if not text:
            return {"error": "Empty or unreadable file"}

        prompt = f"""You are an expert visual content creator for professional journalism. Your task is to generate {max_concepts} distinct, safe, and contextually accurate image prompts based ONLY on the content of this article.

ARTICLE TEXT:
{text[:15000]}

STRICT REQUIREMENTS:
1. CONTEXT ONLY: Each prompt must describe a REAL scene, concept, or visual element that is EXPLICITLY mentioned or directly implied in the article text above.
2. SAFE CONTENT: Generate only professional, workplace-appropriate imagery. Avoid any sensitive, controversial, or inappropriate content.
3. PHOTOREALISTIC STYLE: Describe scenes as if they were professional photographs or documentary shots.
4. TECHNICAL DETAILS: Include specific details about:
   - Lighting (e.g., "natural daylight", "soft studio lighting", "golden hour")
   - Camera perspective (e.g., "wide angle shot", "close-up", "aerial view")
   - Composition (e.g., "centered composition", "rule of thirds")
   - Mood/atmosphere that matches the article tone

5. FORMAT: Output ONLY the prompts separated by a pipe symbol (|). Do NOT include any introductory text, explanations, or numbering.

EXAMPLE OUTPUT FORMAT:
A modern office workspace with employees collaborating on laptops, natural daylight from large windows, wide angle shot, professional photography | A close-up of renewable energy solar panels on a rooftop, golden hour lighting, shallow depth of field, documentary style | An aerial view of a sustainable urban development with green spaces, soft morning light, architectural photography

YOUR OUTPUT (prompts only, separated by |):"""

        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=500
            )
            
            content = completion.choices[0].message.content.strip()
            concepts = [c.strip() for c in content.split('|') if c.strip()]
            
            if not concepts:
                return {"error": "No valid prompts generated", "concepts": []}
            
            return {
                "filename": filename,
                "concepts": concepts[:max_concepts],
                "num_concepts": len(concepts[:max_concepts]),
                "text": text[:200]
            }

        except Exception as e:
            print(f"LLM Error: {e}")
            return {"error": str(e), "concepts": []}

    def get_all_articles(self) -> List[str]:
        if not os.path.exists(self.articles_dir):
            return []
        return [os.path.join(self.articles_dir, f) for f in os.listdir(self.articles_dir) if f.endswith('.docx') and not f.startswith('~')]
