from game import Game
from parsers.json_parser import JSONParser
from network_handlers.tcp_network_handler import TCPNetworkHandler


def main():
    network_handler = TCPNetworkHandler()
    parser = JSONParser()
    game = Game(network_handler, parser)
    game.run()


if __name__ == '__main__':
    main()
