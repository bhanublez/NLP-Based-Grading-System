from sentence_transformers import SentenceTransformer, util
import spacy
import numpy as np

MODEL = SentenceTransformer('paraphrase-MiniLM-L6-v2')
NLP = spacy.load("en_core_web_sm")

def extract_phrases(text):
    """Enhanced phrase extraction with lemmatization and POS filtering"""
    doc = NLP(text.lower())
    phrases = set()
    
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE', 'EVENT','WORK_OF_ART']: 
            phrases.add(ent.text.lower())
    
    for chunk in doc.noun_chunks:
        phrase = ' '.join([token.lemma_ 
                          for token in chunk
                          if not token.is_stop and token.pos_ in ['NOUN', 'PROPN', 'ADJ']])
        if len(phrase) > 2:
            phrases.add(phrase)
    
    return phrases

def analyze_answer(reference, student_answer):
    """Robust answer analysis with proper normalization"""
    try:
        ref_clean = reference.strip().lower()
        student_clean = student_answer.strip().lower()
        
        if not ref_clean or not student_clean:
            return (0.0, 0.0, 0.0, {})
        
        ref_embed = MODEL.encode(ref_clean)
        student_embed = MODEL.encode(student_clean)
        similarity = util.cos_sim(ref_embed, student_embed).item()
        
        ref_phrases = extract_phrases(ref_clean)
        student_phrases = extract_phrases(student_clean)
        
        matched_phrases = ref_phrases & student_phrases
        coverage = len(matched_phrases) / len(ref_phrases) if ref_phrases else 0
        
        final_score = (0.6 * similarity + 0.4 * coverage) * 100
        
        return (
            round(final_score, 1),
            round(similarity * 100, 1),
            round(coverage * 100, 1),
            {
                'matched': sorted(matched_phrases),
                'missing': sorted(ref_phrases - student_phrases),
                'reference_phrases': sorted(ref_phrases),
                'student_phrases': sorted(student_phrases)
            }
        )
        
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        return (0.0, 0.0, 0.0, {})