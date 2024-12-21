choices = [
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    False,
    True,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    True,
    True,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    True,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
]

class Keyboard:
    def __init__(self, pos: tuple[int, int], chars: list[str]):
        self.row = pos[0]
        self.col = pos[1]
        self.chars = chars
        self.start = self.pos
        for i, s in enumerate(chars):
            for j, c in enumerate(s):
                if c not in "0123456789A<>v^":
                    self.illegal = (i, j)
                    return
    
    def reset(self):
        self.row, self.col = self.start
                
    @property
    def pos(self) -> tuple[int, int]:
        return (self.row, self.col)

    def get_char(self) -> str:
        return self.chars[self.row][self.col]

    def operate(self, seq: str) -> str:
        out = ""
        for char in seq:
            match char:
                case "A":
                    out += self.get_char()
                case "^":
                    self.row -= 1
                case "v":
                    self.row += 1
                case "<":
                    self.col -= 1
                case ">":
                    self.col += 1
            if self.pos == self.illegal:
                raise RuntimeError("Illegal position")
        return out
    
    def print(self, char: str) -> str:
        out = ""
        for row, keyboard_row in enumerate(self.chars):
            if char in keyboard_row:
                break
        col = keyboard_row.index(char)
        drow = row - self.row
        dcol = col - self.col
        # Choose the order which will avoid the illegal pos
        i, j = self.illegal
        if self.col == j and row == i:
            out += "<" * abs(dcol) if dcol < 0 else ">" * abs(dcol)
            out += "^" * abs(drow) if drow < 0 else "v" * abs(drow)
        elif self.row == i and col == j:
            out += "^" * abs(drow) if drow < 0 else "v" * abs(drow)
            out += "<" * abs(dcol) if dcol < 0 else ">" * abs(dcol)
        elif drow == 0 and dcol != 0:
            out += "<" * abs(dcol) if dcol < 0 else ">" * abs(dcol)
        elif dcol == 0 and drow != 0:
            out += "^" * abs(drow) if drow < 0 else "v" * abs(drow)
        elif drow == dcol == 0:
            pass
        else:
            choice = choices.pop()
            if choice is None:
                choice = False
            else:
                print(f"{choice} {self.pos}, {drow = }, {dcol = }, {row, col}, {self.illegal}")
            if choice:
                out += "<" * abs(dcol) if dcol < 0 else ">" * abs(dcol)
                out += "^" * abs(drow) if drow < 0 else "v" * abs(drow)
            else:
                out += "^" * abs(drow) if drow < 0 else "v" * abs(drow)
                out += "<" * abs(dcol) if dcol < 0 else ">" * abs(dcol)
        if drow == dcol == 1:
            print(f"None {self.pos}, {drow = }, {dcol = }, {row, col}, {self.illegal}")

        out += "A"
        assert char == self.operate(out)
        return out

    def reverse_operate(self, seq: str) -> str:
        out = ""
        for char in seq:
            out += self.print(char)
        return out
    
    @classmethod
    def numpad(cls) -> "Keyboard":
        return cls((3, 2), ["789", "456", "123", " 0A"])
    
    @classmethod
    def keypad(cls) -> "Keyboard":
        return Keyboard((0, 2), [" ^A", "<v>"])

def chain_keyboards(keyboards: list[Keyboard], seq: str) -> str:
    for keyboard in keyboards:
        seq = keyboard.operate(seq)
    return seq

def reverse_chain_keyboards(keyboards: list[Keyboard], seq: str) -> str:
    for keyboard in reversed(keyboards):
        keyboard.reset()
        seq = keyboard.reverse_operate(seq)
    return seq

def test():
    a = Keyboard.keypad()
    b = Keyboard.keypad()
    n = Keyboard.numpad()

    x = b.operate("v<<A>>^Av<A<A>>^AAvAA^<A>Av<A>^A<A>Av<A^>A<Av<A>>^AAvA^Av<<A>A>^AAA<Av>A^A")
    y = a.operate(x)
    print(x)
    print(y)
    print(n.operate(y))
    
def main():
    seqs = [
        "129A",
        "540A",
        "789A",
        "596A",
        "582A",
    ]
    # seqs = ["029A","980A","179A","456A","379A",]

    numpad = Keyboard.numpad()
    keypad_1 = Keyboard.keypad()
    keypad_2 = Keyboard.keypad()
    keyboards = [keypad_2, keypad_1, numpad]

    t = float("inf")
    for _ in range(1000):
        print("\n"*10)
        s = 0
        out = ""
        for seq in seqs:
            rs = reverse_chain_keyboards(keyboards, seq)
            out += f"{seq}, {rs}\n"
            s += int(seq[:-1]) * len(rs)
        print(t, s)
        t = min(t, s)
        if s == t:
            print(out)
        if t == 184180:
            break
    print(t)
    return
    keyboards = [Keyboard.keypad() for _ in range(25)] + [Keyboard.numpad()]

    t = float("inf")
    for _ in range(1000):
        s = 0
        for seq in seqs:
            rs = reverse_chain_keyboards(keyboards, seq)
            # print(seq, rs)
            s += int(seq[:-1]) * len(rs)
        print(t, s)
        t = min(t, s)
    print(t)
    

if __name__ == "__main__":
    # test()
    main() # ans < 186508
