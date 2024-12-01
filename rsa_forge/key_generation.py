import random
from sympy import isprime

def generate_prime_number(num_digits):
    """
    Génère un nombre premier de `num_digits` chiffres.

    Args:
        num_digits (int): Le nombre de chiffres pour le nombre premier.

    Returns:
        int: Un nombre premier de `num_digits` chiffres.
    """
    lower = 10**(num_digits - 1)
    upper = 10**num_digits - 1
    while True:
        # Generate a random prime candidate
        prime_candidate = random.randint(lower, upper)
        # Make sure it is odd
        if prime_candidate % 2 == 0:
            prime_candidate += 1
        # Check if it is prime
        if isprime(prime_candidate):
            return prime_candidate

def gcd(a, b):
    """
    Calcule le PGCD de a et b.

    Args:
        a (int): Premier entier.
        b (int): Deuxième entier.

    Returns:
        int: Le PGCD de a et b.
    """
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """
    Algorithme d'Euclide étendu.
    Retourne (gcd, x, y) tels que ax + by = gcd.

    Args:
        a (int): Premier entier.
        b (int): Deuxième entier.

    Returns:
        tuple: (gcd, x, y)
    """
    if a == 0:
        return (b, 0, 1)
    else:
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return (gcd_val, x, y)

def mod_inverse(e, phi):
    """
    Calcule l'inverse modulaire de e modulo phi.

    Args:
        e (int): L'entier dont on veut l'inverse.
        phi (int): Le modulo.

    Returns:
        int: L'inverse modulaire de e modulo phi.

    Raises:
        Exception: Si l'inverse modulaire n'existe pas.
    """
    gcd_val, x, _ = extended_gcd(e, phi)
    if gcd_val != 1:
        raise Exception("L'inverse modulaire n'existe pas.")
    else:
        return x % phi

def find_e_d(n_prime):
    """
    Trouve des paires (e, d) telles que:
    - e est premier
    - gcd(e, n’) = 1
    - e ≠ d
    - e*d ≡ 1 mod n’

    Args:
        n_prime (int): La fonction d'Euler de n.

    Returns:
        tuple: (e, d)

    Raises:
        Exception: Si aucune paire satisfaisante n'est trouvée après un nombre maximal de tentatives.
    """
    # First try with e = 65537
    e = 65537
    if gcd(e, n_prime) == 1:
        try:
            d = mod_inverse(e, n_prime)
            if e != d:
                return (e, d)
        except Exception:
            pass

    # Search for other e values
    attempts = 0
    max_attempts = 100000  # Maximum number to avoid infinite loop
    while attempts < max_attempts:
        # Generate a random prime number for e
        e = generate_random_prime(n_prime)
        if gcd(e, n_prime) != 1:
            attempts += 1
            continue  # e needs to be coprime with n_prime
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
    """
    Génère un nombre premier aléatoire inférieur à n_prime.

    Args:
        n_prime (int): La limite supérieure pour la génération de nombres premiers.

    Returns:
        int: Un nombre premier aléatoire inférieur à n_prime.
    """
    # Define range for e : 2 to n_prime - 1
    lower = 2
    upper = n_prime - 1
    while True:
        # Generate a random prime candidate
        prime_candidate = random.randint(lower, upper)
        if isprime(prime_candidate):
            return prime_candidate

def generate_keypair(num_digits=10):
    """
    Génère une paire de clés RSA selon les spécifications.

    Args:
        num_digits (int, optional): Le nombre de chiffres pour p et q. Par défaut à 10.

    Returns:
        tuple: (public_key, private_key)
            public_key = (n, e)
            private_key = (n, d)
    """
    
    p = generate_prime_number(num_digits)
    while True:
        q = generate_prime_number(num_digits)
        if q != p:
            break

    n = p * q
    n_prime = (p - 1) * (q - 1)

    try:
        e, d = find_e_d(n_prime)
    except Exception as ex:
        print(str(ex))
        raise

    public_key = (n, e)
    private_key = (n, d)

    return public_key, private_key