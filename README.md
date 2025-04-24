# **MinAttack** 🔥  
**Automated Pentest Desktop Application**  

MinAttack is a **desktop application for penetration testing**, combining a **FastAPI backend** and a **PySide6 frontend**.  
It integrates various pentesting tools such as **sqlmap, XSStrike, Sublist3r**, and optionally **AI for analysis**.

---

## 🚀 **Project Setup (Development & Production)**
### **1️⃣ Clone the Repository**
```
git clone https://github.com/yourusername/MinAttack.git
cd MinAttack
```

### **2️⃣ Create and Activate the Virtual Environment**
✅ **Linux/macOS**
```
python -m venv minattack_env
source minattack_env/bin/activate
```
✅ **Windows**
```
python -m venv minattack_env
minattack_env\Scripts\activate
```

### **3️⃣ Install Dependencies**
```
pip install -r requirements.txt
```
---
## ▶️️ **Lancement du backend**

### Depuis le repertoire *Backend* le terminal :
`uvicorn app.main:app --reload`

### Depuis le script python *backend/backend_launcher.py*

---
## 🔧 **Updating Dependencies**
Whenever new dependencies are installed, update `requirements.txt`:
```
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Updated dependencies"
git push 
```

---

## ⚡ **Project Structure**
```
/MinAttack/         # Root project directory
│── /backend/       # FastAPI backend
│── /frontend/      # PySide6 frontend
│── /scripts/       # Pentesting tools (sqlmap, XSStrike, etc.)
│── launcher.py     # Unified launcher (runs backend + frontend)
│── config.py       # Configuration file
│── requirements.txt # Python dependencies
│── README.md       # Documentation
```
