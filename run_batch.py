#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Interview Runner - Cron-kompatibles Skript für automatisierte Interviews

Dieses Skript führt Batch-Interviews basierend auf einer Konfigurationsdatei durch.
Es ist für die Verwendung mit cron oder anderen Scheduling-Systemen optimiert.

Usage:
    python run_batch.py [config_file] [--agent AGENT_NAME] [--output-dir DIR] [--log-file LOG]

Examples:
    python run_batch.py                                    # Verwendet interview_batch.json
    python run_batch.py custom_batch.json                  # Verwendet benutzerdefinierte Datei
    python run_batch.py --agent anna                       # Nur Agent Anna
"""

import argparse
import json
import logging
import os
import sys
import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Import our interview functionality
from interview import run_interview, get_available_agents


class BatchInterviewRunner:
    """
    Klasse für die Durchführung von Batch-Interviews
    """
    
    def __init__(self, output_dir: str = "batch_results", log_file: str = "batch_interview.log"):
        """
        Initialisiert den Batch Runner
        
        Args:
            output_dir: Verzeichnis für die Ergebnisse
            log_file: Name der Log-Datei (wird im output_dir gespeichert)
        """
        self.output_dir = Path(output_dir)
        
        # Erstelle Output-Verzeichnis falls es nicht existiert
        self.output_dir.mkdir(exist_ok=True)
        
        # Log-Datei im output_dir speichern
        self.log_file = str(self.output_dir / log_file)
        
        # Setup Logging
        self._setup_logging()
        
        self.logger = logging.getLogger(__name__)
        
    def _setup_logging(self):
        """Konfiguriert das Logging-System"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def load_batch_config(self, config_file: str) -> Dict:
        """
        Lädt die Batch-Konfiguration aus einer JSON-Datei
        
        Args:
            config_file: Pfad zur Konfigurationsdatei
            
        Returns:
            Dictionary mit der Batch-Konfiguration
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validiere die Konfiguration
            if 'questions' not in config:
                raise ValueError("Batch-Konfiguration muss 'questions' enthalten")
            
            if not isinstance(config['questions'], list):
                raise ValueError("'questions' muss eine Liste sein")
            
            self.logger.info(f"Batch-Konfiguration geladen: {len(config['questions'])} Fragen")
            return config
            
        except FileNotFoundError:
            self.logger.error(f"Konfigurationsdatei nicht gefunden: {config_file}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Ungültige JSON-Datei: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Fehler beim Laden der Konfiguration: {e}")
            raise
    
    def create_temp_questions_file(self, questions: List[str]) -> str:
        """
        Erstellt eine temporäre Fragen-Datei für das Interview
        
        Args:
            questions: Liste der Fragen
            
        Returns:
            Pfad zur temporären Datei
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_file = self.output_dir / f"temp_questions_{timestamp}.json"
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        
        return str(temp_file)
    
    def run_batch_interview(self, config: Dict, agent: Optional[str] = None) -> bool:
        """
        Führt ein Batch-Interview durch
        
        Args:
            config: Batch-Konfiguration
            agent: Optionaler spezifischer Agent (None für alle)
            
        Returns:
            True wenn erfolgreich, False bei Fehler
        """
        try:
            # Erstelle temporäre Fragen-Datei
            temp_questions_file = self.create_temp_questions_file(config['questions'])
            
            # Bestimme Output-Dateinamen
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            if agent:
                output_base = f"batch_{agent}_{timestamp}"
            else:
                output_base = f"batch_all_{timestamp}"
            
            output_file = str(self.output_dir / output_base)
            
            # Log Interview-Start
            if agent:
                self.logger.info(f"Starte Batch-Interview für Agent: {agent}")
            else:
                self.logger.info("Starte Batch-Interview für alle Agenten")
            
            # Führe das Interview durch
            if agent:
                results = run_interview(agent, temp_questions_file, format="md", output_file=output_file)
            else:
                results = run_interview(temp_questions_file, format="md", output_file=output_file)
            
            # Lösche temporäre Datei
            os.unlink(temp_questions_file)
            
            if results:
                self.logger.info(f"Batch-Interview erfolgreich abgeschlossen: {output_file}.md")
                
                # Speichere auch JSON-Version für weitere Verarbeitung
                json_output = output_file + "_data.json"
                with open(json_output, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                
                self.logger.info(f"Interview-Daten gespeichert: {json_output}")
                return True
            else:
                self.logger.error("Interview fehlgeschlagen - keine Ergebnisse erhalten")
                return False
                
        except Exception as e:
            self.logger.error(f"Fehler beim Batch-Interview: {e}")
            return False
    
    def _simulate_webhook(self, config_file: str, agent: Optional[str], success: bool):
        """
        Simuliert das Versenden eines Webhooks nach dem Batch-Lauf
        
        Args:
            config_file: Verwendete Konfigurationsdatei
            agent: Verwendeter Agent (None für alle)
            success: Erfolg des Batch-Laufs
        """
        timestamp = datetime.datetime.now().isoformat()
        
        # Erstelle Webhook-Payload (als dict für bessere Lesbarkeit)
        webhook_payload = {
            "event": "batch_interview_completed",
            "timestamp": timestamp,
            "config_file": config_file,
            "agent": agent or "all",
            "success": success,
            "output_directory": str(self.output_dir),
            "log_file": self.log_file
        }
        
        # Simuliere Webhook-Versendung durch Logging
        self.logger.info("=" * 40)
        self.logger.info("WEBHOOK SIMULATION")
        self.logger.info("=" * 40)
        self.logger.info("Simulating webhook POST to configured endpoint...")
        self.logger.info(f"Webhook URL: https://your-webhook-endpoint.com/batch-complete")
        self.logger.info(f"Method: POST")
        self.logger.info(f"Content-Type: application/json")
        self.logger.info("Payload:")
        
        # Log payload als formatierten JSON
        payload_json = json.dumps(webhook_payload, indent=2, ensure_ascii=False)
        for line in payload_json.split('\n'):
            self.logger.info(f"  {line}")
        
        self.logger.info("Webhook simulation completed.")
        self.logger.info("=" * 40)
    
    def run_batch(self, config_file: str, agent: Optional[str] = None) -> bool:
        """
        Führt einen kompletten Batch-Lauf durch
        
        Args:
            config_file: Pfad zur Konfigurationsdatei
            agent: Optionaler spezifischer Agent
            
        Returns:
            True wenn erfolgreich, False bei Fehler
        """
        try:
            self.logger.info("="*60)
            self.logger.info("Batch Interview Runner gestartet")
            self.logger.info("="*60)
            
            # Lade Konfiguration
            config = self.load_batch_config(config_file)
            
            # Validiere Agent falls angegeben
            if agent:
                available_agents = get_available_agents()
                if agent.lower() not in available_agents:
                    self.logger.error(f"Unbekannter Agent: {agent}")
                    self.logger.info(f"Verfügbare Agenten: {', '.join(available_agents)}")
                    return False
                agent = agent.lower()
            
            # Führe Interview durch
            success = self.run_batch_interview(config, agent)
            
            # Log Ergebnis
            if success:
                self.logger.info("Batch-Lauf erfolgreich abgeschlossen")
            else:
                self.logger.error("Batch-Lauf fehlgeschlagen")
            
            # Simuliere Webhook-Versendung
            self._simulate_webhook(config_file, agent, success)
            
            self.logger.info("="*60)
            return success
            
        except Exception as e:
            self.logger.error(f"Kritischer Fehler beim Batch-Lauf: {e}")
            return False


def main():
    """Hauptfunktion für CLI-Verwendung"""
    parser = argparse.ArgumentParser(
        description="Batch Interview Runner für automatisierte Interviews",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python run_batch.py                                    # Verwendet interview_batch.json
  python run_batch.py custom_batch.json                  # Verwendet benutzerdefinierte Datei
  python run_batch.py --agent anna                       # Nur Agent Anna
  python run_batch.py --output-dir ./results --log-file batch.log

Für cron-Jobs (einfachste Verwendung):
  0 9 * * 1 cd /path/to/project && python run_batch.py
        """
    )
    
    parser.add_argument(
        'config_file',
        nargs='?',
        default='interview_batch.json',
        help='Pfad zur Batch-Konfigurationsdatei (Standard: interview_batch.json)'
    )
    
    parser.add_argument(
        '--agent',
        help='Spezifischer Agent für das Interview (z.B. anna, tom, julia)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='batch_results',
        help='Verzeichnis für die Ergebnisse (Standard: batch_results)'
    )
    
    parser.add_argument(
        '--log-file',
        default='batch_interview.log',
        help='Log-Datei Name (wird im output-dir gespeichert, Standard: batch_interview.log)'
    )
    
    args = parser.parse_args()
    
    # Erstelle Batch Runner
    runner = BatchInterviewRunner(
        output_dir=args.output_dir,
        log_file=args.log_file
    )
    
    # Führe Batch-Lauf durch
    success = runner.run_batch(args.config_file, args.agent)
    
    # Exit mit entsprechendem Code für Cron-Jobs
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
