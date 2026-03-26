from flask import Flask, request, jsonify, render_template
import opengradient as og
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

PRIVATE_KEY = os.getenv("OG_PRIVATE_KEY")

if not PRIVATE_KEY:
    raise ValueError("OG_PRIVATE_KEY not found. Please create a .env file. See README.md")

client = og.Client(private_key=PRIVATE_KEY)

# Approve OPG tokens on startup
client.llm.ensure_opg_approval(opg_amount=5.0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    coin = request.json.get('coin', '').strip()
    if not coin:
        return jsonify({'error': 'No coin provided'}), 400

    try:
        messages = [
            {
                "role": "user",
                "content": f"You are a sharp crypto analyst. Give your honest opinion on {coin} — covering what it is, its strengths, weaknesses, and overall sentiment. Be direct and concise."
            }
        ]

        result = client.llm.chat(
            model=og.TEE_LLM.CLAUDE_HAIKU_4_5,
            messages=messages,
            max_tokens=400,
            temperature=0.7
        )

        return jsonify({
            'coin': coin.upper(),
            'opinion': result.chat_output['content'],
            'proof': result.payment_hash
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)