import socket
import argparse
import signal
import sys
import time


def run_udp_server(bind_ip, port):
    # Crea un socket UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Asocia el socket a la dirección IP y puerto especificados
    udp_socket.bind((bind_ip, port))

    print(f"Servidor UDP escuchando en {bind_ip}:{port}")

    # Función de manejo de la señal de interrupción (Ctrl+C)
    def signal_handler(sig, frame):
        print("\nstopping...")
        udp_socket.close()
        sys.exit(0)

    # Registra el manejador de señal
    signal.signal(signal.SIGINT, signal_handler)

    # Establece un tiempo de espera en el socket del servidor
    udp_socket.settimeout(1.0)  # Tiempo de espera de 1 segundo

    while True:
        try:
            # Espera a recibir datos del cliente
            data, address = udp_socket.recvfrom(1024)
            print(f"{data.decode()} from {address[0]}:{address[1]}")

            # Responde al cliente
            print(f"Pong to {address[0]}:{address[1]}")
            response = "Pong"
            udp_socket.sendto(response.encode(), address)

        except:
            pass


def run_udp_client(server_ip, server_port, client_port):
    # Crea un socket UDP para el cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enlaza el socket del cliente a una dirección IP y puerto específicos
    if client_port is not None:
        client_socket.bind(('0.0.0.0', client_port))

    # Establece un tiempo de espera en el socket del cliente
    client_socket.settimeout(1.0)  # Tiempo de espera de 1 segundo

    # Función de manejo de la señal de interrupción (Ctrl+C)
    def signal_handler(sig, frame):
        print("\nstopping...")
        client_socket.close()
        sys.exit(0)

    # Registra el manejador de señal
    signal.signal(signal.SIGINT, signal_handler)

    # Establece un tiempo de espera en el socket
    client_socket.settimeout(1.0)  # Tiempo de espera de 1 segundo

    while True:
        try:
            # Datos a enviar al servidor
            print(f"Ping to {server_ip}:{server_port}")
            message = "Ping"
            client_socket.sendto(message.encode(), (server_ip, server_port))

            # Espera a recibir la respuesta del servidor
            response, server_address = client_socket.recvfrom(1024)
            print(
                f"{response.decode()} from {server_address[0]}:{server_address[1]}")

        except:
            print("Connection timed out")

        time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cliente/Servidor UDP')
    parser.add_argument('action', choices=[
                        'listen', 'ping'], help='Acción a realizar')
    parser.add_argument('--bind', default='0.0.0.0',
                        help='Dirección IP para escuchar (solo para acción "listen")')
    parser.add_argument('--port', type=int, default=15000, help='Puerto UDP')
    parser.add_argument('--client-port', type=int, default=None,
                        help='Puerto UDP Cliente', metavar='client_port')
    parser.add_argument('--proto', default='udp', help='Protocolo')
    parser.add_argument(
        '--server', help='Dirección IP del servidor (solo para acción "ping")')

    args = parser.parse_args()

    if args.action == 'listen' and args.proto == 'udp':
        run_udp_server(args.bind, args.port)
    elif args.action == 'ping' and args.proto == 'udp' and args.server:
        run_udp_client(args.server, args.port, args.client_port)
    else:
        print("Invalid command")
