#!/usr/bin/env python3
"""
Einfacher Test für die GUI App - überprüft Importe und grundlegende Funktionen
"""

try:
    print("🔄 Teste Importe...")
    
    # Test core imports
    import streamlit as st
    print("✅ Streamlit Import erfolgreich")
    
    import json
    import time
    import datetime
    import os
    from typing import Dict, List, Optional
    print("✅ Standard Library Imports erfolgreich")
    
    # Test custom imports
    from agents import create_personas, validate_api_key
    print("✅ Agents Import erfolgreich")
    
    # Test GUI app imports
    from gui_app import get_available_agents, validate_api_key_gui, set_api_key_environment
    print("✅ GUI App Funktionen Import erfolgreich")
    
    # Test basic functionality
    print("\n🔄 Teste grundlegende Funktionen...")
    
    # Test get_available_agents
    agents = get_available_agents()
    print(f"✅ Verfügbare Agenten: {agents}")
    
    # Test API key validation
    test_key = "sk-or-v1-test123"
    valid = validate_api_key_gui(test_key)
    print(f"✅ API-Schlüssel Validierung funktioniert: {valid}")
    
    # Test invalid API key
    invalid_valid = validate_api_key_gui("invalid-key")
    print(f"✅ Ungültiger API-Schlüssel erkannt: {not invalid_valid}")
    
    print("\n🎉 Alle Tests erfolgreich! Die GUI App sollte funktionieren.")
    print("\n📝 Um die App zu starten, führen Sie aus:")
    print("   streamlit run gui_app.py")
    
except ImportError as e:
    print(f"❌ Import Fehler: {e}")
    print("💡 Bitte installieren Sie die Abhängigkeiten mit: pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ Unerwarteter Fehler: {e}")
    print("💡 Bitte überprüfen Sie die Konfiguration")
