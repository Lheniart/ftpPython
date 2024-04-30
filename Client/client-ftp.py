from ftplib import FTP

# Adresse IP du serveur FTP (dans notre cas, c'est localhost)
host = "127.0.0.1"
# Nom d'utilisateur et mot de passe pour se connecter au serveur FTP
user = "epsi"
password = "client24"

# Fonction pour télécharger un fichier depuis le serveur FTP
def download_file(filename):
    # Établir une connexion FTP
    with FTP(host) as ftp:
        # Se connecter au serveur avec le nom d'utilisateur et le mot de passe
        ftp.login(user=user, passwd=password)
        # Télécharger le fichier depuis le serveur
        with open(filename, 'wb') as file:
            ftp.retrbinary('RETR ' + filename, file.write)

# Fonction pour téléverser un fichier vers le serveur FTP
def upload_file(filename):
    # Établir une connexion FTP
    with FTP(host) as ftp:
        # Se connecter au serveur avec le nom d'utilisateur et le mot de passe
        ftp.login(user=user, passwd=password)
        # Téléverser le fichier vers le serveur
        with open(filename, 'rb') as file:
            ftp.storbinary('STOR ' + filename, file)

# Exemple d'utilisation :
# Télécharger un fichier depuis le serveur FTP
download_file("exemple.txt")

# Téléverser un fichier vers le serveur FTP
#upload_file("exemple.txt")
