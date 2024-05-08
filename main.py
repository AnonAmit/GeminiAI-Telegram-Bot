import os
import asyncio
import google.generativeai as genai
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

# Environment variables
TG_TOKEN = os.environ['TG_TOKEN']
GOOGLE_GEMINI_KEY = os.environ['GOOGLE_GEMINI_KEY']

# Gemini models
gemini_player_dict = {}
gemini_pro_player_dict = {}
default_model_dict = {}

# Error message
error_info = "⚠️⚠️⚠️\nSomething went wrong!\nplease try to change your prompt or contact the admin!"
before_generate_info = "🤖Generating🤖"
download_pic_notify = "🤖Loading picture🤖"

# Generation config
n = 10  # Number of historical records to keep
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

# Functions
async def make_new_gemini_convo():
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    convo = model.start_chat()
    return convo

async def make_new_gemini_pro_convo():
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    convo = model.start_chat()
    return convo

async def send_message(player, message):
    await player.send_message(message)

async def async_generate_content(model, contents):
    response = model.generate_content(contents=contents)
    return response

async def gemini(bot, message, m):
    player = None
    if str(message.from_user.id) not in gemini_player_dict:
        player = await make_new_gemini_convo()
        gemini_player_dict[str(message.from_user.id)] = player
    else:
        player = gemini_player_dict[str(message.from_user.id)]
    if len(player.history) > n:
        player.history = player.history[2:]
    try:
        sent_message = await bot.reply_to(message, before_generate_info)
        await send_message(player, m)
        try:
            await bot.edit_message_text(escape(player.last.text), chat_id=sent_message.chat.id, message_id=sent_message.message_id, parse_mode="MarkdownV2")
        except:
            await bot.edit_message_text(escape(player.last.text), chat_id=sent_message.chat.id, message_id=sent_message.message_id)

    except Exception:
        traceback.print_exc()
        await bot.edit_message_text(error_info, chat_id=sent_message.chat.id, message_id=sent_message.message_id)

async def gemini_pro(bot, message, m):
    player = None
    if str(message.from_user.id) not in gemini_pro_player_dict:
        player = await make_new_gemini_pro_convo()
        gemini_pro_player_dict[str(message.from_user.id)] = player
    else:
        player = gemini_pro_player_dict[str(message.from_user.id)]
    if len(player.history) > n:
        player.history = player.history[2:]
    try:
        sent_message = await bot.reply_to(message, before_generate_info)
        await send_message(player, m)
        try:
            await bot.edit_message_text(escape(player.last.text), chat_id=sent_message.chat.id, message_id=sent_message.message_id, parse_mode="MarkdownV2")
        except:
            await bot.edit_message_text(escape(player.last.text), chat_id=sent_message.chat.id, message_id=sent_message.message_id)

    except Exception:
        traceback.print_exc()
        await bot.edit_message_text(error_info, chat_id=sent_message.chat.id, message_id=sent_message.message_id)

async def main():
    # Init bot
    bot = AsyncTeleBot(TG_TOKEN)

    # Init commands
    @bot.message_handler(commands=["start"])
    async def gemini_handler(message: Message):
        try:
            await bot.reply_to(message, escape("Welcome, you can ask me questions now. \nFor example: `Who is Binod`"), parse_mode="MarkdownV2")
        except IndexError:
            await bot.reply_to(message, error_info)

    @bot.message_handler(commands=["gemini"])
    async def gemini_handler(message: Message):
        try:
            m = message.text.strip().split(maxsplit=1)[1].strip()
        except IndexError:
            await bot.reply_to(message, escape("Please add what you want to say after /gemini. \nFor example: `/gemini Who is Binod`"), parse_mode="MarkdownV2")
            return
        await gemini(bot, message, m)

    @bot.message_handler(commands=["gemini_pro"])
    async def gemini_handler(message: Message):
        try:
            m = message.text.strip().split(maxsplit=1)[1].strip()
        except IndexError:
            await bot.reply_to(message, escape("Please add what you want to say after /gemini_pro. \nFor example: `/gemini_pro Who is Binod`"), parse_mode="MarkdownV2")
            return
        await gemini_pro(bot, message, m)

    @bot.message_handler(commands=["clear"])
    async def gemini_handler(message: Message):
        # Check if the player is already in gemini_player_dict.
        if (str(message.from_user.id) in gemini_player_dict):
            del gemini_player_dict[str(message.from_user.id)]
        if (str(message.from_user.id) in gemini_pro_player_dict):
            del gemini_pro_player_dict[str(message.from_user.id)]
        await bot.reply_to(message, "Your history has been cleared")

    @bot.message_handler(func=lambda message: message.chat.type == "private", content_types=['text'])
    async def gemini_private_handler(message: Message):
        m = message.text.strip()

        if str(message.from_user.id) not in default_model_dict:
            default_model_dict[str(message.from_user.id)] = True
            await gemini(bot, message, m)
        else:
            if default_model_dict[str(message.from_user.id)]:
                await gemini(bot, message, m)
            else:
                await gemini_pro(bot, message, m)

    @bot.message_handler(content_types=["photo"])
    async def gemini_photo_handler(message: Message) -> None:
        if message.chat.type != "private":
            s = message.caption
            if not s or not (s.startswith("/gemini")):
                return
            try:
                prompt = s.strip().split(maxsplit=1)[1].strip() if len(s.strip().split(maxsplit=1)) > 1 else ""
                file_path = await bot.get_file(message.photo[-1].file_id)
                sent_message = await bot.reply_to(message, download_pic_notify)
                downloaded_file = await bot.download_file(file_path.file_path)
            except Exception:
                traceback.print_exc()
                await bot.reply_to(message, error_info)
            model = genai.GenerativeModel("gemini-pro-vision")
            contents = {
                "parts": [{"mime_type": "image/jpeg", "data": downloaded_file}, {"text": prompt}]
            }
            try:
                await bot.edit_message_text(before_generate_info, chat_id=sent_message.chat.id, message_id=sent_message.message_id)
                response = await async_generate_content(model, contents)
                await bot.edit_message_text(response.text, chat_id=sent_message.chat.id, message_id=sent_message.message_id)
            except Exception:
                traceback.print_exc()
                await bot.edit_message_text(error_info, chat_id=sent_message.chat.id, message_id=sent_message.message_id)
        else:s = message.caption if message.caption else ""
            try:
                prompt = s.strip()
                file_path = await bot.get_file(message.photo[-1].file_id)
                sent_message = await bot.reply_to(message, download_pic_notify)
                downloaded_file = await bot.download_file(file_path.file_path)
            except Exception:
                traceback.print_exc()
                await bot.reply_to(message, error_info)
            model = genai.GenerativeModel("gemini-pro-vision")
            contents = {
                "parts": [{"mime_type": "image/jpeg", "data": downloaded_file}, {"text": prompt}]
            }
            try:
                await bot.edit_message_text(before_generate_info, chat_id=sent_message.chat.id, message_id=sent_message.message_id)
                response = await async_generate_content(model, contents)
                await bot.edit_message_text(response.text, chat_id=sent_message.chat.id, message_id=sent_message.message_id)
            except Exception:
                traceback.print_exc()
                await bot.edit_message_text(error_info, chat_id=sent_message.chat.id, message_id=sent_message.message_id)

    # Start bot
    print("Starting Gemini_Telegram_Bot.")
    await bot.polling(none_stop=True)

if __name__ == '__main__':
    asyncio.run(main())
