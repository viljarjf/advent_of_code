from dataclasses import dataclass, field
from enum import Enum


class Signal(Enum):
    LOW = 1
    HIGH = 0
    UNINITIALIZED = -1


@dataclass
class Module:
    name: str
    signal: Signal = Signal.UNINITIALIZED
    outputs: list["Module"] = field(default_factory=list)
    receive_high_count = 0
    receive_low_count = 0

    def forward_link(self, other: "Module") -> None:
        self.outputs.append(other)
        other.register_reverse_link(self)
    
    def register_reverse_link(self, other: "Module"):
        pass

    def receive(self, signal: Signal, name: str) -> None:
        if signal == Signal.HIGH:
            self.receive_high_count += 1
        elif signal == Signal.LOW:
            self.receive_low_count += 1

    def send(self) -> list["Module"]:
        """Returns the modules that received a pulse"""
        for module in self.outputs:
            # print(self.name, "sends", self.signal.name, "to", module.name)
            module.receive(self.signal, self.name)
        return self.outputs

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, value: object) -> bool:
        return self.name == value.name
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, signal={self.signal.name}, outputs=({", ".join(m.name for m in self.outputs)}))"

@dataclass
class Button(Module):
    signal: Signal = Signal.LOW


class Broadcaster(Module):
    def receive(self, signal: Signal, name: str) -> None:
        self.signal = signal
        super().receive(signal, name)

@dataclass
class FlipFlop(Module):
    was_flipped: bool = False
    signal: Signal = Signal.LOW

    def receive(self, signal: Signal, name: str) -> None:
        if signal == Signal.LOW:
            # Flip state
            if self.signal == Signal.LOW:
                self.signal = Signal.HIGH
            else:
                self.signal = Signal.LOW
            self.was_flipped = True
        super().receive(signal, name)

    def send(self):
        if self.was_flipped:
            self.was_flipped = not self.was_flipped
            return super().send()
        return []

@dataclass
class Conjunction(Module):
    inputs: dict[str, Signal] = field(default_factory=dict)
    signal: Signal = Signal.LOW

    def receive(self, signal: Signal, name: str) -> None:
        self.inputs[name] = signal
        if all(signal == Signal.HIGH for signal in self.inputs.values()):
            self.signal = Signal.LOW
        else:
            self.signal = Signal.HIGH
        super().receive(signal, name)
    
    def register_reverse_link(self, other: Module):
        self.inputs[other.name] = Signal.LOW


def parse_input(filename: str) -> list[Module]:
    modules = [Button("button")]
    outputs_list = [["broadcaster"]]

    with open(filename, "r") as f:
        for line in f:
            name, outputs = line.strip().split(" -> ")
            # Parse type
            if name[0] == "%":
                module = FlipFlop(name[1:])
            elif name[0] == "&":
                module = Conjunction(name[1:])
            elif name == "broadcaster":
                module = Broadcaster(name)
            else:
                module = Module(name)
            modules.append(module)
            # Parse outputs
            outputs_list.append(outputs.split(", "))
    modules_lookup = {module.name: module for module in modules}
    for module, outputs in zip(modules, outputs_list):
        for output in outputs:
            try:
                module.forward_link(modules_lookup[output])
            except KeyError:
                modules.append(Module(output))
                modules_lookup[output] = modules[-1]
                module.forward_link(modules_lookup[output])

    return modules


def push_the_button(modules: list[Module]):
    button = modules[0]

    queue: list[list[Module]] = [button.send()]
    while queue:
        modules = queue.pop(0)
        next_pulse = []
        for module in modules:
            np = module.send()
            next_pulse += np
        if next_pulse:
            queue.append(next_pulse)



def main():
    modules = parse_input("20")

    for m in modules:
        print(m)
    print("----------------")

    for _ in range(1000):
        push_the_button(modules)

    low_count = sum(m.receive_low_count for m in modules)
    high_count = sum(m.receive_high_count for m in modules)
    print(low_count, high_count)
    print(low_count * high_count)
    print("----------------")

    # Just manually traverse the flip flops and stuff
    modules = parse_input("20")

    mapping = {m.name: m for m in modules}

    all_req = [
                "kt",
                "mt",
                "zp",#
                "rc",#
                "hj",#
                "vc",
                "hf",#
                "nm",
                "dh",
                "mc",
                "lv",
                "tg", # 4003
            ] + [
                "rg",
                "vq",
                "bs",
                "sc",#
                "mv",
                "gl",#
                "kf",#
                "dx",#
                "ts",
                "ng",
                "lh",
                "dl", # 3863
            ] + [
                "xv",
                "nd",#
                "dg",
                "tm",#
                "mh",
                "mk",#
                "pb",#
                "tp",
                "pf",
                "mf",
                "gv",
                "km", # 3989
            ] + [
                "pd",
                "jp",
                "mx",
                "cl",#
                "hm",#
                "qb",
                "bf",
                "vx",#
                "ns",
                "pn",
                "cb",
                "tk", # 3943
            ]
    print(4003 * 3863 * 3989 * 3943)


if __name__ == "__main__":
    main()
