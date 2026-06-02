# SEFS | Semantic Entropy File System
### *Neural Intelligence Interface & Dynamic Security Engine*

**SEFS** is a next-generation file management system that transforms a static directory into a "Living Brain." By leveraging deep semantic analysis, it automatically organizes files based on context, generates AI-driven summaries, and implements a dynamic security layer for sensitive data.

---
## 🎥 Project Demo

[![Watch the video]](https://drive.google.com/file/d/1pvg6uJsi83zc3yxA5o2GRBBc4n-2jD1g/view?usp=sharing)

## 🚀 Project Description
The Semantic Entropy File System (SEFS) solves the problem of "Digital Clutter." Instead of manually sorting files, SEFS uses Natural Language Processing (NLP) to "read" your documents and images, physically organizing them into AI-named folders in your OS. It features a futuristic **Neural HUD** that visualizes your data as a living network, complete with real-time file monitoring and a "Neural Handshake" security protocol.

### Key Unique Features:
* **Semantic Intelligence:** Groups files (PDF, DOCX, TXT, PPTX) based on actual meaning using **MPNet Embeddings**.
* **Multi-Modal Vision:** Integrated **Tesseract OCR** allows the system to extract text from images (PNG, JPG) and cluster them alongside documents.
* **Smart Folder Naming:** Dynamically generates descriptive folder names (e.g., `MACHINE_LEARNING_DATA`) based on cluster content.
* **Dynamic Security Registry:** A right-click interface to lock/unlock files via a persistent JSON-based security handshake.
* **Neural Flow Animation:** A living UI that visualizes data pulses moving through the system using Cytoscape.js.

---

## 🛠️ Tech Stack
| Category | Technology |
| :--- | :--- |
| **Backend** | Python, Flask |
| **Real-time Monitoring** | Watchdog API |
| **AI Models** | MPNet (`all-mpnet-base-v2`), HDBSCAN Clustering |
| **Vision (OCR)** | Tesseract OCR, OpenCV |
| **Summarization** | Sumy (LSA Summarizer) |
| **Frontend** | Cytoscape.js, HTML5, CSS3 (Neon-HUD Aesthetic) |

---

## 📂 Project Structure
```text
SEFS-Neural-Interface/
├── main.py              # Flask server & Real-time Watchdog logic
├── embeddings.py        # MPNet semantic vector generation
├── clustering.py        # HDBSCAN unsupervised clustering logic
├── organizer.py         # AI folder naming & physical file movement
├── file_reader.py       # Multi-format text extraction & OCR
├── graph_generator.py   # Mapping intelligence to Neural Graph JSON
├── security_registry.json # Persistent security database
├── root_folder/         # The target directory monitored by AI
└── frontend/
    └── index.html       # The Neural HUD Interface


---

## ⚙️ Installation & Dependencies

### 1. Install Python Packages
Execute the following command to install the required neural and system libraries:
```bash
pip install flask watchdog sentence-transformers hdbscan PyPDF2 python-docx python-pptx sumy pytesseract opencv-python tqdm



---

## 🚀 How to Run

Follow these steps to initialize the SEFS Neural Engine and start organizing your data.

### 1. Initialize the Engine
Open your terminal or command prompt, navigate to the project directory, and execute the main controller:
```bash
python main.py
