import file_translation
import mount_nodes
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os




os.chdir("/opt/cloudpool")

# Legge la cartella dell'utente da configurazione
with open("config.conf", "r") as file:    
    user_folder = str(file.readlines(1)).replace("['user_folder=", "").replace("']", "")


try:
    os.mkdir("nodes")
except:
    print("Nodes folder already exist!")

# Ottiene i nodi disponibili
nodes = [f for f in os.listdir("/opt/cloudpool/nodes/")]
nodes_number = len(nodes)

# Monta i nodi
mount_nodes.mount()

class MioHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print("New file found!")
            abs_path = event.src_path  # Percorso assoluto del file
            rel_path = os.path.relpath(abs_path, user_folder)  # Percorso relativo rispetto a user_folder
            file = os.path.basename(event.src_path)
            if rel_path.endswith(".desktop") or rel_path.endswith(".lock"):
                return
            
            # Processa il file
            rel_path=rel_path.replace("/"+file, "")
            file_translation.file_division(file, nodes_number, nodes, user_folder, rel_path)

            # Rimuove il file originale
            os.remove(abs_path)

            # Crea il file .desktop
            desktop_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={rel_path}
Exec=python3 '/opt/cloudpool/file_download.py' '{file}' '{user_folder}' '/opt/cloudpool' '{rel_path}'
Icon=utilities-terminal
Terminal=true
"""
            desktop_path = os.path.join(user_folder +"/"+ rel_path +  ".desktop")
      
            with open(desktop_path, "w") as f:
                f.write(desktop_entry)

            os.system(f"chmod +x '{desktop_path}'")

    def on_deleted(self, event):
        if not event.is_directory:
            print("File deleted!")
            abs_path = event.src_path
            rel_path = os.path.relpath(abs_path, user_folder)
            file = os.path.basename(event.src_path)
            rel_path=rel_path.replace("/"+file, "")

            if rel_path.endswith(".desktop"):
                file_translation.file_remove(rel_path.replace(".desktop", ""), user_folder, "/opt/cloudpool", rel_path)

# Configura l'osservatore
handler = MioHandler()
observer = Observer()
observer.schedule(handler, user_folder, recursive=True)  # Attiva il monitoraggio ricorsivo
observer.start()

try:
    print("Waiting for file events...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
