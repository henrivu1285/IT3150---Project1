import heapq
import os

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
    
    def compress(self):
        filename,file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'r+',encoding='utf-8') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip() #loại bỏ kí tự xuống dòng + khoảng trắng

            frequency = self.make_frequency(text)
            self.make_node_heap(frequency)
            self.merge_node()
            self.code_generation()

            encoded_text = self.get_encoded(text)
            pad_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.byte_array(pad_encoded_text)
            output.write(bytes(b))

        print("Đã nén")
        return output_path

#Phần giải nén file
    def remove_padding(self, pad_encoded_text): #Hàm loại bỏ phần bổ sung(bổ sung ở pad_encoded_text)
        pad_info = pad_encoded_text[:8]
        extra_padding = int(pad_info, 2)
        pad_encoded_text = pad_encoded_text[8:]
        encoded_text = pad_encoded_text[:-1*extra_padding]

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
            bit_string = ""

            byte = file.read(1)
            while(len(byte)>0):# Hàm để đọc từng byte và chai về 9 bit
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8,'0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

            print("Đã giải nén")
            return output_path
        

        
        
    

       
        

             
             
             
             
