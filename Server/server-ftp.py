import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class MyHandler(FTPHandler):
    def ftp_CMD_CHPASS(self, line):
        new_password = line.strip()
        new_password = os.path.basename(new_password)
        user = self.username
        self.authorizer.remove_user(user)
        # Mettez à jour le mot de passe de l'utilisateur
        self.authorizer.add_user(user, new_password, '.', perm="elradfmwMT")
        self.respond("230 Mot de passe modifié avec succès.")
        self.handle_close()

# Créer une instance d'autorisateur fictif avec l'utilisateur et le mot de passe spécifiés
authorizer = DummyAuthorizer()
authorizer.add_user("epsi", "client24", ".", perm="elradfmwMT")

# Permettre l'accès anonyme avec des autorisations limitées
authorizer.add_anonymous(os.getcwd())

# Créer une instance de gestionnaire FTP et spécifier l'autorisateur
handler = MyHandler
handler.authorizer = authorizer

handler.banner = "bienvenue sur le serveur de l'epsi"
handler.proto_cmds['CMD_CHPASS'] = {
    'arg': True,
    'perm': 'a',
    'auth': True,
    'callback': MyHandler.ftp_CMD_CHPASS,
    'help': 'Change user password'
}

# Créer une instance de serveur FTP écoutant sur l'adresse locale 127.0.0.1 et le port 21
server = FTPServer(("127.0.0.1", 21), handler)

# Démarrer le serveur FTP
server.serve_forever()
