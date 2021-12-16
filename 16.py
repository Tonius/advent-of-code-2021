from dataclasses import dataclass
from math import prod
from operator import eq, gt, lt
from typing import Callable, Generator


@dataclass
class Packet:
    version: int
    length: int

    @classmethod
    def read(cls, data: str) -> "Packet":
        version = int(data[:3], 2)
        type_id = int(data[3:6], 2)

        if type_id == 4:
            return LiteralValue.read(version, data)

        return Operator.read(version, type_id, data)

    def get_version_sum(self) -> int:
        return self.version

    def get_value(self) -> int:
        raise NotImplementedError


@dataclass
class LiteralValue(Packet):
    value: int

    @classmethod
    def read(cls, version: int, data: str):
        binary_value = ""

        offset = 6
        current_group = None

        while current_group is None or current_group[0] == "1":
            current_group = data[offset : offset + 5]
            binary_value += current_group[1:]
            offset += 5

        return cls(version, offset, int(binary_value, 2))

    def get_value(self):
        return self.value


@dataclass
class Operator(Packet):
    type_id: int
    subpackets: list[Packet]

    @classmethod
    def read(cls, version: int, type_id: int, data: str):
        packet_length = 7
        subpackets = []

        length_type_id = data[6:7]
        read_length = 0

        if length_type_id == "0":
            packet_length += 15

            total_length = int(data[7:22], 2)

            while read_length < total_length:
                subpacket = Packet.read(data[22 + read_length :])
                subpackets.append(subpacket)
                read_length += subpacket.length

        elif length_type_id == "1":
            packet_length += 11

            total_count = int(data[7:18], 2)

            while len(subpackets) < total_count:
                subpacket = Packet.read(data[18 + read_length :])
                subpackets.append(subpacket)
                read_length += subpacket.length

        packet_length += read_length

        return cls(version, packet_length, type_id, subpackets)

    def get_version_sum(self):
        return super().get_version_sum() + sum(
            p.get_version_sum() for p in self.subpackets
        )

    def get_value(self):
        if self.type_id == 0:
            return self.aggregate(sum)
        elif self.type_id == 1:
            return self.aggregate(prod)
        elif self.type_id == 2:
            return self.aggregate(min)
        elif self.type_id == 3:
            return self.aggregate(max)
        elif self.type_id == 5:
            return self.compare(gt)
        elif self.type_id == 6:
            return self.compare(lt)
        elif self.type_id == 7:
            return self.compare(eq)

    def aggregate(self, function: Callable[[Generator[int, None, None]], int]):
        return function(p.get_value() for p in self.subpackets)

    def compare(self, operator: Callable[[int, int], bool]):
        if operator(self.subpackets[0].get_value(), self.subpackets[1].get_value()):
            return 1
        else:
            return 0


def hex_to_binary(number: str):
    return f"{int(number, 16):>04b}"


with open("16-input.txt") as input_file:
    message = "".join([hex_to_binary(number) for number in input_file.read().strip()])


print("\npart 1")

root_packet = Packet.read(message)

print(f"Version sum: {root_packet.get_version_sum()}")


print("\npart 2")
print(f"Result: {root_packet.get_value()}")
