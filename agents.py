"""
KI Persona Agenten - Einfache Klasse für synthetische Interviews
Verwendet moderne LangChain (v0.3+) und OpenRouter für realistische AI-Personas

Moderne Features:
- init_chat_model für Model-Provider-agnostische Initialisierung  
- Strukturierte Message-Types (HumanMessage, AIMessage, SystemMessage)
- ChatPromptTemplate für robuste Prompt-Gestaltung
- Automatische Fallbacks für Kompatibilität
"""

import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Lade Umgebungsvariablen aus .env Datei
load_dotenv()


class PersonaAgent:
    """
    Einfache AI-Persona Klasse für Interviews
    Jede Persona hat einen Namen, Alter, Eigenschaften und kann auf Fragen antworten
    """
    
    def __init__(self, name, age, characteristics, background, detailed_personality=""):
        """
        Erstellt eine neue AI-Persona
        
        Args:
            name: Name der Person (z.B. "Anna")
            age: Alter der Person (z.B. 25)
            characteristics: Kurze Beschreibung (z.B. "umweltbewusst, sportlich")
            background: Detaillierter Hintergrund der Person
            detailed_personality: Zusätzliche Persönlichkeitsdetails
        """
        # Grundlegende Persona-Informationen speichern
        self.name = name
        self.age = age
        self.characteristics = characteristics
        self.background = background
        self.detailed_personality = detailed_personality
        self.conversation_history = []
        
        # AI-Sprachmodell einrichten (das "Gehirn" der Persona)
        self.llm = self._setup_ai_model()
        
        # Prompt-Vorlage erstellen (wie die Persona antworten soll)
        self.prompt = self._create_conversation_template()
        
        # Alles zusammenfügen zu einer "Kette" für Antworten
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def _setup_ai_model(self):
        """
        Richtet das AI-Sprachmodell ein
        Verwendet OpenRouter für kostenlosen Zugang zu verschiedenen AI-Modellen
        """
        # Verwende moderne LangChain init_chat_model Funktion
        try:
            from langchain.chat_models import init_chat_model
            
            return init_chat_model(
                model=get_ai_model_name(),
                model_provider="openai",
                api_key=os.getenv('OPENROUTER_API_KEY'),
                base_url="https://openrouter.ai/api/v1",
                temperature=get_creativity_level(),
                max_tokens=get_max_response_length(),
                default_headers={
                    "HTTP-Referer": os.getenv('YOUR_SITE_URL', 'https://localhost:3000'),
                    "X-Title": os.getenv('YOUR_SITE_NAME', 'Synthetic Interview PoC'),
                }
            )
        except ImportError:
            # Fallback für ältere LangChain Versionen
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=get_ai_model_name(),
                temperature=get_creativity_level(),
                max_tokens=get_max_response_length(),
                openai_api_key=os.getenv('OPENROUTER_API_KEY'),
                openai_api_base="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": os.getenv('YOUR_SITE_URL', 'https://localhost:3000'),
                    "X-Title": os.getenv('YOUR_SITE_NAME', 'Synthetic Interview PoC'),
                }
            )
    
    def _create_conversation_template(self):
        """
        Erstellt die Vorlage dafür, wie die Persona antworten soll
        Das ist wie eine "Anleitung" für die AI
        """
        # Erstelle die Persönlichkeits-Anweisungen
        personality_instructions = create_personality_prompt(
            self.name, 
            self.age, 
            self.characteristics, 
            self.background, 
            self.detailed_personality
        )
        
        return ChatPromptTemplate.from_messages([
            ("system", personality_instructions),
            ("human", "{input}")
        ])
    
    def respond(self, question, previous_responses=None):
        """
        Lässt die Persona auf eine Frage antworten
        
        Args:
            question: Die Frage als Text
            previous_responses: Was andere Personas vorher gesagt haben
            
        Returns:
            Die Antwort der Persona als Text
        """
        try:
            # Erstelle strukturierten Kontext
            context = self._build_context(question, previous_responses)
            
            # Lass die AI antworten - verwende moderne invoke Methode
            response = self.chain.invoke({"input": context})
            
            # Speichere die Unterhaltung für späteren Kontext
            self._save_turn(question, response)
            
            return response
            
        except Exception as error:
            error_message = self._handle_error(error)
            self._save_turn(question, error_message)
            return error_message
    
    def get_agent_info(self):
        """
        Gibt alle wichtigen Informationen über diese Persona zurück
        Nützlich für Berichte und Zusammenfassungen
        """
        return {
            "name": self.name,
            "age": self.age,
            "characteristics": self.characteristics,
            "background": self.background
        }
    
    def reset_memory(self):
        """
        Löscht das Gedächtnis der Persona
        Nützlich um ein neues Interview zu starten
        """
        self.conversation_history.clear()
    
    def _build_context(self, question, previous_responses):
        """Erstellt einfachen Kontext für die AI"""
        context = f"Interview-Frage: {question}"
        
        if previous_responses:
            context += "\n\nAndere Antworten:\n"
            for resp in previous_responses:
                context += f"- {resp['agent_id']}: {resp['response']}\n"
        
        if self.conversation_history:
            context += f"\n\nDein Verlauf:\n"
            for item in self.conversation_history[-2:]:  # Nur die letzten 2
                context += f"F: {item['question']}\nA: {item['response']}\n"
        
        return context
    
    def _save_turn(self, question, response):
        """Speichert Gesprächs-Turn"""
        self.conversation_history.append({
            "question": question,
            "response": response
        })
    
    def _handle_error(self, error):
        """Behandelt Fehler mit klaren Nachrichten"""
        error_str = str(error)
        if "401" in error_str or "No auth credentials" in error_str:
            return "[Fehler: API-Schlüssel ungültig]"
        elif "403" in error_str or "Forbidden" in error_str:
            return "[Fehler: Keine API-Berechtigung]"
        elif "429" in error_str or "rate limit" in error_str.lower():
            return "[Fehler: Zu viele Anfragen]"
        else:
            return f"[Fehler: {error_str}]"

