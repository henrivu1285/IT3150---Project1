class LZ77:
    def __init__(self, window_size=4096):
        self.window_size = window_size

    def encode(self, data):
        if not data:
            return ""
            
        encoded_data = []
        i = 0
        n = len(data)
        SEPARATOR = '|' 
        
        while i < n:
            match_dist = 0
            match_len = 0
            start_search = max(0, i - self.window_size)
            search_buffer = data[start_search:i]
            
            # Tìm chuỗi khớp dài nhất
            for length in range(1, min(n - i, 255)): 
                substring = data[i : i + length]
                pos = search_buffer.rfind(substring)
                if pos != -1:
                    match_dist = len(search_buffer) - pos
                    match_len = length
                else:
                    break
            
            if match_len >= 3:
                if i + match_len < n:
                    next_char = data[i + match_len]
                    if next_char == '~': next_char = 'TILDE'
                    if next_char == '|': next_char = 'PIPE'
                    
                    token = f"~{match_dist}{SEPARATOR}{match_len}{SEPARATOR}{next_char}~"
                    encoded_data.append(token)
                    i += match_len + 1
                else:
                    token = f"~{match_dist}{SEPARATOR}{match_len}{SEPARATOR} ~" 
                    encoded_data.append(token)
                    i += match_len
            else:
                # Ký tự thường (Literal)
                char = data[i]
                if char == '~':
                    encoded_data.append("~~")
                else:
                    encoded_data.append(char)
                i += 1
                
        return "".join(encoded_data)

    def decode(self, data):
        decoded_data = []
        i = 0
        n = len(data)
        SEPARATOR = '|'
        
        while i < n:
            # Nếu gặp dấu hiệu bắt đầu token
            if data[i] == '~':
                # Kiểm tra escape '~~' -> trả về '~'
                if i + 1 < n and data[i+1] == '~':
                    decoded_data.append('~')
                    i += 2
                    continue
                
                # Tìm dấu kết thúc token
                end_token = data.find('~', i + 1)
                if end_token != -1:
                    token_content = data[i+1 : end_token]
                    try:
                        # Cắt chuỗi 
                        parts = token_content.split(SEPARATOR)
                        if len(parts) >= 3: 
                            dist = int(parts[0])
                            length = int(parts[1])
                            # Phần char là phần còn lại (đề phòng char chính là separator)
                            char_part = token_content[len(parts[0]) + len(parts[1]) + 2:]
                            
                            # Khôi phục ký tự đặc biệt
                            char = char_part
                            if char == 'TILDE': char = '~'
                            if char == 'PIPE': char = '|'
                            
                            # Tái tạo dữ liệu từ quá khứ
                            current_len = len(decoded_data)
                            start = current_len - dist
                            
                            for j in range(length):
                                if start + j < len(decoded_data):
                                     decoded_data.append(decoded_data[start + j])
                                else:
                                     decoded_data.append(decoded_data[start + j]) 
                            
                            decoded_data.append(char)
                                
                            i = end_token + 1
                            continue
                    except ValueError:
                        pass # Parse lỗi thì coi như text thường
            
            # Ký tự thường
            decoded_data.append(data[i])
            i += 1
            
        return "".join(decoded_data)