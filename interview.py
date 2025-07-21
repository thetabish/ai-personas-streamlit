#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synthetisches Interview System

Hauptfunktion: run_interview() - für sowohl CLI als auch programmatische Nutzung
"""

import argparse
import json
import sys
import datetime
from typing import List, Dict
from agents import create_personas, PersonaAgent, validate_api_key

# Windows console encoding fix
if sys.platform.startswith('win'):
    import locale
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
    sys.stdout.reconfigure(encoding='utf-8')


class InterviewManager:
    """
    Klasse zum Verwalten von Interviews mit AI-Personas
    Diese Klasse hält alle Personas und führt Interviews durch
    """
    
    def __init__(self):
        """Initialisiert den Interview Manager ohne Personas"""
        self.personas = []
    
    def setup_personas(self):
        """Erstellt und speichert die AI-Personas für das Interview"""
        try:
            self.personas = create_personas()
            return True
        except Exception as e:
            print(f"Fehler beim Erstellen der Personas: {e}")
            return False
    
    def get_personas_count(self):
        """Gibt die Anzahl der verfügbaren Personas zurück"""
        return len(self.personas)
    
    def print_personas_info(self):
        """Zeigt Informationen über alle Personas an"""
        for persona in self.personas:
            print(f"  - {persona.name} ({persona.age}): {persona.characteristics}")
    
    def ask_question_to_all(self, question_number, question_text):
        """
        Stellt eine Frage an alle Personas und sammelt ihre unabhängigen Antworten
        
        Args:
            question_number: Nummer der Frage (1, 2, 3...)
            question_text: Der Text der Frage
            
        Returns:
            Dictionary mit allen Antworten für diese Frage
        """
        print(f"\nFrage {question_number}: {question_text}")
        
        # Erstelle ein Datenpaket für diese Frage
        question_results = {
            "question_id": question_number,
            "question": question_text,
            "responses": []
        }
        
        # Frage jede Persona einzeln - OHNE vorherige Antworten zu teilen
        for persona in self.personas:
            print(f"  {persona.name} antwortet...")
            
            # Hole die unabhängige Antwort von der Persona (keine previous_responses)
            response = persona.respond(question_text, [])
            
            # Erstelle ein Datenpaket für diese Antwort
            response_data = {
                "agent_id": persona.name,
                "agent_age": persona.age,
                "response": response,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            # Speichere die Antwort
            question_results["responses"].append(response_data)
            
            # Zeige die Antwort an
            print(f"  {persona.name}: {response}")
        
        return question_results
    
    def run_full_interview(self, questions_list):
        """
        Führt ein komplettes Interview mit allen Fragen durch
        
        Args:
            questions_list: Liste von Fragen als Strings
            
        Returns:
            Dictionary mit allen Interview-Ergebnissen
        """
        # Erstelle das Haupt-Ergebnis-Paket
        interview_results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "agents": [persona.get_agent_info() for persona in self.personas],
            "interview_data": []
        }
        
        # Gehe durch jede Frage
        for question_index, question_text in enumerate(questions_list):
            question_number = question_index + 1  # Menschen zählen ab 1, nicht 0
            
            # Stelle die Frage an alle Personas
            question_results = self.ask_question_to_all(question_number, question_text)
            
            # Speichere die Ergebnisse dieser Frage
            interview_results["interview_data"].append(question_results)
        
        return interview_results
    

def save_interview_results(interview_results, output_format="json", filename=None):
    """
    Speichert die Interview-Ergebnisse in eine Datei
    
    Args:
        interview_results: Das Dictionary mit allen Interview-Daten
        output_format: "json" oder "md" (Markdown)
        filename: Name der Ausgabedatei (ohne Endung)
    """
    # Wenn kein Dateiname angegeben, erstelle einen mit Zeitstempel
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"interview_ergebnisse_{timestamp}"
    
    # Speichere als JSON-Datei
    if output_format.lower() == "json":
        save_as_json_file(interview_results, filename)
        
    # Speichere als Markdown-Datei
    elif output_format.lower() == "md":
        save_as_markdown_file(interview_results, filename)


def save_as_json_file(interview_results, filename):
    """
    Speichert die Ergebnisse als JSON-Datei
    JSON ist ein Standard-Format für Daten
    """
    full_filename = f"{filename}.json"
    with open(full_filename, "w", encoding="utf-8") as file:
        json.dump(interview_results, file, indent=2, ensure_ascii=False)
    print(f"Ergebnisse gespeichert in {full_filename}")


def save_as_markdown_file(interview_results, filename):
    """
    Speichert die Ergebnisse als Markdown-Datei (.md)
    Markdown ist ein Format für schön formatierte Texte
    """
    full_filename = f"{filename}.md"
    
    with open(full_filename, "w", encoding="utf-8") as file:
        # Schreibe den Titel
        file.write("# Synthetische Interview Ergebnisse\n\n")
        file.write(f"**Zeitstempel:** {interview_results['timestamp']}\n\n")
        
        # Schreibe die Teilnehmer-Informationen
        file.write("## Teilnehmer\n\n")
        for agent in interview_results['agents']:
            file.write(f"- **{agent['name']}** ({agent['age']} Jahre): {agent['characteristics']}\n")
        
        # Schreibe alle Fragen und Antworten
        file.write("\n## Interview Fragen & Antworten\n\n")
        for question_data in interview_results['interview_data']:
            file.write(f"### Frage {question_data['question_id']}: {question_data['question']}\n\n")
            
            for response in question_data['responses']:
                file.write(f"**{response['agent_id']}:** {response['response']}\n\n")
            
            file.write("---\n\n")  # Trennlinie zwischen Fragen
    
    print(f"Ergebnisse gespeichert in {full_filename}")


def load_questions_from_file(filepath):
    """
    Lädt Fragen aus einer JSON-Datei
    
    Args:
        filepath: Der Pfad zur JSON-Datei mit den Fragen
        
    Returns:
        Eine Liste von Fragen als Strings
    """
    try:
        # Öffne die Datei und lese sie
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # Handhabe verschiedene JSON-Formate:
            # Format 1: {"questions": ["Frage1", "Frage2"]}
            # Format 2: ["Frage1", "Frage2"]
            if isinstance(data, dict):
                return data.get('questions', data)
            else:
                return data
                
    except FileNotFoundError:
        print(f"Fehler: Fragen-Datei '{filepath}' nicht gefunden.")
        print("Stellen Sie sicher, dass die Datei existiert!")
        sys.exit(1)
        
    except json.JSONDecodeError:
        print(f"Fehler: Ungültiges JSON in '{filepath}'.")
        print("Prüfen Sie die JSON-Syntax in der Datei!")
        sys.exit(1)


def print_interview_summary(interview_results, output_format, output_filename):
    """
    Zeigt eine schöne Zusammenfassung des Interviews an
    
    Args:
        interview_results: Die Interview-Ergebnisse
        output_format: Das verwendete Ausgabeformat
        output_filename: Der Name der Ausgabedatei
    """
    # Berechne Statistiken
    persona_count = len(interview_results.get('agents', []))
    question_count = len(interview_results.get('interview_data', []))
    total_responses = sum(len(q['responses']) for q in interview_results['interview_data'])
    
    print(f"\n📊 Interview Zusammenfassung:")
    print(f"  - {persona_count} Teilnehmer")
    print(f"  - {question_count} Fragen")
    print(f"  - {total_responses} Gesamtantworten")
    print(f"  - Zeitstempel: {interview_results['timestamp']}")
    print(f"\n💾 Ausgabe gespeichert als {output_format.upper()}-Format in {output_filename}.{output_format}")


def setup_command_line_arguments():
    """
    Richtet alle Kommandozeilen-Optionen ein
    
    Returns:
        Den ArgumentParser für die Kommandozeile
    """
    parser = argparse.ArgumentParser(
        description="Führe synthetische Interviews mit LangChain AI-Personas über OpenRouter durch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
📝 Beispiele für die Nutzung:
  python interview.py --questions questions.json
  python interview.py --questions questions.json --format json
  python interview.py --questions questions.json --output meine_befragung
        """
    )
    
    # Alle verfügbaren Optionen
    parser.add_argument("--questions", required=True, 
                       help="Pfad zur JSON-Datei mit Fragen")
    parser.add_argument("--output", default="results", 
                       help="Ausgabedateiname (ohne Erweiterung)")
    parser.add_argument("--format", choices=["json", "md"], default="md", 
                       help="Ausgabeformat (Standard: md)")

    
    return parser


