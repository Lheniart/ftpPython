from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


# Créer une instance d'autorisateur fictif avec l'utilisateur et le mot de passe spécifiés
authorizer = DummyAuthorizer()
authorizer.add_user("epsi", "client24", ".", perm="elradfmw")

# Permettre l'accès anonyme avec des autorisations limitées
authorizer.add_anonymous(".", perm="elradfm")

# Créer une instance de gestionnaire FTP et spécifier l'autorisateur
handler = FTPHandler
handler.authorizer = authorizer

handler.banner = "Bienvenue sur le serveur de l'epsi"

# Créer une instance de serveur FTP écoutant sur l'adresse locale 127.0.0.1 et le port 21
server = FTPServer(("127.0.0.1", 21), handler)



# Démarrer le serveur FTP
server.serve_forever()