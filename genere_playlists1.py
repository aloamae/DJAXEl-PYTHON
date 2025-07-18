#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assistant DJ - Étape 5
Générer les playlists depuis les fiches Markdown
"""

import os
import re
import sys
import json
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
        
        # Extraire le fichier MP3
        mp3_match = re.search(r'fichier_mp3:\s*\[\[(.+?)\]\]', content)
        if mp3_match:
            song_info['fichier_mp3'] = mp3_match.group(1).strip()
        
        song_info['file_path'] = file_path
        return song_info
        
    except Exception as e:
        print(f"⚠️  Erreur lors du parsing de {file_path}: {str(e)}")
        return None

def generate_m3u_playlist(songs, playlist_name, output_dir):
    """Générer une playlist M3U"""
    try:
        playlist_path = Path(output_dir) / f"{playlist_name}.m3u"
        
        with open(playlist_path, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            f.write(f"# Playlist: {playlist_name}\n")
            f.write(f"# Générée le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Nombre de morceaux: {len(songs)}\n\n")
            
            for song in songs:
                title = song.get('titre', 'Titre inconnu')
                artist = song.get('artiste', 'Artiste inconnu')
                fichier_mp3 = song.get('fichier_mp3', f"mp3/{artist} - {title}.mp3")
                
                f.write(f"#EXTINF:-1,{artist} - {title}\n")
                f.write(f"{fichier_mp3}\n\n")
        
        return playlist_path
        
    except Exception as e:
        raise Exception(f"Erreur lors de la génération M3U: {str(e)}")

def generate_json_playlist(songs, playlist_name, output_dir):
    """Générer une playlist JSON"""
    try:
        playlist_path = Path(output_dir) / f"{playlist_name}.json"
        
        playlist_data = {
            "name": playlist_name,
            "created": datetime.now().isoformat(),
            "total_songs": len(songs),
            "songs": []
        }
        
        for song in songs:
            song_data = {
                "title": song.get('titre', 'Titre inconnu'),
                "artist": song.get('artiste', 'Artiste inconnu'),
                "bpm": int(song.get('bpm', 120)),
                "key": song.get('key', 'A'),
                "energy": int(song.get('energie', 5)),
                "genres": song.get('genres', ['Non classé']),
                "tags": song.get('tags', []),
                "file_path": song.get('fichier_mp3', ''),
                "date_added": song.get('date_ajout', '')
            }
            playlist_data["songs"].append(song_data)
        
        with open(playlist_path, 'w', encoding='utf-8') as f:
            json.dump(playlist_data, f, ensure_ascii=False, indent=2)
        
        return playlist_path
        
    except Exception as e:
        raise Exception(f"Erreur lors de la génération JSON: {str(e)}")

def generate_markdown_playlist(songs, playlist_name, output_dir):
    """Générer une playlist Markdown"""
    try:
        playlist_path = Path(output_dir) / f"{playlist_name}.md"
        
        with open(playlist_path, 'w', encoding='utf-8') as f:
            f.write(f"# Playlist: {playlist_name}\n\n")
            f.write(f"**Créée le:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Nombre de morceaux:** {len(songs)}\n\n")
            
            # Statistiques
            genres = defaultdict(int)
            bpms = []
            energies = []
            
            for song in songs:
                for genre in song.get('genres', ['Non classé']):
                    genres[genre] += 1
                try:
                    bpms.append(int(song.get('bpm', 120)))
                    energies.append(int(song.get('energie', 5)))
                except ValueError:
                    pass
            
            f.write("## 📊 Statistiques\n\n")
            f.write("### Genres\n")
            for genre, count in sorted(genres.items()):
                f.write(f"- {genre}: {count} morceaux\n")
            
            if bpms:
                f.write(f"\n### BPM\n")
                f.write(f"- Moyenne: {sum(bpms) // len(bpms)} BPM\n")
                f.write(f"- Min: {min(bpms)} BPM\n")
                f.write(f"- Max: {max(bpms)} BPM\n")
            
            if energies:
                f.write(f"\n### Énergie\n")
                f.write(f"- Moyenne: {sum(energies) // len(energies)}/10\n")
                f.write(f"- Min: {min(energies)}/10\n")
                f.write(f"- Max: {max(energies)}/10\n")
            
            f.write("\n## 🎵 Morceaux\n\n")
            
            for i, song in enumerate(songs, 1):
                title = song.get('titre', 'Titre inconnu')
                artist = song.get('artiste', 'Artiste inconnu')
                bpm = song.get('bpm', 'N/A')
                key = song.get('key', 'N/A')
                energy = song.get('energie', 'N/A')
                genres_str = ', '.join(song.get('genres', ['Non classé']))
                
                f.write(f"### {i}. {artist} - {title}\n\n")
                f.write(f"- **BPM:** {bpm}\n")
                f.write(f"- **Clé:** {key}\n")
                f.write(f"- **Énergie:** {energy}/10\n")
                f.write(f"- **Genres:** {genres_str}\n")
                f.write(f"- **Fichier:** `{song.get('fichier_mp3', '')}`\n\n")
        
        return playlist_path
        
    except Exception as e:
        raise Exception(f"Erreur lors de la génération Markdown: {str(e)}")

def create_playlists_by_genre(songs, output_dir):
    """Créer des playlists par genre"""
    playlists = []
    genre_groups = defaultdict(list)
    
    for song in songs:
        for genre in song.get('genres', ['Non classé']):
            genre_groups[genre].append(song)
    
    for genre, genre_songs in genre_groups.items():
        if len(genre_songs) >= 2:  # Minimum 2 chansons pour créer une playlist
            playlist_name = f"Playlist_{genre.replace(' ', '_')}"
            
            # Trier par BPM puis par énergie
            sorted_songs = sorted(genre_songs, key=lambda x: (
                int(x.get('bpm', 120)),
                int(x.get('energie', 5))
            ))
            
            # Générer les formats
            m3u_path = generate_m3u_playlist(sorted_songs, playlist_name, output_dir)
            json_path = generate_json_playlist(sorted_songs, playlist_name, output_dir)
            md_path = generate_markdown_playlist(sorted_songs, playlist_name, output_dir)
            
            playlists.append({
                'name': playlist_name,
                'genre': genre,
                'songs_count': len(sorted_songs),
                'files': [m3u_path, json_path, md_path]
            })
    
    return playlists

def create_playlists_by_energy(songs, output_dir):
    """Créer des playlists par niveau d'énergie"""
    playlists = []
    energy_groups = defaultdict(list)
    
    for song in songs:
        try:
            energy = int(song.get('energie', 5))
            if energy <= 3:
                energy_groups['Low_Energy'].append(song)
            elif energy <= 6:
                energy_groups['Medium_Energy'].append(song)
            else:
                energy_groups['High_Energy'].append(song)
        except ValueError:
            energy_groups['Unknown_Energy'].append(song)
    
    for energy_level, energy_songs in energy_groups.items():
        if len(energy_songs) >= 2:
            playlist_name = f"Playlist_{energy_level}"
            
            # Trier par BPM
            sorted_songs = sorted(energy_songs, key=lambda x: int(x.get('bpm', 120)))
            
            # Générer les formats
            m3u_path = generate_m3u_playlist(sorted_songs, playlist_name, output_dir)
            json_path = generate_json_playlist(sorted_songs, playlist_name, output_dir)
            md_path = generate_markdown_playlist(sorted_songs, playlist_name, output_dir)
            
            playlists.append({
                'name': playlist_name,
                'energy_level': energy_level,
                'songs_count': len(sorted_songs),
                'files': [m3u_path, json_path, md_path]
            })
    
    return playlists

