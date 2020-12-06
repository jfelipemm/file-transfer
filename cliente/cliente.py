import socket
import tqdm
import os
import sys

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # quantidade de bytes para enviar em cada passo

# o ip ou nome do servidor
host = "127.0.0.1"
# a porta a ser utilizada
port = 5001

while host:
    print("Digite o ip ou nome do servidor ao qual deseja conectar(vazio para finalizar):")
    host = input()
    if not host:
        sys.exit(0)
    print("Digite a porta a ser utilizada(vazio para finalizar):")
    port = input()
    if not port:
        sys.exit(0)
    port = int(port)

    print("Digite o caminho do arquivo que deseja transferir(vazio para finalizar):")
    filename = input()
    if not filename:
        sys.exit(0)

    # o tamanho do arquivo especificado
    filesize = os.path.getsize(filename)

    # cria o socket do cliente
    s = socket.socket()

    print(f"[+] Conectando-se a {host}:{port}")
    s.connect((host, port))
    print("[+] Conectado.")

    # envia o nome e tamanho do arquivo
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # começa a enviar o arquivo
    progress = tqdm.tqdm(range(filesize), f"Enviando {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        for _ in progress:
            # lê os bytes do arquivo
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # transmissão finalizada
                progress.close()
                print("Envio finalizado\n")
                break
            # usa-se sendall para garantir a transmissão do arquivo completo
            s.sendall(bytes_read)
            # atualiza a barra de progresso
            progress.update(len(bytes_read))
    # fecha o socket
    s.close()