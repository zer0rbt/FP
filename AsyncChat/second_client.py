import asyncio
import sys
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QTextBrowser, QShortcut
from ui_chat_window import Ui_MainWindow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Client:
    def __init__(self):
        self.designer = None
        self.user = ''
        self.host = "127.0.0.1"
        self.port = 8888
        self.reader = None
        self.writer = None

    async def error(self, message):
        logger.error(f"Error: {message}")

    async def receive_message(self):
        while True:
            message = await self.reader.read(1024)
            decoded_message = message.decode().strip()
            logger.info(f"Received message: {decoded_message}")
            await self.designer.receive_message(decoded_message)
            if "you are disconnected from the server" in decoded_message:
                return

    async def send_message(self, message):
        if message == "":
            await self.error("You didn't enter anything")
            return
        self.writer.write(message.encode())
        await self.writer.drain()
        if message == "exit":
            return

    async def send_message_to_server(self, writer, message):
        writer.write(message.encode())
        await writer.drain()

    async def start_client(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        logger.info("Connected to the server")
        await self.receive_message()
        self.writer.close()

class Designer(QMainWindow, Ui_MainWindow):
    def __init__(self, client):
        super().__init__()
        self.setupUi(self)
        self.client = client
        self.pushButton.clicked.connect(self.click)
        self.keyPressEvent = self.on_key_press_event

    def on_key_press_event(self, event):
        # Проверяем, была ли нажата клавиша Enter
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.click()

    def click(self):
        asyncio.create_task(self.send_message())

    async def send_message(self):
        message = self.lineEdit.text()
        await self.client.send_message(message)

    async def receive_message(self, message):
        # Use HTML formatting for QTextBrowser
        formatted_message = f"<b>{message}</b><br><hr>"
        self.textBrowser.append(formatted_message)
        self.lineEdit.clear()

    async def update(self, interval=0.05):
        while True:
            await asyncio.sleep(interval)
            QApplication.processEvents()

async def main():
    my_client = Client()
    my_des = Designer(my_client)
    my_client.designer = my_des
    my_des.show()
    tasks = [
        asyncio.create_task(my_client.start_client()),
        asyncio.create_task(my_des.update())
    ]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    asyncio.run(main())
    sys.exit(app.exec_())
