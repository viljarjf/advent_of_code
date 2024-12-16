from fractions import Fraction

class Game:
    def __init__(self, a: str, b: str, price: str):
        self.a = self._parse_button(a)
        self.b = self._parse_button(b)
        self.price = self._parse_price(price)

    def _parse_button(self, button: str) -> tuple[int, int]:
        s = button[12:]
        x, rest = s.split(",")
        y = rest.split("+")[1].strip()
        return int(x), int(y)
    
    def _parse_price(self, price: str) -> tuple[int, int]:
        x, y = price.split(",")
        x = x[9:]
        y = y[3:].strip()
        return int(x), int(y)
    
    def __repr__(self):
        return f"{self.__class__.__name__}(A={self.a}, B={self.b}, price={self.price})"
    
    def get_score(self) -> int:
        Xa, Ya = self.a
        Xb, Yb = self.b
        Xp, Yp = self.price
        assert Fraction(Xa, Xb) != Fraction(Ya, Yb)
        i = Fraction((-Xb*Yp + Xp*Yb), (Xa*Yb - Xb*Ya))
        j = Fraction((Xa*Yp - Xp*Ya), (Xa*Yb - Xb*Ya))
        score = 3 * i + j
        if i.is_integer() and j.is_integer(): # 3.12 feature, guess I need to upgrade
            return int(score)
        return 0

def get_games(testing: bool = False) -> list[Game]:
    out = []
    with open("13_test" if testing else "13", "r") as f:
        while True:
            out.append(Game(f.readline(), f.readline(), f.readline()))
            if not f.readline():
                break
    return out

def main():
    games = get_games()
    print(sum(game.get_score() for game in games))
    for game in games:
        game.price = (
            10000000000000 + game.price[0],
            10000000000000 + game.price[1],
        )
    print(sum(game.get_score() for game in games))

if __name__ == "__main__":
    main()
