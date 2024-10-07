# rsa_forge/utils.py

def save_key(key, filename):
    """Sauvegarde une clé dans un fichier."""
    with open(filename, 'w') as f:
        f.write(f"{key[0]}\n{key[1]}\n")

def load_key(filename):
    """Charge une clé depuis un fichier."""
    with open(filename, 'r') as f:
        lines = f.readlines()
        key = (int(lines[0].strip()), int(lines[1].strip()))
    return key
