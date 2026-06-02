import os
import time
import datetime

# ============================================================
# SIMULATION ÉDUCATIVE — Intégration malware dans logiciel sain
# ⚠️  Code strictement éducatif dans le cadre du TP
# ============================================================

# --- Configuration simulée ---
LOGICIEL_SAIN     = "VLC_Media_Player_setup.exe"   # Nom du logiciel légitime (simulé)
NOM_MALWARE       = "svchost32.exe"                 # Nom déguisé du malware
REPERTOIRE_DEPOT  = os.path.join(os.environ.get("TEMP", "."), NOM_MALWARE)
CLE_REGISTRE_SIM  = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run"


# --- Étape 1 : Simulation de l'installation du logiciel sain ---
def installer_logiciel_sain():
    """Simule l'installation normale du logiciel légitime"""
    print(f"[INFO] Lancement de l'installateur : {LOGICIEL_SAIN}")
    print("[INFO] Extraction des fichiers...")
    time.sleep(1)
    print("[INFO] Installation en cours... 25%")
    time.sleep(0.5)
    print("[INFO] Installation en cours... 75%")
    time.sleep(0.5)
    print(f"[INFO] {LOGICIEL_SAIN} installé avec succès.")
    print("[INFO] Création du raccourci Bureau...")
    time.sleep(0.3)


# --- Étape 2 : Dépôt furtif du malware (dropper) ---
def deposer_malware():
    """
    Simule le dépôt silencieux du malware pendant l'installation.
    Dans un vrai dropper, cette étape est invisible pour l'utilisateur.
    """
    print("\n[DROPPER] Dépôt du payload en arrière-plan...")
    try:
        # Simulation : on crée un fichier texte à la place d'un vrai exécutable
        with open(REPERTOIRE_DEPOT + ".txt", "w") as f:
            f.write(f"[SIMULATION] Malware déposé le {datetime.datetime.now()}\n")
            f.write(f"Chemin simulé : {REPERTOIRE_DEPOT}\n")
            f.write("Dans un vrai cas : exécutable malveillant (RAT, keylogger...)\n")
        print(f"[DROPPER] Payload déposé dans : {REPERTOIRE_DEPOT}.txt (simulé)")
    except Exception as e:
        print(f"[DROPPER] Erreur lors du dépôt : {e}")


# --- Étape 3 : Persistance (clé de registre simulée) ---
def etablir_persistance():
    """
    Simule l'ajout d'une clé de registre pour que le malware
    se relance automatiquement à chaque démarrage de Windows.
    """
    print("\n[DROPPER] Établissement de la persistance...")
    try:
        # Simulation : on écrit dans un fichier texte à la place du registre réel
        with open("registre_simule.txt", "w", encoding="utf-8") as f:
            f.write(f"[SIMULATION] Cle ajoutee : {CLE_REGISTRE_SIM}\n")
            f.write(f"Valeur : {NOM_MALWARE} -> {REPERTOIRE_DEPOT}\n")
            f.write("Effet reel : le malware se relancerait a chaque demarrage Windows.\n")
        print(f"[DROPPER] Persistance simulee -> {CLE_REGISTRE_SIM}")
        print(f"[DROPPER] Le malware se relancerait à chaque démarrage.")
    except Exception as e:
        print(f"[DROPPER] Erreur persistance : {e}")


# --- Étape 4 : Auto-suppression du dropper ---
def auto_supprimer():
    """
    Simule l'auto-suppression du dropper pour effacer les traces.
    Le logiciel malveillant a été installé, le vecteur initial disparaît.
    """
    print("\n[DROPPER] Nettoyage des traces du dropper...")
    time.sleep(0.5)
    print(f"[DROPPER] Suppression simulée de : {LOGICIEL_SAIN}")
    print("[DROPPER] Le dropper s'est autodétruit. Aucune trace visible.")


# --- Programme principal ---
def principale():
    print("=" * 60)
    print("  SIMULATION — Dropper intégré à un logiciel sain")
    print("  [!] Educatif uniquement -- TP Cybersecurite")
    print("=" * 60)
    print()

    # Phase visible par l'utilisateur
    installer_logiciel_sain()

    # Phases invisibles (en arrière-plan dans un vrai scénario)
    deposer_malware()
    etablir_persistance()
    auto_supprimer()

    print()
    print("=" * 60)
    print("[RÉSULTAT] L'utilisateur croit avoir installé VLC.")
    print("[RÉSULTAT] En réalité, un malware est actif et persistant.")
    print("[RÉSULTAT] Fichiers créés pour la simulation :")
    print(f"           - {REPERTOIRE_DEPOT}.txt  (payload simulé)")
    print(f"           - registre_simule.txt     (persistance simulée)")
    print("=" * 60)


if __name__ == "__main__":
    principale()