def main():
    """
    Hauptfunktion für CLI-Nutzung - parst Argumente und ruft run_interview() auf
    """
    # Kommandozeilen-Argumente einrichten und parsen
    parser = setup_command_line_arguments()
    args = parser.parse_args()
    
    # Interview mit den geparsten Argumenten ausführen (CLI nutzt immer alle Agenten)
    result = run_interview(
        agent_or_questions=args.questions,
        questions_file=None,  # CLI Modus - alle Agenten
        format=args.format,
        output_file=args.output
    )
    
    # Exit-Code setzen basierend auf Erfolg/Fehler
    if result is None:
        sys.exit(1)
    else:
        sys.exit(0)


# =====================================
# CORE INTERVIEW FUNCTION
# =====================================

def run_interview(agent_or_questions, questions_file=None, format="md", output_file=None):
    """
    Führt ein Interview mit AI-Personas durch
    
    Args:
        agent_or_questions: Entweder Agenten-Name (str) oder Questions-Datei (str)
        questions_file: Questions-Datei (nur wenn erster Parameter ein Agent ist)
        format: Ausgabeformat - "md" für Markdown oder "json" (Standard: "md")
        output_file: Dateiname ohne Endung (Standard: automatischer Zeitstempel)
        
    Returns:
        Dictionary mit Interview-Ergebnissen oder None bei Fehler
        
    Examples:
        # Alle Personas (alle antworten)
        results = run_interview("questions.json")
        
        # Nur eine bestimmte Persona
        results = run_interview("anna", "questions.json")
        results = run_interview("tom", "questions.json")
        
        # Mit Format-Optionen
        results = run_interview("julia", "questions.json", format="json")
        results = run_interview("questions.json", format="json")
    """
    try:
        # Bestimme Modus basierend auf Parametern
        if questions_file is None:
            # Modus: run_interview("questions.json") - alle Personas
            actual_questions_file = agent_or_questions
            selected_agent = None
        else:
            # Modus: run_interview("anna", "questions.json") - nur eine Persona
            selected_agent = agent_or_questions.lower()
            actual_questions_file = questions_file
        
        # 1. Validierung der Umgebung
        if not validate_api_key():
            print("❌ Setup fehlgeschlagen: Ungültiger oder fehlender API-Schlüssel")
            return None
        
        # 2. Interview Manager erstellen und Personas einrichten
        interview_manager = InterviewManager()
        
        print("🤖 Initialisiere LangChain Personas...")
        
        if not interview_manager.setup_personas():
            print("❌ Fehler beim Erstellen der Personas")
            print("Stellen Sie sicher, dass Sie die erforderlichen Abhängigkeiten installiert haben:")
            print("  pip install -r requirements.txt")
            return None
        
        # 3. Bei ausgewähltem Agent prüfen ob verfügbar
        if selected_agent:
            available_agents = [p.name.lower() for p in interview_manager.personas]
            if selected_agent not in available_agents:
                print(f"❌ Agent '{selected_agent}' nicht gefunden.")
                print(f"Verfügbare Agenten: {', '.join([p.name for p in interview_manager.personas])}")
                return None
            
            print(f"✓ Einzelner Agent ausgewählt: {selected_agent.title()}")
            # Filtere Personas auf den gewählten Agent
            interview_manager.personas = [p for p in interview_manager.personas if p.name.lower() == selected_agent]
        else:
            print(f"✓ {interview_manager.get_personas_count()} Personas erstellt:")
        
        interview_manager.print_personas_info()
        
        # 4. Fragen aus JSON-Datei laden
        try:
            questions_list = load_questions_from_file(actual_questions_file)
        except Exception as e:
            print(f"❌ Fehler beim Laden der Fragen aus {actual_questions_file}: {e}")
            return None
        
        print(f"\n📋 {len(questions_list)} Fragen geladen aus {actual_questions_file}")
        print("Fragen:")
        for i, question in enumerate(questions_list, 1):
            print(f"  {i}. {question}")
        
        # 5. Das Interview durchführen
        print("\n" + "="*60)
        print("🎤 SYNTHETISCHES INTERVIEW STARTEN")
        print("="*60)
        
        try:
            interview_results = interview_manager.run_full_interview(questions_list)
        except KeyboardInterrupt:
            print("\n\n⚠️  Interview vom Benutzer unterbrochen")
            return None
        except Exception as error:
            print(f"\n\n❌ Fehler während des Interviews: {error}")
            return None
        
        # 6. Ergebnisse speichern
        print("\n" + "="*60)
        print("✅ INTERVIEW ABGESCHLOSSEN")
        print("="*60)
        
        # Wenn kein Output-Dateiname angegeben, erstelle einen mit Zeitstempel
        if output_file is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"interview_results_{timestamp}"
        
        save_interview_results(interview_results, format, output_file)
        
        print_interview_summary(interview_results, format, output_file)
        print(f"🎯 Verwendete Hauptklasse: InterviewManager")
        
        return interview_results
        
    except Exception as error:
        print(f"❌ Fehler beim Interview: {error}")
        return None


def get_available_agents():
    """
    Gibt eine Liste der verfügbaren Agent-Namen zurück
    
    Returns:
        Liste von Agent-Namen (lowercase für run_interview Verwendung)
    """
    try:
        manager = InterviewManager()
        if manager.setup_personas():
            return [persona.name.lower() for persona in manager.personas]
        else:
            return []
    except Exception:
        return []


if __name__ == "__main__":
    main()
