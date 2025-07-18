#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assistant DJ - Étape 3
Générer le set DJ classé par genre depuis les fiches
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from collections import defaultdict

def scan_songs_directory():
    """Scanner le dossier des chansons"""
    songs_dir = Path("data/output/chansons")
    if not songs_dir.exists():
        raise FileNotFoundError(f"Dossier des chansons non trouvé: {songs_dir}")
    
    return list(songs_dir.glob("*.md"))

def parse_song_file(file_path):
    """Parser un fichier de chanson"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        song_info = {}
        
        # Extraire les informations de base
        patterns = {
            'titre': r'titre:\s*(.+)',
            'artiste': r'artiste:\s*(.+)',
            'bpm': r'bpm:\s*(\d+)',
            'key': r'key:\s*(.+)',
            'energie': r'energie:\s*(\d+)',
            'date_ajout': r'date_ajout:\s*(.+)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                song_info[key] = match.group(1).strip()
        
        # Extraire les genres
        genre_section = re.search(r'genre:\s*\n((?:\s*-\s*.+\n?)+)', content)
        if genre_section:
            genres = []
            for line in genre_section.group(1).split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    genres.append(line[2:].strip())
            song_info['genres'] = genres
        else:
            song_info['genres'] = ['Non classé']
        
        # Extraire les tags
        tags_section = re.search(r'tags:\s*\n((?:\s*-\s*.+\n?)+)', content)
        if tags_section:
            tags = []
            for line in tags_section.group(1).split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    tags.append(line[2:].strip())
            song_info['tags'] = tags
        else:
            song_info['tags'] = []
        
        song_info['file_path'] = file_path
        return song_info
        
    except Exception as e:
        print(f"⚠️  Erreur lors du parsing de {file_path}: {str(e)}")
        return None

def group_songs_by_genre(songs):
    """Grouper les chansons par genre"""
    genre_groups = defaultdict(list)
    
    for song in songs:
        if song and 'genres' in song:
            for genre in song['genres']:
                genre_groups[genre].append(song)
    
    return dict(genre_groups)

def group_songs_by_energy(songs):
    """Grouper les chansons par niveau d'énergie"""
    energy_groups = defaultdict(list)
    
    for song in songs:
        if song and 'energie' in song:
            try:
                energy = int(song['energie'])
                if energy <= 3:
                    energy_groups['Faible (1-3)'].append(song)
                elif energy <= 6:
                    energy_groups['Moyenne (4-6)'].append(song)
                else:
                    energy_groups['Élevée (7-10)'].append(song)
            except ValueError:
                energy_groups['Non définie'].append(song)
        else:
            energy_groups['Non définie'].append(song)
    
    return dict(energy_groups)

