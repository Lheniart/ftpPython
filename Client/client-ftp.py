from ftplib import FTP

# Adresse IP du serveur FTP
host = "127.0.0.1"
# Nom d'utilisateur et mot de passe pour se connecter au serveur FTP
user = "epsi"
password = "client25"

# Fonction pour télécharger un fichier depuis le serveur FTP
def download_file(filename):
    with FTP(host) as ftp:
        # Se connecter au serveur avec le nom d'utilisateur et le mot de passe
        ftp.login(user=user, passwd=password)
        print(ftp.getwelcome())
        # Télécharger le fichier depuis le serveur
        with open(filename, 'wb') as file:
            ftp.retrbinary('RETR ' + filename, file.write)

# Fonction pour téléverser un fichier vers le serveur FTP
def upload_file(filename):
    with FTP(host) as ftp:
        # Se connecter au serveur avec le nom d'utilisateur et le mot de passe
        ftp.login(user=user, passwd=password)
        print(ftp.getwelcome())
        # Téléverser le fichier vers le serveur
        with open(filename, 'rb') as file:
            ftp.storbinary('STOR ' + filename, file)

def change_password(new_password):
    with FTP(host) as ftp:
        ftp.login(user=user, passwd=password)
        ftp.sendcmd('CMD_CHPASS ' + new_password)

# Exemple d'utilisation :
# Télécharger un fichier depuis le serveur FTP
download_file("exemple.txt")

# Téléverser un fichier vers le serveur FTP
#upload_file("exemple.txt")

#change_password("client25")