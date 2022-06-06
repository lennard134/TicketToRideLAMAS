from model.map.board import Board


def main_test():
    print("================= STARTING TEST ================")
    playing_board = Board()
    playing_board.init_cities("./data/cities.txt")
    for city in playing_board.cities:
        print(city)


if __name__ == "__main__":
    main_test()
