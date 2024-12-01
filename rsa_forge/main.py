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
    with open(public_key_file, 'r') as f:
        lines = f.readlines()
        if not lines[0].startswith('---begin monRSA public key---'):
            raise Exception("Le fichier de clé publique n'est pas valide.")
        
        # Extract n and e
        b64_content = ''.join(lines[1:-1]).strip()
        decoded_bytes = base64.b64decode(b64_content)
        decoded_str = decoded_bytes.decode('utf-8')
        n_hex, e_hex = decoded_str.split('\n')
        n = int(n_hex, 16)
        e = int(e_hex, 16)

    # Convert the text to a sequence of ASCII codes
    ascii_codes = ''.join([format(ord(c), '03d') for c in text])

    # Determine block size based on n
    block_size = len(str(n)) - 1

    # Split the ASCII codes into blocks of size block_size
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

    # Join the encrypted blocks into a sequence
    encrypted_sequence = ','.join(encrypted_blocks)

    # Encode the sequence in Base64
    encrypted_bytes = encrypted_sequence.encode('utf-8')
    b64_encoded = base64.b64encode(encrypted_bytes).decode('ascii')
    print(b64_encoded)

def decrypt(encrypted_text, private_key_file):
    with open(private_key_file, 'r') as f:
        lines = f.readlines()
        if not lines[0].startswith('---begin monRSA private key---'):
            raise Exception("Le fichier de clé privée n'est pas valide.")
        
        # Extract n and d
        b64_content = ''.join(lines[1:-1]).strip()
        decoded_bytes = base64.b64decode(b64_content)
        decoded_str = decoded_bytes.decode('utf-8')
        n_hex, d_hex = decoded_str.split('\n')
        n = int(n_hex, 16)
        d = int(d_hex, 16)

    # Decode the Base64 sequence
    encrypted_bytes = base64.b64decode(encrypted_text)
    encrypted_sequence = encrypted_bytes.decode('utf-8')

    # Split the sequence into encrypted blocks
    encrypted_blocks_str = encrypted_sequence.split(',')

    # Decrypt each block
    decrypted_blocks = []
    block_size = len(str(n)) - 1
    for block_str in encrypted_blocks_str:
        C = int(block_str)
        B = pow(C, d, n)
        decrypted_blocks.append(str(B).zfill(block_size))

    # Join the decrypted blocks into a sequence
    decrypted_sequence = ''.join(decrypted_blocks)

    # Convert the sequence of ASCII codes to text
    decrypted_text = ''
    i = 0
    while i < len(decrypted_sequence):
        ascii_code_str = decrypted_sequence[i:i+3]
        ascii_code = int(ascii_code_str)
        decrypted_text += chr(ascii_code)
        i += 3

    print(decrypted_text)

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
    
    # Subparser for decrypt command
    parser_decrypt = subparsers.add_parser('decrypt', help='Déchiffrer un texte avec une clé privée RSA')
    parser_decrypt.add_argument(
        '--private', 
        type=str, 
        required=True, 
        help='Fichier de la clé privée'
    )
    parser_decrypt.add_argument(
        'text', 
        type=str, 
        help='Texte à déchiffrer'
    )
    
    args = parser.parse_args()
    
    if args.command == 'keygen':
        keygen(args.digits, args.public, args.private)
    elif args.command == 'crypt':
        crypt(args.text, args.public)
    elif args.command == 'decrypt':
        decrypt(args.text, args.private)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()