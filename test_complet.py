#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet du workflow Assistant DJ
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def test_workflow_complete():
    """Tester le workflow complet"""
    print("🎵 Test du Workflow Complet Assistant DJ")
    print("=" * 60)
    
    # Scripts à tester (sans interface)
    scripts_to_test = [
        ("test_workflow.py", "Tests de base (Étapes 1-2)"),
        ("4_generer_set_classe_depuis_fiches.py", "Génération du set DJ (Étape 3)"),
        ("genere_playlists1.py", "Génération des playlists (Étape 5)")
    ]
    
    results = []
    
    for script, description in scripts_to_test:
        print(f"\n🧪 Test: {description}")
        print("-" * 50)
        
        try:
            result = subprocess.run(
                [sys.executable, script],
                capture_output=True,
                text=True,
                cwd="/app"
            )
            
            if result.returncode == 0:
                print(f"✅ {description} - SUCCÈS")
                results.append((script, True, ""))
            else:
                print(f"❌ {description} - ÉCHEC")
                print(f"Erreur: {result.stderr}")
                results.append((script, False, result.stderr))
                
        except Exception as e:
            print(f"❌ {description} - EXCEPTION")
            print(f"Erreur: {str(e)}")
            results.append((script, False, str(e)))
    
    # Résumé des résultats
    print("\n" + "=" * 60)
    print("📋 RÉSULTATS FINAUX")
    print("=" * 60)
    
    successes = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for script, success, error in results:
        status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        print(f"{status} - {script}")
        if error:
            print(f"  └── {error[:100]}...")
    
    print(f"\n📊 Score: {successes}/{total} tests réussis")
    
    if successes == total:
        print("🎉 Tous les tests sont passés avec succès!")
        
        # Afficher statistiques des fichiers générés
        print("\n📁 Fichiers générés:")
        stats = check_generated_files()
        for category, count in stats.items():
            print(f"  {category}: {count}")
    else:
        print("❌ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return successes == total

def check_generated_files():
    """Vérifier les fichiers générés"""
    stats = {}
    
    # Compter les fichiers dans chaque dossier
    directories = {
        "Fiches individuelles": "data/output/chansons",
        "Playlists M3U": "data/playlists",
        "Playlists JSON": "data/playlists",
        "Playlists Markdown": "data/playlists"
    }
    
    for name, dir_path in directories.items():
        if Path(dir_path).exists():
            if name == "Fiches individuelles":
                count = len(list(Path(dir_path).glob("*.md")))
            elif name == "Playlists M3U":
                count = len(list(Path(dir_path).glob("*.m3u")))
            elif name == "Playlists JSON":
                count = len(list(Path(dir_path).glob("*.json")))
            elif name == "Playlists Markdown":
                count = len(list(Path(dir_path).glob("*.md")))
            else:
                count = len(list(Path(dir_path).glob("*")))
            
            stats[name] = count
        else:
            stats[name] = 0
    
    # Fichiers principaux
    main_files = {
        "Fichier principal morceaux.md": "data/output/morceaux.md",
        "Set DJ classé": "data/output/set_dj_classe.md"
    }
    
    for name, file_path in main_files.items():
        if Path(file_path).exists():
            stats[name] = "✅ Présent"
        else:
            stats[name] = "❌ Absent"
    
    return stats

def show_app_info():
    """Afficher les informations de l'application"""
    print("\n" + "=" * 60)
    print("ℹ️  INFORMATIONS DE L'APPLICATION")
    print("=" * 60)
    
    print("🎵 Assistant DJ - Générateur de Fiches Markdown")
    print("   Une suite complète d'outils pour DJ")
    print()
    
    print("📋 Fonctionnalités principales:")
    print("   • Génération de fiches Markdown détaillées")
    print("   • Extraction depuis YouTube avec yt-dlp")
    print("   • Classification par genre et énergie")
    print("   • Génération de playlists multiples formats")
    print("   • Interface GUI intuitive")
    print()
    
    print("🚀 Utilisation:")
    print("   1. Placez vos listes de chansons dans data/input/")
    print("   2. Lancez python AssistDJ_GUI.py")
    print("   3. Suivez les étapes dans l'interface")
    print()
    
    print("📁 Structure des fichiers générés:")
    print("   • data/output/morceaux.md - Fichier principal")
    print("   • data/output/chansons/ - Fiches individuelles")
    print("   • data/output/set_dj_classe.md - Set classé")
    print("   • data/playlists/ - Playlists en multiples formats")
    print()
    
    print("🔧 Formats supportés:")
    print("   • Entrée: Fichiers texte (.txt)")
    print("   • Sortie: Markdown (.md), M3U (.m3u), JSON (.json)")
    print("   • Extraction: YouTube (via yt-dlp)")

if __name__ == "__main__":
    show_app_info()
    
    # Lancer les tests
    success = test_workflow_complete()
    
    if success:
        print("\n🎉 Application prête à être utilisée!")
        print("💡 Lancez 'python AssistDJ_GUI.py' pour l'interface graphique")
    else:
        print("\n⚠️  Certains composants nécessitent des corrections")