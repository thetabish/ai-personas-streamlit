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
REM Command Prompt (cmd) - Empfohlen
git clone https://github.com/thetabish/ai-personas.git
cd ai-personas
run.bat
```

```powershell
# PowerShell - Alternative
git clone https://github.com/thetabish/ai-personas.git
cd ai-personas
.\run.bat
# oder: cmd /c run.bat
```

> **Was machen die Scripts?** `run.sh` und `run.bat` sind vollautomatische Setup-Scripts, die:
> - Python-Installation prüfen
> - Virtuelle Umgebung erstellen  
> - Alle Abhängigkeiten installieren
> - API-Schlüssel interaktiv abfragen (falls fehlend)
> - Sofort eine Demo mit 3 AI-Personas starten

**Das war's!** Die Scripts richten automatisch alles ein:
✅ Python prüfen ✅ Abhängigkeiten installieren ✅ **API interaktiv eingeben** ✅ Demo starten

**💡 Windows-Tipp:** Bei PowerShell verwenden Sie `.\run.bat` - Command Prompt (cmd) ist empfohlen!

**Demo-Ergebnis:** 3 AI-Personas (Anna, Tom, Julia) beantworten Lifestyle-Fragen
- Ausgabe: `results.json` (Daten) und `results.md` (Bericht)

## ✨ Features

- 🤖 **3 einzigartige AI-Personas** (Anna, Tom, Julia)
- 🎯 **Flexibler Interview-Modus** (alle Personas oder einzeln)
- 🔗 **LangChain + OpenRouter** (kostenlos)
- 📝 **JSON-Fragensystem** (einfach anpassbar)
- 💻 **CLI & Python API** (Kommandozeile + programmierbar)
- 📊 **JSON/Markdown Ausgabe** (strukturierte Daten + Berichte)
- 🧠 **Unabhängige Persona-Gedächtnisse** (konsistente Antworten)
- ⚡ **Kostenfrei** (Mistral AI über OpenRouter)

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
python interview.py --questions questions.json
```

## 💻 Verwendung

### CLI (Kommandozeile)
```bash
# Basis-Interview (alle Personas, Markdown-Ausgabe)
python interview.py --questions questions.json

# JSON-Format gewünscht
python interview.py --questions questions.json --format json

# Eigene Ausgabedatei  
python interview.py --questions questions.json --output meine_befragung
```

### Programmable API (Python Import)

**Flexibler `run_interview()` - zwei Modi:**

#### 1. Alle Personas (Standard)
```python
from interview import run_interview

# Alle 3 Personas antworten (Anna, Tom, Julia)
results = run_interview("questions.json")

# Mit Format-Optionen
results = run_interview("questions.json", format="json")
results = run_interview("questions.json", output_file="my_study")
```

#### 2. Einzelne Persona
```python
# Nur Anna antwortet
results = run_interview("anna", "questions.json")

# Nur Tom antwortet
results = run_interview("tom", "questions.json") 

# Nur Julia antwortet
results = run_interview("julia", "questions.json")

# Mit Format-Optionen
results = run_interview("anna", "questions.json", format="json")
```

**Verfügbare Agenten abrufen:**
```python
from interview import get_available_agents
agents = get_available_agents()  # ['anna', 'tom', 'julia']
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

## 🏗️ Technische Architektur & Entscheidungen

### Warum Mistral AI?
- **Kostenlos**: Mistral Small über OpenRouter ist völlig kostenlos
- **Qualität**: Hochwertiges mehrsprachiges Modell (DE/EN)
- **Performance**: Schnelle Antwortzeiten für Interviews
- **Konsistenz**: Stabile Persona-Charakteristiken

### Warum OpenRouter?
- **Kostenkontrolle**: Kostenlose Modelle ohne versteckte Gebühren
- **Einfachheit**: Ein API-Schlüssel für viele AI-Modelle
- **Zuverlässigkeit**: Professioneller API-Gateway mit hoher Verfügbarkeit
- **Flexibilität**: Einfacher Modellwechsel ohne Code-Änderungen

### LangChain Integration
```python
# Vereinfachter Workflow:
PersonaAgent → LangChain → OpenRouter → Mistral AI → Antwort
```

**Warum LangChain?**
- **Abstraktion**: Einheitliche Schnittstelle für verschiedene AI-Modelle
- **Kontext-Management**: Automatische Verwaltung von Gesprächsverläufen
- **Prompt-Engineering**: Strukturierte Prompts für konsistente Ergebnisse
- **Zukunftssicherheit**: Einfacher Wechsel zwischen AI-Anbietern

### Programm-Flow
1. **Setup**: API-Validierung → Persona-Erstellung (LangChain)
2. **Interview**: Jede Persona antwortet unabhängig (eigener Kontext)
3. **Speicherung**: Strukturierte JSON/Markdown-Ausgabe
4. **Gedächtnis**: Personas erinnern sich an eigene Antworten (konsistent)

### Persona-Unabhängigkeit
```python
# Jede Persona ist eine eigene "Person"
Anna.respond(question, previous_responses=[])  # Keine anderen Antworten
Tom.respond(question, previous_responses=[])   # Nur eigener Kontext
Julia.respond(question, previous_responses=[]) # Unabhängige Meinung
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
- **Windows PowerShell**: Verwenden Sie `.\run.bat` statt `run.bat`
- **Command Prompt empfohlen**: Öffnen Sie `cmd` statt PowerShell für beste Kompatibilität
- **Test**: `python agents.py`

## 📚 Tech Stack & Rationale

### Core Technologies
- **🐍 Python 3.8+** - Robust, weitverbreitet, große AI-Community
- **🔗 LangChain** - De-facto Standard für AI-Anwendungen, vereinfacht Prompt-Management
- **🌐 OpenRouter** - Kostengünstigster Zugang zu hochwertigen AI-Modellen
- **🤖 Mistral AI** - Beste kostenlose Option: mehrsprachig, konsistent, schnell

### Warum diese Kombination?
- **Kosten**: Völlig kostenfrei durch OpenRouter + Mistral
- **Qualität**: Professionelle Ergebnisse ohne Kompromisse
- **Entwicklung**: Schnelle Iteration durch LangChain-Abstraktion
- **Skalierung**: Einfacher Wechsel zu anderen Modellen bei Bedarf

**Gesamtkosten: 0€** 💰 (Ideal für Experimente und kleine Projekte)

---

**MIT License** | **Viel Spaß beim Experimentieren! 🚀**
