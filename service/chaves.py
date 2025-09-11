from cryptography.hazmat.primitives.asymmetric import rsa, padding # type: ignore
from cryptography.hazmat.primitives import serialization, hashes,padding # type: ignore
from cryptography.hazmat.backends import default_backend # type: ignore
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # type: ignore
import secrets
import base64
import os

keys_store = { }
iv = bytes(16)

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return pem_public.decode(), pem_private.decode()

def verify_signature(public_pem: str, message: any, signature_b64: str) -> bool:
    
    public_key = serialization.load_pem_public_key(public_pem)

    

    try:
        signature = base64.b64decode(signature_b64)

        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


def createUser(name: str):
    public, private = generate_keys()

    keys_store[name] = {
        "name": name,
        "saldo": 1000*100,
        "public_pem":public
    }
    return public, private 


def transferir(data: dict, assinatura: str):

    usuario_destino = keys_store.get(data.get("destino"))

    usuario_remetente = keys_store.get(data.get("remetente"))

    if usuario_destino is None:
        return "destino nao existe"
    if usuario_remetente is None:
        return "usuario nao existe"

    #if verify_signature(usuario_remetente["public_pem"], data, assinatura):
    #    return "assinatura invalida"

    saldo = usuario_remetente["saldo"]

    if saldo is not None:
        valor_centavos = int(round(data.get("valor") * 100))
        if saldo < valor_centavos:
            return "saldo insuficiente"
        usuario_destino["saldo"] = usuario_destino["saldo"]+valor_centavos
        usuario_remetente["saldo"] = usuario_remetente["saldo"] - valor_centavos

        keys_store[data.get("destino")] = usuario_destino
        keys_store[data.get("remetente")] = usuario_remetente

    return "Transferencia realizada"

def get_saldo(user_key: str):
    user = keys_store[user_key]
    if user is None:
        return "Cliente não encontrado"
    
    saldo = user["saldo"] / 100
    valor_formatado = f"{saldo:.2f}"

    return "Seu saldo: "+valor_formatado

def encrypt_message(user_key: str, message: str):

    simetric_key = base64.b64decode(user_key)

    iv = os.urandom(16)

    cipher = Cipher(
        algorithms.AES(simetric_key),
        modes.CBC(iv),
        backend=default_backend()
    )

    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()

    ciphertext = encryptor.update(padded_message) + encryptor.finalize()

    return base64.b64encode(iv + ciphertext).decode()


def decrypt_message(user_key: str, encrypted_b64: str):
    
    simetric_key = base64.b64decode(user_key)

    encrypted_data = base64.b64decode(encrypted_b64)

    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    cipher = Cipher(
        algorithms.AES(simetric_key),
        modes.CBC(iv),
        backend=default_backend()
    )

    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode()

def gerar_chave_simetrica(public_key_pem: str) -> str:
    """Gera uma chave simétrica (AES) e a criptografa com a chave pública RSA"""

    chave_simetrica = secrets.token_bytes(16)

    loaded_public_key = serialization.load_pem_public_key(
        public_key_pem.encode(),
        backend=default_backend()
    )

    encrypted_key = loaded_public_key.encrypt(
        chave_simetrica,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(encrypted_key).decode()

def decrypt_assimetric_key(private_key_pem: str, encrypted_key: str) -> bytes:

    encrypted_key = base64.b64decode(encrypted_key)

    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )

    symmetric_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(symmetric_key).decode()

def sign_message(user_key: str, message: str) -> str:
    """Assina mensagem com chave privada"""
    private_key = serialization.load_pem_private_key(user_key.encode(), password=None)

    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return base64.b64encode(signature).decode()


