from pyrogram import Client , filters
from config import *
from text_helper import *
import os
import aioftp
import asyncio
import subprocess


app = Client(session_name,api_id=api_id,api_hash=api_hash,bot_token=token)


async def manager_text_handler(chat_id,msg):
    pass
async def user_text_handler(chat_id,msg):
    pass

async def check_file_name(file_name, file_date=None, mime_type=None):
    new_file_name = file_name
    new_file_date = 'video_' + str(file_date)
    try:
        if not file_name:
            if ' ' in new_file_date:
                new_file_date = new_file_date.replace(' ', '_')
            return new_file_date + '.' + mime_type
        else:
            if ' ' in file_name:
                new_file_name = new_file_name.replace(' ', '_')
            elif '💥' in file_name:
                new_file_name = new_file_name.replace('💥', '_')
            if '"' in file_name:
                new_file_name = new_file_name.replace('"', '_')
            else:
                return new_file_name.replace(' ', '_')
            return new_file_name.replace(' ', '_')
    except Exception as e:
        await app.send_message(dev, f'Error in check_file_name : {str(e)}')
        return False


async def get_file_name(message):

    chat_id = message.chat.id
    file_name = 'None'
    try:
        if message.video:
            if str(message.video.file_name) == 'None':
                file_name = await check_file_name(False, message.video.file_unique_id, message.video.mime_type.split('/')[1])
            else:
                file_name = await check_file_name(message.video.file_name, message.video.file_unique_id)
        elif message.audio:
            file_name = await check_file_name(message.audio.file_name)
        elif message.document:
            file_name = await check_file_name(message.document.file_name)

        # Ensure the file name is encoded using utf-8
        file_name = file_name.encode('utf-8').decode('latin-1')

        return file_name
    except Exception as e:
        await app.send_message(dev, f'Error in get_file_name: {str(e)}')
        return False


async def media_handler(chat_id, msgid, message):
    status = await app.send_message(
        chat_id,
        '⏳ Processing file...',
        reply_to_message_id=msgid
    )

    file_name = await get_file_name(message)
    if not file_name:
        await app.edit_message_text(
            chat_id,
            status.id,
            file_name_error
        )
        return

    try:
        await app.edit_message_text(chat_id, status.id, dl_text)
        await app.download_media(message, dl_path + file_name)
        if os.path.exists(dl_path + file_name):
            try:
                async with aioftp.Client.context(ftp_ip, user=ftp_username, password=ftp_password) as client:
                    ftp_file_path = ftp_path + file_name

                    if await client.exists(ftp_file_path):
                        # Handle the situation when the file already exists
                        await app.edit_message_text(chat_id, status.id, f'File with name "{file_name}" already exists on the FTP server.')
                    else:
                        # Upload the file to the FTP server
                        await app.edit_message_text(chat_id, status.id, upload_text)
                        await client.upload(dl_path + file_name, ftp_file_path)

                        # Save the filename into a text file
                        with open(dl_path + 'uploaded_files.txt', 'a') as file:
                            file.write(file_name + '\n')

                        # Execute the upload.py script
                        subprocess.run(['python', 'upload.py'])

                        # Delete the local file after successful upload
                        os.remove(dl_path + file_name)

                        # Delete the previous message ("Uploading to FTP Server...")
                        await app.delete_messages(chat_id, status.id)

                        # Send the message with the file link
                        await app.send_message(chat_id, dl_url_text.format(ftp_domain, file_name))
            except Exception as e:
                await app.edit_message_text(chat_id, status.id, upload_error_text)
                await app.send_message(dev, f'Error transferring to FTP host {str(e)}')
        else:
            await app.edit_message_text(chat_id, status.id, save_error_text)
            await app.send_message(dev, f'Error saving file {str(e)}')
    except Exception as e:
        await app.edit_message_text(chat_id, status.id, dl_error_text)
        await app.send_message(dev, f'Telegram download error {str(e)}')



@app.on_message(filters.private & filters.incoming)
async def message_handler(_, message):
    chat_id = message.chat.id
    msgid = message.id
    if message.text:
        msg = message.text
        if message.text == '/start':
            await app.send_message(
                chat_id,
                start_text,
                reply_to_message_id = msgid
            )
            return
        if chat_id in admins:
            await manager_text_handler(chat_id,msg)
        else:
            await user_text_handler(chat_id,msg)


    elif message.video or message.document or message.audio :
        if chat_id in admins:
            await media_handler(chat_id , msgid , message)
        else:
            await app.send_message(
                chat_id,
                'Only administrators can upload. Contact @ogaditya to get private access.',
                reply_to_message_id = msgid
            )



app.run()
