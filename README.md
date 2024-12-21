# Codigo-de-protocolo-TCP-em-python
codigo usado para apresentação de um seminario na cadeira de Programação Orientada a Objetos

# Tutorial de Execução do Código TCP

Este tutorial explica como executar o código de um servidor e cliente TCP simples, utilizando Python e sockets. O código simula a comunicação entre um cliente e um servidor, utilizando a troca de segmentos TCP. Para rodá-lo, será necessário abrir dois terminais simultaneamente: um para o servidor e outro para o cliente.

## Passo 1: Preparação do Ambiente

Antes de executar o código, certifique-se de ter o Python instalado em sua máquina. O código utiliza a biblioteca `socket`, que é parte da biblioteca padrão do Python, então não é necessário instalar dependências adicionais.

## Passo 2: Estrutura do Código

### Classes e Funções

1. **Classe `TCPSegment`**: Representa um segmento TCP com três atributos:
   - `seq_num`: Número de sequência do segmento.
   - `ack_num`: Número de confirmação.
   - `data`: Dados do segmento (mensagem).

   Métodos:
   - `__str__`: Retorna uma representação em string do segmento no formato `"seq_num,ack_num,data"`.
   - `from_string`: Converte uma string no formato `"seq_num,ack_num,data"` de volta para um objeto `TCPSegment`.

2. **Classe `TCPConnection`**: Representa uma conexão TCP entre o cliente e o servidor.
   - Possui métodos para enviar (`send_segment`) e receber (`receive_segment`) segmentos TCP.

3. **Classe `TCPClient`**: Implementa a lógica do cliente TCP.
   - Conecta-se ao servidor com o método `connect()`.
   - Envia e recebe mensagens utilizando os métodos `send_message()` e `receive_message()`.
   - Encerra a conexão com o método `close_connection()`.

4. **Classe `TCPServer`**: Implementa a lógica do servidor TCP.
   - Escuta na porta e endereço definidos, aguardando conexões de clientes.
   - Quando um cliente se conecta, o servidor recebe e responde com ACK.

## Passo 3: Executando o Código

### 1. Abrir o Terminal para o Servidor
No primeiro terminal, execute o código como servidor. O servidor ficará aguardando por conexões de clientes. Para isso, selecione a opção "1" ao iniciar o código.

```bash
  $ python tcp_code.py
  Escolha uma opção:
  1 - Servidor
  2 - Cliente
  Opção: 1
  Servidor iniciado em 0.0.0.0:5500
  Aguardando conexão...
```
### 2. Abrir o Terminal para o Cliente
No segundo terminal, execute o código como cliente. O cliente precisa se conectar ao servidor utilizando o endereço e a porta definidos. Para isso, escolha a opção "2" ao iniciar o código.
```bash
$ python tcp_code.py
Escolha uma opção:
1 - Servidor
2 - Cliente
Opção: 2
Conectado ao servidor localhost:5500
```
### Como envio mensagens?
Após a conexão, o cliente pode enviar mensagens ao servidor. Para testar, digite uma mensagem, por exemplo:
```bash
Digite a mensagem (ou 'sair' para encerrar): Olá, servidor!
```
O servidor irá processar a mensagem e retornar uma resposta, que será exibida no terminal do cliente:
```bash
Resposta do servidor: seq_num=0,ack_num=1,ACK
```
### 3. Como encerrar a conexão?
O cliente pode continuar enviando mensagens até digitar "sair" para encerrar a conexão:
```bash
Digite a mensagem (ou 'sair' para encerrar): sair
Conexão encerrada.
```
O servidor, por sua vez, continuará aguardando novas conexões ou mensagens até que seja encerrado manualmente.

## 4.Explicação do Código

### Funcionamento do Servidor
### O servidor é iniciado e começa a escutar por conexões na porta 5500 (ou a porta que você definir).
### Quando um cliente se conecta, o servidor recebe os segmentos TCP enviados pelo cliente, processa a mensagem e envia uma resposta com um segmento ACK (de confirmação).
### O servidor encerra a conexão quando o cliente desconecta ou quando ocorre algum erro.
### Funcionamento do Cliente
### O cliente se conecta ao servidor e envia um segmento TCP com uma mensagem.
### O cliente aguarda a resposta do servidor e exibe a resposta no terminal.
### O cliente pode enviar várias mensagens até decidir encerrar a conexão digitando "sair".




# Bibliografia
https://youtu.be/PpsEaqJV_A0?si=kZs9xcjVhz3tdCaK (What is TCP/IP) <br/>
Chatgpt, Copilot, Gemini, Llama 3 <br/>
https://youtu.be/uwoD5YsGACg?si=pCrZ4DdZqi3ixKgS (TCP vs UDP Comparison) <br/>
https://www.fortinet.com/br/resources/cyberglossary/tcp-ip-model-vs-osi-model (Modelo OSI e TCP/IP) <br/>
https://youtu.be/F27PLin3TV0?si=8SzGP5-10JJjhD_Y (TCP Walkthrough)