# =====================================
# CONFIGURATION FUNCTIONS (Konfiguration)
# =====================================

def get_ai_model_name():
    """
    Gibt den Namen des AI-Modells zurück, das verwendet werden soll
    Standard ist ein kostenloses Mistral-Modell von OpenRouter
    """
    return os.getenv('DEFAULT_MODEL', 'mistralai/mistral-small-24b-instruct-2501:free')


def get_creativity_level():
    """
    Gibt das Kreativitätslevel zurück (0.0 = sehr vorhersagbar, 1.0 = sehr kreativ)
    Standard ist 0.7 für natürliche, aber nicht zu zufällige Antworten
    """
    return float(os.getenv('TEMPERATURE', 0.7))


def get_max_response_length():
    """
    Gibt die maximale Länge einer Antwort zurück (in Tokens)
    Ein Token ist etwa ein Wort oder Wortfragment
    """
    return int(os.getenv('MAX_TOKENS', 150))


def create_personality_prompt(name, age, characteristics, background, detailed_personality):
    """
    Erstellt die Persönlichkeits-Anweisungen für eine Persona
    Das ist wie ein "Charakter-Briefing" für die AI
    
    Args:
        name: Name der Person
        age: Alter der Person
        characteristics: Kurze Eigenschaften
        background: Ausführlicher Hintergrund
        detailed_personality: Zusätzliche Persönlichkeitsdetails
        
    Returns:
        Vollständige Anweisungen als Text
    """
    return f"""Du bist {name}, eine {age}-jährige Person, die an einem Marktforschungsinterview über Lifestyle-Marken teilnimmt.

Deine Eigenschaften: {characteristics}
Dein Hintergrund: {background}
{detailed_personality}

WICHTIGE ANWEISUNGEN:
- Antworte so, wie {name} natürlich antworten würde
- Halte die Antworten prägnant (maximal 2-3 Sätze)
- Sei authentisch zu den Werten und dem Lebensstil deiner Persona
- Berücksichtige, was andere vor dir in dieser Runde gesagt haben
- Zeige Persönlichkeit durch deine Sprache und Meinungen
- Bleibe während des gesamten Interviews bei deinem Charakter"""


# =====================================
# PERSONA CREATION (Persona-Erstellung)
# =====================================

def create_personas():
    """
    Erstellt die Standard-Personas für Lifestyle-Marken-Forschung
    
    Returns:
        Liste von PersonaAgent-Objekten
    """
    # Hier werden unsere drei Haupt-Personas definiert
    personas = [
        create_anna_persona(),
        create_tom_persona(), 
        create_julia_persona()
    ]
    
    return personas


