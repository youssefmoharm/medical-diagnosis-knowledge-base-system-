# MedTriage Expert System 

## Quick Start
**Windows:** Double-click `start.bat`
**Mac/Linux:** `chmod +x start.sh && ./start.sh`
**Manual:** `pip install flask flask-cors` then `python server.py`

Open **http://localhost:5000** — the Evaluation section is built into the UI under the EVALUATION nav link.

## Structure
- `server.py` — Flask server
- `knowledge_base.py` — 10 production rules
- `inference_engine.py` — forward-chaining + conflict resolution
- `working_memory.py` — fact store + validation
- `explanation.py` — WHY/HOW explanation generator
- `triage_api.py` — API layer
- `index.html` — Full UI including Phase 5 Evaluation section
