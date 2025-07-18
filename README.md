# Assistant DJ - Générateur de Fiches Markdown

Ce projet offre une suite complète d'outils pour la gestion de collections musicales DJ avec génération automatique de fiches Markdown détaillées.

## 🎵 Fonctionnalités

- **Interface GUI intuitive** avec tkinter
- **Génération de fiches Markdown** avec métadonnées complètes
- **Extraction depuis YouTube** avec yt-dlp
- **Classification automatique** par genre et énergie
- **Génération de playlists** en multiples formats (M3U, JSON, Markdown)
- **Workflow complet automatisé**

## 🚀 Installation

1. **Cloner le projet**
   ```bash
   git clone <repository-url>
   cd assistant-dj
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'interface**
   ```bash
   python AssistDJ_GUI.py
   ```

## 📋 Utilisation

### Interface Graphique

L'interface principale permet de lancer chaque étape individuellement ou d'exécuter le workflow complet :

1. **Étape 1** : Générer le prompt Markdown morceaux.md
2. **Étape 2** : Extraire les fiches Markdown par chanson
3. **Étape 3** : Générer le set DJ classé par genre
4. **Étape 4** : Extraire les fiches depuis YouTube
5. **Étape 5** : Générer les playlists

### Format des Fichiers d'Entrée

Les listes de chansons doivent être au format texte avec les formats suivants :
- `Artiste - Titre`
- `Titre par Artiste`
- Lignes commençant par `#` sont des commentaires

Exemple :
```
# Disco Classique
Abba - Gimme! Gimme! Gimme! (A Man After Midnight)
Bee Gees - Stayin' Alive

# Pop des années 80
Madonna - Like a Virgin
Michael Jackson - Billie Jean
```

### Format des Fiches Markdown

Chaque chanson génère une fiche avec :
- **Métadonnées** : titre, artiste, BPM, clé, genre, énergie
- **Tags** : classification personnalisée
- **Notes personnelles** : impressions et observations
- **Idées de mix** : suggestions de transitions
- **Liens** : connexions avec d'autres morceaux

Exemple :
```markdown
titre: Gimme! Gimme! Gimme! (A Man After Midnight)
artiste: Abba
bpm: 120
key: A
genre:
  - Disco
  - Pop
energie: 7
date_ajout: 2023-12-07
tags:
  - classic
  - vocal
fichier_mp3: [[mp3/Abba - Gimme! Gimme! Gimme! (A Man After Midnight).mp3]]
```

## 🎛️ Scripts Individuels

### 1. Génération Markdown (`1_generer_markdown_depuis_liste.py`)
- Lit un fichier texte de chansons
- Génère un fichier Markdown consolidé
- Applique le template avec métadonnées par défaut

### 2. Extraction des Fiches (`2_extraire_chansons_en_fichiers.py`)
- Divise le fichier Markdown en fiches individuelles
- Crée un fichier par chanson
- Gère les conflits de noms automatiquement

### 3. Classification par Genre (`4_generer_set_classe_depuis_fiches.py`)
- Analyse toutes les fiches existantes
- Groupe par genre et niveau d'énergie
- Génère des suggestions de sets DJ

### 4. Extraction YouTube (`extraire_fiches_depuis_youtube1.py`)
- Utilise yt-dlp pour extraire les métadonnées
- Supporte vidéos individuelles et playlists
- Génère automatiquement les fiches Markdown

### 5. Génération de Playlists (`genere_playlists1.py`)
- Crée des playlists par genre et énergie
- Génère en formats M3U, JSON et Markdown
- Inclut statistiques et métadonnées

### 6. Workflow Complet (`3_workflow_complet.py`)
- Exécute toutes les étapes séquentiellement
- Gestion d'erreurs et rapports de progression
- Résumé complet des fichiers générés

## 📁 Structure des Dossiers

```
/app/
├── AssistDJ_GUI.py              # Interface principale
├── requirements.txt             # Dépendances Python
├── 1_generer_markdown_depuis_liste.py
├── 2_extraire_chansons_en_fichiers.py
├── 3_workflow_complet.py
├── 4_generer_set_classe_depuis_fiches.py
├── extraire_fiches_depuis_youtube1.py
├── genere_playlists1.py
├── templates/
│   └── chanson_template.md      # Template Markdown
├── data/
│   ├── input/                   # Fichiers texte d'entrée
│   │   └── exemple_chansons.txt
│   ├── output/                  # Fiches Markdown générées
│   │   └── chansons/           # Fiches individuelles
│   └── playlists/              # Playlists générées
└── mp3/                        # Dossier pour fichiers MP3
```

## 🔧 Dépendances

- **yt-dlp** : Extraction YouTube
- **tkinter** : Interface graphique (inclus avec Python)
- **mutagen** : Métadonnées audio
- **beautifulsoup4** : Parsing HTML
- **requests** : Requêtes HTTP
- **pyyaml** : Gestion YAML
- **librosa** : Analyse audio
- **numpy** : Calculs numériques
- **pandas** : Manipulation de données

## 🎵 Exemples d'Utilisation

### Utilisation Basique
1. Placez votre liste de chansons dans `data/input/`
2. Lancez `python AssistDJ_GUI.py`
3. Cliquez sur "Étape 1" pour générer le Markdown
4. Continuez avec les étapes suivantes

### Extraction depuis YouTube
1. Lancez "Étape 4 : Extraire les fiches depuis YouTube"
2. Entrez l'URL de la vidéo ou playlist
3. Les fiches seront automatiquement générées

### Génération de Playlists
1. Assurez-vous d'avoir des fiches dans `data/output/chansons/`
2. Lancez "Étape 5 : Générer les playlists"
3. Les playlists seront créées dans `data/playlists/`

## 📊 Formats de Sortie

### Playlists M3U
```
#EXTM3U
#EXTINF:-1,Abba - Gimme! Gimme! Gimme!
mp3/Abba - Gimme! Gimme! Gimme! (A Man After Midnight).mp3
```

### Playlists JSON
```json
{
  "name": "Playlist_Disco",
  "created": "2023-12-07T10:30:00",
  "songs": [
    {
      "title": "Gimme! Gimme! Gimme!",
      "artist": "Abba",
      "bpm": 120,
      "energy": 7
    }
  ]
}
```

## 🐛 Dépannage

### Problèmes Courants

1. **yt-dlp non trouvé**
   ```bash
   pip install yt-dlp
   ```

2. **Erreur d'encodage**
   - Vérifiez que vos fichiers sont en UTF-8
   - Utilisez un éditeur compatible Unicode

3. **Fichiers non trouvés**
   - Vérifiez la structure des dossiers
   - Exécutez les scripts depuis le dossier racine

### Logs et Débogage

Les scripts affichent des messages détaillés pour faciliter le débogage :
- ✅ Succès
- ❌ Erreurs
- ⚠️ Avertissements
- 🔍 Informations

## 📝 License

Ce projet est sous license MIT. Voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir des issues pour les bugs
- Proposer des améliorations
- Soumettre des pull requests

## 🎉 Remerciements

- **yt-dlp** : Excellent outil d'extraction YouTube
- **tkinter** : Interface graphique simple et efficace
- **Communauté Python** : Bibliothèques fantastiques
