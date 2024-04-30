import tkinter as tk
from tkinter import messagebox
from ftplib import FTP

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
    file_list.delete(0, tk.END)
    ftp.retrlines("LIST", lambda line: file_list.insert(tk.END, extract_file_info(line)))

def extract_file_info(line):
    parts = line.split(maxsplit=8)
    file_name = parts[-1]
    modification_date = ' '.join(parts[-4:-1])
    return f"{file_name} ({modification_date})"

def select_file(event):
    selected_item = file_list.curselection()
    if selected_item:
        selected_filename = file_list.get(selected_item)
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
root.geometry("600x400")  # Définir la taille de la fenêtre principale

file_list_frame = tk.Frame(root)
file_list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

file_list_label = tk.Label(file_list_frame, text="Dossiers distants:")
file_list_label.grid(row=0, column=0, sticky=tk.W)

file_list = tk.Listbox(file_list_frame, width=50)
file_list.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)

scrollbar = tk.Scrollbar(file_list_frame, orient="vertical", command=file_list.yview)
scrollbar.grid(row=1, column=1, sticky="ns")
file_list.configure(yscrollcommand=scrollbar.set)

file_list.bind("<<ListboxSelect>>", select_file)

refresh_button = tk.Button(root, text="Actualiser la liste des fichiers", command=refresh_files_list)
refresh_button.pack(padx=10, pady=5)

download_frame = tk.Frame(root)
download_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

selected_file = tk.StringVar()
selected_file_label = tk.Label(download_frame, text="Fichier sélectionné:")
selected_file_label.grid(row=0, column=0, padx=5)

selected_file_entry = tk.Entry(download_frame, textvariable=selected_file)
selected_file_entry.grid(row=0, column=1, padx=5)

download_button = tk.Button(download_frame, text="Télécharger le fichier sélectionné", command=download_file)
download_button.grid(row=0, column=2, padx=5)

refresh_files_list()

root.mainloop()

ftp.quit()
