### Requerimentos
* Python 3.2 ou superior
* Módulo tqdm
* Módulo socket

### Como instalar o tqdm
Com o python instalado, execute o seguinte comando no terminal:
`pip3 install tqdm`

### Como executar um arquivo python
Basta digitar em um terminal o seguinte comando:
Para linux: `python3 nomedoarquivo`
Para windows: `python nomedoarquivo`
O nome do arquivo deve conter a extensão `.py`.

### Para executar o programa
Execute o arquivo `servidor.py` contido na pasta `servidor`. Ele é o responsável por ficar escutando as requisições dos clientes. Ele suporta apenas uma transferência de arquivo por vez.
Em seguida execute o arquivo `cliente.py` na pasta `cliente`. É necessário informar o ip, porta e arquivo que deseja transferir.

### Funcionamento do programa (Cliente)

Compartilhamento de arquivos fácil e rápido a partir da linha de comando. Este código contém o arquivo de servidor e cliente onde o cliente e o servidor se comunicam através de um socket TCP, utilizado devido a sua confiabilidade no transporte dos dados, usamos o protocolo IP associado ao TCP (que garante a entrega das informações). 

Usamos o módulo de socket que vem embutido no Python que nos fornece operações de socket.
```
  import socket
```
O tqdm é utilizado para imprimir a barra de progresso.

```
  import tqdm

```

Precisamos especificar o endereço IP e a porta do servidor o qual queremos nos conectar, e também o nome do arquivo que queremos enviar.

```
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
```
Obtém o tamanho do arquivo encaminhado em bytes, pois precisamos dele para imprimir a barra de progresso no cliente e no servidor.
```
filesize = os.path.getsize(filename)
```

Após obtermos todas as informações necessárias vamos criar o socket tcp:
```
 s = socket.socket()
```

Conectando-se ao servidor:

```
 s.connect((host, port))
```

O método connect () espera um endereço do par (host, porta) para conectar o socket a esse endereço. 
Assim que a conexão é estabelecida, enviamos o nome e o tamanho do arquivo:

```
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
```

Agora enviamos o arquivo, e imprimimos barras de progresso usando a biblioteca tqdm :

```
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
```

O que estamos fazendo aqui é abrir o arquivo em binário, ler pedaços do arquivo e enviá-los ao soquete usando a função sendall() , e atualizarmos a barra de progresso, assim que acabar, fechamos o socket.



### Funcionamento do programa (Servidor)



Inicializamos alguns parâmetros, o "0.0.0.0" como o endereço IP do servidor para ouvir tanto pelo ip local como pelo ip da rede. Além disso, usamos a mesma porta no servidor e no cliente.

```
import socket
import tqdm
import os
import threading
import sys

# ip a ser utilizado para receber envios
# usa-se 0.0.0.0 para ouvir tanto pelo ip local(127.0.0.1) ou pelo ip da rede
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001

```


Quando o cliente estiver conectado ele enviará o nome e o tamanho do arquivo:
```
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
```   

Estamos abrindo o arquivo como gravação em binário, usando recv (BUFFER_SIZE) para receber bytes BUFFER_SIZE do soquete do cliente e gravá-lo no arquivo. Assim que terminarmos, fechamos o socket do cliente e do servidor.

```
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

```

Vamos criar nosso socket TCP:

```
# cria o socket tcp do servidor
s = socket.socket()

```
Agora que é diferente do cliente, precisamos vincular o socket que criamos ao nosso SERVER_HOST e SERVER_PORT:

```
# vincula o socket ao endereço especificado
s.bind((SERVER_HOST, SERVER_PORT))

```

Ouvivos a conexão:
```
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

```
