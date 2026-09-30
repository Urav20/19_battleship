from board import Board
from ai import AI


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI()
        self._setup()

    def _setup(self):
        # Player fleet
        self.player.place_ship({(1, 1), (1, 2), (1, 3)})
        self.player.place_ship({(3, 1), (4, 1)})

        # Enemy fleet
        self.enemy.place_ship({(2, 2), (2, 3), (2, 4)})
        self.enemy.place_ship({(4, 1), (5, 1)})

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print(
            "Enemy ship cells remaining:",
            self.enemy.remaining_ship_cells()
        )

    def run(self):
        print("Battleship")

        while True:
            self.show()
            raw = input("> ").strip().lower()

            if raw == "q":
                return

            # Convert player's 1-based input to the internal 0-based
            # coordinate system.
            try:
                r, c = map(int, raw.split(","))
                pos = (r - 1, c - 1)
            except ValueError:
                print("Use row,col.")
                continue

            if not (
                0 <= pos[0] < Board.SIZE
                and 0 <= pos[1] < Board.SIZE
            ):
                print("Outside board.")
                continue

            # A repeated coordinate is not an actual shot.
            if pos in self.enemy.shots:
                print("Already fired there.")
                continue

            # ---------------------------------------------------------
            # PLAYER SHOT
            # ---------------------------------------------------------
            hit = self.enemy.fire(pos)

            # Feedback is generated ONLY after the actual shot.
            if hit:
                print("HIT!")

                # Check whether this particular ship has now been sunk.
                for ship in self.enemy.ships:
                    if pos in ship and self.enemy.is_sunk(ship):
                        print("You sank a ship!")
                        break
            else:
                print("MISS!")

            # Check the complete fleet only after the shot is processed.
            if self.enemy.all_sunk():
                print("You sank the entire fleet.")
                return

            # ---------------------------------------------------------
            # AI TARGET SELECTION
            # ---------------------------------------------------------
            # choose() only selects a coordinate. It does NOT fire.
            ai_pos = self.ai.choose()

            if ai_pos is None:
                print("AI has no remaining valid cells.")
                return

            # Convert to 1-based coordinates only for display.
            ai_display = f"{ai_pos[0] + 1},{ai_pos[1] + 1}"
            print("AI fired at", ai_display)

            # ---------------------------------------------------------
            # AI SHOT
            # ---------------------------------------------------------
            # This is the only point where the AI actually fires.
            ai_hit = self.player.fire(ai_pos)

            # Feedback is generated ONLY after the actual AI shot.
            if ai_hit:
                print("AI scored a hit.")

                # Tell the AI about the successful shot so that it can
                # prefer nearby cells on its next turn.
                self.ai.record_result(ai_pos, True)

                # Check whether this particular ship has been sunk.
                for ship in self.player.ships:
                    if ai_pos in ship and self.player.is_sunk(ship):
                        print("AI sank one of your ships.")
                        break
            else:
                print("AI missed.")

            # Check the complete player fleet after the shot.
            if self.player.all_sunk():
                print("AI sank your entire fleet.")
                return

