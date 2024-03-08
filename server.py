import socket  
import pickle  
from player import Player  
from threading import Thread  

class Server:
    def __init__(self):
        self.port = 5555  # Le numéro de port sur lequel le serveur écoute
        self.host = "10.0.94.50"  
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Créer une socket TCP
        self.addr = (self.host, self.host)
        self.players_data = {}  # Utilisé pour stocker les données de tous les joueurs. La clé est l'identifiant du joueur et la valeur est les données du joueur.

    def start(self):
        self.sock.bind((self.host, self.port))  # Se lier à l'hôte et au port spécifiés
        self.sock.listen()  
        print("Waiting for a connection, Server Started")  
        while True:  # Boucle infinie, continuant à accepter les connexions client
            conn, addr = self.sock.accept()  # Accepter une connexion client
            print("Connect to:", self.addr)  
            conn.send(str(id(conn)).encode("utf-8"))  # Envoyer l'identifiant unique de la connexion au client
            Thread(target=self.handle_message, args=(conn, )).start()  # Créer un nouveau fil de discussion pour chaque client afin de gérer les messages
        

    def handle_message(self, conn):
        while True:  # Boucle infinie, surveillance continue des messages clients
            try:
                data = conn.recv(2048)  # Accepter les données envoyées par le client, jusqu'à 2048 octets
                if not data:  # S'il n'y a pas de données, la connexion peut être fermée
                    print("disconnected")
                    self.players_data.pop(str(id(conn)))  # Supprimer les informations correspondantes sur le joueur des données du joueur
                    conn.close()  
                    break  
                else:
                    data = pickle.loads(data)  # Désérialiser les données reçues
                    self.update_one_player_data(data)  # Mettre à jour les données reçues des joueurs
                    conn.sendall(pickle.dumps(self.get_other_players_data(data["id"])))  # Envoyer toutes les données du joueur sauf le joueur actuel
            except Exception as e:
                print(repr(e))  
                break  
        print("Lost connection")
        conn.close()

    def update_one_player_data(self, data):
        #key = data["id"]  
        #value = data["player"] 
        #self.players_data[key] = value  
        player_id = data["id"]
        position = data["position"]
        self.players_data[player_id] = position
        
    def get_other_players_data(self, current_player_id):
        data = {}  # Créer un nouveau dictionnaire pour stocker les données des autres joueurs
        for key, value in self.players_data.items():  # Parcourir toutes les données des joueurs
            if key != current_player_id:  # Si ce ne sont pas les données du joueur actuel
                data[key] = value  
        return data  

if __name__ == '__main__':
    server = Server()  
    server.start()  