def create_anna_persona():
    """
    Erstellt Anna - die umweltbewusste Studentin
    """
    return PersonaAgent(
        name="Anna",
        age=20,
        characteristics="umweltbewusst, schätzt Nachhaltigkeit, aktiv in sozialen Medien, budgetbewusste Studentin",
        background="Universitätsstudentin der Umweltwissenschaften. Kauft in Second-Hand-Läden und unterstützt umweltfreundliche Marken. Aktiv auf Instagram und TikTok, folgt Nachhaltigkeits-Influencern.",
        detailed_personality="Du bist leidenschaftlich für den Klimawandel und erwartest von Marken Transparenz über ihre Umweltauswirkungen. Du bevorzugst Second-Hand-Shopping, investierst aber in nachhaltige neue Produkte. Du wirst von authentischen Social-Media-Inhalten beeinflusst und kannst Greenwashing leicht erkennen."
    )


def create_tom_persona():
    """
    Erstellt Tom - den sportlichen Berufstätigen
    """
    return PersonaAgent(
        name="Tom",
        age=40,
        characteristics="sportlich, gesundheitsbewusst, vielbeschäftigter Berufstätiger, schätzt Qualität und Leistung",
        background="Marketing-Manager in einem Tech-Unternehmen. Läuft Marathon und geht regelmäßig ins Fitnessstudio. Schätzt Effizienz und Qualität über den Preis. Hat verfügbares Einkommen, aber recherchiert Käufe sorgfältig.",
        detailed_personality="Du priorisierst Leistung und Langlebigkeit bei allem, was du kaufst. Zeit ist wertvoll für dich, daher bevorzugst du Marken, die konstante Qualität liefern. Du bist bereit, Premium-Preise für Produkte zu zahlen, die deinen aktiven Lebensstil und dein professionelles Image unterstützen."
    )


def create_julia_persona():
    """
    Erstellt Julia - die praktische Familienmutter
    """
    return PersonaAgent(
        name="Julia",
        age=35,
        characteristics="preisbewusst, praktisch, familienorientiert, schätzt Langlebigkeit und Funktionalität",
        background="Berufstätige Mutter von zwei Kindern im Alter von 8 und 12 Jahren. Teilzeit-Buchhalterin. Sorgfältige Budgetplanerin, die bei Käufen auf Wert und Langlebigkeit achtet. Kauft im Ausverkauf und vergleicht Preise ausgiebig.",
        detailed_personality="Du triffst durchdachte Kaufentscheidungen basierend auf Familienbedürfnissen und Budgetbeschränkungen. Du schätzt Marken, die guten Kundenservice bieten und zu ihren Produkten stehen. Mundpropaganda von anderen Eltern hat großen Einfluss auf deine Entscheidungen."
    )


# =====================================
# API KEY VALIDATION
# =====================================


def validate_api_key():
    """
    Prüft, ob ein gültiger OpenRouter API-Schlüssel vorhanden ist
    
    Returns:
        bool: True wenn gültiger API-Schlüssel vorhanden ist, False sonst
    """
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("❌ Kein OpenRouter API-Schlüssel gefunden!")
        print("   Bitte erstellen Sie eine .env Datei mit Ihrem API-Schlüssel.")
        return False
    
    if api_key == "your_openrouter_api_key_here":
        print("❌ Standard-Platzhalter für API-Schlüssel gefunden!")
        print("   Bitte ersetzen Sie 'your_openrouter_api_key_here' in der .env Datei")
        print("   mit Ihrem echten OpenRouter API-Schlüssel.")
        print("   Erhalten Sie einen kostenlosen Schlüssel unter:")
        print("   https://openrouter.ai/mistralai/mistral-small-24b-instruct-2501:free/api")
        return False
    
    if not api_key.startswith("sk-or-v1-"):
        print("❌ Ungültiges API-Schlüssel-Format!")
        print("   OpenRouter API-Schlüssel müssen mit 'sk-or-v1-' beginnen.")
        print("   Bitte prüfen Sie Ihren Schlüssel in der .env Datei.")
        return False
    
    print("✅ Gültiger OpenRouter API-Schlüssel gefunden!")
    return True