def main():
    """Fonction principale"""
    print("🎵 Assistant DJ - Étape 5: Génération des playlists")
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
        
        # Créer le dossier de sortie
        output_dir = "data/playlists"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Créer les playlists par genre
        print("🎶 Génération des playlists par genre...")
        genre_playlists = create_playlists_by_genre(songs, output_dir)
        
        # Créer les playlists par énergie
        print("⚡ Génération des playlists par énergie...")
        energy_playlists = create_playlists_by_energy(songs, output_dir)
        
        # Créer une playlist complète
        print("📋 Génération de la playlist complète...")
        complete_playlist = "Playlist_Complete"
        all_songs = sorted(songs, key=lambda x: (
            x.get('artiste', 'Artiste inconnu'),
            x.get('titre', 'Titre inconnu')
        ))
        
        complete_m3u = generate_m3u_playlist(all_songs, complete_playlist, output_dir)
        complete_json = generate_json_playlist(all_songs, complete_playlist, output_dir)
        complete_md = generate_markdown_playlist(all_songs, complete_playlist, output_dir)
        
        # Résumé
        total_playlists = len(genre_playlists) + len(energy_playlists) + 1
        
        print(f"✅ Génération terminée avec succès!")
        print(f"📁 Dossier de sortie: {output_dir}")
        print(f"🎵 Morceaux traités: {len(songs)}")
        print(f"📋 Playlists générées: {total_playlists}")
        print(f"  - Par genre: {len(genre_playlists)}")
        print(f"  - Par énergie: {len(energy_playlists)}")
        print(f"  - Complète: 1")
        
        # Afficher le détail
        print("\n📋 Détail des playlists:")
        for playlist in genre_playlists:
            print(f"  🎶 {playlist['name']}: {playlist['songs_count']} morceaux")
        for playlist in energy_playlists:
            print(f"  ⚡ {playlist['name']}: {playlist['songs_count']} morceaux")
        print(f"  📋 {complete_playlist}: {len(all_songs)} morceaux")
        
        # Afficher message de succès
        if 'tkinter' in sys.modules:
            messagebox.showinfo("Succès", f"Playlists générées!\n\nMorceaux: {len(songs)}\nPlaylists: {total_playlists}\nDossier: {output_dir}")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        if 'tkinter' in sys.modules:
            messagebox.showerror("Erreur", f"Erreur lors de la génération:\n{str(e)}")

if __name__ == "__main__":
    main()