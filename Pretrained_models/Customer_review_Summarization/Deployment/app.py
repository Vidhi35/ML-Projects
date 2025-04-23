from flask import Flask, request, jsonify, render_template
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re
import nltk

app = Flask(__name__)

# Initialize model and tokenizer
model_path = "./model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Constants
MAX_INPUT_LENGTH = 384
MAX_TARGET_LENGTH = 48

def clean_text(text):
    text = re.sub(r'<br\\s*/?>', ' ', text)
    text = re.sub(r'\\s+', ' ', text)
    return text.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        text = request.json['text']
        cleaned_text = clean_text(text)
        
        inputs = tokenizer(
            cleaned_text, 
            max_length=MAX_INPUT_LENGTH, 
            truncation=True, 
            return_tensors="pt"
        ).to(device)
        
        summary_ids = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=MAX_TARGET_LENGTH,
            min_length=10,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=2
        )
        
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return jsonify({"summary": summary})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)