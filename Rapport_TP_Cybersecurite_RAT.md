# Rapport TP Cybersécurité — Étude de Trojans (RAT)

**Étudiant :** Jesse Mpiga  
**Date de rendu :** 03 juin 2026  
**Module :** Cybersécurité  
**Environnement de test :** Kali Linux sur VMware — Exécution réelle en VM isolée

> **Note technique — Syntaxe terminal :**
> ```
> ┌────────────┬─────────────────────────────┐
> │  Terminal  │ Variable profil utilisateur │
> ├────────────┼─────────────────────────────┤
> │ PowerShell │ $env:USERPROFILE            │
> ├────────────┼─────────────────────────────┤
> │ CMD        │ %USERPROFILE%               │
> └────────────┴─────────────────────────────┘
> ```
> Les exemples de commandes de ce rapport utilisent la syntaxe **PowerShell**.

---

## Introduction

Un **RAT** (Remote Access Trojan) est un logiciel malveillant qui permet à un attaquant d'obtenir un accès complet et furtif à la machine d'une victime à distance. Contrairement à un accès légitime (TeamViewer, RDP), le RAT s'installe et s'exécute à l'insu de l'utilisateur. Il est généralement distribué via phishing, pièces jointes malveillantes, ou fausses mises à jour logicielles.

Dans ce TP, nous étudions cinq RAT représentatifs ainsi qu'une bombe logique Python exécutée en conditions réelles sur une VM Kali Linux.

---

## 1. DarkComet

### 1.1 Objectif principal

DarkComet est l'un des RAT les plus tristement célèbres. Développé par Jean-Pierre Lesueur (alias DarkCoderSc) initialement à des fins éducatives, il a été massivement détourné à des fins d'espionnage et de surveillance. Son objectif est de donner à l'attaquant un contrôle total et discret sur la machine victime, avec un accent particulier sur la surveillance.

### 1.2 Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| Écoute du microphone | Enregistrement audio en temps réel sans indicateur visuel |
| Vol de mots de passe | Extraction depuis les navigateurs (Chrome, Firefox), clients FTP, messageries |
| Captures d'écran | Screenshots périodiques ou déclenchés à la demande |
| Keylogger | Enregistrement de toutes les frappes clavier |
| Contrôle à distance | Shell CMD distant, gestionnaire de fichiers, gestionnaire de processus |
| Webcam | Activation de la caméra à distance |
| Modification du registre | Persistance via clés de démarrage automatique |
| Communication C2 | Canal chiffré vers un serveur de commande et contrôle |

### 1.3 Risques

- **Espionnage personnel et professionnel** : identifiants bancaires, données confidentielles, communications privées
- **Usage politique** : DarkComet a été utilisé par le gouvernement syrien entre 2011 et 2012 pour surveiller des dissidents et des journalistes
- **Propagation latérale** : une machine compromise peut servir de point d'entrée vers un réseau entier
- **Chantage** : les captures d'écran et enregistrements peuvent être utilisés à des fins d'extorsion

### 1.4 Moyens de détection

