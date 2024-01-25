# app.py
from flask import Flask, jsonify
from flask_cors import CORS
from wordleSolver import runPY

app = Flask(__name__)
CORS(app)

@app.route('/run_wordle_solver', methods=['GET'])
def run_wordle_solver():
    result_word, result_patterns, result_words = runPY()
    print("Found the word:", result_word)
    print("Patterns:", result_patterns)
    return jsonify({"word": result_word, 'patterns': result_patterns, 'words': result_words})

if __name__ == '__main__':
    app.run(debug=True)
