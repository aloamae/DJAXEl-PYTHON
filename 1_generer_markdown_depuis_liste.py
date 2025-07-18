#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assistant DJ - Étape 1
Générer le prompt Markdown morceaux.md depuis une liste de chansons
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

def select_input_file():
    """Sélectionner le fichier d'entrée"""
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(
        title="Sélectionner le fichier liste des chansons",
        filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
        initialdir="data/input"
    )
    
    root.destroy()
    return file_path

def parse_song_line(line):
    """Parser une ligne de chanson"""
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    
    # Format attendu: "Artiste - Titre" ou "Titre par Artiste"
    if ' - ' in line:
        parts = line.split(' - ', 1)
        artiste = parts[0].strip()
        titre = parts[1].strip()
    elif ' par ' in line:
        parts = line.split(' par ', 1)
        titre = parts[0].strip()
        artiste = parts[1].strip()
    else:
        # Si pas de séparateur, considérer comme titre uniquement
        titre = line
        artiste = "Artiste Inconnu"
    
    return {
        'titre': titre,
        'artiste': artiste,
        'bpm': 120,  # Valeur par défaut
        'key': 'A',  # Valeur par défaut
        'genre': ['Pop'],  # Valeur par défaut
        'energie': 5,  # Valeur par défaut
        'date_ajout': datetime.now().strftime('%Y-%m-%d'),
        'tags': ['nouveau'],
        'filename': f"{artiste} - {titre}".replace('/', '_').replace('\\', '_')
    }

def generate_markdown_from_list(input_file, output_file):
    """Générer le fichier Markdown depuis la liste"""
    try:
        # Créer le dossier de sortie
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Lire le template
        template_path = Path("templates/chanson_template.md")
        if not template_path.exists():
            raise FileNotFoundError(f"Template non trouvé: {template_path}")
        
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
        
        return processed_songs
        
    except Exception as e:
        raise Exception(f"Erreur lors de la génération: {str(e)}")

def main():
    """Fonction principale"""
    print("🎵 Assistant DJ - Étape 1: Génération Markdown depuis liste")
    print("="*60)
    
    # Sélectionner le fichier d'entrée
    input_file = select_input_file()
    if not input_file:
        print("❌ Aucun fichier sélectionné.")
        return
    
    # Fichier de sortie
    output_file = "data/output/morceaux.md"
    
    try:
        # Générer le Markdown
        processed_songs = generate_markdown_from_list(input_file, output_file)
        
        print(f"✅ Génération terminée avec succès!")
        print(f"📁 Fichier de sortie: {output_file}")
        print(f"🎵 Morceaux traités: {processed_songs}")
        
        # Afficher message de succès
        if 'tkinter' in sys.modules:
            messagebox.showinfo("Succès", f"Génération terminée!\n\nMorceaux traités: {processed_songs}\nFichier: {output_file}")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        if 'tkinter' in sys.modules:
            messagebox.showerror("Erreur", f"Erreur lors de la génération:\n{str(e)}")

if __name__ == "__main__":
    main()