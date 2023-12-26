import os

#API ID & API Hash -----> my.telegram.org
api_id = 21874726 
api_hash = '5e734e8fbc0dc811b2696d5754297835'

#Bot Token -----> @BotFather
token = '6846406692:AAEFwNDO1Mf5M3A6oUU-IfRyJjeyZrcvNck'

#Session Name -----> optional
session_name = 'FTP_Uploader'


#The robot admin (the person who can give orders to the robot.) -----> @myidbot
admins = [5215061139]

# Chat id to send technical logs
dev = -1002058769683

# When a file is sent to the bot, first that file is downloaded from the Telegram repository and stored in the bot's server.
# Here you need to specify its temporary storage path
# For example, I set the bot to save the downloaded file in the current path (the path where config.py file is located).
dl_path = os.path.abspath(os.getcwd()) + '/'


# The upload path where we give FTP access to the bot.
ftp_path = ''

# The files are temporarily downloaded after they are on the bot server. They are uploaded to another host through FTP.
# Here we have to give FTP access to the bot.
ftp_ip = 'ftp.adisingh.in'
ftp_username = 'tgftpbot@adisingh.in'
ftp_password = 'eB]++DGxPGEW'
ftp_domain = 'https://adisingh.in/adisingh.in/tgftpbot/'
