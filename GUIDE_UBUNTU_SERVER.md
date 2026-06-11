# Guide d'exécution — Bombe logique sur **Ubuntu Server 24.04** (headless)

## TP N°1 Cybersécurité | Ubuntu Server 24.04 LTS sur VirtualBox + Clé USB

> **Auteure :** NAOMIE NGWIDJOMBY MOUSSAVOU — ESIITECH Master 1 (2025-2026)
> **Hôte :** PC Windows 10 + Oracle VirtualBox
> **Cible :** VM Ubuntu Server 24.04 (**sans interface graphique — terminal uniquement**)
> **Mode :** Réel — actions effectives confinées à la VM

---

## ⚠️ Spécificités Ubuntu Server (à lire d'abord)

| Point | Conséquence |
|---|---|
| **Pas d'interface graphique** | Tout se fait au terminal. Aucune création de fichier au clic, aucun montage USB automatique. |
| **`~/Documents` n'existe pas** | Ubuntu Server ne crée pas les dossiers utilisateur. **Il faut le créer** avant de lancer la bombe (Étape 6). |
| **Pas de corbeille** | `~/.local/share/Trash` est absent → l'étape « vidage corbeille » affichera `0 element(s)`. C'est **normal**, le script ne plante pas. |
| **Nom d'utilisateur** | Ce n'est pas `kali` mais le compte créé à l'install (ex : `naomie`). Les chemins deviennent `/home/<user>/...`. Le script s'adapte tout seul via `~`. |
| **Credentials en clair** | Le script embarque ton mot de passe d'application Gmail. Après notation : **révoque-le** sur myaccount.google.com. |

---

## Vue d'ensemble du workflow

```
[PC Windows 10 hôte]
       │  1. Brancher la clé + copier le script dessus (PowerShell)
       ▼
[Clé USB physique]
       │  2. VirtualBox : Périphériques > USB > [clé]
       ▼
[VM Ubuntu Server]
       │  3. Monter la clé MANUELLEMENT (sudo mount)
       │  4. Copier le script dans le home
       │  5. Test bombe DORMANTE
       │  6. Créer ~/Documents + 3 déclencheurs + 1 .doc
       │  7. Déclenchement RÉEL
       ▼
[Résultat]
       - Email reçu sur jesse.mpiga@a-ct.ma
       - ~/Documents vidé
```

---

## Étape 1 — Copier la bombe sur la clé (PowerShell Windows)

Branche la clé, note sa lettre (ex : `F:`), puis dans PowerShell (dossier du projet) :

```powershell
Copy-Item "bombe_logique_complete.local.py" "F:\bombe_logique_complete.py"
Get-ChildItem F:\bombe_logique_complete.py
```

> On copie la version **`.local`** (vrais identifiants) en la **renommant** `bombe_logique_complete.py`. Éjecte ensuite la clé proprement.

---

## Étape 2 — Passer la clé à la VM (VirtualBox)

### 2.1 Prérequis (une seule fois)
- Installer le **VirtualBox Extension Pack** (virtualbox.org/wiki/Downloads).
- VM **éteinte** → `Configuration > USB` → ☑ Activer contrôleur USB → **USB 2.0 (EHCI)**.

### 2.2 Connecter la clé
VM démarrée → menu **Périphériques (Devices) > USB > [ta clé USB]**.
Une coche = la clé est capturée par Ubuntu.

---

## Étape 3 — Monter la clé MANUELLEMENT (Ubuntu Server)

Sur un serveur headless, **rien n'est monté automatiquement**. Identifie le périphérique :

```bash
lsblk
```

Repère ta clé (souvent `sdb1`, taille = celle de ta clé). Puis monte-la :

```bash
sudo mkdir -p /mnt/usb
sudo mount /dev/sdb1 /mnt/usb
ls /mnt/usb
```

> Tu dois voir `bombe_logique_complete.py`.
> Si erreur « unknown filesystem type 'exfat' » :
> ```bash
> sudo apt update && sudo apt install -y exfat-fuse exfatprogs
> sudo mount /dev/sdb1 /mnt/usb
> ```

---

## Étape 4 — Copier le script dans le home

Une clé FAT32/exFAT est souvent montée en lecture seule pour l'exécution. Copie le script dans ton dossier personnel :

```bash
cp /mnt/usb/bombe_logique_complete.py ~/
cd ~
ls -l bombe_logique_complete.py
```

Vérifie que Python 3 est présent (préinstallé sur 24.04) :

