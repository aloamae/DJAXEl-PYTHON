#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assistant DJ - Workflow Complet
Exécuter toutes les étapes séquentiellement (Étapes 1 à 5)
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

def run_script(script_name, step_name, step_number):
    """Exécuter un script Python"""
    try:
        print(f"\n{'='*60}")
        print(f"🎵 ÉTAPE {step_number}: {step_name}")
        print(f"{'='*60}")
        
        if not os.path.exists(script_name):
            raise FileNotFoundError(f"Le script {script_name} n'existe pas.")
        
        # Exécuter le script
        print(f"▶️  Exécution de {script_name}...")
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, encoding='utf-8')
        
        # Afficher la sortie
        if result.stdout:
            print("📄 Sortie:")
            print(result.stdout)
        
        if result.returncode == 0:
            print(f"✅ {step_name} terminé avec succès!")
            return True
        else:
            print(f"❌ Erreur lors de {step_name}:")
            if result.stderr:
                print("🚨 Erreur détaillée:")
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution de {script_name}: {str(e)}")
        return False

def check_dependencies():
    """Vérifier les dépendances nécessaires"""
    print("🔍 Vérification des dépendances...")
    
    # Vérifier les dossiers nécessaires
    directories = [
        'data/input',
        'data/output', 
        'data/playlists',
        'mp3',
        'templates'
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Dossier vérifié: {dir_path}")
    
    # Vérifier les scripts
    scripts = [
        '1_generer_markdown_depuis_liste.py',
        '2_extraire_chansons_en_fichiers.py',
        '4_generer_set_classe_depuis_fiches.py',
        'extraire_fiches_depuis_youtube1.py',
        'genere_playlists1.py'
    ]
    
    missing_scripts = []
    for script in scripts:
        if not os.path.exists(script):
            missing_scripts.append(script)
        else:
            print(f"✅ Script trouvé: {script}")
    
    if missing_scripts:
        print(f"❌ Scripts manquants: {missing_scripts}")
        return False
    
    print("✅ Toutes les dépendances sont présentes!")
    return True

def display_summary():
    """Afficher un résumé des fichiers générés"""
    print("\n" + "="*60)
    print("📋 RÉSUMÉ DU WORKFLOW")
    print("="*60)
    
    # Fichiers générés
    files_to_check = [
        ("data/output/morceaux.md", "Fichier Markdown principal"),
        ("data/output/chansons/", "Fiches individuelles"),
        ("data/output/set_dj_classe.md", "Set DJ classé"),
        ("data/playlists/", "Playlists générées")
    ]
    
    for file_path, description in files_to_check:
        path = Path(file_path)
        if path.exists():
            if path.is_file():
                size = path.stat().st_size
                print(f"✅ {description}: {file_path} ({size} octets)")
            else:
                # Compter les fichiers dans le dossier
                count = len(list(path.glob("*")))
                print(f"✅ {description}: {file_path} ({count} fichiers)")
        else:
            print(f"❌ {description}: {file_path} (non trouvé)")
    
    print("\n🎉 Workflow terminé!")

def main():
    """Fonction principale du workflow complet"""
    print("🎵 Assistant DJ - Workflow Complet")
    print("="*60)
    print("Exécution séquentielle des étapes 1 à 5")
    print("="*60)
    
    # Vérifier les dépendances
    if not check_dependencies():
        print("❌ Dépendances manquantes. Arrêt du workflow.")
        if 'tkinter' in sys.modules:
            messagebox.showerror("Erreur", "Dépendances manquantes.\nVérifiez que tous les scripts sont présents.")
        return
    
    # Définir les étapes
    steps = [
        ("1_generer_markdown_depuis_liste.py", "Générer le prompt Markdown morceaux.md", 1),
        ("2_extraire_chansons_en_fichiers.py", "Extraire les fiches Markdown par chanson", 2),
        ("4_generer_set_classe_depuis_fiches.py", "Générer le set DJ classé par genre", 3),
        ("extraire_fiches_depuis_youtube1.py", "Extraire les fiches depuis YouTube", 4),
        ("genere_playlists1.py", "Générer les playlists", 5)
    ]
    
    # Exécuter chaque étape
    start_time = time.time()
    successful_steps = 0
    
    for script_name, step_name, step_number in steps:
        success = run_script(script_name, step_name, step_number)
        
        if success:
            successful_steps += 1
            print(f"✅ Étape {step_number} terminée!")
        else:
            print(f"❌ Étape {step_number} échouée!")
            
            # Demander si on continue
            if 'tkinter' in sys.modules:
                response = messagebox.askyesno(
                    "Erreur", 
                    f"L'étape {step_number} a échoué.\n\nVoulez-vous continuer avec les étapes suivantes?"
                )
                if not response:
                    break
            else:
                response = input(f"Continuer malgré l'erreur? (o/n): ")
                if response.lower() not in ['o', 'oui', 'y', 'yes']:
                    break
        
        # Petite pause entre les étapes
        time.sleep(1)
    
    # Calculer le temps total
    total_time = time.time() - start_time
    
    # Afficher le résumé
    display_summary()
    
    print(f"\n⏱️  Temps total d'exécution: {total_time:.2f} secondes")
    print(f"✅ Étapes réussies: {successful_steps}/{len(steps)}")
    
    # Message final
    if successful_steps == len(steps):
        message = f"🎉 Workflow terminé avec succès!\n\nToutes les étapes ont été exécutées.\nTemps total: {total_time:.2f} secondes"
        print(f"\n🎉 Workflow terminé avec succès!")
    else:
        message = f"⚠️  Workflow terminé avec des erreurs.\n\nÉtapes réussies: {successful_steps}/{len(steps)}\nTemps total: {total_time:.2f} secondes"
        print(f"\n⚠️  Workflow terminé avec des erreurs.")
    
    # Afficher message de fin
    if 'tkinter' in sys.modules:
        if successful_steps == len(steps):
            messagebox.showinfo("Succès", message)
        else:
            messagebox.showwarning("Attention", message)

if __name__ == "__main__":
    main()