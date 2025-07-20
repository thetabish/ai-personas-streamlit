@echo off
REM Set console to UTF-8 encoding
chcp 65001 >nul 2>&1
REM =============================================================================
REM Synthetisches Interview System - Schnell-Start Script (Windows)
REM =============================================================================
REM Dieses Script richtet alles ein und startet eine Demo in unter 5 Minuten!
REM 
REM Voraussetzungen:
REM - Python 3.8+ installiert
REM - Internet-Verbindung fuer Abhaengigkeiten und API-Zugang
REM =============================================================================

setlocal enabledelayedexpansion

echo.
echo ======================================================================
echo Synthetisches Interview System - Schnell-Start (Windows)
echo ======================================================================
echo.
echo Richtet alles ein und startet eine Demo in unter 5 Minuten!
echo.

REM Schritt 1: Python-Version pruefen
echo Schritt 1/6: Python-Version pruefen...
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo Python nicht gefunden!
        echo Bitte installieren Sie Python 3.8+ von https://python.org
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python3
        for /f "tokens=2" %%i in ('python3 --version') do set PYTHON_VERSION=%%i
    )
) else (
    set PYTHON_CMD=python
    for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
)
echo Python !PYTHON_VERSION! gefunden
echo.

REM Schritt 2: Virtuelle Umgebung erstellen
echo Schritt 2/6: Virtuelle Python-Umgebung einrichten...
if not exist "venv" (
    echo Erstelle virtuelle Umgebung...
    !PYTHON_CMD! -m venv venv
    echo Virtuelle Umgebung erstellt
) else (
    echo Virtuelle Umgebung bereits vorhanden
)

REM Virtuelle Umgebung aktivieren
echo Aktiviere virtuelle Umgebung...
call venv\Scripts\activate.bat
echo Virtuelle Umgebung aktiviert
echo.

REM Schritt 3: Abhaengigkeiten installieren
echo Schritt 3/6: Python-Abhaengigkeiten installieren...
if exist "requirements.txt" (
    python -m pip install --quiet --upgrade pip
    python -m pip install --quiet -r requirements.txt
    echo Alle Abhaengigkeiten installiert
) else (
    echo requirements.txt nicht gefunden!
    pause
    exit /b 1
)
echo.

REM Schritt 4: Umgebungsvariablen einrichten
echo Schritt 4/6: Umgebungsvariablen pruefen...
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo .env Datei von .env.example erstellt
        echo.
        echo WICHTIG: Bitte fuegen Sie Ihren OpenRouter API-Schluessel hinzu:
        echo.
        echo    1. Kostenlosen API-Schluessel erhalten: https://openrouter.ai/mistralai/mistral-small-24b-instruct-2501:free/api
        echo    2. In .env Datei eintragen: OPENROUTER_API_KEY=ihr_schluessel_hier
        echo.
        echo Druecken Sie Enter wenn Sie den API-Schluessel eingetragen haben...
        pause >nul
    ) else (
        echo .env.example nicht gefunden!
        pause
        exit /b 1
    )
) else (
    echo .env Datei bereits vorhanden
)

REM API-Schluessel pruefen - pruefe auf gueltigen sk-or-v1- Schluessel (nicht in Kommentaren)
findstr /B /C:"OPENROUTER_API_KEY=sk-or-v1-" .env >nul
if errorlevel 1 (
    REM Pruefe ob noch der Platzhalter drin steht
    findstr /B /C:"OPENROUTER_API_KEY=your_openrouter_api_key_here" .env >nul
    if not errorlevel 1 (
        echo Noch Standard-Platzhalter in .env Datei gefunden!
        echo.
        echo Bitte geben Sie Ihren OpenRouter API-Schluessel ein:
    ) else (
        echo Gueltiger OpenRouter API-Schluessel nicht gefunden!
        echo.
        echo Bitte geben Sie Ihren OpenRouter API-Schluessel ein:
    )
    echo.
    echo So erhalten Sie einen kostenlosen API-Schluessel:
    echo 1. Gehen Sie zu: https://openrouter.ai/mistralai/mistral-small-24b-instruct-2501:free/api
    echo 2. Erstellen Sie ein kostenloses Konto
    echo 3. Kopieren Sie Ihren API-Schluessel
    echo.
    set /p USER_API_KEY="API-Schluessel eingeben (beginnt mit sk-or-v1-): "
    
    REM Validiere den eingegebenen API-Schluessel
    if "!USER_API_KEY!"=="" (
        echo Fehler: Kein API-Schluessel eingegeben!
        pause
        exit /b 1
    )
    
    REM Pruefe das Format
    echo !USER_API_KEY! | findstr /B "sk-or-v1-" >nul
    if errorlevel 1 (
        echo Fehler: API-Schluessel muss mit "sk-or-v1-" beginnen!
        echo Ihr eingegebener Schluessel: !USER_API_KEY!
        pause
        exit /b 1
    )
    
    REM Speichere den neuen API-Schluessel in der .env Datei
    echo Speichere API-Schluessel in .env Datei...
    (
        for /f "delims=" %%i in (.env) do (
            echo %%i | findstr /B "OPENROUTER_API_KEY=" >nul
            if errorlevel 1 (
                echo %%i
            ) else (
                echo OPENROUTER_API_KEY=!USER_API_KEY!
            )
        )
    ) > .env.tmp
    move .env.tmp .env >nul
    echo Gueltiger API-Schluessel gespeichert!
) else (
    echo Gueltiger API-Schluessel gefunden
)
echo.

REM Schritt 5: System testen
echo Schritt 5/6: System testen...
echo Teste Verbindung zu OpenRouter und Personas...
python check_setup.py
if errorlevel 1 (
    echo Warnung: Setup-Test fehlgeschlagen
    echo Versuche trotzdem fortzufahren...
) else (
    echo Alle Setup-Checks erfolgreich
)
echo.

REM Schritt 6: Demo starten
echo Schritt 6/6: Demo starten...
echo.
echo ======================================================================
echo SETUP ABGESCHLOSSEN! Starte Demo...
echo ======================================================================
echo.

REM Ueberpruefe ob questions.json existiert
if not exist "questions.json" (
    echo questions.json nicht gefunden, erstelle Beispiel-Fragen...
    (
        echo {
        echo   "questions": [
        echo     "Was ist Ihnen bei einer Lifestyle-Marke am wichtigsten?",
        echo     "Wie entscheiden Sie sich zwischen verschiedenen Marken?",
        echo     "Welche Rolle spielen soziale Medien bei Ihren Kaufentscheidungen?",
        echo     "Wie wichtig ist Nachhaltigkeit fuer Sie bei Marken?",
        echo     "Was wuerde Sie dazu bringen, eine neue Marke auszuprobieren?"
        echo   ]
        echo }
    ) > questions.json
    echo Beispiel-Fragen erstellt
)

echo Starte synthetisches Interview mit Beispiel-Fragen...
echo.

REM Demo ausfuehren
python interview.py --questions questions.json --format md --verbose

echo.
echo ======================================================================
echo DEMO ABGESCHLOSSEN!
echo ======================================================================
echo.
echo Die Ergebnisse wurden gespeichert als:
echo    - results.json (JSON-Format)
echo    - results.md (Markdown-Format)
echo.
echo Um weitere Interviews zu fuehren:
echo    python interview.py --questions questions.json
echo.
echo Um eigene Fragen zu verwenden:
echo    1. Bearbeiten Sie questions.json
echo    2. Fuehren Sie das Interview erneut aus
echo.
echo Weitere Optionen:
echo    python interview.py --help
echo.
echo Vielen Dank fuers Ausprobieren!
echo.
pause
