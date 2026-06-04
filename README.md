# SEFS | Semantic Entropy File System
### *Neural Intelligence Interface & Dynamic Security Engine*

**SEFS** is a next-generation file management system that transforms a static directory into a "Living Brain." By leveraging deep semantic analysis, it automatically organizes files based on context, generates AI-driven summaries, and implements a dynamic security layer for sensitive data.

---
## 🎥 Project Demo
[![Watch the video]](https://drive.google.com/file/d/1pvg6uJsi83zc3yxA5o2GRBBc4n-2jD1g/view?usp=sharing)

---

## 🚀 Project Description
The Semantic Entropy File System (SEFS) solves the problem of "Digital Clutter." Instead of manually sorting files, SEFS uses Natural Language Processing (NLP) to "read" your documents and images, physically organizing them into AI-named folders in your OS. It features a futuristic **Neural HUD** that visualizes your data as a living network, complete with real-time file monitoring and a "Neural Handshake" security protocol.

### Key Unique Features:
* **Semantic Intelligence:** Groups files (PDF, DOCX, TXT, PPTX) based on actual meaning using **MPNet Embeddings**.
* **Multi-Modal Vision:** Integrated **Tesseract OCR** allows the system to extract text from images (PNG, JPG) and cluster them alongside documents.
* **Smart Folder Naming:** Dynamically generates descriptive folder names (e.g., `MACHINE_LEARNING_DATA`) based on cluster content.
* **Dynamic Security Registry:** A right-click interface to lock/unlock files via a persistent JSON-based security handshake.
* **Neural Flow Animation:** A living UI that visualizes data pulses moving through the system using Cytoscape.js.
* **Web Upload Panel:** Drag-and-drop file upload directly from the browser (cloud-compatible).

---

## 🛠️ Tech Stack
| Category | Technology |
| :--- | :--- |
| **Backend** | Python 3.11, Flask, Gunicorn |
| **Real-time Monitoring** | Watchdog API |
| **AI Models** | MPNet (`all-mpnet-base-v2`), HDBSCAN Clustering |
| **Vision (OCR)** | Tesseract OCR, OpenCV |
| **Summarization** | Sumy (LSA Summarizer) |
| **Frontend** | Cytoscape.js, HTML5, CSS3 (Neon-HUD Aesthetic) |
| **Cloud Deployment** | Railway.app |
| **Local Packaging** | PyInstaller |

---

## 📂 Project Structure
```text
SEFS-Neural-Interface/
├── main.py                  # Flask server — cloud & local compatible
├── launcher.py              # .exe entry point (auto-opens browser)
├── embeddings.py            # MPNet semantic vector generation
├── clustering.py            # HDBSCAN unsupervised clustering logic
├── organizer.py             # AI folder naming & physical file movement
├── file_reader.py           # Multi-format text extraction & OCR
├── graph_generator.py       # Mapping intelligence to Neural Graph JSON
├── security_registry.json   # Persistent security database
├── requirements.txt         # Python dependencies
├── Procfile                 # Railway/Heroku process config
├── runtime.txt              # Python version pin
├── build_exe.bat            # One-click Windows .exe builder
├── root_folder/             # The target directory monitored by AI
└── frontend/
    └── index.html           # The Neural HUD Interface
```

---

## ⚙️ Installation & Local Run

### 1. Install Python Packages
```bash
pip install -r requirements.txt
```

### 2. Run Locally
```bash
python main.py
```
Open your browser at: **http://127.0.0.1:5000**

Drop files into the `root_folder/` directory — SEFS will auto-organize and update the graph.

---

## ☁️ Option A: Deploy to Railway (Public Cloud Link)

Anyone with the link can use SEFS from any device, anywhere.

### Step 1 — Push to GitHub
```bash
git add .
git commit -m "Add cloud deployment files"
git push origin main
```

### Step 2 — Deploy on Railway.app
1. Go to **[railway.app](https://railway.app)** and sign in with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your **SEFS repository**
4. Railway detects the `Procfile` automatically
5. Click **Deploy** — wait ~5 minutes for build

### Step 3 — Get Your Public Link
- After deploy: Railway gives you a URL like `https://sefs-xyz.railway.app`
- Share this link — anyone can open it on any laptop, no installation needed!

> **Note:** On first load, the ML model (~420MB) downloads automatically. This takes ~2 minutes on Railway.

### Environment Variables (optional)
Set in Railway dashboard → Settings → Variables:
```
PORT=5000   (Railway sets this automatically)
```

---

## 💻 Option B: Windows .exe (Any Laptop, No Python Needed)

Package SEFS as a self-contained `.exe` that any Windows user can double-click.

### Step 1 — Build the .exe
Double-click `build_exe.bat` and wait ~10 minutes.

```
build_exe.bat
```

### Step 2 — Distribute
- Copy `dist/SEFS_Neural_Interface.exe` to any Windows PC
- Double-click it — the browser opens automatically at `http://127.0.0.1:5000`
- **No Python installation required**

> **Note:** The .exe will be ~1-2GB due to bundled ML models. This is expected.

---

## 🔒 Security Features
- Right-click any file node → **"Make Private"** to set a password
- The node turns 🔴 red and requires the password to view or download
- Right-click → **"Remove Privacy"** to unlock with the correct password

---

## 📊 How Files Are Processed
1. Upload files via drag-and-drop or drop into `root_folder/`
2. SEFS reads text from PDFs, DOCX, PPTX, TXT, and images (OCR)
3. MPNet generates semantic embedding vectors for each file
4. HDBSCAN clusters similar files together
5. AI generates descriptive folder names from cluster keywords
6. The Neural Graph updates with colored nodes showing clusters
