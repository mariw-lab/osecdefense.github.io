from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

@app.route('/')
def terminal():
    with open('index.html', 'r', encoding='utf-8') as f:
        return render_template_string(f.read())

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
