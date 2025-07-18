#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assistant DJ - Étape 2
Extraire les fiches Markdown par chanson en fichiers séparés
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

def select_input_file():
    """Sélectionner le fichier Markdown d'entrée"""
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(
        title="Sélectionner le fichier morceaux.md",
        filetypes=[("Fichiers Markdown", "*.md"), ("Tous les fichiers", "*.*")],
        initialdir="data/output"
    )
    
    root.destroy()
    return file_path

def extract_song_info(song_content):
    """Extraire les informations d'une chanson depuis le contenu Markdown"""
    info = {}
    
    # Extraire titre et artiste
    titre_match = re.search(r'titre:\s*(.+)', song_content)
    artiste_match = re.search(r'artiste:\s*(.+)', song_content)
    
    if titre_match:
        info['titre'] = titre_match.group(1).strip()
    if artiste_match:
        info['artiste'] = artiste_match.group(1).strip()
    
    # Générer nom de fichier sécurisé
    if 'titre' in info and 'artiste' in info:
        filename = f"{info['artiste']} - {info['titre']}"
    elif 'titre' in info:
        filename = info['titre']
    else:
        filename = "Chanson_sans_titre"
    
    # Nettoyer le nom de fichier
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.strip()
    
    return info, filename

def split_markdown_file(input_file, output_dir):
    """Diviser le fichier Markdown en fichiers séparés"""
    try:
        # Créer le dossier de sortie
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Lire le fichier d'entrée
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Diviser par le séparateur
        sections = content.split('=' * 50)
        
        # Supprimer l'en-tête (première section)
        if sections and ('Morceaux DJ - Généré le' in sections[0] or 'Total des morceaux traités' in sections[0]):
            sections = sections[1:]
        
        extracted_files = []
        
        for i, section in enumerate(sections):
            section = section.strip()
            if not section:
                continue
            
            # Extraire les informations de la chanson
            info, filename = extract_song_info(section)
            
            # Créer le nom de fichier final
            if filename:
                output_filename = f"{filename}.md"
            else:
                output_filename = f"chanson_{i+1:03d}.md"
            
            # Chemin complet du fichier
            output_path = Path(output_dir) / output_filename
            
            # Éviter les conflits de noms
            counter = 1
            base_path = output_path
            while output_path.exists():
                name = base_path.stem
                suffix = base_path.suffix
                output_path = base_path.parent / f"{name}_{counter:02d}{suffix}"
                counter += 1
            
            # Écrire le fichier
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(section)
            
            extracted_files.append(output_path)
            print(f"✅ Extrait: {output_path.name}")
        
        return extracted_files
        
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction: {str(e)}")

def main():
    """Fonction principale"""
    print("🎵 Assistant DJ - Étape 2: Extraction des fiches par chanson")
    print("="*60)
    
    # Sélectionner le fichier d'entrée
    input_file = select_input_file()
    if not input_file:
        print("❌ Aucun fichier sélectionné.")
        return
    
    # Dossier de sortie
    output_dir = "data/output/chansons"
    
    try:
        # Extraire les fichiers
        extracted_files = split_markdown_file(input_file, output_dir)
        
        print(f"✅ Extraction terminée avec succès!")
        print(f"📁 Dossier de sortie: {output_dir}")
        print(f"🎵 Fichiers extraits: {len(extracted_files)}")
        
        # Afficher la liste des fichiers
        if extracted_files:
            print("\n📋 Fichiers créés:")
            for file_path in extracted_files[:10]:  # Montrer les 10 premiers
                print(f"  • {file_path.name}")
            if len(extracted_files) > 10:
                print(f"  ... et {len(extracted_files) - 10} autres fichiers")
        
        # Afficher message de succès
        if 'tkinter' in sys.modules:
            messagebox.showinfo("Succès", f"Extraction terminée!\n\nFichiers extraits: {len(extracted_files)}\nDossier: {output_dir}")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        if 'tkinter' in sys.modules:
            messagebox.showerror("Erreur", f"Erreur lors de l'extraction:\n{str(e)}")

if __name__ == "__main__":
    main()