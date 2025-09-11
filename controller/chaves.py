from flask import Blueprint, request, jsonify # type: ignore
from service.chaves import createUser, transferir, decrypt_message, get_saldo,sign_message, gerar_chave_simetrica, decrypt_assimetric_key

crypto_bp = Blueprint("banco", __name__)

@crypto_bp.route("/user", methods=["POST"])
def route_create_user():
    data = request.get_json()
    public_key, private_key = createUser(data.get("name"))
    return jsonify({"public_key": public_key, "private_key": private_key})

@crypto_bp.route("/transferir", methods=["POST"])
def route_transf():    
    data = request.get_json()
    sign = request.headers.get("Assinatura")    
    message = transferir(data, sign)
    return jsonify({"message": message,})

@crypto_bp.route("/saldo/<user>", methods=["GET"])
def route_saldo(user):
    message = get_saldo(user)
    return jsonify({"message": message})

@crypto_bp.route("/decrypt", methods=["POST"])
def route_decrypt():
    data = request.get_json()
    decrypted = decrypt_message(data.get("key"), data.get("encrypted"))
    return jsonify({"decrypted": decrypted})

@crypto_bp.route("/simetric", methods=["POST"])
def route_simetric():
    data = request.get_json()
    signature = gerar_chave_simetrica(data.get("public_key_pem"))
    return jsonify({"signature": signature})

@crypto_bp.route("/decript-simetric", methods=["POST"])
def route_decript_simetric():
    data = request.get_json()
    signature = decrypt_assimetric_key(data.get("private_key_pem"),data.get("encrypted_key"))
    return jsonify({"signature": signature})

@crypto_bp.route("/sign", methods=["POST"])
def route_sign():
    data = request.get_json()
    signature = sign_message(data.get("private_key"), data.get("payload"))
    return jsonify({"signature": signature})
