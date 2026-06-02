# TP N°1 Cybersécurité — Bombe logique Python
## Environnement : Kali Linux sur VMware | Clé USB physique

---

## Contenu du projet

| Fichier | Description |
|---|---|
| `bombe_logique_complete.py` | Code principal — bombe logique réelle (Kali Linux) |
| `Integration_Malware_Logiciel_Sain.md` | Rapport : intégration malware dans logiciel sain (mardi) |
| `Rapport_TP_Cybersecurite_RAT.md` | Rapport : étude comparative des 5 RATs (jeudi) |
| `simulation_dropper.py` | Code dropper — intégration via logiciel sain |
| `GUIDE_DEMONSTRATION.md` | Guide de démonstration étape par étape |

## RATs étudiés (jeudi)

1. **DarkComet** — Espionnage Windows (microphone, webcam, keylogger)
2. **Remcos** — RAT commercial détourné, campagnes APT
3. **QuasarRAT** — RAT open-source, groupes APT étatiques
4. **NjRAT** — RAT simple, botnets et vol de credentials
5. **SpyNote** — RAT Android, surveillance mobile

## Exécution réelle sur Kali Linux (VM)

### Prérequis

- VM Kali Linux démarrée sur VMware
- Clé USB physique connectée à la VM (VM > Removable Devices)
- Python 3 installé dans Kali (installé par défaut)
- Credentials Gmail configurés dans `bombe_logique_complete.py`

### Cloner le projet dans Kali

```bash
git clone https://<token>@github.com/mpigajesse/tp-cybersecurite.git
cd tp-cybersecurite
```

### Créer les fichiers déclencheurs

```bash
touch ~/Documents/declencheur1.txt
touch ~/Documents/declencheur2.txt
touch ~/Documents/declencheur3.txt
echo "confidentiel" > ~/Documents/rapport_confidentiel.doc
```

### Lancer la bombe (exécution réelle)

```bash
python3 bombe_logique_complete.py
```

### Résultat réel attendu

```
[INFO] Verification des conditions de declenchement...
  [PRESENT] declencheur1.txt
  [PRESENT] declencheur2.txt
  [PRESENT] declencheur3.txt
[ALERTE] Activation de la bombe.

[ACTION] Collecte des fichiers .doc dans Documents...
[OK] Email envoye a jesse.mpiga@a-ct.ma.
[OK] Contenu de Documents supprime.
[OK] Corbeille videe.
```

## Livraisons

| Deadline | Sujet | Statut |
|---|---|---|
| Mardi 03/06 00h | Intégration malware dans logiciel sain — envoi par mail | Prêt |
| Jeudi 05/06 | Étude comparative RATs — discussion en classe | Prêt |