- **Trafic réseau** : connexions sortantes anormales sur le port **1604/TCP** (port par défaut), détectables par un pare-feu ou un IDS (Suricata, Snort)
- **Registre Windows** : présence de la clé `HKCU\Software\DarkComet-RAT` ou entrées suspectes dans `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- **Processus suspects** : nom de processus inhabituels comme `dcomnet.exe`, `scvvhsot.exe`
- **Antivirus** : signatures connues dans la plupart des solutions AV modernes
- **Analyse comportementale** : accès simultané au microphone, à la webcam et au clavier sans action utilisateur

### 1.5 Mesures de protection

- Maintenir l'antivirus et l'OS à jour
- Utiliser un pare-feu applicatif avec politique de refus par défaut (default-deny)
- Ne pas ouvrir les pièces jointes d'emails non sollicités
- Surveiller les processus en cours d'exécution (Task Manager, Process Explorer)
- Utiliser un EDR (Endpoint Detection and Response) capable de détecter les comportements anormaux

---

## 2. Remcos

### 2.1 Objectif principal

Remcos (Remote Control and Surveillance Software) est commercialisé légalement par la société Breaking Security comme outil de télémaintenance. Cependant, il est fréquemment distribué sur des forums underground et utilisé comme RAT dans des campagnes d'attaque ciblées (spear-phishing, APT). Son objectif est le contrôle complet et la surveillance de la machine victime.

### 2.2 Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| Shell distant | Exécution de commandes CMD/PowerShell à distance |
| Keylogger | Enregistrement des frappes avec horodatage |
| Capture webcam et microphone | Surveillance audiovisuelle en temps réel |
| Panneau C2 web | Interface d'administration sophistiquée pour gérer plusieurs victimes |
| Exfiltration de données | Transfert de fichiers vers le serveur attaquant |
| Persistance | Via le registre, tâches planifiées ou dossier Startup |
| Contournement UAC | Élévation de privilèges sur certaines versions Windows |
| Chiffrement des communications | Trafic C2 chiffré (TLS/SSL) pour éviter l'inspection réseau |

### 2.3 Risques

- **Campagnes APT** : Remcos est régulièrement associé à des groupes APT ciblant des entreprises et des gouvernements
- **Distribution via phishing** : souvent livré dans des macros Office malveillantes ou des PDF piégés
- **Difficulté de détection** : le chiffrement TLS rend l'analyse du trafic réseau plus difficile
- **Vol de données sensibles** : documents confidentiels, identifiants, communications

### 2.4 Moyens de détection

- **Signatures AV et YARA** : règles disponibles publiquement (source : malpedia.caad.fkie.fraunhofer.de)
- **Registre** : clé `HKCU\Software\Remcos` ou `HKCU\Software\Remcos-[ID]`
- **Analyse réseau** : connexions TLS vers des domaines récemment enregistrés ou avec certificats auto-signés
- **Sandbox** : soumission du binaire à Any.run, Joe Sandbox, ou Cuckoo pour analyse comportementale
- **EDR** : détection de l'injection dans des processus légitimes (process hollowing)

### 2.5 Mesures de protection

- **Désactiver les macros Office** par défaut (via GPO en entreprise)
- Filtrage des emails avec sandboxing des pièces jointes
- Activer l'authentification multifacteur (MFA) sur tous les comptes
- Segmenter le réseau pour limiter la propagation
- Former les utilisateurs au phishing (sensibilisation)

---

## 3. QuasarRAT

### 3.1 Objectif principal

QuasarRAT est un outil open-source (disponible sur GitHub) développé initialement à des fins légitimes de télémaintenance. Sa légèreté, sa stabilité et son code source accessible en font un outil fréquemment réutilisé et modifié par des attaquants pour mener des attaques ciblées, y compris par des groupes APT étatiques.

### 3.2 Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| Prise en main à distance | Interface graphique simulant un bureau distant (type RDP) |
| Gestionnaire de fichiers | Navigation, téléchargement et upload de fichiers |
| Keylogger | Enregistrement des frappes clavier |
| Gestionnaire de processus | Affichage et arrêt des processus en cours |
| Shell distant | Exécution de commandes système |
| Informations système | Récupération de l'OS, IP, nom de la machine, utilisateurs |
| Persistance | Clés de registre et dossier Startup |
| Chiffrement | Communications chiffrées entre client et serveur |

### 3.3 Risques

- **Attributable aux APT étatiques** : utilisé notamment par APT10 (Chine) dans des campagnes d'espionnage industriel
- **Variantes personnalisées** : le code source public permet de créer des versions modifiées contournant les signatures AV classiques
- **Exfiltration à grande échelle** : propriété intellectuelle, données gouvernementales
- **Ciblage d'infrastructures critiques** : secteurs de l'énergie, de la défense, de la santé

### 3.4 Moyens de détection

- **Réseau** : connexions sortantes sur le port **4782/TCP** (par défaut), certificats TLS auto-signés
- **Règles Snort/Suricata** : signatures disponibles dans les bases de règles communautaires
- **Hachages de fichiers** : comparaison avec les IOC (Indicators of Compromise) publiés par les CERT
- **Comportement** : création de fichiers dans `%AppData%`, modifications du registre de démarrage
- **VirusTotal** : soumission du binaire pour analyse multi-moteurs

### 3.5 Mesures de protection

- **Segmentation réseau** : interdire les connexions sortantes non autorisées par pare-feu
- Surveillance des connexions réseau (netstat, Wireshark, SIEM)
- Mettre en place un programme de **Threat Intelligence** pour suivre les IOC
- Appliquer le principe du **moindre privilège** (utilisateurs sans droits admin)
- Utiliser un **IDS/IPS** sur le périmètre réseau

---

## 4. NjRAT

### 4.1 Objectif principal

NjRAT (également connu sous les noms Bladabindi ou LV) est l'un des RAT les plus répandus dans le monde, notamment au Moyen-Orient et en Afrique du Nord. Sa simplicité d'utilisation le rend très populaire parmi les cybercriminels débutants (script kiddies). Son objectif est le contrôle à distance, le vol d'informations et la constitution de botnets.

### 4.2 Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| Contrôle à distance | Shell distant et gestionnaire de fichiers |
| Keylogger | Enregistrement des frappes avec capture du titre de la fenêtre active |
| Vol de mots de passe | Extraction des credentials stockés localement |
| Webcam et microphone | Surveillance audiovisuelle |
| Exécution de plugins | Architecture modulaire permettant d'étendre les fonctionnalités |
| Propagation par USB | Copie automatique sur les clés USB connectées |
| Botnets | Gestion centralisée de nombreuses machines infectées |
| Screenshots | Captures d'écran à la demande |

### 4.3 Risques

- **Large diffusion** : distribué via liens Dropbox, Google Drive, clés USB, fausses mises à jour
- **Botnets massifs** : des campagnes ont infecté des centaines de milliers de machines
- **Vol d'identité** : identifiants bancaires, comptes réseaux sociaux, emails
- **Utilisation comme pivot** : la machine infectée sert de relai pour attaquer d'autres cibles

### 4.4 Moyens de détection

- **Registre** : clé `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` avec valeur suspecte
- **Réseau** : connexions sur le port **1177/TCP** (par défaut), DNS anormal (utilisation de No-IP ou DynDNS)
- **Antivirus** : signatures très largement connues (taux de détection élevé sur VirusTotal)
- **Analyse des fichiers** : présence de fichiers `.exe` dans `%TEMP%` ou `%AppData%`
- **Outils de monitoring** : Autoruns (Sysinternals) pour détecter les entrées de démarrage suspectes

### 4.5 Mesures de protection

- Maintenir l'antivirus à jour (détection élevée pour ce RAT)
- **Désactiver l'exécution automatique des USB** (AutoRun désactivé par GPO)
- Ne pas télécharger de logiciels depuis des sources non officielles
- Former les utilisateurs à la détection de liens suspects
- Bloquer les connexions vers les services DNS dynamiques (No-IP, DynDNS) en entreprise

---

## 5. SpyNote

### 5.1 Objectif principal

SpyNote est un RAT conçu spécifiquement pour les appareils Android. Il cible les smartphones et tablettes pour exercer une surveillance complète : localisation GPS, écoute, accès aux données personnelles, et contrôle à distance de certaines fonctionnalités. Il est distribué sous forme d'APK malveillant en dehors du Play Store officiel.

### 5.2 Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| Localisation GPS | Suivi en temps réel de la position géographique |
| Accès aux SMS et contacts | Lecture et exfiltration de la liste de contacts et des messages |
| Activation microphone/caméra | Écoute et enregistrement vidéo à distance |
| Keylogger mobile | Enregistrement des saisies sur le clavier virtuel |
| Accès aux applications | Lecture des données d'autres applications (réseaux sociaux, banque) |
| Notifications | Interception des notifications (WhatsApp, Telegram, etc.) |
| Appels téléphoniques | Écoute des appels, journaux d'appels |
| Persistance | Se déguise en app système pour résister à la désinstallation |

### 5.3 Risques

- **Atteinte à la vie privée** : surveillance totale de la vie privée (déplacements, conversations, photos)
- **Ciblage d'activistes et journalistes** : utilisé dans des contextes de surveillance politique
- **Vol d'authentifiants** : interception des SMS de double authentification (2FA par SMS compromis)
- **Chantage et espionnage conjugal** : vendu comme "stalkerware" sur certains forums

### 5.4 Moyens de détection

- **Permissions excessives** : une app demandant l'accès au microphone, à la caméra, aux SMS et à la localisation simultanément est suspecte
- **Analyse via MobSF** : Mobile Security Framework permet l'analyse statique et dynamique des APK
- **Google Play Protect** : détecte les apps malveillantes connues
- **Consommation anormale de batterie/données** : indicateur d'une activité en arrière-plan
- **Audit des apps installées** : vérifier la liste des applications, notamment celles sans icône

### 5.5 Mesures de protection

- **N'installer que depuis le Play Store officiel** (ou App Store pour iOS)
- **Activer Google Play Protect** dans les paramètres
- Vérifier et limiter les permissions accordées à chaque application
- Ne pas activer les "Sources inconnues" dans les paramètres Android
- Mettre à jour Android régulièrement (correctifs de sécurité)
- Utiliser un antivirus mobile (Malwarebytes, Bitdefender Mobile)

---

## 6. Analyse du code Python — Bombe logique (exécution réelle sur VM Kali Linux)

### 6.1 Qu'est-ce qu'une bombe logique ?

Une **bombe logique** est un fragment de code malveillant intégré dans un programme ou un système, qui reste dormant jusqu'à ce qu'une ou plusieurs conditions prédéfinies soient remplies. Contrairement aux virus ou vers qui s'activent immédiatement, la bombe logique attend son déclencheur pour exécuter sa charge utile (payload).

### 6.2 Analyse du code

```python
import datetime
import os

