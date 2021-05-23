from rest import app


config = {
    "debug": True,
    "ssl_context": ('certs/cert.pem', 'certs/key.pem'),
    "host": "localhost",
    "port": 8000
}


if __name__ == "__main__":
    app.run(**config)
