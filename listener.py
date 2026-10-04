
#!/usr/bin/env python3
import bluetooth
from pathlib import Path
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

DIR = Path(__file__).resolve().parent
secret_key = os.getenv("MAC_ADDRESS")


def handle_button(button_id):
    val = button_id.split("-")
    layout = val[0]
    button = str(val[1]) + ".sh"
    bt_sh = DIR / "scripts" / layout / button # this is a fake language, i swear. i love it.
    subprocess.run(["/bin/bash", bt_sh])



server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "8ce255c0-200a-11e0-ac64-0800200c9a66"

bluetooth.advertise_service(server_sock, "echo-show-streamdeck", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        handle_button(data.decode())
except OSError:
    pass

print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.")