# --- Déclencheurs de la bombe logique ---

# Condition 1 : Déclenchement à une date précise
DATE_DECLENCHEMENT = datetime.date(2026, 5, 28)

# Condition 2 : Déclenchement si un fichier spécifique existe
FICHIER_DECLENCHEUR = r"C:\Users\Admin\secret.txt"

def verifier_declencheur():
    """Vérifie si une des conditions de déclenchement est remplie"""
    aujourdhui = datetime.date.today()
    fichier_present = os.path.exists(FICHIER_DECLENCHEUR)
    if aujourdhui >= DATE_DECLENCHEMENT or fichier_present:
        return True
    return False

def action_malveillante():
    """Simulation d'une action destructrice (TP uniquement)"""
    print("[ALERTE] Conditions de déclenchement remplies.")
    print("Exécution de la charge utile simulée...")
    try:
        with open("system_data_dump.txt", "w") as f:
            f.write("Données simulées comme effacées !")
        print("Action effectuée : simulation d'écriture système.")
    except Exception as e:
        print(f"Erreur lors de l'action : {e}")

def principale():
    if verifier_declencheur():
        action_malveillante()
    else:
        print("Le système est sécurisé. En attente...")

if __name__ == "__main__":
    principale()
```

### 6.3 Explication ligne par ligne

| Élément | Rôle |
|---|---|
| `DATE_DECLENCHEMENT` | Constante définissant la date à partir de laquelle la bombe s'active (28 mai 2026) |
| `FICHIER_DECLENCHEUR` | Chemin d'un fichier dont la présence active la bombe (second déclencheur) |
| `verifier_declencheur()` | Évalue les deux conditions avec un **OU logique** : une seule suffit à déclencher |
| `action_malveillante()` | Simule une action destructrice — dans un vrai malware, ce serait un chiffrement de fichiers (ransomware) ou une suppression de données |
| `principale()` | Point d'entrée : vérifie les conditions et déclenche ou non la charge utile |

### 6.4 Comportement selon la date du système

Puisque `DATE_DECLENCHEMENT = 2026-05-28` et que nous sommes le **2 juin 2026**, la condition de date est **remplie** (`aujourd'hui >= date_déclenchement`). Le code affichera donc :

