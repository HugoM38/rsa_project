from setuptools import setup, find_packages

setup(
    name='RSAForge',
    version='1.0.0',
    packages=find_packages(),
    description='Un outil de chiffrement RSA personnalisé',
    author='Hugo Martin',
    author_email='pv.hugom@gmail.com',
    entry_points={
        'console_scripts': [
            'RSAForge = rsa_forge.main:main',
        ],
    },
    python_requires='>=3.6',
)
