# 🐢 Marine Turtle Stranding and Release Monitoring Tool

A Streamlit app for crowdsourced monitoring of marine turtle releases, strandings, and sightings based on image OCR and social media post text analysis.

---

## 🧰 Features

- 🖼️ OCR extraction from screenshots (supports English + Urdu)
- 🧠 Auto-parsing of species, interaction type, location, and status
- ✍️ Manual override of all fields including account, species, status, and location
- 🧾 Hash-based deduplication
- 📊 Visual dashboards (Plotly)
- 📁 Record download and admin logs

---

## 📂 Project Structure

```
📁 turtle_monitor
├── main.py                  # Streamlit frontend
├── parser.py                # Text analysis
├── ocr_utils.py             # OCR support
├── config.py                # Config/keyword loading
├── constants.py             # Label constants
├── turtle_release_records.csv  # Auto-generated data
├── config/
│   └── keywords.json        # Configurable keywords (auto-generated)
├── logs/
│   └── app.log              # Streamlit + parsing logs
```

---

## 🗃️ Expected CSV Schema

```
Date, Time, Account Name (Manual), Account Name (Detected),
Post Date (Detected), Post Content, Location, Turtle Count,
Province, District, Species, Interaction, Status, Content Hash
```

These fields are dynamically updated after form submission.

---

## 🐢 Taxonomies

- **Species:** Green Turtle, Olive Ridley, Leatherback, Loggerhead, Hawksbill
- **Interaction:** Stranded, Sighted, Bycatch
- **Status:** Alive, Dead (normalized from variations like "Released Dead")

---

## 📈 Dashboard Insights

- 📌 Status breakdown
- 📌 Location × Status bar charts
- 📌 District-wise frequency
- 📌 Monthly trends
- 📌 Species pie chart
- 📌 Interaction types
- 📌 Posts per account

---

## 🚀 Getting Started

### ✅ Requirements
- Python 3.9+
- Tesseract-OCR installed and added to PATH
- Anaconda (recommended)

### 📦 Install Dependencies

```bash
conda activate NED
pip install -r requirements.txt
```

### ▶️ Launch the App

```bash
streamlit run main.py
```

> Make sure `keywords.json` and `turtle_release_records.csv` are auto-generated on first run.

---

## 🛠️ Developer Utilities

- Admin > App Logs
- Admin > Clear Records
- Auto fallback for missing or malformed CSV/config

---

## 🧪 Coming Soon

- Filtering by species, interaction in dashboard
- Editable keyword mapping in the UI
- Record editing from table view

---

## 🐳 Maintainer

Developed for marine conservation teams and citizen scientists working on Pakistan's coastlines. Built with ❤️ in Python.

