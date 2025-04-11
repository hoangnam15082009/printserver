from flask import Flask, render_template, request, redirect
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/print', methods=['POST'])
def print_pdf():
    file = request.files['pdf_file']
    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        pdf_viewer = r"C:\Program Files\SumatraPDF\SumatraPDF.exe"
        print_command = f'"{pdf_viewer}" -print-to-default -print-settings "duplex,long" "{os.path.abspath(filepath)}"'
        subprocess.run(print_command, shell=True)

        return "✅ Đã gửi lệnh in!"
    return "❌ File không hợp lệ!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
