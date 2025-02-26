import os

def mount():
    nodes = []
    try:
        with open("rclone-nodes.conf", "r") as file:
            for ln in file:
                if ln.startswith("["):
                    nodes.append(ln.replace("[","").replace("]", "").replace("\n", ""))
    except:
        print("ERROR: No Rclone database found, firt add a node using 'cloudpool config'")
        exit()
    n=0
    n_nodes = len(nodes)
    while n < n_nodes:
        try:
            os.mkdir("nodes/"+nodes[n])
        except:
            print("Direcoty already exist")
        n = n+1
        
    with open("mount_nodes.sh", "w") as file:
        file.write(f"rclone mount --config rclone-nodes.conf '{nodes[0]}:/' '{os.getcwd()}/nodes/{nodes[0]}' --vfs-cache-mode full &")
    with open("mount_nodes.sh", "a") as file:
        n = 1
        while n < n_nodes:
            file.write(f"\nrclone mount --config rclone-nodes.conf '{nodes[n]}:/' '{os.getcwd()}/nodes/{nodes[n]}' --vfs-cache-mode full &")
            n=n+1

    os.system("bash mount_nodes.sh")

