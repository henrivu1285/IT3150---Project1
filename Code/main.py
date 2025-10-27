from huffman import Huffman
import sys

path = "D:\\Project 1\\BTL\\Code\\example.txt"

run = Huffman(path)

output_path = run.compress()
print("File da nen la " + output_path)

decompressed_path = run.decompress(output_path)
print("File da giai nen la " + decompressed_path)