# rsa_forge/key_generation.py

import random
from sympy import isprime  # Utilisation de sympy pour une vérification de primalité efficace

def generate_prime_number(num_digits):
    """Génère un nombre premier de `num_digits` chiffres."""
    lower = 10**(num_digits - 1)
    upper = 10**num_digits - 1
    while True:
        # Génère un candidat premier aléatoire dans la plage spécifiée
        prime_candidate = random.randint(lower, upper)
        # Assure que le candidat est impair
        if prime_candidate % 2 == 0:
            prime_candidate += 1
        # Vérifie la primalité
        if isprime(prime_candidate):
            return prime_candidate

def gcd(a, b):
    """Calcule le PGCD de a et b."""
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """Algorithme d'Euclide étendu. Retourne (gcd, x, y) tels que ax + by = gcd."""
    if a == 0:
        return (b, 0, 1)
    else:
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return (gcd_val, x, y)

def mod_inverse(e, phi):
    """Calcule l'inverse modulaire de e modulo phi."""
    gcd_val, x, _ = extended_gcd(e, phi)
    if gcd_val != 1:
        raise Exception("L'inverse modulaire n'existe pas.")
    else:
        return x % phi

def find_e_d(n_prime):
    """Trouve des paires (e, d) telles que e est premier, gcd(e, n’) = 1, e ≠ d, et e*d ≡ 1 mod n’."""
    attempts = 0
    max_attempts = 100000  # Limite pour éviter une boucle infinie
    while attempts < max_attempts:
        # Génère un e premier (sans limitation de taille)
        e = generate_random_prime(n_prime)
        if gcd(e, n_prime) != 1:
            attempts += 1
            continue  # e doit être coprime avec n_prime
        try:
            d = mod_inverse(e, n_prime)
            if e != d:
                return (e, d)
            else:
                attempts += 1
                continue
        except Exception:
            attempts += 1
            continue
    raise Exception("Impossible de trouver des paires (e, d) satisfaisant les conditions après de nombreux essais.")

def generate_random_prime(n_prime):
    """Génère un nombre premier aléatoire inférieur à n_prime."""
    # Définir la plage pour e : 2 à n_prime - 1
    lower = 2
    upper = n_prime - 1
    while True:
        # Choisir un nombre aléatoire dans la plage
        prime_candidate = random.randint(lower, upper)
        if isprime(prime_candidate):
            return prime_candidate

def generate_keypair(num_digits=10):
    """Génère une paire de clés RSA selon les spécifications."""
    print(f"Génération d'un premier p de {num_digits} chiffres...")
    p = generate_prime_number(num_digits)
    print(f"Premier p généré : {p}")

    print(f"Génération d'un premier q de {num_digits} chiffres...")
    while True:
        q = generate_prime_number(num_digits)
        if q != p:
            break
    print(f"Premier q généré : {q}")

    n = p * q
    print(f"Calcul de n = p * q = {n}")

    n_prime = (p - 1) * (q - 1)
    print(f"Calcul de n’ = (p - 1) * (q - 1) = {n_prime}")

    print("Recherche des paires (e, d) satisfaisant les conditions...")
    try:
        e, d = find_e_d(n_prime)
        print(f"Trouvé e = {e} et d = {d} satisfaisant e * d ≡ 1 mod n’")
    except Exception as ex:
        print(str(ex))
        raise

    public_key = (n, e)
    private_key = (n, d)

    return public_key, private_key