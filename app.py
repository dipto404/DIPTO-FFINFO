import os
import json
import base64
from flask import Flask, jsonify, request, render_template_string

# Import existing protobuf and secret modules from your project
try:
    from secret import key, iv
    import uid_generator_pb2
    from proto import AccountPersonalShow_pb2, FreeFire_pb2
except ImportError:
    key = "Yg&tc%DEuh6%Zc^8"
    iv = "6oyZDr22E3ychjM%"

app = Flask(__name__)

# --- HTML TEMPLATE (Single Page UI) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Fire Player Info Checker</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .container { background: #1e293b; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); width: 100%; max-width: 500px; padding: 30px; border: 1px solid #334155; }
        h2 { text-align: center; margin-bottom: 20px; color: #38bdf8; font-size: 24px; }
        .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
        input[type="text"] { flex: 1; padding: 12px 15px; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: #fff; font-size: 16px; outline: none; }
        input[type="text"]:focus { border-color: #38bdf8; }
        button { padding: 12px 20px; border: none; border-radius: 8px; background: #0284c7; color: white; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.3s; }
        button:hover { background: #0369a1; }
        .result-box { background: #0f172a; padding: 15px; border-radius: 8px; border: 1px solid #334155; display: none; margin-top: 15px; }
        .result-item { display: flex; justify-content: space-between; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #1e293b; }
        .result-item:last-child { border-bottom: none; }
        .label { color: #94a3b8; }
        .value { font-weight: bold; color: #f1f5f9; }
        .error { color: #ef4444; text-align: center; margin-top: 10px; display: none; }
        .loading { text-align: center; color: #38bdf8; display: none; margin-top: 10px; }
    </style>
</head>
<body>

<div class="container">
    <h2>🎮 FF Profile Checker</h2>
    <div class="input-group">
        <input type="text" id="uidInput" placeholder="Enter Player UID (e.g. 12345678)" />
        <button onclick="fetchProfile()">Search</button>
    </div>
    
    <div class="loading" id="loading">Searching player info...</div>
    <div class="error" id="error">Player not found or invalid UID!</div>

    <div class="result-box" id="resultBox">
        <div class="result-item"><span class="label">UID:</span><span class="value" id="resUid">-</span></div>
        <div class="result-item"><span class="label">Nickname:</span><span class="value" id="resName">-</span></div>
        <div class="result-item"><span class="label">Level:</span><span class="value" id="resLevel">-</span></div>
        <div class="result-item"><span class="label">Likes:</span><span class="value" id="resLikes">-</span></div>
        <div class="result-item"><span class="label">Region:</span><span class="value" id="resRegion">-</span></div>
    </div>
</div>

<script>
    async function fetchProfile() {
        const uid = document.getElementById('uidInput').value.trim();
        const resultBox = document.getElementById('resultBox');
        const errorBox = document.getElementById('error');
        const loadingBox = document.getElementById('loading');

        if (!uid) return alert('Please enter a UID!');

        resultBox.style.display = 'none';
        errorBox.style.display = 'none';
        loadingBox.style.display = 'block';

        try {
            const response = await fetch(`/api/profile?uid=${uid}`);
            const data = await response.json();

            loadingBox.style.display = 'none';

            if (data.status === 'success') {
                document.getElementById('resUid').innerText = data.data.uid || uid;
                document.getElementById('resName').innerText = data.data.nickname || 'N/A';
                document.getElementById('resLevel').innerText = data.data.level || 'N/A';
                document.getElementById('resLikes').innerText = data.data.likes || '0';
                document.getElementById('resRegion').innerText = data.data.region || 'N/A';
                resultBox.style.display = 'block';
            } else {
                errorBox.innerText = data.message || 'Error fetching data';
                errorBox.style.display = 'block';
            }
        } catch (err) {
            loadingBox.style.display = 'none';
            errorBox.innerText = 'Failed to connect to server!';
            errorBox.style.display = 'block';
        }
    }
</script>

</body>
</html>
"""

# --- ROUTE 1: Home Page (UI View) ---
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# --- ROUTE 2: Profile API Endpoint ---
@app.route('/api/profile', methods=['GET'])
def get_profile():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"status": "error", "message": "UID parameter is required"}), 400

    try:
        # Protobuf / Logic integration goes here
        # (এখানে আপনার প্রজেক্টের আসল ডাটা ফেচিং লজিক অটোমেট হবে)
        
        # ডেমো রেসপন্স স্ট্রাকচার:
        return jsonify({
            "status": "success",
            "data": {
                "uid": uid,
                "nickname": "Player_" + uid[:4],
                "level": 65,
                "likes": 1250,
                "region": "BD"
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
