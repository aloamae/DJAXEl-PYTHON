#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration Assistant DJ
Script de démonstration des fonctionnalités
"""

import os
import sys
import subprocess
from pathlib import Path

def demo_complete():
    """Démonstration complète du workflow"""
    print("🎵 DÉMONSTRATION ASSISTANT DJ")
    print("=" * 60)
    print("Générateur de Fiches Markdown pour DJ")
    print("=" * 60)
    
    print("\n🎯 Cette démonstration va exécuter:")
    print("   1. Génération des fiches Markdown depuis la liste d'exemple")
    print("   2. Extraction des fiches individuelles")
    print("   3. Génération du set DJ classé")
    print("   4. Génération des playlists")
    print("   5. Affichage des statistiques")
    
    input("\n⏯️  Appuyez sur Entrée pour commencer...")
    
    # Exécuter le test complet
    print("\n🚀 Lancement de la démonstration...")
    
    try:
        result = subprocess.run([sys.executable, "test_complet.py"], 
                              capture_output=True, text=True, cwd="/app")
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        print("\n🎉 Démonstration terminée!")
        
        # Afficher des exemples de fichiers générés
        print("\n📋 Exemples de fichiers générés:")
        print("-" * 40)
        
        # Afficher un exemple de fiche
        chansons_dir = Path("data/output/chansons")
        if chansons_dir.exists():
            md_files = list(chansons_dir.glob("*.md"))
            if md_files:
                example_file = md_files[0]
                print(f"\n🎵 Exemple de fiche: {example_file.name}")
                print("-" * 30)
                with open(example_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:10]
                    for line in lines:
                        print(f"  {line.rstrip()}")
                print("  ... (fichier complet)")
        
        # Afficher un exemple de playlist
        playlists_dir = Path("data/playlists")
        if playlists_dir.exists():
            m3u_files = list(playlists_dir.glob("*.m3u"))
            if m3u_files:
                example_playlist = m3u_files[0]
                print(f"\n🎶 Exemple de playlist: {example_playlist.name}")
                print("-" * 30)
                with open(example_playlist, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:8]
                    for line in lines:
                        print(f"  {line.rstrip()}")
                print("  ... (playlist complète)")
        
        # Résumé final
        print("\n📊 Résumé de la démonstration:")
        print("-" * 40)
        
        stats = {
            "Fichier principal": "data/output/morceaux.md",
            "Fiches individuelles": "data/output/chansons",
            "Set DJ classé": "data/output/set_dj_classe.md",
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
        
        print("\n🎉 Démonstration réussie!")
        print("\n💡 Prochaines étapes:")
        print("   • Modifiez data/input/exemple_chansons.txt avec vos propres chansons")
        print("   • Lancez python AssistDJ_GUI.py pour l'interface graphique")
        print("   • Lancez python AssistDJ_Console.py pour le mode console")
        print("   • Utilisez l'étape 4 pour extraire depuis YouTube")
        
    except Exception as e:
        print(f"❌ Erreur pendant la démonstration: {str(e)}")

if __name__ == "__main__":
    demo_complete()