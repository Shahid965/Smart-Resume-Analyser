import pdfplumber
import PyPDF2
import docx
import re  # THIS WAS MISSING
import os

class ResumeParser:
    @staticmethod
    def extract_text(filepath):
        ext = os.path.splitext(filepath)[1].lower()
        text = ""
        try:
            if ext == '.pdf':
                with pdfplumber.open(filepath) as pdf:
                    for page in pdf.pages:
                        val = page.extract_text()
                        if val: text += val + " "
                if len(text.strip()) < 20:
                    with open(filepath, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        for page in reader.pages:
                            text += (page.extract_text() or "") + " "
            elif ext == '.docx':
                doc = docx.Document(filepath)
                text = " ".join([p.text for p in doc.paragraphs])
            
            # Clean up whitespace
            clean_text = re.sub(r'\s+', ' ', text).strip()
            return clean_text
        except Exception as e:
            print(f"Extraction Error: {e}")
            return ""

    @staticmethod
    def extract_profile(text):
        # Extract email
        email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        # Extract phone
        phone = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        
        # Simple name extraction (first two words of the text)
        words = text.split()
        name = " ".join(words[:2]) if len(words) > 2 else "Candidate"
        
        return {
            "name": name.upper(),
            "email": email.group(0) if email else "Not Found",
            "phone": phone.group(0) if phone else "Not Found"
        }

    @staticmethod
    def check_sections(text):
        sections = ["Education", "Experience", "Skills", "Projects", "Summary"]
        found = {}
        for s in sections:
            found[s] = bool(re.search(s, text, re.IGNORECASE))
        return found