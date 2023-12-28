import sys
import vk_api
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton
from datetime import datetime
import string
import threading
from telethon.sync import TelegramClient
import asyncio
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config["DEFAULT"]["VK_TOKEN"]


# tg ids: postupashki, anekdot18, 
# vk ids: 67991642, 15755094, 20169232, 40316705, 27532693
class GroupIDInput(QWidget):
    def __init__(self):
        super().__init__()

        self.group_ids = []
        self.channels = []

        self.init_ui()

        self.tg_api_id = config["DEFAULT"]["TELEGRAM_ID"]
        self.tg_api_hash = config["DEFAULT"]["TELEGRAM_HASH"]

    def init_ui(self):
        layout = QVBoxLayout()

        self.group_id_input = QLineEdit(self)
        self.group_id_input.setPlaceholderText("Введите ID группы VK")
        layout.addWidget(self.group_id_input)

        self.add_vk_group_button = QPushButton("Добавить группу в VK", self)
        self.add_vk_group_button.clicked.connect(self.add_vk_group)
        layout.addWidget(self.add_vk_group_button)

        self.channel_input = QLineEdit(self)
        self.channel_input.setPlaceholderText("Введите название канала Telegram")
        layout.addWidget(self.channel_input)

        self.add_telegram_channel_button = QPushButton("Добавить канал в Telegram", self)
        self.add_telegram_channel_button.clicked.connect(self.add_telegram_channel)
        layout.addWidget(self.add_telegram_channel_button)

        self.show_button = QPushButton("Начать чтение", self)
        self.show_button.clicked.connect(self.start_reading)
        layout.addWidget(self.show_button)

        self.setLayout(layout)

    def add_vk_group(self):
        group_id = self.group_id_input.text()
        if group_id:
            self.group_ids.append(group_id)
            self.group_id_input.clear()

    def add_telegram_channel(self):
        channel_name = self.channel_input.text()
        if channel_name:
            self.channels.append(channel_name)
            self.channel_input.clear()

    def start_reading(self):
        vk_threads = []
        for group_id in self.group_ids:
            thread = threading.Thread(target=self.read_vk_group_wall, args=(group_id,))
            vk_threads.append(thread)

        tg_thread = threading.Thread(target=lambda: asyncio.run(
            self.read_tg(self.channels, 100)))

        for thread in vk_threads:
            thread.start()

        tg_thread.start()

        for thread in vk_threads:
            thread.join()

        tg_thread.join()

        self.start_analyzing()

    def start_analyzing(self):
        analyze_threads = []

        for group_id in self.group_ids:
            thread = threading.Thread(target=self.analyze, args=(f"vk_group_{group_id}",))
            analyze_threads.append(thread)

        for channel in self.channels:
            thread = threading.Thread(target=self.analyze, args=(f"tg_channel_{channel}",))
            analyze_threads.append(thread)

        for thread in analyze_threads:
            thread.start()

        for thread in analyze_threads:
            thread.join()

    async def read_tg(self, group_names, num_messages):
        client = TelegramClient('session_name', api_id=self.tg_api_id, api_hash=self.tg_api_hash,
                                system_version='4.16.30-vxCUSTOM')
        await client.start()
        for group_name in group_names:
            group_entity = await client.get_input_entity(group_name)

            async for message in client.iter_messages(group_entity, limit=num_messages):
                post_text = message.text
                refined_text = self.refine(post_text)
                self.save_to_file(refined_text, f"tg_channel_{group_name}")
        await client.disconnect()
        client.disconnect()

    lock = threading.Lock()

    def read_vk_group_wall(self, group_id):
        vk_session = vk_api.VkApi(token=TOKEN)
        vk = vk_session.get_api()
        response = vk.wall.get(owner_id=f'-{group_id}', count=100)

        for post in response['items']:
            post_text = post['text']
            refined_text = self.refine(post_text)
            self.save_to_file(refined_text, f"vk_group_{group_id}")

    def analyze(self, name):
        with open(f"{name}.txt", mode="r", encoding="utf-8") as f:
            f = f.read()
            f = f.replace('\n', " ").split(" ")
            unique = list(set(f))
            analytics = sorted(list(map(lambda x: (x, f.count(x)), list(filter(lambda y: len(y) > 2, unique)))),
                               key=lambda z: z[1])[::-1]
            self.save_to_file(text=f"Top 10 trends in {name}:", source_name=f"analyzed_{name}")
            for i in range(10):
                self.save_to_file(text=" :".join(list(map(str, analytics[i]))), source_name=f"analyzed_{name}")

    def refine(self, text):
        text = text.replace("@anekdot18", "BLOCKED_SELF_AD")
        return text

    def save_to_file(self, text, source_name):
        # with open(f"{source_name}_dt{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt", "a", encoding="utf-8") as file:
        with open(f"{source_name}.txt", "a", encoding="utf-8") as file:
            file.write(text + "\n")


def main():
    app = QApplication(sys.argv)
    window = GroupIDInput()
    window.setWindowTitle('Чтение стен и сообщений из групп VK и каналов Telegram')
    window.setGeometry(100, 100, 400, 200)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
