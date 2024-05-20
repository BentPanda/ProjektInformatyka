import subprocess
import json
from flask import Flask, request, render_template, redirect, flash
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'py'}

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def audit_security(file_path):
    result = subprocess.run(['bandit', '-q', '-ll', '-f', 'json', file_path], capture_output=True, text=True)
    
    if result.returncode != 0:
        try:
            parsed_result = json.loads(result.stdout)
            if parsed_result['results']:
                issues = []
                for issue in parsed_result['results']:
                    issues.append({
                        'filename': issue['filename'],
                        'issue_text': issue['issue_text'],
                        'line_range': issue['line_range'],
                        'issue_severity': issue['issue_severity'],
                        'issue_confidence': issue['issue_confidence'],
                        'issue_cwe_link': issue['issue_cwe']['link'],
                        'more_info': issue['more_info'],
                        'code': issue['code'].replace('\\n', '\n')
                    })
                return issues
            else:
                return []
        except json.JSONDecodeError:
            return "JSONDecodeError"
    else:
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            issues = audit_security(file_path)
            if issues == "JSONDecodeError":
                flash('Failed to process the file as JSON.')
                return redirect(request.url)
            return render_template('index.html', issues=issues)
    return render_template('index.html', issues=None)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
