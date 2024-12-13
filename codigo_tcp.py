import socket

class TCPSegment:
    def __init__(self, seq_num, ack_num, data):
        """
        Inicializa um segmento TCP.
        
        Parâmetros:
        seq_num (int): Número de sequência.
        ack_num (int): Número de confirmação.
        data (str): Dados do segmento.
        """
        self.seq_num = seq_num  # Número de sequência
        self.ack_num = ack_num  # Número de confirmação
        self.data = data        # Dados

    def __str__(self):
        """
        Retorna uma representação em string do segmento TCP.
        
        Retorna:
        str: Representação no formato "seq_num,ack_num,data".
        """
        return f"{self.seq_num},{self.ack_num},{self.data}"

    @staticmethod
    def from_string(segment_str):
        """
        Converte uma string representando um segmento TCP em um objeto TCPSegment.
        
        Parâmetros:
        segment_str (str): String no formato "seq_num,ack_num,data".
        
        Retorna:
        TCPSegment: Objeto TCPSegment com os valores extraídos.
        """
        seq_num, ack_num, data = segment_str.split(',', 2)
        return TCPSegment(int(seq_num), int(ack_num), data)

class TCPConnection:
    def __init__(self, address):
        """
        Inicializa uma conexão TCP.
        
        Parâmetros:
        address (tuple): Endereço IP e porta do servidor.
        """
        self.address = address  # Endereço IP e porta
        self.state = 'CLOSED'   # Estado da conexão
        self.segments = []      # Segmentos enviados/recebidos

    def send_segment(self, segment):
        """
        Envia um segmento TCP.
        
        Parâmetros:
        segment (TCPSegment): Objeto TCPSegment a ser enviado.
        """
        print(f"Enviando segmento: {segment}")
        self.segments.append(segment)

    def receive_segment(self, segment):
        """
        Recebe um segmento TCP.
        
        Parâmetros:
        segment (TCPSegment): Objeto TCPSegment recebido.
        """
        print(f"Recebendo segmento: {segment}")
        self.segments.append(segment)

class TCPClient:
    def __init__(self, server_address, server_port):
        """
        Inicializa um cliente TCP.
        
        Parâmetros:
        server_address (str): Endereço IP do servidor.
        server_port (int): Porta do servidor.
        """
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = None
        self.connection = TCPConnection((server_address, server_port))

    def connect(self):
        """
        Conecta ao servidor TCP.
        """
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.client_socket.connect((self.server_address, self.server_port))
            print(f"Conectado ao servidor {self.server_address}:{self.server_port}")
            self.connection.state = 'SYN_SENT'
            syn_segment = TCPSegment(seq_num=0, ack_num=0, data='SYN')
            self.send_segment(syn_segment)
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            self.client_socket = None

    def send_segment(self, segment):
        """
        Envia um segmento TCP ao servidor.
        
        Parâmetros:
        segment (TCPSegment): Objeto TCPSegment a ser enviado.
        """
        if self.client_socket:
            try:
                self.client_socket.sendall(str(segment).encode())
                print("Segmento enviado com sucesso.")
            except Exception as e:
                print(f"Erro ao enviar segmento: {e}")

    def send_message(self, message):
        """
        Envia uma mensagem ao servidor.
        
        Parâmetros:
        message (str): Mensagem a ser enviada.
        """
        if self.client_socket:
            try:
                seq_num = len(self.connection.segments)
                data_segment = TCPSegment(seq_num=seq_num, ack_num=0, data=message)
                self.send_segment(data_segment)
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")

    def receive_message(self):
        """
        Recebe uma mensagem do servidor.
        
        Retorna:
        str: Mensagem recebida do servidor.
        """
        if self.client_socket:
            try:
                response = self.client_socket.recv(1024)
                segment_str = response.decode()
                segment = TCPSegment.from_string(segment_str)
                self.connection.receive_segment(segment)
                return segment_str
            except socket.error as e:
                print(f"Erro ao receber mensagem: {e}") #importante
                return None
            except Exception as e:
                print(f"Erro inesperado ao receber mensagem: {e}")
                return None

    def close_connection(self):
        """
        Encerra a conexão com o servidor.
        """
        if self.client_socket:
            self.client_socket.close()
            print("Conexão encerrada.")
        self.client_socket = None

class TCPServer:
    def __init__(self, host='0.0.0.0', port=5500):#ngrok
        """
        Inicializa um servidor TCP.
        
        Parâmetros:
        host (str): Endereço IP do servidor.
        port (int): Porta do servidor.
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = TCPConnection((host, port))

    def start(self):
        """
        Inicia o servidor TCP e aguarda conexões.
        """
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor iniciado em {self.host}:{self.port}")

        while True:
            print("Aguardando conexão...")
            client_socket, client_address = self.server_socket.accept()
            print(f"Conexão recebida de {client_address}")
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        """
        Lida com as mensagens do cliente.
        
        Parâmetros:
        client_socket (socket): Socket do cliente.
        """
        try:
            while True:
                try:
                    message = client_socket.recv(1024)
                    if not message:
                        break
                    segment_str = message.decode()
                    segment = TCPSegment.from_string(segment_str)
                    print(f"Segmento recebido: {segment}")
                    self.connection.receive_segment(segment)
                    response_segment = TCPSegment(seq_num=0, ack_num=segment.seq_num + 1, data='ACK')
                    self.send_segment(client_socket, response_segment)
                except socket.error as e:
                    print(f"Erro na comunicação com o cliente: {e}")
                    break
        except Exception as e:
            print(f"Erro ao lidar com o cliente: {e}")
        finally:
            client_socket.close()
            print("Conexão com o cliente encerrada.")

    def send_segment(self, client_socket, segment):
        """
        Envia um segmento TCP ao cliente.
        
        Parâmetros:
        client_socket (socket): Socket do cliente.
        segment (TCPSegment): Objeto TCPSegment a ser enviado.
        """
        try:
            client_socket.sendall(str(segment).encode())
            print("Segmento enviado com sucesso.")
        except Exception as e:
            print(f"Erro ao enviar segmento: {e}")

# Criando a conexão
if __name__ == "__main__":
    print("Escolha uma opção:")
    print("1 - Servidor")
    print("2 - Cliente")
    opcao = input("Opção: ")

    if opcao == "1":
        # Inicializa e inicia o servidor TCP
        server = TCPServer(host="localhost", port=5500)
        server.start()
    elif opcao == "2":
        # Inicializa o cliente TCP e conecta ao servidor
        client = TCPClient(server_address="localhost", server_port=5500)
        client.connect()
        while True:
            msg = input("Digite a mensagem (ou 'sair' para encerrar): ")
            if msg.lower() == "sair":
                client.close_connection()
                break
            client.send_message(msg)
            response = client.receive_message()
            print(f"Resposta do servidor: {response}")
    else:
        print("Opção inválida.")
