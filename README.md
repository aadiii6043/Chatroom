# 🗨️ Chatroom Project Documentation

This project is a **real-time chatroom** built using **Flask-SocketIO**. It allows multiple users to connect and chat, with an optional admin approval system for new users. The chatroom can also be made public using **Ngrok**.

---

## 📌 1. Installation & Setup

### 🔹 Step 1: Clone the Repository
```sh
git clone https://github.com/your-username/chatroom-project.git
cd chatroom-project
```

### 🔹 Step 2: Create a Virtual Environment
```sh
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# OR on Windows:
.venv\Scripts\activate
```
### 🔹 Step 3:Running the Chatroom Locally
```sh
python server.py
```
Once started, the server will be available at:
```
http://127.0.0.1:8000
```
---

## 🌍 2. Making Your Chatroom Public Using Ngrok

### 🔹 Step 1: Install Ngrok
```sh
brew install ngrok
```
### 🔹 Step 2: Authenticate Ngrok (First-Time Users)
```sh
ngrok authtoken YOUR_NGROK_AUTH_TOKEN
```
### 🔹 Step 3: Start Ngrok
```sh
ngrok http 8000
```
Ngrok will generate a public URL, like:
```sh
Forwarding      http://abc123.ngrok.io -> http://localhost:8000
```

Make sure your index.html is inside the templates/ folder:















