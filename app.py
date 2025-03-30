from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from image_processor import process_image, extract_text
from grading import analyze_answer
import logging
from spellchecker import SpellChecker  # Using a more powerful spell checker
import re

# Initialize Flask app
app = Flask(__name__)

# Flask configuration
app.config.update({
    'UPLOAD_FOLDER': 'static/uploads',
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB
    'SECRET_KEY': os.urandom(24)
})
logging.basicConfig(level=logging.DEBUG)

# Initialize spell checker with academic vocabulary
spell = SpellChecker()
# spell.word_frequency.load_text_file('academic_vocabulary.txt')  # Add your custom dictionary

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_ocr_text(text):
    """Preprocess OCR output for better correction"""
    # Remove special characters except basic punctuation
    text = re.sub(r'[^a-zA-Z0-9\s.,;?!\-]', '', text)
    # Fix common OCR errors
    ocr_replacements = {
        r'\b([A-Za-z])[0-9]+\b': r'\1',  # Fix letter-number combinations
        r'\b([0-9])[A-Za-z]+\b': r'\1',
        '’': "'",
        '‘': "'",
        '“': '"',
        '”': '"'
    }
    for pattern, replacement in ocr_replacements.items():
        text = re.sub(pattern, replacement, text)
    return text

def correct_spelling(text):
    """Enhanced spelling correction with context awareness"""
    words = text.split()
    corrected_words = []
    
    for word in words:
        # Handle mixed case words
        original_case = [c.isupper() for c in word]
        word_lower = word.lower()
        
        # Get correction
        correction = spell.correction(word_lower)
        
        if correction:
            # Restore original case pattern
            corrected = ''.join([
                c.upper() if i < len(original_case) and original_case[i] else c.lower()
                for i, c in enumerate(correction)
            ])
            corrected_words.append(corrected)
        else:
            corrected_words.append(word)
    
    return ' '.join(corrected_words)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files or 'reference' not in request.form:
            return redirect(request.url)
            
        file = request.files['file']
        reference = request.form['reference'].strip()
        
        if not all([file.filename, reference]):
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            try:
                # Save the original uploaded image
                orig_filename = f"orig_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                orig_path = os.path.join(app.config['UPLOAD_FOLDER'], orig_filename)
                file.save(orig_path)
                
                # Process the image
                processed_filename = process_image(orig_path)
                if not processed_filename:
                    raise Exception("Image processing failed")
                
                # Extract text from the processed image
                raw_text = extract_text(
                    os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
                )
                
                # Clean and correct the text
                cleaned_text = clean_ocr_text(raw_text)
                corrected_answer = correct_spelling(cleaned_text)
                
                # Analyze the corrected answer against the reference
                score, similarity, coverage, key_data = analyze_answer(reference, corrected_answer)
                
                # Render results
                return render_template('results.html',
                    orig_image=orig_filename,
                    processed_image=processed_filename,
                    reference=reference,
                    student_answer=corrected_answer,
                    score=score,
                    similarity=similarity,
                    coverage=coverage,
                    key_entities=key_data)
                    
            except Exception as e:
                logging.error(f"Error processing submission: {str(e)}")
                return render_template('error.html', 
                    message="Processing failed. Please check input and try again.")
    
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000)