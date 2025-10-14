#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Migration GEOPOLIS v2 → v3
Architecture unifiée avec frontend SPA
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

print("=" * 70)
print("   GEOPOLIS - MIGRATION v2 → v3")
print("   Architecture Unifiée avec Frontend SPA")
print("=" * 70)
print()

# ============================================
# 1. BACKUP COMPLET
# ============================================

print("[1/7] Création du backup complet...")
backup_dir = Path("backup_v2")
backup_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_path = backup_dir / f"backup_{timestamp}"
backup_path.mkdir(exist_ok=True)

# Fichiers à sauvegarder
files_to_backup = [
    "app.py",
    "__init_modules__.py",
    "start_geopolis.bat"
]

for file in files_to_backup:
    if Path(file).exists():
        shutil.copy2(file, backup_path / file)
        print(f"  [OK] {file} sauvegardé")

# Dossiers à sauvegarder
dirs_to_backup = ["Analyse_thematique", "templates", "app"]
for dir_name in dirs_to_backup:
    src = Path(dir_name)
    if src.exists():
        dst = backup_path / dir_name
        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"  [OK] {dir_name}/ sauvegardé")

print(f"\n✓ Backup créé: {backup_path}")
print()

# ============================================
# 2. CRÉER NOUVELLE STRUCTURE
# ============================================

print("[2/7] Création de la nouvelle structure...")

new_structure = [
    "backend/core",
    "backend/modules/analyse_thematique",
    "backend/modules/tuteur_ia",
    "backend/modules/plugins",
    "frontend/js/views",
    "frontend/css",
    "plugins",
    "logs",
    "db",
    "data",
    "config"
]

for path in new_structure:
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"  [+] {path}/")

# Créer __init__.py
init_files = [
    "backend/__init__.py",
    "backend/core/__init__.py",
    "backend/modules/__init__.py",
    "backend/modules/analyse_thematique/__init__.py",
    "backend/modules/tuteur_ia/__init__.py",
    "backend/modules/plugins/__init__.py"
]

for init_file in init_files:
    Path(init_file).write_text('"""Module GEOPOLIS v3"""\n', encoding='utf-8')

print()

# ============================================
# 3. GÉNÉRER LE FRONTEND
# ============================================

print("[3/7] Génération du frontend SPA...")

try:
    from backend.core.frontend_generator import generate_frontend
    generate_frontend()
    print("  [OK] Frontend généré")
except Exception as e:
    print(f"  [!] Erreur: {e}")
    print("  [INFO] Le frontend sera généré au premier démarrage")

print()

# ============================================
# 4. MIGRER L'ANCIEN MODULE ANALYSE_THEMATIQUE
# ============================================

print("[4/7] Migration du module Analyse_thematique...")

old_analyse = Path("Analyse_thematique")
if old_analyse.exists():
    # Copier l'ancien server.py pour référence
    old_server = old_analyse / "server.py"
    if old_server.exists():
        ref_file = backup_path / "Analyse_thematique_old_server.py"
        shutil.copy2(old_server, ref_file)
        print(f"  [OK] Ancien server.py sauvegardé dans backup")
    
    print("  [INFO] Les nouveaux modules sont déjà générés")
else:
    print("  [SKIP] Ancien module non trouvé")

print()

# ============================================
# 5. INSTALLER DÉPENDANCES
# ============================================

print("[5/7] Vérification des dépendances...")

required_packages = [
    "flask",
    "flask-cors",
    "requests",
    "feedparser"
]

missing = []
for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
        print(f"  [OK] {package}")
    except ImportError:
        missing.append(package)
        print(f"  [X] {package} MANQUANT")

if missing:
    print(f"\n  [!] Installez les dépendances manquantes:")
    print(f"      pip install {' '.join(missing)}")
else:
    print("\n  [OK] Toutes les dépendances sont présentes")

print()

# ============================================
# 6. CRÉER requirements.txt
# ============================================

print("[6/7] Génération de requirements.txt...")

requirements = """# GEOPOLIS v3.0 - Dépendances

# Core
Flask>=2.3.0
flask-cors>=4.0.0

# HTTP & RSS
requests>=2.31.0
feedparser>=6.0.0

# Parsing HTML (optionnel)
beautifulsoup4>=4.12.0
lxml>=4.9.0

# IA (optionnel - décommenter si besoin)
# openai>=1.0.0
# anthropic>=0.7.0

# Data processing (optionnel)
# pandas>=2.0.0
"""

Path("requirements.txt").write_text(requirements, encoding='utf-8')
print("  [OK] requirements.txt créé")
print()

# ============================================
# 7. CRÉER SCRIPT DE DÉMARRAGE
# ============================================

print("[7/7] Création du script de démarrage...")

start_script = """@echo off
chcp 65001 >nul
title GEOPOLIS v3.0
color 0A

echo.
echo ================================================================
echo    GEOPOLIS v3.0 - Architecture Unifiee
echo ================================================================
echo.

REM Vérifier Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERREUR] Python non detecte
    pause
    exit /b 1
)

REM Installer dépendances si nécessaire
if not exist ".deps_v3_installed" (
    echo Installation des dependances...
    pip install -r requirements.txt
    echo. > .deps_v3_installed
)

REM Démarrer le serveur
echo Demarrage du serveur...
echo.

python app.py

pause
"""

Path("start_geopolis_v3.bat").write_text(start_script, encoding='utf-8')
print("  [OK] start_geopolis_v3.bat créé")
print()

# ============================================
# RÉSUMÉ
# ============================================

print("=" * 70)
print("   MIGRATION TERMINÉE AVEC SUCCÈS")
print("=" * 70)
print()
print("✓ Backup complet créé:", backup_path)
print("✓ Nouvelle structure créée")
print("✓ Frontend SPA généré")
print("✓ Scripts de démarrage créés")
print()
print("PROCHAINES ÉTAPES:")
print("=" * 70)
print()
print("1. Vérifiez que app.py contient le nouveau code v3.0")
print("   (remplacez-le par le code fourni si nécessaire)")
print()
print("2. Installez les dépendances manquantes:")
print("   pip install -r requirements.txt")
print()
print("3. Lancez l'application:")
print("   python app.py")
print("   OU")
print("   start_geopolis_v3.bat")
print()
print("4. Ouvrez votre navigateur:")
print("   http://127.0.0.1:5000")
print()
print("5. Si le frontend n'est pas configuré, cliquez sur le bouton")
print("   'Configurer Frontend' qui s'affichera automatiquement")
print()
print("=" * 70)
print()
print("DOCUMENTATION:")
print("- Votre ancien code est sauvegardé dans:", backup_path)
print("- Les logs sont dans: logs/geopolis.log")
print("- Configuration: config/geopolis.json")
print()
print("=" * 70)
