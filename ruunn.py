import telebot
import os
import shutil

# Replace with your bot token from BotFather
TOKEN = "8010409321:AAGyaKkm5VXgSgouTH7TUH9yPfnwlh-JZTE"
bot = telebot.TeleBot(TOKEN)

# Allowed file formats for /getall
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".jpg", ".png", ".zip", ".mp4",".py"}

# Command to list files and folders in the current directory
@bot.message_handler(commands=['list'])
def list_files(message):
    try:
        files = os.listdir(os.getcwd())
        file_list = "\n".join(files) if files else "Directory is empty."
        bot.reply_to(message, f"Files in directory:\n{file_list}")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Command to start the bot and show available commands


# Command to change the working directory
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
            if os.path.isfile(file) and any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                with open(file, 'rb') as f:
                    bot.send_document(message.chat.id, f)
                files_sent += 1

        if files_sent == 0:
            bot.reply_to(message, "No valid files found to send.")
        else:
            bot.reply_to(message, f"Sent {files_sent} files.")

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Command to delete a file or folder
@bot.message_handler(commands=['del'])
def delete_file_or_folder(message):
    try:
        path = message.text.split(' ', 1)[1]

        if not os.path.exists(path):
            bot.reply_to(message, "File or folder not found.")
            return

        if os.path.isfile(path):
            os.remove(path)
            bot.reply_to(message, f"File '{path}' has been deleted.")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            bot.reply_to(message, f"Folder '{path}' has been deleted.")
        else:
            bot.reply_to(message, "Cannot determine if it's a file or folder.")

    except IndexError:
        bot.reply_to(message, "Usage: /del <path>")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Start the bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
