from flask import Blueprint, request, jsonify # type: ignore
import json
from service.chaves import createUser, transferir, get_saldo,sign_message

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


@crypto_bp.route("/sign", methods=["POST"])
def route_sign():
    data = request.get_json()
    private_key = data.get("private_key")
    payload = data.get("payload")

    if not private_key or not payload:
        return jsonify({"error": "private_key e payload são obrigatórios"}), 400

    # transforma o dict em string JSON determinística
    payload_str = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    signature = sign_message(data.get("private_key"), payload_str)
    return jsonify({"signature": signature})
