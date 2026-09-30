import random


class AI:
    def __init__(self, size=6):
        self.size = size
        self.tried = set()
        self.hits = set()

    def choose(self):
        # First, look for untried cells next to previous successful hits.
        nearby = []

        for r, c in self.hits:
            neighbours = [
                (r - 1, c),
                (r + 1, c),
                (r, c - 1),
                (r, c + 1)
            ]

            for pos in neighbours:
                if (
                    0 <= pos[0] < self.size
                    and 0 <= pos[1] < self.size
                    and pos not in self.tried
                    and pos not in nearby
                ):
                    nearby.append(pos)

        # Prefer nearby cells after a successful hit.
        if nearby:
            pos = random.choice(nearby)
            self.tried.add(pos)
            return pos

        # Otherwise choose any remaining untried cell.
        options = [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if (r, c) not in self.tried
        ]

        # No valid cells remain.
        if not options:
            return None

        pos = random.choice(options)
        self.tried.add(pos)
        return pos

    def record_result(self, pos, hit):
        if hit:
            self.hits.add(pos)
