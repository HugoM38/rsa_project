# rsa_forge/main.py

import argparse
from rsa_forge.key_generation import generate_keypair
from rsa_forge.utils import save_key

def keygen(num_digits, public_key_file, private_key_file):
    public_key, private_key = generate_keypair(num_digits)
    
    # Sauvegarder les clés
    save_key(public_key, public_key_file)
    print(f"Clé publique sauvegardée dans {public_key_file}")
    
    save_key(private_key, private_key_file)
    print(f"Clé privée sauvegardée dans {private_key_file}")

def main():
    parser = argparse.ArgumentParser(
        description="RSAForge - Un outil de chiffrement RSA personnalisé"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Sous-commandes disponibles')
    
    # Sous-commande keygen
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