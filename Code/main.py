from huffman import Huffman
import sys

path = "D:\\Project 1\\BTL\\Code\\example.txt"

run = Huffman(path)

output_path = run.compress()
print("File da nen la " + output_path)