from flask import Flask, render_template, send_from_directory, jsonify, request
import os, subprocess

app = Flask(__name__)

# wav folder
AUDIO_FOLDER = 'outputs'

@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    per_page = 10  # Set number of items per page
    files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith('.wav')]
    files.sort(key=lambda f: os.path.getmtime(os.path.join(AUDIO_FOLDER, f)), reverse=True)

    total_files = len(files)
    pages = total_files // per_page + (total_files % per_page > 0)

    # Pagination logic
    files = files[(page-1)*per_page:page*per_page]

    return render_template('index.html', files=files, page=page, pages=pages)


@app.route('/audio/<filename>')
def audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

@app.route('/update-files')
def update_files():
    files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith('.wav')]
    return jsonify(files=files)

@app.route('/run-script', methods=['POST'])
def run_script():
    text = request.json['text']
    # Ensure the text is safely handled if it's going into a system command
    # This is a simple example; consider more robust validation depending on your use case

    # Corrected line: Added a comma between '-text' and text
    process = subprocess.Popen(['python3', 'run.py', '-text', text], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        return jsonify(error=stderr.decode()), 500

    return jsonify(result=stdout.decode())

if __name__ == '__main__':
    app.run(debug=True)
