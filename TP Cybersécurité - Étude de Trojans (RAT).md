# TP N°1 — Création d'une bombe logique

## 1. Objectif du TP

L'objectif du présent TP est de créer en langage Python une bombe logique dont la mission sera :

1. De récupérer les fichiers `*.doc` du répertoire **Mes Documents** d'un utilisateur
2. De retourner ces fichiers par mail à l'adresse email de l'étudiant
3. De supprimer le contenu du répertoire Mes Documents
4. De vider la Corbeille

---

## 2. Condition de déclenchement

La bombe logique doit entrer en activité dès que **les 3 fichiers suivants** sont présents dans Mes Documents simultanément :

- `declencheur1.txt` *(noms exacts à préciser par le professeur)*
- `declencheur2.txt`
- `declencheur3.txt`

La bombe s'exécutera dès lors que les 3 fichiers seront présents dans Mes Documents.

---

## 3. Introduction dans le système

La bombe logique sera introduite via une **clé USB** d'un utilisateur.

> Technique : le fichier malveillant peut être déguisé en logiciel légitime sur la clé USB, de sorte que l'utilisateur l'exécute lui-même ou qu'il se lance automatiquement à la connexion de la clé.

---

## 4. Code Python

*(Voir fichier `bombe_logique_complete.py`)*

Inspiré du code fourni par le professeur, avec les 4 actions demandées :
- Vérification des 3 fichiers déclencheurs dans Documents
- Collecte des `.doc` dans Documents
- Envoi par email
- Suppression du contenu de Documents + vidage Corbeille

---

## 5. Livraisons

| Deadline | Sujet | Fichier(s) |
|---|---|---|
| Mardi 03/06 00h | Comment intégrer un malware dans un logiciel sain | `Integration_Malware_Logiciel_Sain.md` + `simulation_dropper.py` |
| Jeudi 05/06 | Étude comparative des 5 RATs (discussion en classe) | `Rapport_TP_Cybersecurite_RAT.md` |

---

## Annexe — Code de référence du professeur

```python
import datetime
import os

# --- Déclencheurs de la bombe logique ---

# Condition 1 : Déclenchement à une date précise
DATE_DECLENCHEMENT = datetime.date(2026, 5, 28)

# Condition 2 : Déclenchement si un fichier spécifique existe sur le système
FICHIER_DECLENCHEUR = r"C:\Users\Admin\secret.txt"

def verifier_declencheur():
    # Vérification de la date actuelle
    aujourdhui = datetime.date.today()
    # Vérification de l'existence du fichier
    fichier_present = os.path.exists(FICHIER_DECLENCHEUR)
    # Si l'une des deux conditions est remplie, la bombe explose
    if aujourdhui >= DATE_DECLENCHEMENT or fichier_present:
        return True
    return False

def action_malveillante():
    print("[ALERTE] Conditions de déclenchement remplies. Execution de la charge utile...")
    # EXEMPLE D'ACTION DESTRUCTIVE (Simulee)
    # Dans un cas reel, cela pourrait etre la suppression de repertoires critiques :
    # shutil.rmtree('/chemin/vers/dossier/critique')
    try:
        with open("system_data_dump.txt", "w") as f:
            f.write("Donnees effacees !")
        print("Action effectuee : Donnees ecrasees.")
    except Exception as e:
        print(f"Erreur lors de l'action : {e}")

def principale():
    if verifier_declencheur():
        action_malveillante()
    else:
        print("Le systeme est securise. En attente...")

if __name__ == "__main__":
    principale()
```
