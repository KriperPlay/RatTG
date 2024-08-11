import telebot
import os
import os.path
from os import path
import threading
import sys
import time

API_TOKEN = ""
YOUR_ID = None
bot = telebot.TeleBot(API_TOKEN,threaded=True)
message_var = ""
my_voices_name = ""


@bot.business_message_handler(commands=['start'])
def start(message):
    try:
        os.mkdir(f"chats/{message.from_user.id}:{message.business_connection_id}")
        os.mkdir(f"chats/{message.from_user.id}:{message.business_connection_id}/voices")
        os.mkdir(f"chats/{message.from_user.id}:{message.business_connection_id}/documents")
        chat_file = open(f"chats/{message.from_user.id}:{message.business_connection_id}/chat.txt", 'w')
        chat_file.close()
        list_file = open("chat_list.txt", 'a')
        list_file.write(f"{message.from_user.id}:{message.business_connection_id} - {message.from_user.first_name} {message.from_user.last_name}\n")
        list_file.close()
    except FileExistsError:
        pass

@bot.business_message_handler(content_types=['text','document','photo','voice'])
def check(message):
    try:
        if message.from_user.id == YOUR_ID:
            chat_file = open(f"chats/{message.chat.id}:{message.business_connection_id}/chat.txt", 'a')
            chat_file.write(f"You: {message.text}\n")      
        if message.content_type == 'text':
            chat_file = open(f"chats/{message.from_user.id}:{message.business_connection_id}/chat.txt", 'a')
            chat_file.write(f"{message.from_user.first_name}: {message.text}\n")
        if message.content_type == 'document':
            download_document(message)
        if message.content_type == 'voice':
            if message.from_user.id == YOUR_ID:
                download_voice(message)
                chat_file = open(f"chats/{message.chat.id}:{message.business_connection_id}/chat.txt", 'a')
                chat_file.write(f"You: {my_voices_name}\n") 
            else:
                download_voice(message)
    except FileNotFoundError:
        pass


def download_document(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'chats/{message.from_user.id}:{message.business_connection_id}/documents/' + message.document.file_name
        if path.exists(src) == False:
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            chat_file = open(f"chats/{message.from_user.id}:{message.business_connection_id}/chat.txt", 'a')
            chat_file.write(f"{message.from_user.first_name}: File: {message.document.file_name}\n")
        else:
            name, ext = os.path.splitext(src)
            i = 1
            while True:
                new_filename = f"{name}_copy({i}){ext}"
                if not os.path.exists(new_filename):
                    src = new_filename
                    break
                i += 1
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            chat_file = open(f"chats/{message.from_user.id}:{message.business_connection_id}/chat.txt", 'a')
            chat_file.write(f"{message.from_user.first_name}: File: {message.document.file_name}\n")
    except Exception:
        pass

def download_voice(message):
    global my_voices_name
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'chats/{message.from_user.id}:{message.business_connection_id}/voices/' + "voice.ogg"
        if path.exists(src) == False:
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            chat_file = open(f"chats/{message.from_user.id}:{message.business_connection_id}/chat.txt", 'a')
            chat_file.write(f"{message.from_user.first_name}: voice\n")
        else:
            name, ext = os.path.splitext(src)
            i = 1
            while True:
                new_filename = f"{name}_copy({i}){ext}"
                if not os.path.exists(new_filename):
                    src = new_filename
                    break
                i += 1
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            chat_file = open(f"chats/{message.from_user.id}:{message.business_connection_id}/chat.txt", 'a')
            name1,ext1 = os.path.splitext(new_filename)
            for j in range(len(name1)):
                if name1[j] == '/':
                    b = j
            chat_file.write(f"{message.from_user.first_name}: {name1[b+1:]}\n")
            my_voices_name = f"{name1[b+1:]}"
    except Exception:
        pass

def CLI():
    try:
        id1 = ""
        id2 = ""
        dot1 = 0
        print("Contacts: ")
        list_file = open("chat_list.txt", 'r')
        for line in list_file:
            line0 = line.strip()
            print(line0)
        chat_id =input("Enter id contact: ")
        for i in range(len(chat_id)):
            if chat_id[i] == ':':
                dot1 = i
                id1 = chat_id[:i]
                break
        id2 = chat_id[dot1+1:]

        while True:
            chat = open(f"chats/{chat_id}/chat.txt", 'r')
            for line in chat:
                line0 = line.strip()
                print(line0)
            message_var = input("Your message: ")
            if message_var == "":
                pass
                os.system('cls' if os.name == 'nt' else 'clear')
            elif message_var[0] == '[':
                if message_var[len(message_var)-1] == ']':
                    bot.send_document(id1, open(f'{message_var[1:len(message_var)-1]}', 'rb'),business_connection_id=id2)
                    chat_file = open(f"chats/{chat_id}/chat.txt", 'a')
                    chat_file.write(f"You: File: {message_var[1:len(message_var)-1]}\n")
                    chat_file.close()
            elif message_var == "restart()":
                os.system('cls' if os.name == 'nt' else 'clear')
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                chat_file = open(f"chats/{chat_id}/chat.txt", 'a')
                chat_file.write(f"You: {message_var}\n")
                chat_file.close()
                bot.send_message(id1, message_var,business_connection_id=id2)
                message_var = ""
                os.system('cls' if os.name == 'nt' else 'clear')
    except FileNotFoundError:
        print("Contact not found!")
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        os.execl(sys.executable, sys.executable, *sys.argv)

threading.Thread(target=CLI).start()
bot.polling(none_stop = True)