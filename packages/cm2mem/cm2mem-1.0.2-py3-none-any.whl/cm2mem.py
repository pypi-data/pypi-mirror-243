from string import ascii_lowercase, ascii_uppercase, digits



class Util:
    """Contains various utility functions."""
    def pbin(num : int, width=4):
        """Turns a number into string form, then pads it to the specified amount of bits. Ex: pbin(1,4) -> '0001'"""
        if isinstance(num, str):
            num = int(num)
        binary_str = bin(num)[2:]
        padded_str = binary_str.zfill(width)
        return padded_str

    def decode(encoded_data : str):
        """Decodes MassiveMemory strings into a list of bytes."""
        alphabet = ascii_uppercase + ascii_lowercase + digits + "+/"
        outp = [encoded_data[i:i + 3] for i in range(0, len(encoded_data), 3)]
        outb = []
        for i in outp:
            bits = 0
            for c in i[::-1]:
                bits = bits + alphabet.index(c)
                bits <<= 6
            bits >>= 6
            outb.append(bits)
        return outb
    def load(data : str):
        """Returns a Memory object, with 'data' loaded into it. Intended ONLY for loading data copied directly from a MassiveMemory or MassMemory."""
        massive = len(data) == 12288
        if massive:
            raw = Util.decode(data)
            for i in range(4096-len(raw)):
                raw.append(0)
            mem = Memory(massive=True)
            mem.raw = raw
            return mem
        else:
            outp = [data[i:i + 2] for i in range(0, len(data), 2)]
            raw = []
            for i in outp:
                raw.append(int('0x'+i.lower(),16))
            for i in range(4096-len(raw)):
                raw.append(0)
            mem = Memory(massive=False)
            mem.raw = raw
            return mem
class Memory:
    raw = []
    """The raw data in the memory. It is not recommended to use this directly."""
    massive = True
    """Whether the memory is a MassiveMemory or not. True unless set to False when initialized."""
    def __init__(self,massive : bool=True) -> None:
        """Creates a Memory instance. Use massive=False if you're using/going to use a MassMemory instead of a MassiveMemory."""
        for i in range(4096):
            self.raw.append(0)
        self.massive = massive
        return

    def load_raw(self, data : list) -> None:
        """Loads a list of bytes into this Memory object."""
        if self.massive:
            idx = 0
            for i in data:
                if i > 65535:
                    raise Exception(f"Only 16-bit (or less) integers are allowed in a MassiveMemory [At byte #{idx}, byte = {i}]")
                idx += 1
        else:
            idx = 0
            for i in data:
                if i > 255:
                    raise Exception(f"Only 8-bit (or less) integers are allowed in a MassMemory [At byte #{idx}, byte = {i}]")
                idx += 1

        self.raw = data
    def pack(self) -> str: 
        """Packs your code into a string to be pasted into a memory."""
        if self.massive:
            alphabet = ascii_uppercase + ascii_lowercase + digits + "+/"

            instructions = ""
            for i in self.raw:
                hx = hex(i)[2:]
                instructions += ("0"*(4-len(hx))) + hx + " "
            instructions = instructions[:-1]
            instruction_bytes = bytes.fromhex(instructions)

            output = ""
            for b1, b2 in zip(instruction_bytes[::2], instruction_bytes[1::2]):
                bits = b1 << 8 | b2
                for _ in range(3):
                    output += alphabet[bits & 0x3f]
                    bits >>= 6
            return output + ("A" * (12288-len(output)))
        else:
            rawout = ""
            for i in self.raw:
                hx = hex(i)[2:]
                rawout += ("0"*(2-len(hx))) + hx
            return rawout.upper()
    def __getitem__(self, key : str or int):
        if isinstance(key,str):
            if key.startswith('0b'):
                key = key[2:]
            key = int(key,2)
        if key > 4095:
            raise Exception("Key must not be greater than 4095.")
        return self.raw[key]
    def __setitem__(self, key : str or int, value : str or int):
        if isinstance(key,str):
            if key.startswith('0b'):
                key = key[2:]
            key = int(key,2)
        if isinstance(value,str):
            if value.startswith('0b'):
                value = value[2:]
            value = int(value,2)
        if self.massive:
            if value > 65535:
                raise Exception("Value must not be greater than 65535 for a MassiveMemory.")
        else:
            if value > 255:
                raise Exception("Value must not be greater than 255 for a MassMemory.")
        self.raw[key] = value

class Premade:
    """Functions to load pre-made 'programs' to a Memory instance, allowing you to do subtraction, addition, etc.. using a MassiveMemory."""
    def divider(mem_instance : Memory) -> None:
        """6-bit divider (0 / 0 = 0). Outputs are rounded."""
        if not mem_instance.massive:
            raise Exception("Memory is not a MassiveMemory")
        fp = mem_instance
        for i in range(4096):
            param1 = (i & 0b111111000000)>>6
            param2 = (i & 0b000000111111)
            if param2 == 0:
                fp[i] = 0
            else:
                fp[i] = int(round(param1/param2))

    def multiplier(mem_instance : Memory) -> None:
        """6-bit multiplier."""
        if not mem_instance.massive:
            raise Exception("Memory is not a MassiveMemory")
        fp = mem_instance
        for i in range(4096):
            param1 = (i & 0b111111000000)>>6
            param2 = (i & 0b000000111111)
            fp[i] = param1*param2

    def adder(mem_instance : Memory) -> None:
        """6-bit adder."""
        if not mem_instance.massive:
            raise Exception("Memory is not a MassiveMemory")
        fp = mem_instance
        for i in range(4096):
            param1 = (i & 0b111111000000)>>6
            param2 = (i & 0b000000111111)
            fp[i] = param1+param2
        
    def subtractor(mem_instance : Memory) -> None:
        """6-bit subtractor (any result below 0 just outputs 0)."""
        if not mem_instance.massive:
            raise Exception("Memory is not a MassiveMemory")
        fp = mem_instance
        for i in range(4096):
            param1 = (i & 0b111111000000)>>6
            param2 = (i & 0b000000111111)
            if param1-param2 < 0:
                fp[i] = 0
            else:
                fp[i] = param1-param2

    def displaydriver(mem_instance : Memory) -> None:
        """For a 4 digit seven segment display (displays the number fed into the input). Outputs 4 4-bit numbers, each being a digit of the number to display."""
        if not mem_instance.massive:
            raise Exception("Memory is not a MassiveMemory")
        fp = mem_instance
        for i in range(4096):
            st = ('0' * (4-len(str(i)))) + str(i)
            fp[i] = Util.pbin(st[3]) + Util.pbin(st[2]) + Util.pbin(st[1]) + Util.pbin(st[0])
