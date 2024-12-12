from http_server import run_http_server
from network_discovery import calculate_broadcast, discover_terminals
from wlan import connect_to_wifi
from terminals import poll_terminal_data
import uasyncio as asyncio


# Datos para conectarse a la red WiFi
#WLAN_SSID = "wfrre"
#WLAN_PASSWORD = "BityAtomo"
WLAN_SSID = "Fibertel WiFi925 2.4GHz"
WLAN_PASSWORD = "00439317996"

# Datos para las interfaces del maestro
BROADCAST_PORT = 10000
HTTP_SERVER_PORT = 8080


async def master_monitoring():
    print("Controlador maestro")

    if_config = await connect_to_wifi(WLAN_SSID, WLAN_PASSWORD)
    if if_config is None:
        print("Error al conectar a la red Wifi.")
        return None

    ip_address, subnet_mask, _, _ = if_config
    print(f"Conectado! IP: {ip_address}, Máscara de subred: {subnet_mask}")

    broadcast_ip = calculate_broadcast(ip_address, subnet_mask)
    print("Dirección de broadcast:", broadcast_ip)

    await asyncio.gather(
        run_http_server(ip_address, HTTP_SERVER_PORT),
        discover_terminals(broadcast_ip, BROADCAST_PORT),
        poll_terminal_data(),
    )

asyncio.run(master_monitoring())
