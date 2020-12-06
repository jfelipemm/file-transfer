import socket
import tqdm
import os
import threading
import sys

# ip a ser utilizado para receber envios
# usa-se 0.0.0.0 para ouvir tanto pelo ip local(127.0.0.1) ou pelo ip da rede
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# quantidade de bytes a ser recebida por vez
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
is_waiting = False

def receive_file(s):
    global is_waiting
    is_waiting = True
    
    print(f"[*] Escutando em {SERVER_HOST}:{SERVER_PORT}")
    # aceita a conexão se existir alguma
    client_socket, address = s.accept()
    # somente executa se algum cliente se conectou
    print(f"[+] {address} se conectou.")

    # recebe as informações do arquivo
    # recebe pelo socket do cliente
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove o caminho absoluto do arquivo(se existir)
    # para pegar só o nome do arquivo
    filename = os.path.basename(filename)
    # converte o tamanho do arquivo para int
    filesize = int(filesize)

    # começa a receber o arquivo e escrever na stream
    progress = tqdm.tqdm(range(filesize), f"Recebendo {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for _ in progress:
            # lê os bytes do socket
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                # se nada foi recebido, finaliza a conexão
                progress.close()
                print("Recebimento finalizado\n")
                break
            # escreve no arquivo o que recebeu
            f.write(bytes_read)
            # atualiza a barra de progresso
            progress.update(len(bytes_read))
    # fecha o socket com o cliente
    client_socket.close()
    is_waiting = False

# cria o socket tcp do servidor
s = socket.socket()

# vincula o socket ao endereço especificado
s.bind((SERVER_HOST, SERVER_PORT))

while True:
    try:
        # permite ao servidor aceitar conexões
        # 5 é o número máximo de conexões recusadas até parar de aceitar novas
        s.listen(5)
        if not is_waiting:
                t = threading.Thread(target=receive_file, args=(s,), daemon=True)
                t.start()
    except KeyboardInterrupt:
        print("Finalizando servidor...")
        sys.exit(1)

# fecha o socket do servidor
s.close()