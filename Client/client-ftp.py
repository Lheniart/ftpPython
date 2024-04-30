import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ftplib import FTP
import os

ftp_server = "localhost"


def login():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        try:
            with FTP(ftp_server) as ftp:
                ftp.login(user=username, passwd=password)
                messagebox.showinfo("Connexion réussie", "Vous êtes connecté au serveur FTP.")
                refresh_files_list()
                change_password_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
                upload_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
                server_file_list_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        except Exception as e:
            messagebox.showerror("Erreur de connexion", f"Impossible de se connecter au serveur FTP : {str(e)}")
    else:
        messagebox.showerror("Erreur", "Veuillez saisir un nom d'utilisateur et un mot de passe.")


def change_password():
    new_password = new_password_entry.get()
    if new_password:
        with FTP(ftp_server) as ftp:
            ftp.login(user=username_entry.get(), passwd=password_entry.get())
            response = ftp.sendcmd('CMD_CHPASS ' + new_password)
            messagebox.showinfo("Changement de mot de passe", "Le mot de passe a été changé avec succès.")
    else:
        messagebox.showerror("Erreur", "Veuillez saisir un nouveau mot de passe.")


def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        filename = os.path.basename(file_path)
        try:
            with open(file_path, "rb") as file:
                ftp.storbinary(f"STOR {filename}", file)
            refresh_files_list()
            messagebox.showinfo("Upload réussi", f"Le fichier {filename} a été uploadé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur d'upload", f"Une erreur s'est produite lors de l'upload du fichier : {str(e)}")
    else:
        messagebox.showerror("Erreur", "Aucun fichier sélectionné.")


def download_file():
    filename = selected_file.get()
    if filename:
        local_filepath = f"downloads/{filename}"
        with open(local_filepath, "wb") as local_file:
            ftp.retrbinary(f"RETR {filename}", local_file.write)
        messagebox.showinfo("Téléchargement terminé", f"Le fichier {filename} a été téléchargé avec succès.")
    else:
        messagebox.showerror("Erreur", "Veuillez sélectionner un fichier à télécharger.")


def refresh_files_list():
    # Actualiser la liste des fichiers sur le serveur
    server_file_list.delete(0, tk.END)
    with FTP(ftp_server) as ftp:
        ftp.login(user=username_entry.get(), passwd=password_entry.get())
        ftp.retrlines("LIST", lambda line: server_file_list.insert(tk.END, extract_file_info(line)))


def extract_file_info(line):
    parts = line.split(maxsplit=8)
    file_name = parts[-1]
    modification_date = ' '.join(parts[-4:-1])
    return f"{file_name} ({modification_date})"


root = tk.Tk()
root.title("Gestionnaire FTP")
root.geometry("800x400")  # Définir la taille de la fenêtre principale

# Header (connexion / changement de mot de passe)
header_frame = ttk.Frame(root)
header_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

username_label = ttk.Label(header_frame, text="Nom d'utilisateur:")
username_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

username_entry = ttk.Entry(header_frame)
username_entry.grid(row=0, column=1, padx=5, pady=5)

password_label = ttk.Label(header_frame, text="Mot de passe:")
password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

password_entry = ttk.Entry(header_frame, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

login_button = ttk.Button(header_frame, text="Se connecter", command=login)
login_button.grid(row=2, columnspan=2, pady=5)

change_password_frame = ttk.Frame(root)
change_password_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

new_password_label = ttk.Label(change_password_frame, text="Nouveau mot de passe:")
new_password_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

new_password_entry = ttk.Entry(change_password_frame)
new_password_entry.grid(row=0, column=1, padx=5, pady=5)

change_password_button = ttk.Button(change_password_frame, text="Changer le mot de passe", command=change_password)
change_password_button.grid(row=1, columnspan=2, pady=5)

# Centre (Upload)
upload_frame = ttk.Frame(root)
upload_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

upload_label = ttk.Label(upload_frame, text="Fichiers à uploader:")
upload_label.pack(padx=5, pady=5, anchor=tk.W)

upload_button = ttk.Button(upload_frame, text="Uploader un fichier", command=upload_file)
upload_button.pack(padx=5, pady=5)

# Droite (Download)
server_file_list_frame = ttk.Frame(root)
server_file_list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

refresh_files_button = ttk.Button(server_file_list_frame, text="Actualiser la liste des fichiers sur le serveur",
                                  command=refresh_files_list)
refresh_files_button.pack(side=tk.TOP, padx=10, pady=5)

server_file_list = tk.Listbox(server_file_list_frame, width=50)
server_file_list.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)

server_scrollbar = ttk.Scrollbar(server_file_list_frame, orient="vertical", command=server_file_list.yview)
server_scrollbar.pack(side=tk.RIGHT, fill="y")
server_file_list.configure(yscrollcommand=server_scrollbar.set)

server_file_list.bind("<<ListboxSelect>>", lambda event: select_file())

download_button = ttk.Button(server_file_list_frame, text="Télécharger le fichier sélectionné", command=download_file)
download_button.pack(side=tk.BOTTOM, padx=10, pady=5)

selected_file = tk.StringVar()

root.mainloop()
