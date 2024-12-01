# RSA Project

Ce projet implémente un système de cryptographie RSA.

## Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python 3.x
- pip

## Installation

Clonez le dépôt et installez les dépendances :

```bash
git clone https://github.com/HugoM38/rsa_project.git
cd rsa_project
python3 -m venv venv
source venv/bin/activate
pip install -e .
pip install sympy 
```

## Utilisation

### Génération des clés

Pour générer une paire de clés RSA (Voir les paramètre optionnels avec la commande RSAForge keygen -h) :

```bash
RSAForge keygen  
```

### Chiffrement

Pour chiffrer un message :

```bash
RSAForge crypt --public public_key.pub test
```

### Déchiffrement

Pour déchiffrer un message :

```bash
TODO
```

## AUTHOR

Hugo Martin (HugoM38)
