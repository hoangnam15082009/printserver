from flask import Flask, request
import os
import tempfile
import platform
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

html = """
<!doctype html>
<html>
<head>
    <title>In từ xa</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family:sans-serif;padding:20px;">
    <h2>🖨️ Gửi Lệnh In Từ Xa</h2>

    <form method="POST" action="/print-text">
        <textarea name="text" rows="8" cols="40" placeholder="Nhập nội dung cần in..." style="width:100%;"></textarea><br>
        <label>Khổ giấy:</label>
        <select name="paper_size">
            <option value="A4">A4</option>
            <option value="A5">A5</option>
            <option value="Letter">Letter</option>
        </select>
        <label style="margin-left:10px;">In:</label>
        <select name="duplex">
            <option value="one-sided">1 mặt</option>
            <option value="two-sided-long-edge">2 mặt</option>
        </select><br><br>
        <button type="submit">📝 In Văn Bản</button>
    </form>

    <hr>

    <form method="POST" action="/print-pdf" enctype="multipart/form-data">
        <p>📄 Chọn file PDF để in:</p>
        <input type="file" name="pdf" accept="application/pdf"><br>
        <label>Khổ giấy:</label>
        <select name="paper_size">
            <option value="A4">A4</option>
            <option value="A5">A5</option>
            <option value="Letter">Letter</option>
        </select>
        <label style="margin-left:10px;">In:</label>
        <select name="duplex">
            <option value="one-sided">1 mặt</option>
            <option value="two-sided-long-edge">2 mặt</option>
        </select><br><br>
        <button type="submit">🖨️ In File PDF</button>
    </form>
</body>
</html>
"""

@app.route("/")
def home():
    return html

@app.route("/print-text", methods=["POST"])
def print_text():
    content = request.form.get("text", "")
    paper_size = request.form.get("paper_size", "A4")
    duplex = request.form.get("duplex", "one-sided")

    if content.strip() == "":
        return "Không có nội dung để in."

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as f:
        f.write(content)
        filename = f.name

    print_file(filename, paper_size, duplex)
    return "🖨️ Đã gửi lệnh in văn bản."

@app.route("/print-pdf", methods=["POST"])
def print_pdf():
    file = request.files.get("pdf")
    paper_size = request.form.get("paper_size", "A4")
    duplex = request.form.get("duplex", "one-sided")

    if not file:
        return "Không có file nào được tải lên."

    filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filename)

    print_file(filename, paper_size, duplex)
    return "🖨️ Đã gửi lệnh in file PDF."

def print_file(filepath, paper_size="A4", duplex="one-sided"):
    system = platform.system()

    if system == "Windows":
        if filepath.lower().endswith(".pdf"):
            sumatra_path = r"C:\Program Files\SumatraPDF\SumatraPDF.exe"
            if not os.path.exists(sumatra_path):
                print("⚠️ SumatraPDF chưa được cài hoặc sai đường dẫn!")
                return
            os.system(f'"{sumatra_path}" -print-to-default "{filepath}"')
        else:
            os.startfile(filepath, "print")

    else:
        cmd = f'lp -o media={paper_size} -o sides={duplex} "{filepath}"'
        os.system(cmd)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
