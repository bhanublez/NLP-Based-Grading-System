# Create virtual environment

python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows

# Install dependencies

pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Create required directories

mkdir -p static/uploads static/css static/images

# Run application

python app.py
