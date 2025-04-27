import secrets
import base64

def generate_secret_key():
    # Générer 32 bytes aléatoires
    random_bytes = secrets.token_bytes(32)
    # Encoder en base64 pour une utilisation facile
    secret_key = base64.b64encode(random_bytes).decode('utf-8')
    return secret_key

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print(f"Votre clé secrète JWT : {secret_key}")
    print("\nCopiez cette clé dans votre fichier .env :")
    print(f"JWT_SECRET_KEY={secret_key}") 