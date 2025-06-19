
# 🔴 **RESPONSABILITÉ ET USAGE LÉGAL / LEGAL RESPONSIBILITY AND USAGE**

**🇫🇷 :**
> **ATTENTION : Cet outil est développé UNIQUEMENT à des fins éducatives dans le cadre d'un projet de cours.**
> 
> - ❌ **Toute utilisation malveillante, illégale ou non autorisée de cet outil est STRICTEMENT INTERDITE**
> - ❌ **Les développeurs de ce projet déclinent toute responsabilité concernant l'usage abusif de cet outil**
> - ✅ **Utilisez cet outil UNIQUEMENT sur vos propres systèmes ou avec autorisation écrite explicite**
> - ✅ **Respectez les lois locales et internationales en matière de cybersécurité**
> 
> **L'utilisateur est SEUL RESPONSABLE de l'usage qu'il fait de cet outil.**

**🇬🇧 :**
> **WARNING: This tool is developed ONLY for educational purposes as part of a course project.**
> 
> - ❌ **Any malicious, illegal or unauthorized use of this tool is STRICTLY PROHIBITED**
> - ❌ **The developers of this project disclaim any responsibility regarding misuse of this tool**
> - ✅ **Use this tool ONLY on your own systems or with explicit written authorization**
> - ✅ **Comply with local and international cybersecurity laws**
> 
> **The user is SOLELY RESPONSIBLE for how they use this tool.**

---

# MinAttack
**Automated Pentest Desktop Application**

MinAttack is a **desktop application for penetration testing**, combining a **FastAPI backend** and a **PySide6 frontend**.

---

## Project Setup (Development & Production)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/MinAttack.git
cd MinAttack
```

### 2️⃣ Create and Activate the Virtual Environment

✅ **Linux/macOS**
```bash
python -m venv minattack_env
source minattack_env/bin/activate
```

✅ **Windows**
```bash
python -m venv minattack_env
minattack_env\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Lancement du backend

### Depuis le repertoire ***Backend*** le terminal :
```bash
uvicorn minattack.backend.app.main:app --reload
```

### Depuis le script python ***backend/backend_launcher.py***
```bash
python backend/backend_launcher.py
```

---

## Updating Dependencies

Whenever new dependencies are installed, update `requirements.txt`:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Updated dependencies"
git push
```

---

## Project Structure
```
/MinAttack/                # Root project directory
│── /backend/              # FastAPI backend
│── /frontend/             # PySide6 frontend
│── /scripts/              # Utils
│── launcher.py            # Unified launcher (runs backend + frontend)
│── config.py              # Configuration file
│── requirements.txt       # Python dependencies
│── README.md              # Documentation
```

---

## 📚 **Contexte Éducatif / Educational Context**

Ce projet a été développé dans le cadre d'un cours de cybersécurité à l'EPF. Il vise à comprendre les techniques de test d'intrusion à des fins purement pédagogiques.

*This project was developed as part of a cybersecurity course at EPF. It aims to understand penetration testing techniques for purely educational purposes.*