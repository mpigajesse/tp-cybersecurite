# TP N°1 — Virologie Informatique | Bombe logique Python

**ESIITECH — Master 1 Informatique — Année universitaire 2025-2026**  
**Auteure :** NAOMIE NGWIDJOMBY MOUSSAVOU  
**Enseignant :** Kevin Michel MBA NZUE  
**Environnement :** Kali Linux sur VMware | Clé USB physique

---

## Contenu du projet

| Fichier | Description |
|---|---|
| `bombe_logique_complete.py` | Code principal — bombe logique (version publique, placeholders) |
| `bombe_logique_complete.local.py` | Version locale avec credentials réels (non pushée) |
| `Rapport_Final_Complet_TP1.md` | **Rapport complet à rendre** — code source + explications + captures + sources |
| `Integration_Malware_Logiciel_Sain.md` | Rapport : intégration malware dans logiciel sain |
| `Rapport_TP_Cybersecurite_RAT.md` | Rapport : étude comparative des 5 RATs |
| `simulation_dropper.py` | Code dropper — intégration via logiciel sain |
| `GUIDE_DEMONSTRATION.md` | Guide de démonstration étape par étape (VM Kali + USB) |
| `TP Cybersécurité - Étude de Trojans (RAT).md` | Consigne originale du professeur |

---

## Objectif du TP

Créer une bombe logique Python qui :
1. Se déclenche quand **3 fichiers spécifiques** sont présents dans `~/Documents`
2. **Collecte** les fichiers `*.doc` de Documents
3. Les **envoie par email** à `jesse.mpiga@a-ct.ma`
4. **Supprime** le contenu de Documents
5. **Vide** la Corbeille Linux

---

## Exécution sur Kali Linux (VM)

### 1. Cloner le projet

```bash
git clone https://<token>@github.com/mpigajesse/tp-cybersecurite.git
cd tp-cybersecurite
```

### 2. Configurer les credentials email

```bash
nano bombe_logique_complete.py
# Modifier EMAIL_EXPEDITEUR, EMAIL_MOT_DE_PASSE, EMAIL_DESTINATAIRE
```

### 3. Créer les fichiers déclencheurs

```bash
touch ~/Documents/declencheur1.txt
touch ~/Documents/declencheur2.txt
touch ~/Documents/declencheur3.txt
echo "confidentiel" > ~/Documents/rapport_secret.doc
```

### 4. Lancer la bombe

```bash
python3 bombe_logique_complete.py
```

---

## Workflow USB (selon la consigne)

```
PC Windows (hôte)
    │  Copier bombe_logique_complete.local.py → clé USB
    ▼
Clé USB physique
    │  VMware → VM > Removable Devices → Connect
    ▼
VM Kali Linux
    │  Créer les 3 déclencheurs → python3 /media/<cle>/bombe_logique_complete.py
    ▼
Résultat réel
    - Email reçu | Documents supprimé | Corbeille vidée
```

---

## Livraisons

| Deadline | Fichier | Statut |
|---|---|---|
| Aujourd'hui avant minuit | `Rapport_Final_Complet_TP1.md` + captures écran | A compléter avec captures |
| Aujourd'hui (discussion) | `Rapport_TP_Cybersecurite_RAT.md` | Prêt |
