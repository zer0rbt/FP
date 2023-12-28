import asyncio
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger(__name__).setLevel(logging.DEBUG)


class Server:
    def __init__(self):
        self.clients_rooms = dict()
        self.clients = set()

    async def log_message(self, client, room, message):
        logger.info(f"Client {client[2]} in room {room}: {message}")

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        await self.send_message_to_client(writer, "Welcome! Enter your name:")
        name_new_client = (await reader.read(1024)).decode().strip()
        new_client = (writer, reader, name_new_client)
        await self.log_message(new_client, "No room", "connected to the server")
        await self.send_message_to_client(writer,
                                          f"Hello, {name_new_client}!\nTo create a room, enter '/create [name]'.\nTo join, enter '/join [name]'.")

        while True:
            action = (await new_client[1].read(1024)).decode().strip()
            await self.log_message(new_client, "No room", f"executed command: {action}")

            if action.startswith("/create "):
                await self.create_and_enter_room(new_client, action[len("/create "):])
            elif action.startswith("/join "):
                await self.enter_existing_room(new_client, action[len("/join "):])
            else:
                await self.send_message_to_client(new_client[0], "Unknown command. Please try again.")

    async def send_message_to_client(self, writer, response):
        writer.write(f"Server: {response}\n".encode())
        await writer.drain()

    async def receive_message(self, client, name_room):
        tasks = []
        while True:
            message = (await client[1].read(1024)).decode().strip()
            tasks.append(
                asyncio.create_task(self.log_message(client, name_room, f"sent message: {message}")))

            if message.startswith("/direct "):
                await self.send_direct_message(client, message[len("/direct "):], name_room)
            elif message.startswith("/silent "):
                await self.send_silent_message(client, message[len("/silent "):], name_room)
            elif message.lower() == "/exit":
                await self.exit(client, name_room)
                return
            elif message.lower() == "/help":
                await self.send_help_message(client)
            else:
                tasks.append(asyncio.create_task(self.send_message_to_clients(client, message, name_room)))
            await asyncio.gather(*tasks)
            tasks.clear()

    async def send_message_to_clients(self, send_client, message, name_room, silent=False):
        tasks = []
        client_name = send_client[2] if not silent else "????"
        time_now = datetime.now().strftime("%H:%M")
        for client in self.clients_rooms[name_room]:
            if send_client == client:
                client[0].write(f"You {'(Silently)' * silent}, {time_now}: {message}\n".encode())
            else:
                client[0].write(f"{client_name}, {time_now}: {message}\n".encode())
            tasks.append(asyncio.create_task(client[0].drain()))
        await asyncio.gather(*tasks)

    async def create_and_enter_room(self, client, room_name):
        while True:
            name_room = room_name.strip()
            if name_room in self.clients_rooms.keys():
                await self.send_message_to_client(client[0], "Room with this name already exists. Do you want to join?")
                return
            else:
                self.clients_rooms[name_room] = [client]
                self.clients.add((client, name_room))
                await self.log_message(client, "No room", f"created and entered room: {name_room}")
                await self.send_message_to_clients(client, f"{client[2]} joined the room.", name_room)
                await self.send_message_to_client(client[0], f"Room '{name_room}' created. You are now in the room.")
                await self.receive_message(client, name_room)
                return

    async def enter_existing_room(self, client, room_name):
        self.clients.add((client, "no room"))
        await self.send_message_to_client(client[0], "Enter the name of the room you want to join:")
        while True:
            name_room = room_name.strip()
            if name_room in self.clients_rooms.keys():
                self.clients_rooms[name_room].append(client)
                await self.log_message(client, "No room", f"entered the room: {name_room}")
                await self.send_message_to_clients(client, f"{client[2]} joined the room.", name_room)
                await self.receive_message(client, name_room)
                return
            await self.send_message_to_client(client[0], "Room does not exist. Try again.")
            return 

    async def send_direct_message(self, client, msg_params, name_room):
        params = msg_params.split(maxsplit=1)
        if len(params) == 2:
            usr, msg = params
            recipient = None
            print(list(map(lambda x: x[2], self.clients_rooms[name_room])))
            for cl in self.clients_rooms[name_room]:
                if cl[2] == usr:
                    recipient = cl
                    break
            if recipient:
                await self.send_message_to_client(recipient[0], f"Direct message from {client[2]}: {msg}")
                await self.send_message_to_client(client[0], f"Direct message sent to {usr}: {msg}")
            else:
                await self.send_message_to_client(client[0], f"User {usr} not found.")
        else:
            await self.send_message_to_client(client[0], "Invalid direct message format. Use '/direct [usr] [msg]'.")

    async def send_silent_message(self, client, msg, room_name):
        await self.send_message_to_clients(client, f"{msg}", room_name, silent=True)

    async def send_help_message(self, client):
        help_message = (
            "List of commands:\n"
            "/direct [usr] [msg] - Send a direct message to the specified user.\n"
            "/silent [msg] - Send a silent message to all users.\n"
            "/exit - Disconnect from the server.\n"
            "/help - View a list of all commands and their descriptions."
        )
        await self.send_message_to_client(client[0], help_message)

    async def exit(self, client, users_room):
        await self.send_message_to_client(client[0], "You are disconnected from the server.")
        if users_room != "no room":
            self.clients_rooms[users_room].remove(client)
            await self.log_message(client, users_room, f"executed command: exit")
            await self.send_message_to_clients(client, f"{client[2]} left the room.", users_room)


    async def start_server(self):
        server = await asyncio.start_server(
            self.handle_client, '127.0.0.1', 8888)
        addr = server.sockets[0].getsockname()
        logger.info(f"Server is running on {addr}")

        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    my_server = Server()
    asyncio.run(my_server.start_server())
