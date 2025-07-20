# Synthetisches Interview System 🎤

Automatisierte synthetische Interviews mit AI-Personas für Lifestyle-Marken-Forschung mit LangChain und OpenRouter.

**📦 Repository:** [github.com/thetabish/ai-personas](https://github.com/thetabish/ai-personas)

## Vor dem Start: API-Schlüssel besorgen

**5-Sekunden Setup:**
1. Gehen Sie zu: https://openrouter.ai/mistralai/mistral-small-24b-instruct-2501:free/api
2. Erstellen Sie einen kostenlosen Account
3. Kopieren Sie Ihren API-Schlüssel (beginnt mit `sk-or-v1-...`)
4. **Schlüssel wird automatisch abgefragt!** ⬇️

## 🚀 Schnell-Start (5 Minuten)

### Linux/macOS:
```bash
# SSH (empfohlen)
git clone git@github.com:thetabish/ai-personas.git
# oder HTTPS
git clone https://github.com/thetabish/ai-personas.git

cd ai-personas
chmod +x run.sh && ./run.sh
# Script fragt automatisch nach API-Schlüssel falls keiner vorhanden
```

### Windows:
```cmd
REM SSH (empfohlen)
git clone git@github.com:thetabish/ai-personas.git
REM oder HTTPS
git clone https://github.com/thetabish/ai-personas.git

cd ai-personas
run.bat
REM Script fragt automatisch nach API-Schlüssel falls keiner vorhanden
```

**Das war's!** Die Scripts richten automatisch alles ein:
✅ Python prüfen ✅ Abhängigkeiten installieren ✅ **API interaktiv eingeben** ✅ Demo starten

**Demo-Ergebnis:** 3 AI-Personas (Anna, Tom, Julia) beantworten Lifestyle-Fragen
- Ausgabe: `results.json` (Daten) und `results.md` (Bericht)

## ✨ Features

- 🤖 3 einzigartige AI-Personas (Anna, Tom, Julia)
- 🔗 LangChain + OpenRouter (kostenlos)
- 📝 JSON-Fragensystem
- 💻 Einfache CLI-Bedienung
- 📊 JSON/Markdown Ausgabe
- 🧠 Gedächtnissystem für kontextbewusste Antworten

## 🔧 Manuelle Installation

**Voraussetzungen:** Python 3.8+

```bash
# 1. Repository klonen
git clone git@github.com:thetabish/ai-personas.git
# oder: git clone https://github.com/thetabish/ai-personas.git
cd ai-personas

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. API-Schlüssel einrichten
cp .env.example .env
# Bearbeiten Sie .env und fügen Sie Ihren OpenRouter API-Schlüssel ein:
# OPENROUTER_API_KEY=sk-or-v1-ihr_schluessel_hier
# Schlüssel erhalten: https://openrouter.ai/mistralai/mistral-small-24b-instruct-2501:free/api

# 4. Demo starten
python interview.py --questions questions.json --format md --verbose
```

## 💻 Verwendung

```bash
# Basis-Interview
python interview.py --questions questions.json

# Mit Markdown-Ausgabe
python interview.py --questions questions.json --format md --verbose

# Eigene Ausgabedatei  
python interview.py --questions questions.json --output meine_befragung
```

### Eigene Fragen erstellen
```json
{
  "questions": [
    "Ihre erste Frage hier",
    "Ihre zweite Frage hier"
  ]
}
```

## 🛠️ Anpassung

### Neue Personas hinzufügen
```python
def create_neue_persona():
    return PersonaAgent(
        name="Max",
        age=25,
        characteristics="technikaffin, innovativ",
        background="Software-Entwickler...",
        detailed_personality="Du liebst neue Technologien..."
    )
```

### AI-Modell wechseln
In `.env` ändern:
```
DEFAULT_MODEL=mistralai/mistral-small-24b-instruct-2501:free
```

## 🔍 Fehlerbehebung

- **API-Schlüssel fehlt**: `.env` Datei prüfen
- **Abhängigkeiten fehlen**: `pip install -r requirements.txt`
- **Python fehlt**: Python 3.8+ von https://python.org installieren
- **Test**: `python agents.py`

## 📚 Tech Stack

- **LangChain** - AI Framework
- **OpenRouter** - API Gateway (kostenlos)
- **Python** - Programmiersprache

---

**MIT License** | **Viel Spaß beim Experimentieren! 🚀**
