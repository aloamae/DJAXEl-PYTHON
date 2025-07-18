#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du workflow Assistant DJ sans interface graphique
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_step1():
    """Test de la génération Markdown depuis liste"""
    print("🧪 Test Étape 1 : Génération Markdown depuis liste")
    print("-" * 50)
    
    # Importer les fonctions nécessaires
    from pathlib import Path
    from datetime import datetime
    
    # Simuler les fonctions du script 1
    def parse_song_line(line):
        """Parser une ligne de chanson"""
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
            'tags': ['test'],
            'filename': f"{artiste} - {titre}".replace('/', '_').replace('\\', '_')
        }
    
    # Utiliser le fichier d'exemple
    input_file = "data/input/exemple_chansons.txt"
    output_file = "data/output/morceaux.md"
    
    if not os.path.exists(input_file):
        print(f"❌ Fichier d'exemple non trouvé: {input_file}")
        return False
    
    try:
        # Créer le dossier de sortie
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Lire le template
        template_path = Path("templates/chanson_template.md")
        if not template_path.exists():
            print(f"❌ Template non trouvé: {template_path}")
            return False
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Lire le fichier d'entrée
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        markdown_content = ""
        processed_songs = 0
        
        for line in lines:
            song = parse_song_line(line)
            if song:
                # Formater les listes
                genre_list = '\n'.join([f"  - {g}" for g in song['genre']])
                tags_list = '\n'.join([f"  - {t}" for t in song['tags']])
                
                # Formater le contenu
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
                    notes_personnelles="  - À compléter...",
                    idees_mix="  - À définir...",
                    liens="  - À ajouter...",
                    notes_personnelles_detaillees="À compléter selon vos impressions...",
                    idees_mix_detaillees="À définir selon vos expériences de mix..."
                )
                
                markdown_content += song_md + "\n\n" + "="*50 + "\n\n"
                processed_songs += 1
        
        # Écrire le fichier de sortie
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Morceaux DJ - Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total des morceaux traités: {processed_songs}\n\n")
            f.write("="*50 + "\n\n")
            f.write(markdown_content)
        
        print(f"✅ Génération terminée avec succès!")
        print(f"📁 Fichier de sortie: {output_file}")
        print(f"🎵 Morceaux traités: {processed_songs}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_step2():
    """Test de l'extraction des fiches"""
    print("\n🧪 Test Étape 2 : Extraction des fiches par chanson")
    print("-" * 50)
    
    import re
    
    def extract_song_info(song_content):
        """Extraire les informations d'une chanson"""
        info = {}
        
        titre_match = re.search(r'titre:\s*(.+)', song_content)
        artiste_match = re.search(r'artiste:\s*(.+)', song_content)
        
        if titre_match:
            info['titre'] = titre_match.group(1).strip()
        if artiste_match:
            info['artiste'] = artiste_match.group(1).strip()
        
        if 'titre' in info and 'artiste' in info:
            filename = f"{info['artiste']} - {info['titre']}"
        elif 'titre' in info:
            filename = info['titre']
        else:
            filename = "Chanson_sans_titre"
        
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.strip()
        
        return info, filename
    
    input_file = "data/output/morceaux.md"
    output_dir = "data/output/chansons"
    
    if not os.path.exists(input_file):
        print(f"❌ Fichier source non trouvé: {input_file}")
        return False
    
    try:
        # Créer le dossier de sortie
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Lire le fichier d'entrée
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Diviser par le séparateur
        sections = content.split('=' * 50)
        
        # Supprimer l'en-tête
        if sections and ('Morceaux DJ - Généré le' in sections[0] or 'Total des morceaux traités' in sections[0]):
            sections = sections[1:]
        
        extracted_files = []
        
        for i, section in enumerate(sections):
            section = section.strip()
            if not section:
                continue
            
            info, filename = extract_song_info(section)
            
            if filename:
                output_filename = f"{filename}.md"
            else:
                output_filename = f"chanson_{i+1:03d}.md"
            
            output_path = Path(output_dir) / output_filename
            
            # Éviter les conflits
            counter = 1
            base_path = output_path
            while output_path.exists():
                name = base_path.stem
                suffix = base_path.suffix
                output_path = base_path.parent / f"{name}_{counter:02d}{suffix}"
                counter += 1
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(section)
            
            extracted_files.append(output_path)
        
        print(f"✅ Extraction terminée avec succès!")
        print(f"📁 Dossier de sortie: {output_dir}")
        print(f"🎵 Fichiers extraits: {len(extracted_files)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Fonction principale de test"""
    print("🎵 Test du Workflow Assistant DJ")
    print("=" * 60)
    
    # Test étape 1
    success1 = test_step1()
    
    # Test étape 2
    success2 = test_step2()
    
    print("\n" + "=" * 60)
    print("📋 RÉSULTATS DES TESTS")
    print("=" * 60)
    
    print(f"✅ Étape 1 (Génération Markdown): {'✅ SUCCÈS' if success1 else '❌ ÉCHEC'}")
    print(f"✅ Étape 2 (Extraction fiches): {'✅ SUCCÈS' if success2 else '❌ ÉCHEC'}")
    
    if success1 and success2:
        print("\n🎉 Tous les tests sont passés avec succès!")
        print("\n📁 Fichiers générés:")
        
        # Vérifier les fichiers générés
        files_to_check = [
            "data/output/morceaux.md",
            "data/output/chansons/"
        ]
        
        for file_path in files_to_check:
            path = Path(file_path)
            if path.exists():
                if path.is_file():
                    size = path.stat().st_size
                    print(f"  ✅ {file_path} ({size} octets)")
                else:
                    count = len(list(path.glob("*")))
                    print(f"  ✅ {file_path} ({count} fichiers)")
            else:
                print(f"  ❌ {file_path} (non trouvé)")
    else:
        print("\n❌ Certains tests ont échoué.")
    
    return success1 and success2

if __name__ == "__main__":
    main()