#!/bin/bash

# =============================================================================
# Synthetisches Interview System - Schnell-Start Script (Linux/macOS)
# =============================================================================
# Dieses Script richtet alles ein und startet eine Demo in unter 5 Minuten!
# 
# Voraussetzungen:
# - Python 3.8+ installiert
# - Internet-Verbindung für Abhängigkeiten und API-Zugang
# =============================================================================

set -e  # Beende bei Fehlern

# Farben für bessere Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner anzeigen
echo -e "${PURPLE}"
echo "======================================================================"
echo "🚀 SYNTHETISCHES INTERVIEW SYSTEM - SCHNELL-START (Linux/macOS)"
echo "======================================================================"
echo -e "${NC}"
echo -e "${CYAN}Richtet alles ein und startet eine Demo in unter 5 Minuten!${NC}"
echo ""

# Schritt 1: Python-Version prüfen
echo -e "${BLUE}📋 Schritt 1/5: Python-Version prüfen...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python ${PYTHON_VERSION} gefunden${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python ${PYTHON_VERSION} gefunden${NC}"
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python nicht gefunden!${NC}"
    echo "Bitte installieren Sie Python 3.8+ über Ihren Paketmanager:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  CentOS/RHEL:   sudo yum install python3 python3-pip"
    echo "  macOS:         brew install python3"
    exit 1
fi

# Schritt 2: Virtuelle Umgebung erstellen
echo -e "${BLUE}📦 Schritt 2/5: Virtuelle Python-Umgebung einrichten...${NC}"
if [ ! -d "venv" ]; then
    echo "Erstelle virtuelle Umgebung..."
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}✓ Virtuelle Umgebung erstellt${NC}"
else
    echo -e "${GREEN}✓ Virtuelle Umgebung bereits vorhanden${NC}"
fi

# Virtuelle Umgebung aktivieren
echo "Aktiviere virtuelle Umgebung..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash)
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi
echo -e "${GREEN}✓ Virtuelle Umgebung aktiviert${NC}"

# Schritt 3: Abhängigkeiten installieren
echo -e "${BLUE}📚 Schritt 3/5: Python-Abhängigkeiten installieren...${NC}"
if [ -f "requirements.txt" ]; then
    pip install --quiet --upgrade pip
    pip install --quiet -r requirements.txt
    echo -e "${GREEN}✓ Alle Abhängigkeiten installiert${NC}"
else
    echo -e "${RED}❌ requirements.txt nicht gefunden!${NC}"
    exit 1
fi

# Schritt 4: Umgebungsvariablen einrichten
echo -e "${BLUE}🔑 Schritt 4/5: Umgebungsvariablen prüfen...${NC}"
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠️  .env Datei von .env.example erstellt${NC}"
        echo -e "${CYAN}📝 WICHTIG: Bitte fügen Sie Ihren OpenRouter API-Schlüssel hinzu:${NC}"
        echo ""
        echo -e "${YELLOW}   1. Kostenlosen API-Schlüssel erhalten: ${BLUE}https://openrouter.ai/mistralai/mistral-small-24b-instruct-2501:free/api${NC}"
        echo -e "${YELLOW}   2. In .env Datei eintragen: ${GREEN}OPENROUTER_API_KEY=ihr_schluessel_hier${NC}"
        echo ""
        echo -e "${CYAN}Drücken Sie Enter wenn Sie den API-Schlüssel eingetragen haben...${NC}"
        read -r
    else
        echo -e "${RED}❌ .env.example nicht gefunden!${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ .env Datei bereits vorhanden${NC}"
fi

# API-Schlüssel prüfen - prüfe auf gültigen sk-or-v1- Schlüssel
if grep -q "^OPENROUTER_API_KEY=sk-or-v1-" .env 2>/dev/null; then
    echo -e "${GREEN}✓ Gültiger API-Schlüssel gefunden${NC}"
else
    # Prüfe ob noch der Platzhalter drin steht
    if grep -q "^OPENROUTER_API_KEY=your_openrouter_api_key_here" .env 2>/dev/null; then
        echo -e "${RED}❌ Noch Standard-Platzhalter in .env Datei gefunden!${NC}"
        echo ""
        echo -e "${CYAN}Bitte geben Sie Ihren OpenRouter API-Schlüssel ein:${NC}"
    else
        echo -e "${RED}❌ Gültiger OpenRouter API-Schlüssel nicht gefunden!${NC}"
        echo ""
        echo -e "${CYAN}Bitte geben Sie Ihren OpenRouter API-Schlüssel ein:${NC}"
    fi
    echo ""
    echo -e "${YELLOW}So erhalten Sie einen kostenlosen API-Schlüssel:${NC}"
    echo -e "${CYAN}1. Gehen Sie zu: ${BLUE}https://openrouter.ai/mistralai/mistral-small-24b-instruct-2501:free/api${NC}"
    echo -e "${CYAN}2. Erstellen Sie ein kostenloses Konto${NC}"
    echo -e "${CYAN}3. Kopieren Sie Ihren API-Schlüssel${NC}"
    echo ""
    
    # Prompt für API-Schlüssel
    while true; do
        echo -e -n "${YELLOW}API-Schlüssel eingeben (beginnt mit sk-or-v1-): ${NC}"
        read -r USER_API_KEY
        
        # Validiere den eingegebenen API-Schlüssel
        if [ -z "$USER_API_KEY" ]; then
            echo -e "${RED}❌ Fehler: Kein API-Schlüssel eingegeben!${NC}"
            continue
        fi
        
        # Prüfe das Format
        if [[ "$USER_API_KEY" =~ ^sk-or-v1- ]]; then
            break
        else
            echo -e "${RED}❌ Fehler: API-Schlüssel muss mit 'sk-or-v1-' beginnen!${NC}"
            echo -e "${YELLOW}Ihr eingegebener Schlüssel: $USER_API_KEY${NC}"
            echo -e "${CYAN}Bitte versuchen Sie es erneut.${NC}"
            echo ""
        fi
    done
    
    # Speichere den neuen API-Schlüssel in der .env Datei
    echo -e "${CYAN}Speichere API-Schlüssel in .env Datei...${NC}"
    sed -i.bak "s/^OPENROUTER_API_KEY=.*/OPENROUTER_API_KEY=$USER_API_KEY/" .env
    echo -e "${GREEN}✓ Gültiger API-Schlüssel gespeichert!${NC}"
