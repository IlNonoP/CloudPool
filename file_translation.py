import os
def file_division(file, nodes_number, nodes, user_folder, rel_path):    
    print("Start division...")
    file_path = rel_path+"/"+file
    with open(user_folder+"/"+file, "rb") as f:
        data = f.read()

    def split_str(seq, chunk, skip_tail=False):
        lst = []
        while len(seq) > 0:
            try:
                da_archiviare = seq[:chunk]
                lst.append(da_archiviare)
                seq = seq[chunk:]
            except:
                lst.append(da_archiviare) 
        return lst

    len_part=int(int(len(data))/nodes_number)
    if len_part*nodes_number < int(len(data)):  
        commodo = len(data) - len_part*nodes_number 
        len_part = len_part + commodo

    parts = split_str(data, len_part)

    print("FIle: "+str(file))
    n_part = 0
    trace = ""




    while n_part <= nodes_number-1:
        print("Sto creando: "+str("nodes/"+nodes[n_part]+"/"+rel_path))
        
        rel_path =rel_path.replace("/"+file, "")
        if rel_path == file:
            file_directory = f"{str(n_part)+file.replace(".", "(") + ")"}.txt"
        else:
            file_directory = f"{str(rel_path)+"/"+str(n_part)+file.replace(".", "(") + ")"}.txt"
            try:            
                os.mkdir("nodes/"+nodes[n_part]+"/"+rel_path)
            except:
                print("Directory already exist")


        with open("nodes/"+nodes[n_part]+"/"+file_directory, "wb") as part_file:      
            part_file.write(parts[n_part])        
        trace = trace+"|"+nodes[n_part]
        n_part = n_part+1

    with open(".Cloud_Bucket_index.txt", "a") as f:
        f.write(f"\n{file}{trace}")
    print("End division...")
        
    
   

def file_recomposition(file, user_folder, directory, rel_path):
 

    with open(f"{directory}/.Cloud_Bucket_index.txt", "r") as index:
        for ln in index:
            if ln.startswith(str(rel_path+"/"+file)):
                index_data=ln

    n_part = 0
    print("INDEXDATA = "+str(index_data))
    index_data = index_data.replace(rel_path + "/"+file+"|", "").replace("\\n", "")
    nodes = index_data.split("|")
    print("NODES = "+str(nodes))

    nodes_number=len(nodes)
    print("NODES NUMBER = "+str(nodes_number))
    
    rel_path =rel_path.replace("/"+file, "")
    

    while n_part <= nodes_number-1:
        if rel_path == file:
            file_directory = f"{str(n_part)+file.replace(".", "(") + ")"}.txt"
        else:
            file_directory = f"{str(rel_path)+"/"+str(n_part)+file.replace(".", "(") + ")"}.txt"

        with open("/opt/cloudpool/nodes/"+nodes[n_part]+"/"+file_directory, "rb") as part_file:      
            commodo = part_file.read()
        if n_part == 0:
            original_file=commodo
        else:
            original_file = original_file + commodo
        n_part = n_part+1





    def get_download_dir():
        config_path = os.path.expanduser("~/.config/user-dirs.dirs")
        if os.path.exists(config_path):
            with open(config_path) as f:
                for line in f:
                    if line.startswith("XDG_DOWNLOAD_DIR"):
                        path = line.split('"')[1]
                        return path.replace("$HOME", os.path.expanduser("~"))
        return os.path.join(os.path.expanduser("~"), "Downloads") 

    download_dir = get_download_dir()

   
    with open(download_dir+"/"+file, "wb") as file:        
        file.write(original_file)



def file_remove(filename, user_folder, directory, rel_path):
    # Apro l'indice per trovare in quali nodi è presente il file
    directory="/opt/cloudpool"
    with open(f"{directory}/.Cloud_Bucket_index.txt", "r") as index:
        index_data = None
        print("FILENAME="+str(filename))
        for ln in index:
            if ln.startswith(str(filename)):
                print(ln)
                print(filename)
                index_data = ln
                break
        if index_data is None:
            print("File non trovato nell'indice")
            return
    

    # Puliamo la stringa dell'indice
    index_data = index_data.replace(filename + "|", "").strip().replace("\\n", "")
    nodes = index_data.split("|")
    nodes_number = len(nodes)
    print("NODES = ", nodes)
    print("NODES NUMBER = ", nodes_number)

    # Ciclo per ciascun nodo in cui è presente il file
    for n_number in range(nodes_number):
        node_directory = os.path.join(directory, "nodes", nodes[n_number])
        print(f"Verificando nella cartella: {node_directory}")
        
        # Costruiamo il nome atteso: il numero del nodo seguito dal nome originale
        expected_filename = f"{n_number}{filename.replace(".", "(")+")"+".txt"}"
        print(f"File atteso: {expected_filename}")

        # Verifichiamo se il file atteso esiste nella directory corrente
        if expected_filename in os.listdir(node_directory):
            file_path = os.path.join(node_directory, expected_filename)
            try:
                os.remove(file_path)
                print(f"File {expected_filename} eliminato.")
            except Exception as e:
                print(f"Errore durante la rimozione di {expected_filename}: {e}")
        else:
            print(f"Il file {expected_filename} non è presente in {node_directory}.")
    contenent = ""
    with open(".Cloud_Bucket_index.txt", "r") as f:
        for ln in f:
            if ln.startswith(filename) == False:
                contenent = contenent + ln
    with open(".Cloud_Bucket_index.txt", "w") as file:
        file.write(contenent)   
