#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assistant DJ - Étape 4
Extraire les fiches depuis YouTube avec yt-dlp
"""

import os
import re
import sys
import json
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess

def get_youtube_url():
    """Demander l'URL YouTube à l'utilisateur"""
    root = tk.Tk()
    root.withdraw()
    
    url = simpledialog.askstring(
        "URL YouTube",
        "Entrez l'URL de la vidéo/playlist YouTube:",
        parent=root
    )
    
    root.destroy()
    return url

def check_ytdlp_installed():
    """Vérifier si yt-dlp est installé"""
    try:
        result = subprocess.run(['yt-dlp', '--version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def extract_youtube_metadata(url):
    """Extraire les métadonnées YouTube avec yt-dlp"""
    try:
        # Commande yt-dlp pour extraire les métadonnées seulement
        cmd = [
            'yt-dlp',
            '--no-download',
            '--dump-json',
            '--flat-playlist',
            url
        ]
        
        print(f"🔍 Extraction des métadonnées depuis: {url}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Erreur yt-dlp: {result.stderr}")
        
        # Parser les résultats JSON
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                try:
                    video_data = json.loads(line)
                    videos.append(video_data)
                except json.JSONDecodeError:
                    continue
        
        return videos
        
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction: {str(e)}")

def extract_detailed_metadata(video_id):
    """Extraire les métadonnées détaillées d'une vidéo"""
    try:
        cmd = [
            'yt-dlp',
            '--no-download',
            '--dump-json',
            f'https://www.youtube.com/watch?v={video_id}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return None
        
        return json.loads(result.stdout)
        
    except Exception:
        return None

def parse_title_for_song_info(title):
    """Parser le titre pour extraire artiste et titre"""
    title = title.strip()
    
    # Patterns courants pour les titres YouTube
    patterns = [
        r'(.+?)\s*-\s*(.+?)(?:\s*\([^)]*\))?(?:\s*\[[^\]]*\])?$',  # Artiste - Titre
        r'(.+?)\s*:\s*(.+?)(?:\s*\([^)]*\))?(?:\s*\[[^\]]*\])?$',  # Artiste : Titre
        r'(.+?)\s*\|\s*(.+?)(?:\s*\([^)]*\))?(?:\s*\[[^\]]*\])?$',  # Artiste | Titre
        r'(.+?)\s*by\s*(.+?)(?:\s*\([^)]*\))?(?:\s*\[[^\]]*\])?$', # Titre by Artiste
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            part1, part2 = match.groups()
            part1, part2 = part1.strip(), part2.strip()
            
            # Détecter si c'est "Titre by Artiste"
            if 'by' in pattern:
                return part2, part1  # Artiste, Titre
            else:
                return part1, part2  # Artiste, Titre
    
    # Si aucun pattern ne correspond, utiliser tout comme titre
    return "Artiste Inconnu", title

def guess_genre_from_title(title, description=""):
    """Deviner le genre à partir du titre et de la description"""
    content = (title + " " + description).lower()
    
    genre_keywords = {
        'Disco': ['disco', 'boogie', 'funk', 'groove'],
        'Pop': ['pop', 'hit', 'chart', 'mainstream'],
        'Rock': ['rock', 'metal', 'guitar', 'band'],
        'Electronic': ['electronic', 'edm', 'techno', 'house', 'trance', 'dance'],
        'Hip-Hop': ['hip hop', 'rap', 'beats', 'urban'],
        'R&B': ['r&b', 'rnb', 'soul', 'smooth'],
        'Jazz': ['jazz', 'swing', 'blues'],
        'Classical': ['classical', 'orchestra', 'symphony'],
        'Reggae': ['reggae', 'jamaica', 'dub'],
        'Country': ['country', 'folk', 'acoustic']
    }
    
    for genre, keywords in genre_keywords.items():
        if any(keyword in content for keyword in keywords):
            return genre
    
    return 'Pop'  # Genre par défaut

def generate_song_file(video_data, output_dir):
    """Générer un fichier de chanson depuis les métadonnées YouTube"""
    try:
        # Extraire les informations de base
        title = video_data.get('title', 'Titre inconnu')
        duration = video_data.get('duration', 0)
        description = video_data.get('description', '')
        upload_date = video_data.get('upload_date', '')
        
        # Parser le titre pour extraire artiste et titre
        artiste, titre = parse_title_for_song_info(title)
        
        # Deviner le genre
        genre = guess_genre_from_title(title, description)
        
        # Estimer le BPM (très approximatif)
        bpm = 120  # Valeur par défaut
        if duration:
            if duration < 180:  # Moins de 3 minutes
                bpm = 140
            elif duration > 300:  # Plus de 5 minutes
                bpm = 100
        
        # Estimer l'énergie
        energie = 5  # Valeur par défaut
        if 'party' in title.lower() or 'dance' in title.lower():
            energie = 8
        elif 'chill' in title.lower() or 'slow' in title.lower():
            energie = 3
        
        # Formater la date
        if upload_date:
            try:
                date_obj = datetime.strptime(upload_date, '%Y%m%d')
                date_ajout = date_obj.strftime('%Y-%m-%d')
            except:
                date_ajout = datetime.now().strftime('%Y-%m-%d')
        else:
            date_ajout = datetime.now().strftime('%Y-%m-%d')
        
        # Créer le contenu du fichier
        filename = f"{artiste} - {titre}".replace('/', '_').replace('\\', '_')
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Lire le template
        template_path = Path("templates/chanson_template.md")
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
        else:
            # Template de base si le fichier n'existe pas
            template = """titre: {titre}
artiste: {artiste}
bpm: {bpm}
key: {key}
genre:
{genre_list}
energie: {energie}
date_ajout: {date_ajout}
tags:
{tags_list}
fichier_mp3: [[mp3/{filename}.mp3]]
Notes Personnelles:
{notes_personnelles}
Idées de Mix:
{idees_mix}
Liens:
{liens}
---

## 🎵 Notes Personnelles

{notes_personnelles_detaillees}

## 🎛️ Idées de Mix

{idees_mix_detaillees}
"""
        
        # Formater le contenu
        content = template.format(
            titre=titre,
            artiste=artiste,
            bpm=bpm,
            key='A',  # Valeur par défaut
            genre_list=f"  - {genre}",
            energie=energie,
            date_ajout=date_ajout,
            tags_list="  - youtube\n  - extrait",
            filename=filename,
            notes_personnelles="  - Extrait depuis YouTube",
            idees_mix="  - À définir après écoute",
            liens="  - À ajouter après analyse",
            notes_personnelles_detaillees=f"Extrait depuis YouTube: {title}",
            idees_mix_detaillees="À définir après écoute et analyse du BPM/clé"
        )
        
        # Écrire le fichier
        output_path = Path(output_dir) / f"{filename}.md"
        
        # Éviter les conflits de noms
        counter = 1
        base_path = output_path
        while output_path.exists():
            name = base_path.stem
            suffix = base_path.suffix
            output_path = base_path.parent / f"{name}_{counter:02d}{suffix}"
            counter += 1
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Erreur lors de la génération du fichier: {str(e)}")

def main():
    """Fonction principale"""
    print("🎵 Assistant DJ - Étape 4: Extraction depuis YouTube")
    print("="*60)
    
    try:
        # Vérifier yt-dlp
        if not check_ytdlp_installed():
            raise Exception("yt-dlp n'est pas installé. Installez-le avec: pip install yt-dlp")
        
        # Demander l'URL
        url = get_youtube_url()
        if not url:
            print("❌ Aucune URL fournie.")
            return
        
        print(f"🔍 URL: {url}")
        
        # Extraire les métadonnées
        videos = extract_youtube_metadata(url)
        print(f"📹 Vidéos trouvées: {len(videos)}")
        
        if not videos:
            raise Exception("Aucune vidéo trouvée à cette URL")
        
        # Dossier de sortie
        output_dir = "data/output/chansons"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Traiter chaque vidéo
        generated_files = []
        for i, video in enumerate(videos):
            print(f"🎵 Traitement {i+1}/{len(videos)}: {video.get('title', 'Titre inconnu')}")
            
            # Extraire les métadonnées détaillées si nécessaire
            if 'id' in video:
                detailed_data = extract_detailed_metadata(video['id'])
                if detailed_data:
                    video.update(detailed_data)
            
            # Générer le fichier
            output_path = generate_song_file(video, output_dir)
            generated_files.append(output_path)
            print(f"✅ Généré: {output_path.name}")
        
        print(f"✅ Extraction terminée avec succès!")
        print(f"📁 Dossier de sortie: {output_dir}")
        print(f"🎵 Fichiers générés: {len(generated_files)}")
        
        # Afficher message de succès
        if 'tkinter' in sys.modules:
            messagebox.showinfo("Succès", f"Extraction terminée!\n\nFichiers générés: {len(generated_files)}\nDossier: {output_dir}")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        if 'tkinter' in sys.modules:
            messagebox.showerror("Erreur", f"Erreur lors de l'extraction:\n{str(e)}")

if __name__ == "__main__":
    main()