fi

# Schritt 5: Demo starten
echo -e "${BLUE}🎤 Schritt 5/5: Demo starten...${NC}"
echo ""
echo -e "${GREEN}======================================================================"
echo "🎉 SETUP ABGESCHLOSSEN! Starte Demo..."
echo "======================================================================${NC}"
echo ""

# Überprüfe ob questions.json existiert
if [ ! -f "questions.json" ]; then
    echo -e "${YELLOW}⚠️  questions.json nicht gefunden, erstelle Beispiel-Fragen...${NC}"
    cat > questions.json << 'EOF'
{
  "questions": [
    "Was ist Ihnen bei einer Lifestyle-Marke am wichtigsten?",
    "Wie entscheiden Sie sich zwischen verschiedenen Marken?",
    "Welche Rolle spielen soziale Medien bei Ihren Kaufentscheidungen?",
    "Wie wichtig ist Nachhaltigkeit für Sie bei Marken?",
    "Was würde Sie dazu bringen, eine neue Marke auszuprobieren?"
  ]
}
EOF
    echo -e "${GREEN}✓ Beispiel-Fragen erstellt${NC}"
fi

echo -e "${CYAN}Starte synthetisches Interview mit Beispiel-Fragen...${NC}"
echo ""

# Demo ausführen
echo -e "${CYAN}Starte synthetisches Interview mit allen Agenten...${NC}"
$PYTHON_CMD interview.py questions.json

echo ""
echo -e "${GREEN}======================================================================"
echo "🎊 DEMO ABGESCHLOSSEN!"
echo "======================================================================${NC}"
echo ""
echo -e "${CYAN}📄 Die Ergebnisse wurden gespeichert mit Zeitstempel:${NC}"
echo -e "${YELLOW}   - interview_results_[timestamp].md (Markdown-Format)${NC}"
echo -e "${YELLOW}   - interview_results_[timestamp].json (JSON-Format)${NC}"
echo ""
echo -e "${CYAN}🔄 Weitere Interview-Optionen:${NC}"
echo -e "${YELLOW}   # Alle Agenten:${NC}"
echo -e "${YELLOW}   $PYTHON_CMD interview.py questions.json${NC}"
echo ""
echo -e "${YELLOW}   # Einzelner Agent:${NC}"
echo -e "${YELLOW}   $PYTHON_CMD interview.py anna questions.json${NC}"
echo -e "${YELLOW}   $PYTHON_CMD interview.py tom questions.json${NC}"
echo -e "${YELLOW}   $PYTHON_CMD interview.py julia questions.json${NC}"
echo ""
echo -e "${YELLOW}   # JSON-Format:${NC}"
echo -e "${YELLOW}   $PYTHON_CMD interview.py questions.json --format json${NC}"
echo ""
echo -e "${CYAN}🤖 Automatisierung (Batch-Modus):${NC}"
echo -e "${YELLOW}   # Einmaliger Batch-Lauf:${NC}"
echo -e "${YELLOW}   $PYTHON_CMD run_batch.py${NC}"
echo ""
echo -e "${YELLOW}   # Für Cron-Jobs (automatisiert):${NC}"
echo -e "${YELLOW}   0 9 * * 1 cd $(pwd) && $PYTHON_CMD run_batch.py${NC}"
echo ""
echo -e "${CYAN}📝 Um eigene Fragen zu verwenden:${NC}"
echo -e "${YELLOW}   1. Bearbeiten Sie questions.json oder interview_batch.json${NC}"
echo -e "${YELLOW}   2. Führen Sie das Interview erneut aus${NC}"
echo ""
echo -e "${CYAN}📚 Weitere Optionen:${NC}"
echo -e "${YELLOW}   $PYTHON_CMD interview.py --help${NC}"
echo -e "${YELLOW}   $PYTHON_CMD run_batch.py --help${NC}"
echo ""
echo -e "${GREEN}Vielen Dank fürs Ausprobieren! 🚀${NC}"
