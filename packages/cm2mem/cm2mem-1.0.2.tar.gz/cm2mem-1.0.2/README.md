# cm2mem

To use, initialize a Memory instance. Use massive=False if you're using a ``MassMemory`` and not a ``MassiveMemory``.
Use the Memory class as if it were an array, for example: ``print(mem[123])`` or ``mem[123] = 255``.
You can also use binary strings as indexes and values, for example: ``print(mem['00000011'])`` or ``mem['0b00000011'] = '00000001'``

To initialize a Memory object from pre-existing data (data you copied from a Memory ingame), use ``Util.load(data)``. (This will automatically determine the type of memory aswell)

You can use the various functions under the ``Premade`` class to (quickly) write values to a ``MassiveMemory`` that allow you to use the ``MassiveMemory`` as a multiplier, adder, etc..
``Premade`` usage example: 
```
from cm2mem import *
mem = Memory()
Premade.multiplier(mem)
print(mem.pack())
```
**The functions under the ``Premade`` class ONLY work with ``MassiveMemory``**

You can find a couple utility functions under the ``Util`` class.

If you need help with anything, feel free to DM me on Discord @animepfp

May break if memory in Circuit Maker 2 is modified. (DM me if that happens, or if you find a bug)