```
[ALERTE] Conditions de déclenchement remplies.
Exécution de la charge utile simulée...
Action effectuée : simulation d'écriture système.
```

Et créera un fichier `system_data_dump.txt` dans le répertoire courant.

### 6.5 Dangers dans un contexte réel

Dans un contexte malveillant réel, la fonction `action_malveillante()` pourrait :
- **Chiffrer tous les fichiers** utilisateur (ransomware)
- **Supprimer des données critiques** (`os.remove`, `shutil.rmtree`)
- **Exfiltrer des données** vers un serveur distant
- **Désactiver des services système** (sabotage industriel)

### 6.6 Moyens de détection d'une bombe logique

- **Revue de code** : seule méthode vraiment fiable pour les insiders malveillants
- **Analyse statique** : outils comme Bandit (Python) pour détecter du code suspect
- **Surveillance des accès fichiers** : journaux d'audit (Windows Event Log, auditd)
- **Contrôle d'intégrité** : outils type AIDE, Tripwire pour détecter des modifications inattendues

### 6.7 Mesures de protection

- **Séparation des tâches** (Segregation of Duties) : aucun développeur ne devrait avoir accès seul à la production
- **Revue de code obligatoire** (pull request / peer review) avant tout déploiement
- **Tests automatisés** couvrant les cas limites (dates, fichiers déclencheurs)
- **Monitoring continu** des exécutions en production (logs, alertes)

---

## Conclusion

Les RAT représentent une menace sérieuse et polymorphe : qu'ils ciblent des PC Windows (DarkComet, NjRAT, QuasarRAT, Remcos) ou des smartphones Android (SpyNote), ils partagent tous les mêmes caractéristiques fondamentales : furtivité, persistance, et contrôle à distance. Les bombes logiques, elles, illustrent le danger des menaces internes (insiders).

La défense en profondeur reste la meilleure stratégie : combinaison d'antivirus, pare-feu, EDR, formation des utilisateurs, segmentation réseau et surveillance comportementale.

---

*Rapport rédigé dans le cadre du TP Cybersécurité — Étude de Trojans (RAT)*