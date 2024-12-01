import base64

def save_key(key, filename, key_type='public'):
    """
    Sauvegarde une clé dans un fichier avec le format spécifié.

    Args:
        key (tuple): La clé à sauvegarder, sous la forme (n, e) ou (n, d).
        filename (str): Le nom du fichier où sauvegarder la clé.
        key_type (str): Le type de clé, 'public' ou 'private'.
    """
    if key_type == 'public':
        header = "---begin monRSA public key---\n"
        footer = "---end monRSA key---\n"
    elif key_type == 'private':
        header = "---begin monRSA private key---\n"
        footer = "---end monRSA key---\n"
    else:
        raise ValueError("key_type doit être 'public' ou 'private'.")

    # Convertir n et e/d en hexadécimal sans le préfixe '0x'
    n_hex = format(key[0], 'x')
    ed_hex = format(key[1], 'x')

    # Concatenation avec un retour chariot
    concat_str = f"{n_hex}\n{ed_hex}"

    # Encodage en base64
    b64_encoded = base64.b64encode(concat_str.encode('utf-8')).decode('utf-8')

    # Écriture dans le fichier
    with open(filename, 'w') as f:
        f.write(header)
        f.write(b64_encoded + '\n')
        f.write(footer)

def load_key(filename):
    """
    Charge une clé depuis un fichier.

    Args:
        filename (str): Le nom du fichier contenant la clé.

    Returns:
        tuple: La clé sous la forme (n, e) ou (n, d).
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
        # Extraire le contenu base64
        b64_content = ''.join(lines[1:-1]).strip()
        # Décoder base64
        decoded_bytes = base64.b64decode(b64_content)
        decoded_str = decoded_bytes.decode('utf-8')
        # Séparer n et e/d
        n_hex, ed_hex = decoded_str.split('\n')
        # Convertir de l'hexadécimal au décimal
        n = int(n_hex, 16)
        ed = int(ed_hex, 16)
        return (n, ed)