import argparse
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
    
    args = parser.parse_args()
    
    if args.command == 'keygen':
        keygen(args.digits, args.public, args.private)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()