# Activer l'environnement virtuel
& "C:\Users\Aloulou\Desktop\xgboostproject\.venv\Scripts\Activate.ps1"

# Naviguer vers le dossier backend
Set-Location "C:\Users\Aloulou\Desktop\xgboostproject\web_api\backend"

# Démarrer le serveur
Write-Host "🚀 Starting Backend Server..." -ForegroundColor Green
python main.py
