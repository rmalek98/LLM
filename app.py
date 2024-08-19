from flask import Flask, render_template, request, jsonify
from src.main import after_rag_chain  # This should work now

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    answer = after_rag_chain.invoke(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
