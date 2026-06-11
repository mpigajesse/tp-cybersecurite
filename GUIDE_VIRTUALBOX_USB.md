# Guide d'exécution — Bombe logique via clé USB (VirtualBox)

## TP N°1 Cybersécurité | Kali Linux sur **VirtualBox** + Clé USB physique

> **Auteure :** NAOMIE NGWIDJOMBY MOUSSAVOU — ESIITECH Master 1 (2025-2026)
> **Hôte :** PC Windows 10 + Oracle VirtualBox
> **Cible :** VM Kali Linux (environnement isolé)
> **Mode :** Réel — actions effectives confinées à la VM

---

## ⚠️ À lire avant de commencer

| Point | Détail |
|---|---|
| **Isolation** | Toutes les actions (email, suppression) sont **réelles** mais **uniquement dans la VM**. Ne jamais exécuter le script sur l'hôte Windows. |
| **`~/Documents` sera vidé** | Le dossier Documents de Kali sera réellement supprimé. Déplace tout fichier à conserver avant l'étape 6. |
| **Credentials en clair** | Le script embarque ton mot de passe d'application Gmail en clair. Après notation : **révoque-le** sur myaccount.google.com et ne laisse pas la clé sur une machine tierce. |
| **Extension Pack** | VirtualBox a besoin du **Extension Pack** pour le passthrough USB 2.0/3.0 (voir Étape 3). |

---

## Vue d'ensemble du workflow

```
[PC Windows 10 hôte]
       │  1. Brancher la clé USB
       │  2. Copier bombe_logique_complete.local.py → clé (renommée)
       ▼
[Clé USB physique]
       │  3. VirtualBox : Devices > USB > [clé] (passthrough)
       ▼
[VM Kali Linux]
       │  4. Monter / localiser la clé
       │  5. Test bombe DORMANTE
       │  6. Créer les 3 déclencheurs + 1 fichier .doc
       │  7. Déclenchement RÉEL
       ▼
[Résultat]
       - Email reçu sur jesse.mpiga@a-ct.ma
       - ~/Documents vidé
       - Corbeille vidée
```

---

## Étape 1 — Brancher la clé USB sur le PC Windows 10

1. Insère la clé USB dans un port du **PC hôte**.
2. Ouvre l'Explorateur (`Win + E`) et note la **lettre du lecteur** (ex : `E:`, `F:`…).

---

## Étape 2 — Copier la bombe sur la clé (PowerShell Windows)

Ouvre **PowerShell** dans le dossier du projet, puis adapte la lettre de ta clé (ici `F:`) :

```powershell
Copy-Item "bombe_logique_complete.local.py" "F:\bombe_logique_complete.py"
```

> On copie la version **`.local`** (avec tes vrais identifiants) en la **renommant** `bombe_logique_complete.py` sur la clé.

Vérifie la copie :

```powershell
Get-ChildItem F:\bombe_logique_complete.py
```

Puis **éjecte proprement** la clé (icône « Retirer le périphérique » dans la barre des tâches) avant de la passer à la VM.

---

## Étape 3 — Passer la clé à la VM Kali (VirtualBox)

### 3.1 Prérequis : Extension Pack (une seule fois)

Le passthrough USB nécessite le **Oracle VirtualBox Extension Pack** :

1. Télécharge-le sur **virtualbox.org/wiki/Downloads** (même version que ton VirtualBox).
2. Installe-le : `Fichier > Outils > Gestionnaire d'extensions > Installer`.

### 3.2 Activer le contrôleur USB de la VM

VM Kali **éteinte** → `Configuration > USB` :

- ☑ Activer le contrôleur USB
- Sélectionner **USB 2.0 (EHCI)** ou **USB 3.0 (xHCI)**

### 3.3 Connecter la clé pendant que la VM tourne

Démarre la VM Kali, puis dans la fenêtre VirtualBox :

```
Menu : Périphériques (Devices) > USB > [ta clé USB]
```

Une coche apparaît à côté du nom de la clé = elle est désormais capturée par Kali.

---

## Étape 4 — Localiser la clé dans Kali Linux

Dans un terminal Kali :

```bash
lsblk
```

Repère ta clé (souvent `sdb1`). Le point de montage est généralement :

```
/media/kali/<NOM_DE_LA_CLE>/
```

Si elle n'est pas montée automatiquement, ouvre le **gestionnaire de fichiers** et clique sur la clé, ou monte-la manuellement :

```bash
sudo mkdir -p /mnt/usb
sudo mount /dev/sdb1 /mnt/usb
ls /mnt/usb
```

