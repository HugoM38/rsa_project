import argparse
import base64
from rsa_forge.key_generation import generate_keypair
from rsa_forge.utils import save_key

def keygen(num_digits, public_key_file, private_key_file):
    """
    Génère une paire de clés RSA et les sauvegarde dans les fichiers spécifiés.

    Args:
        num_digits (int): Le nombre de chiffres pour p et q.
        public_key_file (str): Le fichier de sauvegarde de la clé publique.
        private_key_file (str): Le fichier de sauvegarde de la clé privée.
    """
    public_key, private_key = generate_keypair(num_digits)
    
    # Save public key
    save_key(public_key, public_key_file, key_type='public')
    print(f"Clé publique sauvegardée dans {public_key_file}")
    
    # Save private key
    save_key(private_key, private_key_file, key_type='private')
    print(f"Clé privée sauvegardée dans {private_key_file}")
    
def crypt(text, public_key_file):
    """
    Chiffre le texte donné avec la clé publique spécifiée.

    Args:
        text (str): Le texte à chiffrer.
        public_key_file (str): Le fichier de la clé publique.
    """
    # Read public key
    with open(public_key_file, 'r') as f:
        lines = f.readlines()
        if not lines[0].startswith('---begin monRSA public key---'):
            raise Exception("Le fichier de clé publique n'est pas valide.")
        
        # Extract base64 content
        b64_content = ''.join(lines[1:-1]).strip()
        # Decode base64
        decoded_bytes = base64.b64decode(b64_content)
        decoded_str = decoded_bytes.decode('utf-8')
        # Split n and e
        n_hex, e_hex = decoded_str.split('\n')
        # Convert from hexadecimal to decimal
        n = int(n_hex, 16)
        e = int(e_hex, 16)

    # Transform text into ASCII codes on 3 digits
    ascii_codes = ''.join([format(ord(c), '03d') for c in text])

    # Determine block size
    block_size = len(str(n)) - 1

    # Split ASCII codes into blocks of size block_size
    blocks = []
    i = len(ascii_codes)
    while i > 0:
        start = max(0, i - block_size)
        block = ascii_codes[start:i]
        if start == 0 and len(block) < block_size:
            block = block.zfill(block_size)
        blocks.insert(0, block)
        i -= block_size

    # Encrypt each block
    encrypted_blocks = []
    for block in blocks:
        B = int(block)
        C = pow(B, e, n)
        encrypted_blocks.append(str(C))

    # Assemblate encrypted blocks into a sequence
    encrypted_sequence = ''.join(encrypted_blocks)

    # Encode encrypted sequence in ASCII then Base64
    ascii_chars = []
    i = 0
    while i < len(encrypted_sequence):
        chunk = encrypted_sequence[i:i+3]
        if len(chunk) < 3:
            chunk = chunk.ljust(3, '0')
        ascii_code = int(chunk) % 256
        ascii_chars.append(chr(ascii_code))
        i += 3

    ascii_str = ''.join(ascii_chars)
    b64_encoded = base64.b64encode(ascii_str.encode('latin1')).decode('ascii')
    print(b64_encoded)


def main():
    parser = argparse.ArgumentParser(
        description="RSAForge - Un outil de chiffrement RSA personnalisé"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Sous-commandes disponibles')
    
    # Subparser for keygen command
    parser_keygen = subparsers.add_parser('keygen', help='Générer une paire de clés RSA')
    parser_keygen.add_argument(
        '--digits', 
        type=int, 
        default=10, 
        help='Nombre de chiffres pour p et q (par défaut: 10)'
    )
    parser_keygen.add_argument(
        '--public', 
        type=str, 
        default='public_key.pub', 
        help='Fichier de sauvegarde de la clé publique (par défaut: public_key.pub)'
    )
    parser_keygen.add_argument(
        '--private', 
        type=str, 
        default='private_key.priv', 
        help='Fichier de sauvegarde de la clé privée (par défaut: private_key.priv)'
    )
    
    # Subparser for crypt command
    parser_crypt = subparsers.add_parser('crypt', help='Chiffrer un texte avec une clé publique RSA')
    parser_crypt.add_argument(
        '--public', 
        type=str, 
        required=True, 
        help='Fichier de la clé publique'
    )
    parser_crypt.add_argument(
        'text', 
        type=str, 
        help='Texte à chiffrer'
    )
    
    args = parser.parse_args()
    
    if args.command == 'keygen':
        keygen(args.digits, args.public, args.private)
    elif args.command == 'crypt':
        crypt(args.text, args.public)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()