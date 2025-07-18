#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assistant DJ - Mode Console
Version console pour environnements sans interface graphique
"""

import os
import sys
import subprocess
from pathlib import Path

def run_script(script_name, step_name):
    """Exécuter un script Python en mode console"""
    try:
        print(f"\n🎵 Exécution: {step_name}")
        print("-" * 50)
        
        if not os.path.exists(script_name):
            print(f"❌ Le script {script_name} n'existe pas.")
            return False
            
        # Exécuter le script
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, encoding='utf-8')
        
        # Afficher la sortie
        if result.stdout:
            print(result.stdout)
        
        if result.returncode == 0:
            print(f"✅ {step_name} terminé avec succès!")
            return True
        else:
            print(f"❌ Erreur lors de {step_name}:")
            if result.stderr:
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {str(e)}")
        return False

def show_menu():
    """Afficher le menu principal"""
    print("\n" + "=" * 60)
    print("🎵 Assistant DJ - Mode Console")
    print("=" * 60)
    print("1. Étape 1 : Générer le prompt Markdown morceaux.md")
    print("2. Étape 2 : Extraire les fiches Markdown par chanson")
    print("3. Étape 3 : Générer le set DJ classé par genre")
    print("4. Étape 4 : Extraire les fiches depuis YouTube")
    print("5. Étape 5 : Générer les playlists")
    print("6. Lancer le workflow complet (Étapes 1 à 5)")
    print("7. Afficher les statistiques")
    print("8. Quitter")
    print("-" * 60)
    return input("Choisissez une option (1-8): ")

def show_stats():
    """Afficher les statistiques des fichiers générés"""
    print("\n📊 Statistiques des fichiers générés:")
    print("-" * 40)
    
    stats = {
        "Fichier principal": "data/output/morceaux.md",
        "Set DJ classé": "data/output/set_dj_classe.md",
        "Fiches individuelles": "data/output/chansons",
        "Playlists": "data/playlists"
    }
    
    for name, path in stats.items():
        path_obj = Path(path)
        if path_obj.exists():
            if path_obj.is_file():
                size = path_obj.stat().st_size
                print(f"✅ {name}: {size} octets")
            else:
                count = len(list(path_obj.glob("*")))
                print(f"✅ {name}: {count} fichiers")
        else:
            print(f"❌ {name}: Non trouvé")

def main():
    """Fonction principale du mode console"""
    print("🎵 Assistant DJ - Mode Console")
    print("Générateur de Fiches Markdown pour DJ")
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            # Utiliser le fichier d'exemple par défaut
            print("\n📁 Utilisation du fichier d'exemple: data/input/exemple_chansons.txt")
            # Créer un script temporaire qui utilise le fichier d'exemple
            temp_script = """
import sys
sys.path.append('.')
from pathlib import Path
from datetime import datetime

# Utiliser directement le fichier d'exemple
input_file = "data/input/exemple_chansons.txt"
output_file = "data/output/morceaux.md"

# Importer les fonctions nécessaires
def parse_song_line(line):
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    
    if ' - ' in line:
        parts = line.split(' - ', 1)
        artiste = parts[0].strip()
        titre = parts[1].strip()
    elif ' par ' in line:
        parts = line.split(' par ', 1)
        titre = parts[0].strip()
        artiste = parts[1].strip()
    else:
        titre = line
        artiste = "Artiste Inconnu"
    
    return {
        'titre': titre,
        'artiste': artiste,
        'bpm': 120,
        'key': 'A',
        'genre': ['Pop'],
        'energie': 5,
        'date_ajout': datetime.now().strftime('%Y-%m-%d'),
        'tags': ['console'],
        'filename': f"{artiste} - {titre}".replace('/', '_').replace('\\\\', '_')
    }

# Exécuter la génération
try:
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open("templates/chanson_template.md", 'r', encoding='utf-8') as f:
        template = f.read()
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    markdown_content = ""
    processed_songs = 0
    
    for line in lines:
        song = parse_song_line(line)
        if song:
            genre_list = '\\n'.join([f"  - {g}" for g in song['genre']])
            tags_list = '\\n'.join([f"  - {t}" for t in song['tags']])
            
            song_md = template.format(
                titre=song['titre'],
                artiste=song['artiste'],
                bpm=song['bpm'],
                key=song['key'],
                genre_list=genre_list,
                energie=song['energie'],
                date_ajout=song['date_ajout'],
                tags_list=tags_list,
                filename=song['filename'],
                notes_personnelles="  - Mode console...",
                idees_mix="  - À définir...",
                liens="  - À ajouter...",
                notes_personnelles_detaillees="Généré en mode console",
                idees_mix_detaillees="À définir selon vos expériences de mix..."
            )
            
            markdown_content += song_md + "\\n\\n" + "="*50 + "\\n\\n"
            processed_songs += 1
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Morceaux DJ - Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
        f.write(f"Total des morceaux traités: {processed_songs}\\n\\n")
        f.write("="*50 + "\\n\\n")
        f.write(markdown_content)
    
    print(f"✅ Génération terminée avec succès!")
    print(f"📁 Fichier de sortie: {output_file}")
    print(f"🎵 Morceaux traités: {processed_songs}")
    
except Exception as e:
    print(f"❌ Erreur: {str(e)}")
"""
            
            # Écrire et exécuter le script temporaire
            with open("/tmp/temp_step1.py", "w") as f:
                f.write(temp_script)
            
            result = subprocess.run([sys.executable, "/tmp/temp_step1.py"], 
                                  capture_output=True, text=True)
            
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            
        elif choice == "2":
            run_script("2_extraire_chansons_en_fichiers.py", "Extraction des fiches")
        elif choice == "3":
            run_script("4_generer_set_classe_depuis_fiches.py", "Génération du set DJ")
        elif choice == "4":
            print("\n⚠️  Étape 4 nécessite une URL YouTube")
            print("Cette étape est interactive et nécessite une interface graphique.")
            print("Utilisez la version GUI pour cette fonctionnalité.")
        elif choice == "5":
            run_script("genere_playlists1.py", "Génération des playlists")
        elif choice == "6":
            print("\n🚀 Lancement du workflow complet...")
            run_script("3_workflow_complet.py", "Workflow complet")
        elif choice == "7":
            show_stats()
        elif choice == "8":
            print("\n👋 Au revoir!")
            break
        else:
            print("❌ Option invalide. Veuillez choisir entre 1 et 8.")
        
        input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()