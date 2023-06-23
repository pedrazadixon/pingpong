# PingPong - An UDP port test tool

1. Up a server in a especific port

`python pingpong.py listen --bind=0.0.0.0 --port=15000 --proto=udp`

2. ping this server (change the ip for your server ip)

`python pingpong.py ping --server=192.168.2.100 --port=15000 --proto=udp --client-port=10000`