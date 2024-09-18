import threading
import time
import requests
import os
import configparser

config = configparser.ConfigParser()
path_dir = os.path.dirname(os.path.abspath(__file__))

# Đọc file cấu hình
config.read(os.path.join(path_dir, 'config.ini'))
current_dir = config.get('paths', 'data_path')
time_loop = config.getint('time', 'time_loop')


current_date = time.strftime("%Y%m%d")
log_path_dir = os.path.join(current_dir, "log")
if not os.path.exists(log_path_dir):
    os.makedirs(log_path_dir)

output_log_path = os.path.join(log_path_dir, f"{current_date}.log")

# Theo dõi file .log để kiểm tra dòng mới
def follow_log_file(output_log_path):
    current_date = time.strftime("%Y%m%d")
    file_path = os.path.join(current_dir, f"{current_date}.log")
    while True:
        try:
            # Check file exists
            log_to_file(output_log_path, f"Monitoring file: {file_path}")
            file = open(file_path, 'rb')
            file.seek(0, 2)  # Đặt con trỏ về cuối file
            
            while True:
                # check file path 
                current_date = time.strftime("%Y%m%d")
                new_file_path = os.path.join(current_dir, f"{current_date}.log")
    
                if new_file_path != file_path:
                    file.close()
                    file_path = new_file_path
                    file = open(file_path, 'rb')
                    file.seek(0, 2)

                    output_log_path = os.path.join(log_path_dir, f"{current_date}.log")
                    log_to_file(output_log_path, f"New date file: {file_path}")
                    time.sleep(time_loop)
                    continue
                
                binary_data = file.read()
                line = binary_data.decode('utf-16')
                if not line:
                    time.sleep(1) 
                    continue
                yield line
        except Exception as e:
            log_to_file(output_log_path, f"File not found: {file_path} - {e}")
            time.sleep(time_loop)


# Gửi tin nhắn tới Telegram
def send_telegram_message(token, chat_id, message):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message
        }
        response = requests.post(url, data=data)
        return response.status_code
    except Exception as e:
        log_to_file(output_log_path, f"Error sending message: {e}")


# Ghi log vào file .txt
def log_to_file(log_file_path, message):
    try:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            date_time = time.strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{date_time}] - {message}\n")
    except Exception as e:
        log_to_file(output_log_path, f"Error logging to file: {e}")


# Hàm để theo dõi log và gửi thông báo
def monitor_log_and_notify(token, chat_id, output_log_path):
    try:
        for line in follow_log_file(output_log_path):
            if line.strip() == '\x00':
                continue
            list_text = line.strip().split('\t')
            # Gửi tin nhắn tới Telegram
            date_time = time.strftime("%Y-%m-%d %H:%M:%S")
            send_telegram_message(token, chat_id, f"[{date_time}] - {line.strip()}")
            # Ghi log ra file .txt
            log_to_file(output_log_path, line.strip())
    except Exception as e:
        log_to_file(output_log_path, f"Error monitoring file: {e}")


# Chạy ngầm
def start_background_monitor(token, chat_id, output_log_path):
    monitor_thread = threading.Thread(target=monitor_log_and_notify, args=(token, chat_id, output_log_path))
    monitor_thread.daemon = True  # Đặt thread chạy ngầm
    monitor_thread.start()


# if __name__ == "__main__":
telegram_token = "7541641643:AAHgl-WobHqrUak3fBTjerDsF_Ws3jriRw0"
telegram_chat_id = "1899348741"


# Bắt đầu tiến trình theo dõi log chạy ngầm
start_background_monitor(telegram_token, telegram_chat_id, output_log_path)

while True:
    time.sleep(10)  # Giữ cho chương trình chính tiếp tục chạy ngầm
