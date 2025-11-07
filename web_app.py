import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from app import extract_text_from_pdf, summarize_text, generate_mind_map, download_nltk_data

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return redirect(request.url)
        file = request.files['pdf_file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            language = request.form['language']
            num_sentences = int(request.form['num_sentences'])

            text = extract_text_from_pdf(filepath)
            summary = summarize_text(text, language, num_sentences)
            mind_map = generate_mind_map(summary)

            return render_template('index.html', mind_map=mind_map)

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    download_nltk_data()
    app.run(debug=True)
