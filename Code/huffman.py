import heapq
import os
import pickle
from rle import RLE
from lz77 import LZ77

#Phần mã hóa Huffman
class Huffman:
    def __init__(self,path):
        self.path = path
        self.heap = []
        self.code = {}
        self.reverse ={}
    
    class HeapNode:
        def __init__(self,char,freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq
        
        def __equal__(self,other):
            if(other == None):
                return False
            if (not isinstance(other,HeapNode)):
                return False
            return self.freq == other.freq
        
    
    def make_frequency(self,text): #Hàm xác định số lần xuất hiện của ký tự
        frequency = {}
        for character in text:
          if not character in frequency:
            frequency[character] = 0
          frequency[character]+=1
        return frequency
    
    def make_node_heap(self,frequency): #Hàm chuyển số lần xuất hiện thành các node và đẩy vào heap
        for key in frequency:
            node = self.HeapNode(key,frequency[key])
            heapq.heappush(self.heap,node)

    def merge_node(self): #Lấy ra 2 phần tử có số lần suất hiện ít nhất và tạo node cha mới
        while(len(self.heap)>1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merge = self.HeapNode(None,node1.freq + node2.freq)
            merge.left = node1
            merge.right = node2
            heapq.heappush(self.heap,merge)
    
    def tree_traversal(self,root,current_code): #Hàm đệ quy để duyệt cây, sinh bit
        if(root == None):
           return
        if(root.char != None):
           self.code[root.char] = current_code
           self.reverse[current_code] = root.char
           return
        
        self.tree_traversal(root.left, current_code + "0")
        self.tree_traversal(root.right,current_code + "1")

#Phần nén file
    
    def code_generation(self): #tạo ra chuỗi bit
        root = heapq.heappop(self.heap)
        current_code = ""
        self.tree_traversal(root, current_code)

    def get_encoded(self,text): #hàm nối xâu
        encoded_text = ""
        for character in text:
             encoded_text+= self.code[character]
        return encoded_text
    
    def pad_encoded_text(self,encoded_text): #Bổ sung xâu bội số của 8 để ghép file
        extra_padding = 8-len(encoded_text)%8
        for i in range(extra_padding):
            encoded_text += "0"
        pad_info = "{0:08b}".format(extra_padding)
        encoded_text = pad_info + encoded_text
        return encoded_text
    
    def byte_array(self, pad_encode_text): #Chuyển thành mảng byte để ghi file
        if(len(pad_encode_text)%8 != 0):
            exit(0)
        
        b = bytearray()
        for i in range(0,len(pad_encode_text),8):
            byte = pad_encode_text[i:i+8]
            b.append(int(byte,2))
        
        return b
    
    def compress(self, mode="NORMAL"):
        filename,file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'r+',encoding='utf-8') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip() #loại bỏ kí tự xuống dòng + khoảng trắng
            if mode == "RLE":

                text = RLE.encode(text)
            elif mode == "LZ77":
                lz = LZ77()
                text = lz.encode(text)

            frequency = self.make_frequency(text)
            self.make_node_heap(frequency)
            self.merge_node()
            self.code_generation()

            encoded_text = self.get_encoded(text)
            pad_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.byte_array(pad_encoded_text)
            #Tạo Header chứa: Bảng tần suất + Cờ xác nhận có dùng RLE không
            header_info = {
                "freq": frequency,
                "mode": mode
            }
            header_data = pickle.dumps(header_info)
            
            # Ghi độ dài header (4 byte) + header + dữ liệu nén
            output.write(len(header_data).to_bytes(4, 'big'))
            output.write(header_data)

            output.write(bytes(b))

        print("Đã nén")
        return output_path

#Phần giải nén file
    def remove_padding(self, pad_encoded_text): #Hàm loại bỏ phần bổ sung(bổ sung ở pad_encoded_text)
        pad_info = pad_encoded_text[:8]
        extra_padding = int(pad_info, 2)
        pad_encoded_text = pad_encoded_text[8:]
        if extra_padding > 0:
           encoded_text = pad_encoded_text[:-1*extra_padding]
        else: encoded_text = pad_encoded_text

        return encoded_text
    
    def decode_text(self,encoded_text): #Hàm chuyển bit thành kí tự
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse):
                character = self.reverse[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text
    
    def decompress(self, input): #quá trình giải mã
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input, 'rb') as file, open(output_path, 'w', encoding='utf-8') as output:
            # 1. Đọc Header
            header_len_data = file.read(4)
            if not header_len_data: return ""
            header_len = int.from_bytes(header_len_data, 'big')
            
            header_data = file.read(header_len)
            header_info = pickle.loads(header_data)
            
            # Lấy thông tin từ header
            frequency = header_info["freq"]
            mode = header_info.get("mode", "NORMAL")

            # Tái tạo cây Huffman
            self.heap = []
            self.code = {}
            self.reverse = {}
            self.make_node_heap(frequency)
            self.merge_node()
            self.code_generation()

            bit_string = ""
            byte = file.read(1)
            while(len(byte)>0):# Hàm để đọc từng byte và chia về 8 bit
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8,'0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decoded_text = self.decode_text(encoded_text) 

            if mode == "RLE":
                    print("Phát hiện RLE, đang giải mã...")
                    decoded_text = RLE.decode(decoded_text)
            elif mode == "LZ77":
                    print("Phát hiện LZ77, đang giải mã...")
                    lz = LZ77()
                    decoded_text = lz.decode(decoded_text)

            output.write(decoded_text)

            print("Đã giải nén")
            return output_path
        

        
        
    

       
        

             
             
             
             
