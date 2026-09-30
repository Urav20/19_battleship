class Board:
    SIZE = 6

    def __init__(self):
        self.ships = []
        self.shots = set()

    def place_ship(self, cells):
        self.ships.append(set(cells))

    def fire(self, pos):
        if pos in self.shots:
            return False

        self.shots.add(pos)
        return any(pos in ship for ship in self.ships)

    def is_sunk(self, ship):
        return ship <= self.shots

    def all_sunk(self):
        return all(self.is_sunk(ship) for ship in self.ships)

    def remaining_ship_cells(self):
        return sum(
            len(ship - self.shots)
            for ship in self.ships
        )