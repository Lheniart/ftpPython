import tkinter as tk
from tkinter import messagebox, filedialog
from ftplib import FTP
import os

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
    ftp.retrlines("LIST", lambda line: server_file_list.insert(tk.END, extract_file_info(line)))

def extract_file_info(line):
    parts = line.split(maxsplit=8)
    file_name = parts[-1]
    modification_date = ' '.join(parts[-4:-1])
    return f"{file_name} ({modification_date})"

def select_file(event):
    selected_item = server_file_list.curselection()
    if selected_item:
        selected_filename = server_file_list.get(selected_item)
        selected_filename = selected_filename.split()[0]  # Récupérer le nom du fichier sans la date
        selected_file.set(selected_filename)

ftp_server = "localhost"
username = "epsi"
password = "client24"

ftp = FTP()
ftp.connect(ftp_server)
ftp.login(username, password)

root = tk.Tk()
root.title("Gestionnaire FTP")
root.geometry("800x400")  # Définir la taille de la fenêtre principale

upload_frame = tk.Frame(root)
upload_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

upload_label = tk.Label(upload_frame, text="Fichiers à uploader:")
upload_label.pack(padx=5, pady=5, anchor=tk.W)

upload_button = tk.Button(upload_frame, text="Uploader un fichier", command=upload_file)
upload_button.pack(padx=5, pady=5)

server_file_list_frame = tk.Frame(root)
server_file_list_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

server_file_list_label = tk.Label(server_file_list_frame, text="Fichiers sur le serveur:")
server_file_list_label.pack(padx=5, pady=5, anchor=tk.W)

server_file_list = tk.Listbox(server_file_list_frame, width=50)
server_file_list.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

server_scrollbar = tk.Scrollbar(server_file_list_frame, orient="vertical", command=server_file_list.yview)
server_scrollbar.pack(side=tk.RIGHT, fill="y")
server_file_list.configure(yscrollcommand=server_scrollbar.set)

server_file_list.bind("<<ListboxSelect>>", select_file)

download_frame = tk.Frame(root)
download_frame.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.BOTH, expand=True)

selected_file = tk.StringVar()
selected_file_label = tk.Label(download_frame, text="Fichier sélectionné:")
selected_file_label.grid(row=0, column=0, padx=5)

selected_file_entry = tk.Entry(download_frame, textvariable=selected_file)
selected_file_entry.grid(row=0, column=1, padx=5)

download_button = tk.Button(download_frame, text="Télécharger le fichier sélectionné", command=download_file)
download_button.grid(row=0, column=2, padx=5)

refresh_files_button = tk.Button(root, text="Actualiser la liste des fichiers sur le serveur", command=refresh_files_list)
refresh_files_button.pack(side=tk.TOP, padx=10, pady=5)

welcome_text = ftp.getwelcome()
welcome_label = tk.Label(root, text=welcome_text, font=("Helvetica", 12), wraplength=700)
welcome_label.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)


refresh_files_list()
root.mainloop()

ftp.quit()
