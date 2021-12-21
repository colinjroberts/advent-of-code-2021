from tools import (get_csv_line_input_as_list, get_line_input_as_list)

"""
Started writing this as a Packet class that would have some interpretation methods,
but the further I get, the more I want to have a sliding reader/state machine approach.

Really, that ended up just turning into a big single method that does all of the processing.
"""


class PacketReader:
    """Sets up a packet to be ready by converting from hex to binary
    """

    def __init__(self, input_as_string_of_hex, debug=False):
        self.debug = debug
        self.packet_version_numbers = []
        self.hex_data = input_as_string_of_hex
        self.binary_data = self.convert_input_to_binary()
        self.packet_total_length = len(self.binary_data)
        self.current_digit = 0
        self.end_at_length = [] # for ending operator packets with length_id 0
        self.operator_lookup = {
            0: "sum",
            1: "product",
            2: "min",
            3: "max",
            5: "gt",
            6: "lt",
            7: "eq",
        }

        if self.debug:
            print(f"============================")
            print(f"Initializing Packet Reader")
            print(f"============================")
            print(f"{self.hex_data=}")
            print(f"{self.binary_data=}")

    def parse_packet(self, depth=0):
        """Runs through a whole packet and sums version numbers for part 1 and performs the operations for part 2.

        General structure is as follows:
        - Check version number
        - Check id number
        - If it's a literal packet, get and return the number
        - Otherwise it is an operator packet:
            - Get length version (next bit)
            - if 0:
                - make note of how long the subpackets are, and until that length is reached
                  get subpackets and add their result to a list
                - when no more subpackets, return the operation over the subpackets
            - else it's 1:
                - for each subpacket, add the value of the subpacket to a list
                - when no more subpackets, return the operation over the subpackets
        """

        if self.debug and depth != 0:
            print(f"---------------")
            print(f"{depth=}, {self.current_digit=} of {len(self.binary_data)=}")
            print(f"---------------")

        # Check first three numbers for version number
        packet_version = self.get_next_numbers(3)
        if self.debug: print(f"{packet_version=}, {int(packet_version, 2)}")
        self.packet_version_numbers.append(int(packet_version, 2)) # part 1

        # Check second three numbers for id number
        packet_id = self.get_next_numbers(3)

        # Literal packet
        if packet_id == "100":
            if self.debug: print(f"{packet_id=}, {int(packet_id, 2)}, literal, on {self.current_digit=}")

            # Loop until the last literal byte is found
            literal_packet_value = ""
            literal_byte_type = self.get_next_numbers()
            while literal_byte_type == "1":
                if self.debug: print(f"Literal byte 1 found at position {self.current_digit-1=}")
                literal_packet_value += self.get_next_numbers(4)
                literal_byte_type = self.get_next_numbers()

            if self.debug: print(f"Literal byte 0 found at position {self.current_digit-1=}")
            literal_packet_value += self.get_next_numbers(4)
            if self.debug: print(f"{literal_packet_value=}, {int(literal_packet_value, 2)}")

            return int(literal_packet_value, 2)

        # Operator packet
        else:
            if self.debug:
                print(f"{packet_id=}, {int(packet_id, 2)}, operator {self.operator_lookup[int(packet_id, 2)]}")

            # Check next number
            packet_length_id = self.get_next_numbers(1)
            if self.debug: print(f"{packet_length_id=}, {int(packet_length_id, 2)}")

            # If 0:
            if packet_length_id == '0':
                if self.debug: print("operator - 0")

                length_of_all_contained_subpackets = self.get_next_numbers(15)
                if self.debug: print(
                    f"{length_of_all_contained_subpackets=}, {int(length_of_all_contained_subpackets, 2)}")

                # next 15 bits are length of all subpackets
                # In this case, I know where the last subpacket ends
                # start processing new subpackets until end is reached
                # I think I can just call this method again
                self.end_at_length.append(self.current_digit + int(length_of_all_contained_subpackets, 2))
                if self.debug: print(f"{self.end_at_length=} while {self.current_digit=}")

                sub_packets = []

                while self.current_digit < self.end_at_length[len(self.end_at_length) - 1]:
                    sub_packets.append(self.parse_packet(depth + 1))
                self.end_at_length.pop()
                if self.debug: print(f"Ended at length {self.current_digit=} with {self.end_at_length=}")

                if self.debug:
                    print(f"Performing operation {self.operator_lookup[int(packet_id, 2)]} on subpackets: {sub_packets}")

                return self.perform_operation(self.operator_lookup[int(packet_id, 2)], sub_packets)

            # If 1:
            else:
                if self.debug: print("operator - 1")
                count_of_subpackets_to_follow = int(self.get_next_numbers(11), 2)
                if self.debug: print(f"{count_of_subpackets_to_follow=}")

                sub_packets = []
                # next 11 bits are the count of subpackets
                for i in range(count_of_subpackets_to_follow):
                    if self.debug: print(f"Investigating packet {i + 1}, of {count_of_subpackets_to_follow}:")
                    sub_packets.append(self.parse_packet(depth + 1))

                # In this case, I will know which packet I'm processing is the last one
                # start processing the subpackets until the last one is reached
                if self.debug:
                    print(f"Performing operation {self.operator_lookup[int(packet_id, 2)]} on subpackets: {sub_packets}")
                return self.perform_operation(self.operator_lookup[int(packet_id, 2)], sub_packets)

    def get_next_numbers(self, numbers_to_get=1):
        output = ""
        for i in range(numbers_to_get):
            output += self.binary_data[self.current_digit]
            self.current_digit += 1
        return output

    def convert_input_to_binary(self):
        output = []
        for item in self.hex_data:
            integer = int(item, 16)
            string_number = f"{integer:0>4b}"
            output.append(string_number)
        return "".join(output)

    def get_sum_of_version_numbers(self):
        return sum(self.packet_version_numbers)

    def perform_operation(self, operation, numbers):

        if operation == "sum":
            if self.debug: print(f"pushing {sum(numbers)=} to stack")
            return sum(numbers)

        elif operation == "product":
            result = 1
            num_list = [str(x) for x in numbers]
            result_explanation = "*".join(num_list)
            for number in numbers:
                result *= number
            if self.debug: print(f"pushing {result_explanation} {result=} to stack")
            return result

        elif operation == "min":
            if self.debug: print(f"pushing {min(numbers)=} to stack")
            return min(numbers)

        elif operation == "max":
            if self.debug: print(f"pushing {max(numbers)=} to stack")
            return max(numbers)

        elif operation == "gt":
            # Pretty sure these should be in the correct order
            if self.debug: print(f"pushing {int(numbers[0] > numbers[1])=} to the stack")
            return int(numbers[0] > numbers[1])

        elif operation == "lt":
            if self.debug: print(f"pushing {int(numbers[0] < numbers[1])=} to the stack")
            return int(numbers[0] < numbers[1])

        elif operation == "eq":
            if self.debug: print(f"pushing {int(numbers[-1] == numbers[-2])=} to the stack")
            return int(numbers[-1] == numbers[-2])


def part1(input_list, test=False, debug=False):
    if test:
        for i, item in enumerate(input_list):
            line = item.split("|")
            p = PacketReader(line[0], debug)
            result = p.parse_packet()
            print(p.get_sum_of_version_numbers())
    else:
        p = PacketReader(input_list[0], debug)
        result = p.parse_packet()
        return p.get_sum_of_version_numbers()


def part2(input_list, test=False, debug=False):
    if test:
        for i, item in enumerate(input_list):
            line = item.split("|")
            p = PacketReader(line[0], debug)
            result = p.parse_packet()
            print(result)
            print()

    else:
        p = PacketReader(input_list[0], debug)
        result = p.parse_packet()
        return result


def p16():
    filename = "inputs/16"
    ext = ".txt"
    input_list = get_line_input_as_list(filename + ext, "string")
    input_list_test = get_line_input_as_list(filename + "-test" + ext, "string")
    input_list_test2 = get_line_input_as_list(filename + "-test2" + ext, "string")

    # output1 = part1(input_list_test2, test=True, debug=True)
    output1 = part1(input_list, test=False, debug=False)
    # output2 = part2(input_list_test2, test=True, debug=False)
    output2 = part2(input_list, test=False, debug=False)

    return output1, output2
