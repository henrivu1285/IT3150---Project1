class RLE:
    def encode(text):
        if not text:
            return ""
        encoded_str = ""
        count = 1
        SEPARATOR = '*'
        for i in range (1,len(text)):
            if text[i] == text[i-1]:
                count += 1
            else:
                encoded_str += str(count) + SEPARATOR+ text[i-1] 
                count = 1
        encoded_str += str(count) + text[-1]
        return encoded_str
    
    def decode(text):
        decoded_str = ""
        i = 0
        SEPARATOR = '*'
        while i <len(text):
            count_str = ""
            while i<len(text) and text[i]!= SEPARATOR:
                count_str += text[i]
                i += 1
            if not count_str or i >= len(text):
                break
            i += 1
            try:
                count = int(count_str)
            except ValueError:
                # Nếu file lỗi, bỏ qua cụm này
                if i < len(text): i += 1
                continue
            if i<len(text):
                char=text[i]
                decoded_str+= char * count
                i += 1
        return decoded_str
    