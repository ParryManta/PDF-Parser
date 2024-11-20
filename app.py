from flask import Flask, request, jsonify
from docling.document_converter import DocumentConverter
import os
import tempfile

app = Flask(__name__)

@app.route('/parse-pdf', methods=['POST'])
def parse_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400

    # Save uploaded file to temp directory
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)
    file.save(temp_path)

    try:
        # Convert PDF using docling
        converter = DocumentConverter()
        result = converter.convert(temp_path)
        markdown_text = result.document.export_to_markdown()
        
        return jsonify({
            'markdown': markdown_text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        os.rmdir(temp_dir)

if __name__ == '__main__':
    app.run(debug=True)
