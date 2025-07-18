#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assistant DJ - Générateur de Fiches Markdown
Interface GUI pour lancer les différentes étapes du workflow DJ
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import sys
import os
from pathlib import Path

class AssistDJGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistant DJ - Générateur de Fiches Markdown")
        self.root.geometry("700x550")
        self.root.configure(bg='#2c3e50')
        
        # Configuration des couleurs
        self.colors = {
            'bg': '#2c3e50',
            'fg': '#ecf0f1',
            'button': '#3498db',
            'button_hover': '#2980b9',
            'success': '#27ae60',
            'error': '#e74c3c'
        }
        
        self.setup_gui()
        self.setup_directories()
        
    def setup_directories(self):
        """Créer les dossiers nécessaires"""
        directories = [
            'data/input',
            'data/output', 
            'data/playlists',
            'mp3',
            'templates'
        ]
        
        for dir_path in directories:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def setup_gui(self):
        """Configuration de l'interface graphique"""
        
        # Titre principal
        title_label = tk.Label(
            self.root,
            text="🎵 Assistant DJ",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        title_label.pack(pady=20)
        
        # Sous-titre
        subtitle_label = tk.Label(
            self.root,
            text="Générateur de Fiches Markdown pour DJ",
            font=("Segoe UI", 12),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Frame pour les boutons
        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Boutons du workflow
        self.create_workflow_buttons(button_frame)
        
        # Frame pour les boutons de contrôle
        control_frame = tk.Frame(self.root, bg=self.colors['bg'])
        control_frame.pack(pady=20, padx=40, fill='x')
        
        # Bouton workflow complet
        workflow_btn = tk.Button(
            control_frame,
            text="🚀 Lancer le Workflow Complet (Étapes 1 à 5)",
            command=self.run_complete_workflow,
            bg=self.colors['success'],
            fg='white',
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=10,
            relief='flat'
        )
        workflow_btn.pack(pady=10, fill='x')
        
        # Bouton fermer
        close_btn = tk.Button(
            control_frame,
            text="❌ Fermer",
            command=self.root.quit,
            bg=self.colors['error'],
            fg='white',
            font=("Segoe UI", 10),
            padx=20,
            pady=8,
            relief='flat'
        )
        close_btn.pack(pady=10, fill='x')
        
        # Zone de statut
        self.status_var = tk.StringVar(value="Prêt à commencer...")
        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        status_label.pack(pady=10)
        
    def create_workflow_buttons(self, parent):
        """Créer les boutons pour chaque étape du workflow"""
        
        buttons_config = [
            ("1️⃣", "Étape 1 : Générer le prompt Markdown morceaux.md", self.run_step1),
            ("2️⃣", "Étape 2 : Extraire les fiches Markdown par chanson", self.run_step2),
            ("3️⃣", "Étape 3 : Générer le set DJ classé par genre", self.run_step3),
            ("4️⃣", "Étape 4 : Extraire les fiches depuis YouTube", self.run_step4),
            ("5️⃣", "Étape 5 : Générer les playlists", self.run_step5)
        ]
        
        for emoji, text, command in buttons_config:
            btn = tk.Button(
                parent,
                text=f"{emoji} {text}",
                command=command,
                bg=self.colors['button'],
                fg='white',
                font=("Segoe UI", 10),
                padx=20,
                pady=12,
                relief='flat',
                anchor='w'
            )
            btn.pack(pady=8, fill='x')
            
            # Effet hover
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors['button_hover']))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.colors['button']))
    
    def update_status(self, message, color='fg'):
        """Mettre à jour le message de statut"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def run_python_script(self, script_name, step_name):
        """Exécuter un script Python"""
        try:
            self.update_status(f"Exécution de {step_name}...")
            
            if not os.path.exists(script_name):
                messagebox.showerror("Erreur", f"Le script {script_name} n'existe pas.")
                return
                
            # Exécuter le script
            result = subprocess.run([sys.executable, script_name], 
                                  capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                self.update_status(f"✅ {step_name} terminé avec succès")
                messagebox.showinfo("Succès", f"{step_name} terminé avec succès!\n\nSortie:\n{result.stdout}")
            else:
                self.update_status(f"❌ Erreur lors de {step_name}")
                messagebox.showerror("Erreur", f"Erreur lors de {step_name}:\n{result.stderr}")
                
        except Exception as e:
            self.update_status(f"❌ Erreur lors de {step_name}")
            messagebox.showerror("Erreur", f"Erreur lors de l'exécution:\n{str(e)}")
    
    def run_step1(self):
        """Étape 1 : Générer le prompt Markdown morceaux.md"""
        self.run_python_script("1_generer_markdown_depuis_liste.py", "Génération Markdown")
    
    def run_step2(self):
        """Étape 2 : Extraire les fiches Markdown par chanson"""
        self.run_python_script("2_extraire_chansons_en_fichiers.py", "Extraction des fiches")
    
    def run_step3(self):
        """Étape 3 : Générer le set DJ classé par genre"""
        self.run_python_script("4_generer_set_classe_depuis_fiches.py", "Génération du set DJ")
    
    def run_step4(self):
        """Étape 4 : Extraire les fiches depuis YouTube"""
        self.run_python_script("extraire_fiches_depuis_youtube1.py", "Extraction YouTube")
    
    def run_step5(self):
        """Étape 5 : Générer les playlists"""
        self.run_python_script("genere_playlists1.py", "Génération des playlists")
    
    def run_complete_workflow(self):
        """Lancer le workflow complet"""
        self.run_python_script("3_workflow_complet.py", "Workflow complet")

def main():
    root = tk.Tk()
    app = AssistDJGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()