def generate_set_by_genre(songs, output_file):
    """Générer le set DJ classé par genre"""
    try:
        # Grouper par genre
        genre_groups = group_songs_by_genre(songs)
        
        # Grouper par énergie
        energy_groups = group_songs_by_energy(songs)
        
        # Créer le dossier de sortie
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Set DJ Classé - Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total des morceaux: {len(songs)}\n")
            f.write(f"Genres identifiés: {len(genre_groups)}\n\n")
            
            # Section par genre
            f.write("## 🎵 Classification par Genre\n\n")
            
            for genre, genre_songs in sorted(genre_groups.items()):
                f.write(f"### {genre} ({len(genre_songs)} morceaux)\n\n")
                
                # Trier par BPM puis par énergie
                sorted_songs = sorted(genre_songs, key=lambda x: (
                    int(x.get('bpm', 120)),
                    int(x.get('energie', 5))
                ))
                
                for song in sorted_songs:
                    title = song.get('titre', 'Titre inconnu')
                    artist = song.get('artiste', 'Artiste inconnu')
                    bpm = song.get('bpm', 'N/A')
                    key = song.get('key', 'N/A')
                    energy = song.get('energie', 'N/A')
                    
                    f.write(f"- **{artist} - {title}**\n")
                    f.write(f"  - BPM: {bpm} | Clé: {key} | Énergie: {energy}\n")
                    f.write(f"  - Fichier: `{song['file_path'].name}`\n\n")
            
            f.write("\n" + "="*60 + "\n\n")
            
            # Section par énergie
            f.write("## ⚡ Classification par Niveau d'Énergie\n\n")
            
            for energy_level, energy_songs in sorted(energy_groups.items()):
                f.write(f"### {energy_level} ({len(energy_songs)} morceaux)\n\n")
                
                # Trier par genre puis par BPM
                sorted_songs = sorted(energy_songs, key=lambda x: (
                    x.get('genres', [''])[0] if x.get('genres') else '',
                    int(x.get('bpm', 120))
                ))
                
                for song in sorted_songs:
                    title = song.get('titre', 'Titre inconnu')
                    artist = song.get('artiste', 'Artiste inconnu')
                    bpm = song.get('bpm', 'N/A')
                    genres = ', '.join(song.get('genres', ['Non classé']))
                    
                    f.write(f"- **{artist} - {title}**\n")
                    f.write(f"  - BPM: {bpm} | Genres: {genres}\n")
                    f.write(f"  - Fichier: `{song['file_path'].name}`\n\n")
            
            f.write("\n" + "="*60 + "\n\n")
            
            # Suggestions de sets
            f.write("## 🎛️ Suggestions de Sets DJ\n\n")
            
            # Set progression énergétique
            f.write("### Set Progression Énergétique\n\n")
            f.write("**Warm-up (Énergie faible):**\n")
            if 'Faible (1-3)' in energy_groups:
                for song in energy_groups['Faible (1-3)'][:5]:
                    f.write(f"- {song.get('artiste', 'Artiste inconnu')} - {song.get('titre', 'Titre inconnu')}\n")
            f.write("\n")
            
            f.write("**Build-up (Énergie moyenne):**\n")
            if 'Moyenne (4-6)' in energy_groups:
                for song in energy_groups['Moyenne (4-6)'][:5]:
                    f.write(f"- {song.get('artiste', 'Artiste inconnu')} - {song.get('titre', 'Titre inconnu')}\n")
            f.write("\n")
            
            f.write("**Peak-time (Énergie élevée):**\n")
            if 'Élevée (7-10)' in energy_groups:
                for song in energy_groups['Élevée (7-10)'][:5]:
                    f.write(f"- {song.get('artiste', 'Artiste inconnu')} - {song.get('titre', 'Titre inconnu')}\n")
            f.write("\n")
            
            # Sets par genre
            f.write("### Sets par Genre\n\n")
            for genre, genre_songs in sorted(genre_groups.items()):
                if len(genre_songs) >= 3:
                    f.write(f"**Set {genre}:**\n")
                    for song in genre_songs[:5]:
                        f.write(f"- {song.get('artiste', 'Artiste inconnu')} - {song.get('titre', 'Titre inconnu')}\n")
                    f.write("\n")
        
        return len(songs), len(genre_groups)
        
    except Exception as e:
        raise Exception(f"Erreur lors de la génération du set: {str(e)}")

def main():
    """Fonction principale"""
    print("🎵 Assistant DJ - Étape 3: Génération du set DJ classé")
    print("="*60)
    
    try:
        # Scanner les fichiers de chansons
        song_files = scan_songs_directory()
        print(f"📁 Fichiers trouvés: {len(song_files)}")
        
        if not song_files:
            raise Exception("Aucun fichier de chanson trouvé dans data/output/chansons/")
        
        # Parser les fichiers
        songs = []
        for file_path in song_files:
            song = parse_song_file(file_path)
            if song:
                songs.append(song)
        
        print(f"🎵 Chansons analysées: {len(songs)}")
        
        # Générer le set
        output_file = "data/output/set_dj_classe.md"
        total_songs, total_genres = generate_set_by_genre(songs, output_file)
        
        print(f"✅ Génération terminée avec succès!")
        print(f"📁 Fichier de sortie: {output_file}")
        print(f"🎵 Morceaux traités: {total_songs}")
        print(f"🎶 Genres identifiés: {total_genres}")
        
        # Afficher message de succès
        try:
            if 'tkinter' in sys.modules:
                messagebox.showinfo("Succès", f"Set DJ généré!\n\nMorceaux: {total_songs}\nGenres: {total_genres}\nFichier: {output_file}")
        except:
            pass  # Ignorer les erreurs d'interface graphique
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        try:
            if 'tkinter' in sys.modules:
                messagebox.showerror("Erreur", f"Erreur lors de la génération:\n{str(e)}")
        except:
            pass  # Ignorer les erreurs d'interface graphique

if __name__ == "__main__":
    main()