#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Einfacher Setup-Checker für das Synthetische Interview System
"""

import os
from dotenv import load_dotenv

def check_setup():
    """Prüft ob alles korrekt eingerichtet ist"""
    print("🔍 Prüfe System-Setup...")
    print()
    
    # .env Datei laden
    if os.path.exists('.env'):
        load_dotenv()
        print("✅ .env Datei gefunden")
    else:
        print("❌ .env Datei nicht gefunden!")
        return False
    
    # API-Schlüssel prüfen
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY nicht in .env Datei gefunden!")
        return False
    
    if api_key == "your_openrouter_api_key_here":
        print("❌ Standard-Platzhalter gefunden!")
        print("   Bitte ersetzen Sie 'your_openrouter_api_key_here' in der .env Datei")
        print("   mit Ihrem echten OpenRouter API-Schlüssel.")
        print()
        print("   So erhalten Sie einen kostenlosen API-Schlüssel:")
        print("   1. Gehen Sie zu: https://openrouter.ai/mistralai/mistral-small-24b-instruct-2501:free/api")
        print("   2. Erstellen Sie ein kostenloses Konto")
        print("   3. Kopieren Sie Ihren API-Schlüssel")
        print("   4. Ersetzen Sie den Platzhalter in der .env Datei")
        return False
    
    if not api_key.startswith("sk-or-v1-"):
        print("❌ Ungültiges API-Schlüssel-Format!")
        print("   OpenRouter API-Schlüssel müssen mit 'sk-or-v1-' beginnen.")
        print(f"   Ihr Schlüssel beginnt mit: {api_key[:10]}...")
        return False
    
    print("✅ Gültiger OpenRouter API-Schlüssel gefunden!")
    print(f"   Schlüssel beginnt mit: {api_key[:15]}...")
    print()
    
    # Modell prüfen
    model = os.getenv('DEFAULT_MODEL', 'mistralai/mistral-small-24b-instruct-2501:free')
    print(f"✅ Verwendetes AI-Modell: {model}")
    
    print()
    print("🎉 Setup ist korrekt! Sie können das Interview starten.")
    return True

if __name__ == "__main__":
    if not check_setup():
        print()
        print("⚠️  Bitte beheben Sie die Probleme oben und versuchen Sie es erneut.")
        exit(1)
    else:
        print()
        print("▶️  Um ein Interview zu starten:")
        print("   python interview.py --questions questions.json --format md --verbose")
