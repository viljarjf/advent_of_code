from __future__ import annotations
from collections import defaultdict

CARDS = [
    "A",
    "K",
    "Q",
    "J",
    "T",
    "9",
    "8",
    "7",
    "6",
    "5",
    "4",
    "3",
    "2",
]
TYPES = [
    "Five of a kind",
    "Four of a kind",
    "Full house",
    "Three of a kind",
    "Two pairs",
    "One pair",
    "High card",
]

class Hand:
    def __init__(self, cards: str, bid: str) -> None:
        self.cardstr = cards
        self.cards = self._parse_cards()
        self.bid = int(bid.strip())
        self.hand_type = self._hand_type()

    def _parse_cards(self) -> dict[str, int]:
        out = defaultdict(lambda: 0)
        for card in self.cardstr.strip():
            out[card] += 1
        return out

    def _hand_type(self) -> int:
        cards = self.cards
        if any(cards[card] == 5 for card in cards):
            return 0
        if any(cards[card] == 4 for card in cards):
            return 1
        if any(cards[card] == 3 for card in cards):
            if any(cards[card] == 2 for card in cards):
                return 2
            return 3
        if list(cards.values()).count(2) == 2:
            return 4
        if any(cards[card] == 2 for card in cards):
            return 5
        return 6

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}:\n - {self.cardstr}\n - {TYPES[self.hand_type]}\n - bet: {self.bid}\n"

    def __gt__(self, other: Hand) -> bool:
        # first check type
        if self.hand_type == other.hand_type:
            # check cards
            for self_card, other_card in zip(self.cardstr, other.cardstr):
                if self_card == other_card:
                    continue
                else:
                    return CARDS.index(self_card) < CARDS.index(other_card)
        else:
            return self.hand_type < other.hand_type

    def __lt__(self, other: Hand) -> bool:
        return not self > other


class JokerHand(Hand):
    def _parse_cards(self) -> dict[str, int]:
        out = super()._parse_cards()

        if self.cardstr == "JJJJJ":
            return out

        # distribute jokers
        wildcards = out.pop("J", 0)
        max_key = max(out, key=out.get)
        out[max_key] += wildcards

        return out

def main():
    file = "07"

    with open(file, "r", encoding="utf-8") as inp:
        hands = [Hand(*line.split(" ")) for line in inp]
        hands.sort()
        if any(hands[i-1] > hands[i] for i in range(1, len(hands))):
            return

        winnings = sum(h.bid * (i + 1) for i, h in enumerate(hands))
        print(winnings)


    with open(file, "r", encoding="utf-8") as inp:
        global CARDS
        CARDS.append(CARDS.pop(CARDS.index("J")))
        hands = [JokerHand(*line.split(" ")) for line in inp]
        hands.sort()
        if any(hands[i-1] > hands[i] for i in range(1, len(hands))):
            return
        [print(h) if "J" in h.cardstr else 0 for h in hands[400:500]]

        winnings = sum(h.bid * (i + 1) for i, h in enumerate(hands))
        print(winnings)


if __name__ == "__main__":
    main()
