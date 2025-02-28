<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatroom Project Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 20px auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: #f9f9f9;
        }
        h1, h2 {
            color: #333;
        }
        code {
            background-color: #eef;
            padding: 2px 4px;
            border-radius: 4px;
        }
        pre {
            background-color: #eef;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        ul {
            padding-left: 20px;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Chatroom Project Documentation</h1>
    <p>This project is a **real-time chatroom** built using **Flask-SocketIO**. It allows multiple users to connect and chat, with an optional admin approval system for new users. The chatroom can also be made public using **Ngrok**.</p>

    <h2>📂 Folder Structure</h2>
    <pre><code>
/chatroom-project
│── server.py             # Main Flask server file
│── ngrok.yml             # (Optional) Ngrok authentication file
│── requirements.txt      # List of dependencies (Flask, Flask-SocketIO, eventlet)
│── /templates
│    ├── index.html       # Chatroom frontend (HTML, JS, CSS)
    </code></pre>

    <h2>📌 1. Installation & Setup</h2>
    <h3>🔹 Step 1: Clone the Repository</h3>
    <pre><code>git clone https://github.com/your-username/chatroom-project.git
cd chatroom-project</code></pre>

    <h3>🔹 Step 2: Create a Virtual Environment (Recommended)</h3>
    <pre><code>python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR on Windows:
.venv\Scripts\activate</code></pre>

    <h3>🔹 Step 3: Install Dependencies</h3>
    <pre><code>pip install -r requirements.txt</code></pre>

    <h2>📌 2. Running the Chatroom Locally</h2>
    <h3>🔹 Start the Flask Server</h3>
    <pre><code>python server.py</code></pre>
    <p>Once started, the server will be available at:</p>
    <pre><code>http://127.0.0.1:8000</code></pre>
    <p>Open this URL in your browser to access the chatroom.</p>

    <h2>🌍 3. Making Your Chatroom Public Using Ngrok</h2>
    <p>To allow anyone to access your chatroom globally, use <strong>Ngrok</strong>.</p>

    <h3>🔹 Step 1: Install Ngrok</h3>
    <pre><code>brew install ngrok  # macOS (Homebrew)</code></pre>
    <p>For Windows/Linux, download and install Ngrok from <a href="https://ngrok.com/download">Ngrok.com</a>.</p>

    <h3>🔹 Step 2: Authenticate Ngrok (First-Time Users)</h3>
    <pre><code>ngrok authtoken YOUR_NGROK_AUTH_TOKEN</code></pre>

    <h3>🔹 Step 3: Start Ngrok</h3>
    <pre><code>ngrok http 8000</code></pre>
    <p>Ngrok will generate a public URL like:</p>
    <pre><code>Forwarding                    http://abc123.ngrok.io -> http://localhost:8000</code></pre>
    <p>Copy and share the Ngrok link (<code>http://abc123.ngrok.io</code>) to allow external users to join the chat.</p>

    <h2>📌 4. Running the Chatroom with Ngrok</h2>
    <h3>🔹 Step 1: Run the Server (if not already running)</h3>
    <pre><code>python server.py</code></pre>

    <h3>🔹 Step 2: Start Ngrok in a New Terminal Window</h3>
    <pre><code>ngrok http 8000</code></pre>

    <h3>🔹 Step 3: Open Chatroom in Browser</h3>
    <ul>
        <li><strong>Locally:</strong> <pre><code>http://127.0.0.1:8000</code></pre></li>
        <li><strong>Publicly (Ngrok Link):</strong> Open the Ngrok-generated URL.</li>
    </ul>

    <h2>🔧 5. Troubleshooting</h2>

    <h3>❌ Flask Can't Find <code>index.html</code>?</h3>
    <p>Ensure that the <code>index.html</code> file is inside the <code>templates/</code> folder:</p>
    <pre><code>/chatroom-project
├── server.py
└── /templates
    └── index.html</code></pre>

    <h3>❌ Ngrok Not Working?</h3>
    <p>Make sure your Flask server is running before starting Ngrok.</p>

    <h3>❌ Getting <code>403 Forbidden</code> in Ngrok?</h3>
    <pre><code>ngrok config add-authtoken YOUR_NGROK_AUTH_TOKEN</code></pre>

    <h2>🎉 Now Your Chatroom is Live!</h2>
    <ul>
        <li>Test it on multiple devices.</li>
        <li>Share the Ngrok link with friends.</li>
        <li>Enhance the project by adding new features.</li>
    </ul>

    <p>🚀 Happy coding!</p>
</body>
</html>
