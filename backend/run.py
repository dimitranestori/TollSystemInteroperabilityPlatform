from . import app

if(__name__ == "__main__"):
    context = (r"backend\ssl\server.crt", r"backend\ssl\server.key") # certificate and key files
    app.run(ssl_context=context, debug = True, host = "localhost", port = 9115)