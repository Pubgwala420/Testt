import telebot
import os

# Replace with your bot token from BotFather
TOKEN = "8191199392:AAF_lvjCgEdavIaKKRK8DhNte7TfW8sR2es"
bot = telebot.TeleBot(TOKEN)

# Allowed file formats (modify as needed)
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".jpg", ".png", ".zip", ".mp4",".py",".json",".html"}

# Command to list files in the bot's directory
@bot.message_handler(commands=['list'])
def list_files(message):
    try:
        files = os.listdir(os.getcwd())
        file_list = "\n".join(files) if files else "Directory is empty."
        bot.reply_to(message, f"Files in directory:\n{file_list}")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi! Use /list to see files, /ch <directory> to change directory, /get <filename> to retrieve a file, and /getall to get all files in the current directory.")

# Command to change directory
@bot.message_handler(commands=['ch'])
def change_directory(message):
    try:
        new_dir = message.text.split(' ', 1)[1]
        if os.path.isdir(new_dir):
            os.chdir(new_dir)
            bot.reply_to(message, f"Changed directory to: {os.getcwd()}")
        else:
            bot.reply_to(message, "Not a valid directory.")
    except IndexError:
        bot.reply_to(message, "Usage: /ch <directory>")
    except FileNotFoundError:
        bot.reply_to(message, "Directory not found.")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Command to send a requested file
@bot.message_handler(commands=['get'])
def send_file(message):
    try:
        file_name = message.text.split(' ', 1)[1]
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as file:
                bot.send_document(message.chat.id, file)
        else:
            bot.reply_to(message, "File not found or not a valid file.")
    except IndexError:
        bot.reply_to(message, "Usage: /get <filename>")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Command to get all allowed files in the current directory
@bot.message_handler(commands=['getall'])
def send_all_files(message):
    try:
        files_sent = 0
        for file in os.listdir(os.getcwd()):
            file_path = os.path.join(os.getcwd(), file)
            if os.path.isfile(file_path) and any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                with open(file_path, 'rb') as f:
                    bot.send_document(message.chat.id, f)
                files_sent += 1

        if files_sent == 0:
            bot.reply_to(message, "No valid files found to send.")
        else:
            bot.reply_to(message, f"Sent {files_sent} files.")

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")
@bot.message_handler(commands=['del'])
def delete_file_or_folder(message):
    try:
        path = Path(message.text.split(' ', 1)[1])
        if path.exists():
            if path.is_file():
                path.unlink()
                bot.reply_to(message, f"File '{path}' has been deleted.")
            elif path.is_dir():
                for sub_path in sorted(path.rglob('*'), key=lambda p: -p.is_file()):  # Sort to delete files first
                    if sub_path.is_file():
                        sub_path.unlink()
                    elif sub_path.is_dir():
                        sub_path.rmdir()
                path.rmdir()  # Finally remove the main directory
                bot.reply_to(message, f"Folder '{path}' has been deleted.")
            else:
                bot.reply_to(message, "Cannot determine if it's a file or folder.")
        else:
            bot.reply_to(message, "File or folder not found.")
    except IndexError:
        bot.reply_to(message, "Usage: /del <path>")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Start the bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
