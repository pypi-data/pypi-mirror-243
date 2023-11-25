# Documentation

## Links

### Github Gist
[https://gist.github.com/Hawkking-cloud/f7d694541421b6d6cf88ce4e1d3d8844](https://gist.github.com/Hawkking-cloud/f7d694541421b6d6cf88ce4e1d3d8844)

## Block Part Numbers

Can also used as the capitalized or uncapitalized version  (e.g., `createBlock(0,0,0,'nor')`)
- 0: NOR
- 1: AND
- 2: OR
- 3: XOR
- 4: Input
- 5: FLIPFLOP
- 6: LED
- 7: Sound
- 8: Conductor
- 10: NAND
- 11: XNOR
- 12: Random
- 13: Letter
- 14: Tile

## Functions

### `finish()`
Call after making all your blocks, finalizes and formats it into a string and pastes it.

### `text_to_hexadecimal(text)`
Converts ASCII text to hexadecimal for the sign.

### `xyztoindex(x, y, z)`
Takes an XYZ coordinate. If there's a block there, it gets the index of it. Mainly used in wires.

### `createBlock(x, y, z, part, specialparams)`
- Part: Block part ID.
- Special Params (optional): Used in special blocks like LED, sound blocks, etc. RGB values are defined by arrays, e.g., r:255, g:0, b:0 → [255, 0, 0].
- Letter blocks can be entered as single letter characters (e.g., `createBlock(0,0,0,13,'A')`)
- 

### `createWire(start_x, start_y, start_z, end_x, end_y, end_z)`
Adds wires using two XYZ inputs.

### `createWireIndex(index1, index2)`
Adds wires using two index inputs.

### `number_to_binary(num, numofbits)`
Turns a number into binary.

### `import_build(input_string, offset_x, offset_y, offset_z)`
Puts a registry string into the build. Offsets are not mandatory.

### `createBlockCustom(string)`
Allows you to input a string like `7,0,0,0,0,1234.00` directly into the parts.

### `cube(x1, y1, z1, x2, y2, z2, part, specialparams)`
Creates an array of blocks based on two 3D points. Special params are not mandatory.

### `createCustomBuilding(Type, x, y, z, rotX, rotY, rotZ, value)`
Creates a custom building. Valid types: Sign, Door, Graph, MassiveMemory, MassMemory, KeyInput, QwertyKeyInput.

### `ascii_to_number(char)`
Converts a single character to ascii number, for letter block

### `getString()`
Returns the formatted string of blocks. (Won't work unless used after `finish()`)

### `getBlocks()`
Returns the unformatted list of blocks.

### `getConnections()`
Returns the unformatted index list of connections.

### `getBuilds()`
Returns the unformatted list of builds.

### `getBuildvalues()`
Returns the unformatted list of builds values.

### `getIndex()`
Returns the current block index, (e.g., `print(getIndex()) createBlock(0,0,0,5) print(getIndex())`)

### `getIndex()`
Returns the current block index, (e.g., `print(getIndex()) createBlock(0,0,0,5) print(getIndex())`)

### `getIndex()`
Returns the current block index, (e.g., `print(getIndex()) createBlock(0,0,0,5) print(getIndex())`)