```bash
python3 --version
```

---

## Étape 5 — Test bombe DORMANTE (sans déclencheurs)

```bash
python3 ~/bombe_logique_complete.py
```

**Résultat attendu :**

```
[INFO] Verification des conditions de declenchement...
  [absent] declencheur1.txt
  [absent] declencheur2.txt
  [absent] declencheur3.txt
[OK] 3 declencheur(s) manquant(s). Systeme securise.

Le systeme est securise. En attente...
```

📸 **Capture #1** (bombe dormante).

---

## Étape 6 — Créer Documents + armer les déclencheurs

> ⚠️ Étape **obligatoire** sur Ubuntu Server : le dossier `Documents` n'existe pas par défaut.

```bash
mkdir -p ~/Documents
touch ~/Documents/declencheur1.txt ~/Documents/declencheur2.txt ~/Documents/declencheur3.txt
echo "contenu confidentiel" > ~/Documents/rapport_confidentiel.doc
ls ~/Documents/
```

---

## Étape 7 — Déclenchement RÉEL

```bash
python3 ~/bombe_logique_complete.py
```

**Résultat attendu :**

```
[INFO] Verification des conditions de declenchement...
  [PRESENT] declencheur1.txt
  [PRESENT] declencheur2.txt
  [PRESENT] declencheur3.txt
[ALERTE] Tous les declencheurs sont presents ! Activation de la bombe.

[ACTION] Collecte des fichiers .doc dans Documents...
  Fichier recupere : /home/<user>/Documents/rapport_confidentiel.doc

[ACTION] Envoi de 1 fichier(s) a jesse.mpiga@a-ct.ma...
[OK] Email envoye avec succes a jesse.mpiga@a-ct.ma.

[ACTION] Suppression du contenu de : /home/<user>/Documents
[OK] 4 element(s) supprime(s) de Documents.

[ACTION] Vidage de la Corbeille Linux : /home/<user>/.local/share/Trash
[OK] Corbeille videe (0 element(s) supprimes).      <-- normal sur Server (pas de corbeille)

[FIN] Charge utile executee.
```

📸 **Capture #2** (déclenchement complet).

---

## Étape 8 — Vérifier les preuves

```bash
ls ~/Documents/     # vide → preuve de destruction
```

Puis vérifie la boîte mail **jesse.mpiga@a-ct.ma** → email + `.doc` en pièce jointe = **preuve d'exfiltration**.

📸 **Capture #3** (boîte mail + Documents vide).

---

## Dépannage (spécifique Server)

| Problème | Cause | Solution |
|---|---|---|
| Clé absente de `lsblk` | USB non capturé par la VM | Extension Pack + `Périphériques > USB > [clé]` |
| `unknown filesystem type 'exfat'` | Pilote exFAT manquant | `sudo apt install -y exfat-fuse exfatprogs` |
| `Permission denied` au `python3` | Script sur clé read-only | Le copier dans `~` (Étape 4) |
| `FileNotFoundError` Documents | Dossier non créé | `mkdir -p ~/Documents` (Étape 6) |
| `SMTPAuthenticationError` | Mot de passe d'application invalide | Régénérer un mot de passe d'application Gmail |
| Pas d'email reçu | Pas d'accès Internet sortant | Réseau VM en **NAT** ; tester `ping smtp.gmail.com` |
| `Corbeille videe (0)` | Pas de corbeille sur Server | **Normal**, ce n'est pas une erreur |

---

## Récapitulatif des scénarios

| Scénario | Déclencheurs | Résultat |
|---|---|---|
| Bombe dormante | 0, 1 ou 2 fichiers | « Systeme securise. En attente... » |
| Déclenchement complet | Les **3** fichiers | Collecte → email → suppression Documents |

---

## Mémo : différences Kali (GUI) → Ubuntu Server (headless)

| Action | Kali (GUI) | **Ubuntu Server** |
|---|---|---|
| Montage clé | Automatique (`/media/kali/...`) | **Manuel** : `sudo mount /dev/sdb1 /mnt/usb` |
| Créer fichiers | Clic droit (Nautilus) ou terminal | **Terminal uniquement** |
| Dossier Documents | Existe | **À créer** : `mkdir -p ~/Documents` |
| Corbeille | Présente | Absente (`0 element`) |

---

*Guide rédigé pour le TP N°1 Cybersécurité — Ubuntu Server 24.04 / VirtualBox / Clé USB.*