> Dans la suite, remplace `<CHEMIN_CLE>` par le chemin réel (ex : `/media/kali/USB32`).

---

## Étape 5 — Test bombe DORMANTE (sans déclencheurs)

```bash
python3 <CHEMIN_CLE>/bombe_logique_complete.py
```

**Résultat attendu :**

```
============================================================
  TP N 1 - Bombe logique Python | Kali Linux
============================================================

[INFO] Verification des conditions de declenchement...
  [absent] declencheur1.txt
  [absent] declencheur2.txt
  [absent] declencheur3.txt
[OK] 3 declencheur(s) manquant(s). Systeme securise.

Le systeme est securise. En attente...
```

📸 **Capture d'écran #1** (bombe dormante) pour le rapport.

---

## Étape 6 — Armer les déclencheurs (Kali)

### Option A — Terminal

```bash
touch ~/Documents/declencheur1.txt ~/Documents/declencheur2.txt ~/Documents/declencheur3.txt
echo "contenu confidentiel" > ~/Documents/rapport_confidentiel.doc
ls ~/Documents/
```

### Option B — Interface graphique (Fichiers / Nautilus)

1. Ouvre **Dossier personnel > Documents**
2. Clic droit → *Nouveau document > Document vide* → nomme `declencheur1.txt`
3. Répète pour `declencheur2.txt` et `declencheur3.txt`
4. Crée `rapport_confidentiel.doc`

---

## Étape 7 — Déclenchement RÉEL

```bash
python3 <CHEMIN_CLE>/bombe_logique_complete.py
```

**Résultat attendu :**

```
[INFO] Verification des conditions de declenchement...
  [PRESENT] declencheur1.txt
  [PRESENT] declencheur2.txt
  [PRESENT] declencheur3.txt
[ALERTE] Tous les declencheurs sont presents ! Activation de la bombe.

[ACTION] Collecte des fichiers .doc dans Documents...
  Fichier recupere : /home/kali/Documents/rapport_confidentiel.doc

[ACTION] Envoi de 1 fichier(s) a jesse.mpiga@a-ct.ma...
[OK] Email envoye avec succes a jesse.mpiga@a-ct.ma.

[ACTION] Suppression du contenu de : /home/kali/Documents
[OK] 4 element(s) supprime(s) de Documents.

[ACTION] Vidage de la Corbeille Linux : /home/kali/.local/share/Trash
[OK] Corbeille videe.

[FIN] Charge utile executee.
```

📸 **Capture d'écran #2** (déclenchement complet) pour le rapport.

---

## Étape 8 — Vérifier les preuves

```bash
ls ~/Documents/          # doit être vide → preuve de destruction
```

Puis vérifie la boîte mail **jesse.mpiga@a-ct.ma** → l'email avec le `.doc` en pièce jointe = **preuve d'exfiltration**.

📸 **Capture d'écran #3** (boîte mail + Documents vide).

---

## Récapitulatif des scénarios

| Scénario | Déclencheurs présents | Résultat |
|---|---|---|
| Bombe dormante | 0, 1 ou 2 fichiers | « Systeme securise. En attente... » |
| Déclenchement complet | Les **3** fichiers | Collecte → email → suppression → corbeille vidée |

---

## Dépannage rapide

| Problème | Cause probable | Solution |
|---|---|---|
| Clé absente du menu `Périphériques > USB` | Extension Pack non installé / contrôleur USB désactivé | Étape 3.1 et 3.2 |
| Clé non montée dans Kali | Auto-montage désactivé | Monter manuellement (Étape 4) |
| `SMTPAuthenticationError` | Mot de passe d'application invalide / 2FA non activée | Régénérer un mot de passe d'application Gmail |
| `Permission denied` à l'exécution | Clé montée en lecture seule | Copier le script dans `~` puis l'exécuter : `cp <CHEMIN_CLE>/bombe_logique_complete.py ~ && python3 ~/bombe_logique_complete.py` |
| Pas d'email reçu | Réseau VM en NAT sans accès sortant | Vérifier `Configuration > Réseau > NAT` et la connexion Internet de la VM |

---

## Différences VMware → VirtualBox (mémo)

| Action | VMware | **VirtualBox** |
|---|---|---|
| Passer la clé à la VM | `VM > Removable Devices > Connect` | `Périphériques > USB > [clé]` |
| Prérequis USB | Intégré | **Extension Pack** requis |
| Point de montage Kali | `/media/` | `/media/kali/<nom>` ou montage manuel |

---

*Guide rédigé pour le TP N°1 Cybersécurité — Kali Linux / VirtualBox / Clé USB physique.*
