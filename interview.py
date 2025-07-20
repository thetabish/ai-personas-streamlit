#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synthetisches Interview System
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
        # Prüfe API-Schlüssel bevor Personas erstellt werden
        if not validate_api_key():
            print("\n❌ Setup fehlgeschlagen: Ungültiger oder fehlender API-Schlüssel")
            print("Bitte richten Sie Ihren OpenRouter API-Schlüssel ein, bevor Sie fortfahren.")
            return False
            
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
        Stellt eine Frage an alle Personas und sammelt ihre Antworten
        
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
        
        # Sammle vorherige Antworten (damit Personas aufeinander reagieren können)
        previous_responses = []
        
        # Frage jede Persona einzeln
        for persona in self.personas:
            print(f"  {persona.name} antwortet...")
            
            # Hole die Antwort von der Persona
            response = persona.respond(question_text, previous_responses)
            
            # Erstelle ein Datenpaket für diese Antwort
            response_data = {
                "agent_id": persona.name,
                "agent_age": persona.age,
                "response": response,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            # Speichere die Antwort
            question_results["responses"].append(response_data)
            previous_responses.append(response_data)
            
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
  python interview.py --questions questions.json --format md --verbose
  python interview.py --questions questions.json --output meine_befragung
        """
    )
    
    # Alle verfügbaren Optionen
    parser.add_argument("--questions", required=True, 
                       help="Pfad zur JSON-Datei mit Fragen")
    parser.add_argument("--output", default="results", 
                       help="Ausgabedateiname (ohne Erweiterung)")
    parser.add_argument("--format", choices=["json", "md"], default="json", 
                       help="Ausgabeformat (Standard: json)")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Ausführliche Ausgabe mit mehr Details")
    
    return parser


def main():
    """
    Hauptfunktion - hier läuft das ganze Programm ab
    Diese Funktion koordiniert alle anderen Funktionen
    """
    # 1. Kommandozeilen-Argumente einrichten
    parser = setup_command_line_arguments()
    args = parser.parse_args()
    
    # 2. Prüfen ob API-Schlüssel vorhanden ist
    if not validate_api_key():
        sys.exit(1)
    
    # 3. Interview Manager erstellen und Personas einrichten
    interview_manager = InterviewManager()
    
    if args.verbose:
        print("🤖 Initialisiere LangChain Personas...")
    
    if not interview_manager.setup_personas():
        print("Stellen Sie sicher, dass Sie die erforderlichen Abhängigkeiten installiert haben:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    if args.verbose:
        print(f"✓ {interview_manager.get_personas_count()} Personas erstellt:")
        interview_manager.print_personas_info()
    
    # 4. Fragen aus der JSON-Datei laden
    questions = load_questions_from_file(args.questions)
    print(f"\n📋 {len(questions)} Fragen geladen aus {args.questions}")
    
    if args.verbose:
        print("Fragen:")
        for i, question in enumerate(questions, 1):
            print(f"  {i}. {question}")
    
    # 5. Das Interview durchführen
    print("\n" + "="*60)
    print("🎤 SYNTHETISCHES INTERVIEW STARTEN")
    print("="*60)
    
    try:
        # Hier passiert die Hauptarbeit: Interview durchführen
        interview_results = interview_manager.run_full_interview(questions)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interview vom Benutzer unterbrochen")
        sys.exit(1)
    except Exception as error:
        print(f"\n\n❌ Fehler während des Interviews: {error}")
        sys.exit(1)
    
    # 6. Ergebnisse speichern und Zusammenfassung anzeigen
    print("\n" + "="*60)
    print("✅ INTERVIEW ABGESCHLOSSEN")
    print("="*60)
    
    try:
        # Speichere die Ergebnisse
        save_interview_results(interview_results, args.format, args.output)
        
        # Zeige eine schöne Zusammenfassung
        print_interview_summary(interview_results, args.format, args.output)
        
        if args.verbose:
            print(f"🎯 Verwendete Hauptklasse: InterviewManager")
            
    except Exception as error:
        print(f"❌ Fehler beim Speichern der Ergebnisse: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
