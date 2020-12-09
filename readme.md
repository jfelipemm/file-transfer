### Requerimentos
* Python 3.2 ou superior
* Módulo tqdm

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

### Funcionamento do programa

Compartilhamento de arquivos fácil e rápido a partir da linha de comando. Este código contém o arquivo de servidor e cliente onde o cliente e o servidor se comunicam através de um socket TCP, utilizado devido a sua confiabilidade no transporte dos dados, usamos o protocolo IP associado ao TCP (que garante a entrega das informações). 

Usamos o módulo de socket que vem embutido no Python que nos fornece operações de socket.
```
  import socket
```
O tqdm é utilizado para imprimir a barra de progresso.

```
  import tqdm
  
  progress = tqdm.tqdm(range(filesize), f"Enviando {filename}", unit="B", unit_scale=True, unit_divisor=1024)
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
