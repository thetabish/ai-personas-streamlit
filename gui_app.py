#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit GUI für AI Persona Interview System
Ein WhatsApp-ähnliches Chat Interface für synthetische Interviews

Usage:
    streamlit run gui_app.py
"""

import streamlit as st
import json
import time
import datetime
import os
from typing import Dict, List, Optional

# Import our core functionality
from agents import create_personas, validate_api_key


def init_streamlit_config():
    """Konfiguriert Streamlit Layout und Styling"""
    st.set_page_config(
        page_title="AI Persona Chat Interview",
        page_icon="🎤",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for chat-like appearance
    st.markdown("""
    <style>
    .persona-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .chat-message {
        padding: 0.8rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        max-width: 70%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .anna-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        margin-right: auto;
        text-align: left;
    }
    
    .tom-message {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        margin-right: auto;
        text-align: left;
    }
    
    .julia-message {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        color: white;
        margin-right: auto;
        text-align: left;
    }
    
    .question-bubble {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-left: 4px solid #4facfe;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
        font-weight: bold;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .typing-indicator {
        color: #888;
        font-style: italic;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def get_available_agents() -> List[str]:
    """
    Gibt eine Liste der verfügbaren Agenten-Namen zurück
    """
    try:
        personas = create_personas()
        return [persona.name for persona in personas]
    except Exception:
        # Fallback zu Standard-Agenten wenn create_personas fehlschlägt
        return ["Anna", "Tom", "Julia"]


def validate_api_key_gui(api_key: str) -> bool:
    """
    Validiert API-Schlüssel für die GUI
    """
    if not api_key:
        return False
    
    # Check for placeholder values
    placeholder_values = [
        "your_openrouter_api_key_here",
        "your_key_here", 
        "INSERT_YOUR_KEY_HERE",
        "sk-or-v1-example"
    ]
    
    if api_key.lower() in [p.lower() for p in placeholder_values]:
        return False
    
    if not api_key.startswith("sk-or-v1-"):
        return False
    
    return True


def set_api_key_environment(api_key: str):
    """
    Setzt den API-Schlüssel als Umgebungsvariable für die aktuelle Session
    """
    os.environ['OPENROUTER_API_KEY'] = api_key


def show_persona_cards():
    """Zeigt die Persona-Beschreibungen als ansprechende Karten"""
    st.markdown("### 👥 Meet Our AI Personas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="persona-card">
            <h4>🌱 Anna (20)</h4>
            <p><strong>Umweltbewusste Studentin</strong></p>
            <p>• Studiert Umweltwissenschaften</p>
            <p>• Kauft Second-Hand & nachhaltig</p>
            <p>• Aktiv auf Social Media</p>
            <p>• Kann Greenwashing erkennen</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="persona-card">
            <h4>🏃‍♂️ Tom (40)</h4>
            <p><strong>Sportlicher Manager</strong></p>
            <p>• Marketing-Manager in Tech</p>
            <p>• Marathon-Läufer & Fitness</p>
            <p>• Schätzt Qualität über Preis</p>
            <p>• Effizienz-orientiert</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="persona-card">
            <h4>👨‍👩‍👧‍👦 Julia (35)</h4>
            <p><strong>Praktische Familienmutter</strong></p>
            <p>• Mutter von 2 Kindern</p>
            <p>• Teilzeit-Buchhalterin</p>
            <p>• Preisbewusst & budgetorientiert</p>
            <p>• Vertraut auf Mundpropaganda</p>
        </div>
        """, unsafe_allow_html=True)


def load_questions_from_file(uploaded_file) -> List[str]:
    """Lädt Fragen aus einer hochgeladenen JSON-Datei"""
    try:
        content = uploaded_file.read()
        data = json.loads(content)
        
        # Handle different JSON structures
        if 'questions' in data:
            return data['questions']
        elif isinstance(data, list):
            return data
        else:
            st.error("❌ Ungültiges JSON-Format. Datei muss 'questions' Array enthalten.")
            return []
    except json.JSONDecodeError:
        st.error("❌ Fehler beim Lesen der JSON-Datei. Bitte überprüfen Sie das Format.")
        return []
    except Exception as e:
        st.error(f"❌ Fehler beim Laden der Datei: {e}")
        return []


def display_chat_message(agent_name: str, message: str, is_typing: bool = False):
    """Zeigt eine Chat-Nachricht im WhatsApp-ähnlichen Stil"""
    agent_lower = agent_name.lower()
    
    if is_typing:
        st.markdown(f'<div class="typing-indicator">💭 {agent_name} tippt...</div>', 
                   unsafe_allow_html=True)
        time.sleep(1)  # Simulate typing delay
        return
    
    # Choose message style based on agent
    if agent_lower == "anna":
        css_class = "anna-message"
        emoji = "🌱"
    elif agent_lower == "tom":
        css_class = "tom-message"
        emoji = "🏃‍♂️"
    elif agent_lower == "julia":
        css_class = "julia-message"
        emoji = "👨‍👩‍👧‍👦"
    else:
        css_class = "chat-message"
        emoji = "🤖"
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <strong>{emoji} {agent_name}:</strong><br>
        {message}
    </div>
    """, unsafe_allow_html=True)


def display_question(question: str, question_num: int):
    """Zeigt eine Frage als hervorgehobene Bubble"""
    st.markdown(f"""
    <div class="question-bubble">
        <strong>❓ Frage {question_num}:</strong> {question}
    </div>
    """, unsafe_allow_html=True)


def run_chat_interview(questions: List[str], selected_agents: List[str]):
    """Führt das Interview im Chat-Format durch"""
    try:
        if not questions:
            st.warning("⚠️ Keine Fragen gefunden!")
            return None
        
        if not selected_agents:
            st.warning("⚠️ Keine Agenten ausgewählt!")
            return None
        
        # Initialize personas with error handling
        try:
            all_personas = create_personas()
        except Exception as e:
            st.error(f"❌ Fehler beim Erstellen der Personas: {str(e)}")
            st.info("💡 Bitte überprüfen Sie Ihren API-Schlüssel und die Internetverbindung.")
            return None
            
        personas = [p for p in all_personas if p.name.lower() in [a.lower() for a in selected_agents]]
        
        if not personas:
            st.error("❌ Keine gültigen Personas ausgewählt!")
            st.info(f"Verfügbare Personas: {[p.name for p in all_personas]}")
            return None
        
        # Container for chat messages
        chat_container = st.container()
        
        # Initialize interview results
        interview_results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "agents": [],
            "questions_and_answers": []
        }
        
        # Safely get agent info
        try:
            interview_results["agents"] = [p.get_agent_info() for p in personas]
        except Exception as e:
            st.warning(f"⚠️ Warnung beim Laden der Agent-Informationen: {str(e)}")
            interview_results["agents"] = [{"name": p.name, "error": "Info nicht verfügbar"} for p in personas]
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
    except Exception as e:
        st.error(f"❌ Unerwarteter Fehler beim Initialisieren des Interviews: {str(e)}")
        st.info("💡 Bitte versuchen Sie es erneut oder kontaktieren Sie den Support.")
        return None
    
    try:
        total_steps = len(questions) * len(personas)
        current_step = 0
        
        with chat_container:
            st.markdown("### 💬 Live Interview Chat")
            
            for q_idx, question in enumerate(questions, 1):
                try:
                    # Display question
                    display_question(question, q_idx)
                    
                    # Collect responses for this question
                    question_data = {
                        "question": question,
                        "responses": []
                    }
                    
                    previous_responses = []
                    
                    for persona in personas:
                        try:
                            # Show typing indicator
                            status_text.text(f"💭 {persona.name} überlegt...")
                            display_chat_message(persona.name, "", is_typing=True)
                            
                            # Get response with timeout handling
                            response = persona.respond(question, previous_responses)
                            
                            # Validate response
                            if not response or response.strip() == "":
                                response = f"[{persona.name} konnte nicht antworten]"
                            
                            # Display response
                            display_chat_message(persona.name, response)
                            
                            # Store response
                            response_data = {
                                "agent_id": persona.name,
                                "response": response,
                                "status": "success"
                            }
                            question_data["responses"].append(response_data)
                            previous_responses.append(response_data)
                            
                        except Exception as e:
                            error_msg = f"❌ Fehler bei {persona.name}: {str(e)}"
                            st.error(f"Fehler bei Persona {persona.name}: {str(e)}")
                            display_chat_message(persona.name, f"[Entschuldigung, ich kann momentan nicht antworten: {str(e)}]")
                            
                            question_data["responses"].append({
                                "agent_id": persona.name,
                                "response": error_msg,
                                "status": "error",
                                "error_details": str(e)
                            })
                        
                        # Update progress
                        current_step += 1
                        try:
                            progress_bar.progress(current_step / total_steps)
                        except:
                            pass  # Continue even if progress update fails
                        
                        # Small delay between responses
                        time.sleep(0.5)
                    
                    interview_results["questions_and_answers"].append(question_data)
                    
                    # Add separator between questions
                    if q_idx < len(questions):
                        st.markdown("---")
                        
                except Exception as e:
                    st.error(f"❌ Fehler bei Frage {q_idx}: {str(e)}")
                    # Continue with next question
                    continue
                    
    except Exception as e:
        st.error(f"❌ Schwerwiegender Fehler während des Interviews: {str(e)}")
        st.info("💡 Das Interview wurde unterbrochen. Versuchen Sie es bitte erneut.")
        return None
    
    # Interview completed successfully
    status_text.text("✅ Interview abgeschlossen!")
    progress_bar.progress(1.0)
    
    return interview_results


def create_download_files(results: Dict):
    """Erstellt Download-Dateien für die Ergebnisse"""
    try:
        if not results:
            return None, None
        
        # JSON file
        try:
            json_content = json.dumps(results, indent=2, ensure_ascii=False)
            json_bytes = json_content.encode('utf-8')
        except Exception as e:
            st.error(f"❌ Fehler beim Erstellen der JSON-Datei: {str(e)}")
            json_bytes = None
        
        # Markdown file
        try:
            md_content = create_markdown_report(results)
            md_bytes = md_content.encode('utf-8')
        except Exception as e:
            st.error(f"❌ Fehler beim Erstellen der Markdown-Datei: {str(e)}")
            md_bytes = None
        
        return json_bytes, md_bytes
        
    except Exception as e:
        st.error(f"❌ Unerwarteter Fehler beim Erstellen der Download-Dateien: {str(e)}")
        return None, None


def create_markdown_report(results: Dict) -> str:
    """Erstellt einen Markdown-Bericht"""
    try:
        timestamp = results.get("timestamp", "Unknown")
        
        md_content = f"""# Synthetische Interview Ergebnisse

**Zeitstempel:** {timestamp}

## Teilnehmer

"""
        
        # Safe agent processing
        agents = results.get("agents", [])
        if agents:
            for agent in agents:
                try:
                    name = agent.get('name', 'Unbekannt')
                    age = agent.get('age', 'Unbekannt')
                    characteristics = agent.get('characteristics', 'Keine Angaben')
                    md_content += f"- **{name}** ({age} Jahre): {characteristics}\n"
                except Exception as e:
                    md_content += f"- **Fehler beim Laden der Agent-Info**: {str(e)}\n"
        else:
            md_content += "- Keine Agenten-Informationen verfügbar\n"
        
        md_content += "\n## Interview Fragen & Antworten\n\n"
        
        # Safe Q&A processing
        qa_list = results.get("questions_and_answers", [])
        if qa_list:
            for i, qa in enumerate(qa_list, 1):
                try:
                    question = qa.get('question', 'Frage nicht verfügbar')
                    md_content += f"### Frage {i}: {question}\n\n"
                    
                    responses = qa.get("responses", [])
                    if responses:
                        for response in responses:
                            try:
                                agent_id = response.get('agent_id', 'Unbekannter Agent')
                                answer = response.get('response', 'Antwort nicht verfügbar')
                                status = response.get('status', 'unknown')
                                
                                if status == 'error':
                                    md_content += f"**{agent_id}:** ❌ {answer}\n\n"
                                else:
                                    md_content += f"**{agent_id}:** {answer}\n\n"
                            except Exception as e:
                                md_content += f"**Fehler beim Verarbeiten der Antwort:** {str(e)}\n\n"
                    else:
                        md_content += "*Keine Antworten für diese Frage*\n\n"
                    
                    md_content += "---\n\n"
                except Exception as e:
                    md_content += f"### Frage {i}: Fehler beim Verarbeiten ({str(e)})\n\n---\n\n"
        else:
            md_content += "*Keine Fragen und Antworten verfügbar*\n\n"
        
        return md_content
        
    except Exception as e:
        error_report = f"""# Interview Ergebnisse - Fehler beim Generieren

**Fehler:** {str(e)}
**Zeitstempel:** {datetime.datetime.now().isoformat()}

Es trat ein Fehler beim Generieren des Berichts auf. Die Rohdaten könnten trotzdem verfügbar sein.
"""
        return error_report


def main():
    """Hauptfunktion der Streamlit App"""
    init_streamlit_config()
    
    # Header
    st.title("🎤 AI Persona Chat Interview")
    st.markdown("**Interaktive Marktforschung mit AI-Personas im Chat-Format**")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Konfiguration")
        
        # API Key input section
        st.subheader("🔑 API-Schlüssel")
        
        # Always start with empty API key field for security
        # User must enter API key on each session for security reasons
        
        # API Key input field - always empty on page refresh
        api_key_input = st.text_input(
            "OpenRouter API-Schlüssel eingeben:",
            value="",  # Always empty for security
            type="password",
            help="Ihr API-Schlüssel beginnt mit 'sk-or-v1-'",
            placeholder="sk-or-v1-..."
        )
        
        # API Key validation and status
        api_key_valid = False
        if api_key_input:
            if validate_api_key_gui(api_key_input):
                st.success("✅ API-Schlüssel gültig")
                # Set API key in environment for this session only
                set_api_key_environment(api_key_input)
                # Store in session state only for the current session, cleared on refresh
                st.session_state.api_key = api_key_input
                api_key_valid = True
            else:
                st.error("❌ Ungültiger API-Schlüssel")
                st.info("API-Schlüssel muss mit 'sk-or-v1-' beginnen")
        else:
            st.warning("⚠️ Bitte API-Schlüssel eingeben")
            # Clear any old API key from session state when input is empty
            if 'api_key' in st.session_state:
                del st.session_state.api_key
        
        # Show API key help
        with st.expander("🆘 Wie bekomme ich einen API-Schlüssel?"):
            st.markdown("""
            **Kostenlosen OpenRouter API-Schlüssel erhalten:**
            
            1. Besuchen Sie: [OpenRouter](https://openrouter.ai/mistralai/mistral-small-24b-instruct-2501:free/api)
            2. Erstellen Sie ein kostenloses Konto
            3. Kopieren Sie Ihren API-Schlüssel
            4. Fügen Sie ihn oben ein
            
            **Format:** `sk-or-v1-abcdef123456789...`
            """)
        
        st.divider()
        
        # Agent selection (always show, but may be disabled)
        st.subheader("👥 Personas auswählen")
        available_agents = get_available_agents()
        selected_agents = st.multiselect(
            "Welche Personas sollen teilnehmen?",
            available_agents,
            default=available_agents,
            help="Wählen Sie mindestens eine Persona aus",
            disabled=not api_key_valid
        )
        
        if not selected_agents and api_key_valid:
            st.warning("⚠️ Bitte mindestens eine Persona auswählen")
        
        # File upload (always show, but may be disabled)
        st.subheader("📁 Fragen hochladen")
        uploaded_file = st.file_uploader(
            "JSON-Datei mit Fragen",
            type=['json'],
            help="Laden Sie questions.json oder interview_batch.json hoch",
            disabled=not api_key_valid
        )
        
        # Sample questions option (always show, but may be disabled)
        use_sample = st.checkbox(
            "📝 Beispiel-Fragen verwenden", 
            value=not uploaded_file,
            disabled=not api_key_valid
        )
    
    # Main content area
    show_persona_cards()
    
    # Load questions (always show this section)
    questions = []
    if uploaded_file and api_key_valid:
        questions = load_questions_from_file(uploaded_file)
        if questions:
            st.success(f"✅ {len(questions)} Fragen geladen")
            with st.expander("📋 Geladene Fragen anzeigen"):
                for i, q in enumerate(questions, 1):
                    st.write(f"{i}. {q}")
    elif use_sample and api_key_valid:
        questions = [
            "Was ist dir bei einer Lifestyle-Marke am wichtigsten?",
            "Wie bewertest du Nachhaltigkeit bei den Marken, die du wählst?",
            "Welche Rolle spielt der Preis bei deinen Kaufentscheidungen?"
        ]
        st.info("📝 Beispiel-Fragen werden verwendet")
        with st.expander("📋 Beispiel-Fragen anzeigen"):
            for i, q in enumerate(questions, 1):
                st.write(f"{i}. {q}")
    elif not api_key_valid:
        # Show preview of what will be available once API key is entered
        st.info("💡 **Vorschau:** Nach der API-Schlüssel-Eingabe können Sie:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **📁 Eigene Fragen hochladen:**
            - JSON-Dateien mit Fragen
            - Batch-Konfigurationen
            """)
        with col2:
            st.markdown("""
            **� Beispiel-Fragen verwenden:**
            - Lifestyle-Marken Fragen
            - Sofort einsatzbereit
            """)
    
    # Determine if interview can be started
    can_start_interview = api_key_valid and questions and selected_agents
    
    # Show status message about what's needed
    if not api_key_valid:
        st.warning("🔑 **API-Schlüssel erforderlich:** Bitte geben Sie zuerst einen gültigen API-Schlüssel in der Seitenleiste ein.")
    elif not questions:
        st.warning("📝 **Fragen erforderlich:** Bitte laden Sie Fragen hoch oder verwenden Sie die Beispiel-Fragen.")
    elif not selected_agents:
        st.warning("👥 **Personas erforderlich:** Bitte wählen Sie mindestens eine Persona aus.")
    else:
        st.success("🎉 **Bereit für das Interview!** Alle Voraussetzungen erfüllt.")
    
    # Start interview button (always visible, but disabled when requirements not met)
    if st.button(
        "🚀 Interview starten", 
        disabled=not can_start_interview,
        help="Alle Voraussetzungen müssen erfüllt sein: API-Schlüssel, Fragen und Personas"
    ):
        try:
            # Ensure API key is set in environment before starting
            # Use the current API key input since we don't persist it across refreshes
            if api_key_input and api_key_valid:
                set_api_key_environment(api_key_input)
            elif 'api_key' in st.session_state:
                set_api_key_environment(st.session_state.api_key)
            
            with st.spinner("🔄 Interview wird gestartet..."):
                results = run_chat_interview(questions, selected_agents)
                
                if results:
                    st.success("🎉 Interview erfolgreich abgeschlossen!")
                    
                    # Store results in session state for download
                    st.session_state['interview_results'] = results
                    
                    # Download section
                    st.markdown("### 📥 Ergebnisse herunterladen")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        try:
                            json_bytes, md_bytes = create_download_files(results)
                            if json_bytes:
                                st.download_button(
                                    label="📄 JSON herunterladen",
                                    data=json_bytes,
                                    file_name=f"interview_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                    mime="application/json"
                                )
                            else:
                                st.error("❌ JSON-Download nicht verfügbar")
                        except Exception as e:
                            st.error(f"❌ Fehler beim Erstellen des JSON-Downloads: {str(e)}")
                    
                    with col2:
                        try:
                            if 'json_bytes' in locals() and 'md_bytes' in locals() and md_bytes:
                                st.download_button(
                                    label="📝 Markdown herunterladen",
                                    data=md_bytes,
                                    file_name=f"interview_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                    mime="text/markdown"
                                )
                            else:
                                st.error("❌ Markdown-Download nicht verfügbar")
                        except Exception as e:
                            st.error(f"❌ Fehler beim Erstellen des Markdown-Downloads: {str(e)}")
                else:
                    st.error("❌ Interview fehlgeschlagen oder abgebrochen")
                    st.info("💡 Bitte überprüfen Sie Ihren API-Schlüssel und versuchen Sie es erneut.")
                    
        except Exception as e:
            st.error(f"❌ Kritischer Fehler beim Starten des Interviews: {str(e)}")
            st.info("💡 Bitte laden Sie die Seite neu und versuchen Sie es erneut.")
            
            # Log error details for debugging (only shown in development)
            if st.secrets.get("DEBUG_MODE", False):
                st.exception(e)
                
                with col2:
                    if md_bytes:
                        st.download_button(
                            label="📝 Markdown herunterladen",
                            data=md_bytes,
                            file_name=f"interview_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )
        
    # Footer
    st.markdown("---")
    st.markdown("*Powered by LangChain, OpenRouter & Streamlit* 🚀")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("❌ **Kritischer Anwendungsfehler**")
        st.error(f"Es ist ein unerwarteter Fehler aufgetreten: {str(e)}")
        st.info("💡 **Lösungsvorschläge:**")
        st.info("1. Laden Sie die Seite neu (F5)")
        st.info("2. Überprüfen Sie Ihre Internetverbindung")
        st.info("3. Stellen Sie sicher, dass alle Abhängigkeiten installiert sind")
        st.info("4. Kontaktieren Sie den Support wenn das Problem weiterhin besteht")
