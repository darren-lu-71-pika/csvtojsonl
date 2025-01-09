from flask import Flask, request, jsonify, send_file
import pandas as pd
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/convert', methods=['POST'])
def convert_csv_to_jsonl():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})

    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({'success': False, 'error': 'Invalid file format. Please upload a CSV file.'})

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # Read CSV and convert to JSONL
        df = pd.read_csv(file_path)
        if 'role' not in df.columns or 'content' not in df.columns:
            return jsonify({'success': False, 'error': 'CSV must contain "role" and "content" columns.'})

        conversation_id = 'conversation_id' in df.columns
        grouped = df.groupby('conversation_id') if conversation_id else [('', df)]

        jsonl_lines = []
        for _, group in grouped:
            messages = group[['role', 'content']].to_dict(orient='records')
            jsonl_lines.append(json.dumps({'messages': messages}))

        output_file = os.path.join(OUTPUT_FOLDER, 'output.jsonl')
        with open(output_file, 'w') as f:
            f.write('\n'.join(jsonl_lines))

        return jsonify({'success': True, 'download_url': '/download/output.jsonl'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
