from huffman import Huffman
import sys

path = "D:\\Project 1\\BTL\\Code\\example.txt"
path2 = "D:\\Project 1\\BTL\\Code\\example2.txt"
run = Huffman(path2)

output_path = run.compress()
print("File da nen la " + output_path)

decompressed_path = run.decompress(output_path)
print("File da giai nen la " + decompressed_path)