from flask import Flask # type: ignore
from controller.chaves import crypto_bp

app = Flask(__name__)

app.register_blueprint(crypto_bp, url_prefix="/banco")

if __name__ == "__main__":
    app.run(debug=True)
