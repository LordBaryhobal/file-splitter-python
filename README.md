# File Splitter

The script in this repository allow to split a file into multiple random files. Combining all the files using the joiner script can then create back the original file.

There are several version of the algorithm used to "encrypt" and split the files:

### Version 1:

1. When encoding data A, bytes are first grouped by 4 to make 32-bit words. Padding bytes are added first to ensure a multiple of 4.
2. A random byte-array B of the same size is generated.
3. The two are XORed resulting in byte-array C.
4. Every other byte is switched between B and C.
5. The process is repeated on B and C a number of time (depth)
6. The resulting byte-arrays are saved in separate files

The reverse process is used to rebuild the original data.

### Version 2:

Improved version of the scripts using `numpy`.

### Version 3:

The algorithm is very similar, but instead of repeating the process systematically on all the arrays (step 5), a random binary tree is built first deciding which array is further split. A seed is thus needed to reliably re-join the files, adding a supplementary layer of security.

When all the splits have been applied, the "leaves" of the tree are saved to files in order (from left to right). If the files are renamed in a way that the numerical order is broken, then the joiner script will not be able to recover the original data.

## Requirements:

- Python 3 or higher
- Python modules: `numpy` (for V2+)

## Warning:

There is **no security** put in place to limit the amount of data that is output. Be very careful when **splitting large files** or when **changing the `depth` argument**.

For versions 1 and 2, the number of files generated is equal to `2 ^ depth`, and for version 3 it is equal to the argument `n` of the `split` function.

Each file will contain as much data as the original file.

### Example 1 (with version 1/2):
- Input file size: `400 kB`
- Depth: `15`
- Total output size: `> 13 GB`

### Example 2 (with version 1/2):
- Input file size: `35 MB`
- Depth: `15`
- Total output size: **`> 1 TB`**