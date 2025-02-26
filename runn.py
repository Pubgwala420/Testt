import telebot
import os
import shutil  # Needed to remove directories

# Replace with your bot token from BotFather
TOKEN = "8191199392:AAG0QteHHdTHgWMYS31cuxG73wZChA4aWXI"
bot = telebot.TeleBot(TOKEN)

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
    bot.reply_to(message, "Hi! Use /list to see files, /ch <directory> to change directory, /get <filename> to retrieve a file, and /del <path> to delete a file or folder.")

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

# Command to delete a file or directory
@bot.message_handler(commands=['del'])
def delete_file_or_folder(message):
    try:
        path = message.text.split(' ', 1)[1]
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
                bot.reply_to(message, f"File '{path}' has been deleted.")
            elif os.path.isdir(path):
                shutil.rmtree(path)
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
