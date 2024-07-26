import asyncio
from datetime import datetime
from json import dumps
from random import choice, randint
from string import ascii_letters, digits
import httpx
import pyfiglet

WARP_CLIENT_ID = input("Enter your WARP Client ID:\n")

# Defaults
SUCCESS_COUNT, FAIL_COUNT = 0, 0


def genString(stringLength):
    try:
        letters = ascii_letters + digits
        return ''.join(choice(letters) for _ in range(stringLength))
    except Exception as error_code:
        print(error_code)


def digitString(stringLength):
    try:
        digit = digits
        return ''.join(choice(digit) for _ in range(stringLength))
    except Exception as error_code:
        print(error_code)


async def send_request(url, body, headers):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=body, headers=headers)
            return response.status_code
        except Exception as error_code:
            print(error_code)
            return None


async def cooldown(cooldown_time):
    print(f"Sleep: {cooldown_time} seconds.")
    await asyncio.sleep(cooldown_time)


url = f"https://api.cloudflareclient.com/v0a{digitString(3)}/reg"

# Print Figlet Font name
figlet_text = pyfiglet.figlet_format('PARVEJ')
print(figlet_text)


async def main():
    global SUCCESS_COUNT, FAIL_COUNT
    while True:
        try:
            install_id = genString(22)
            body = {
                "key": f"{genString(43)}=",
                "install_id": install_id,
                "fcm_token": f"{install_id}:APA91b{genString(134)}",
                "referrer": WARP_CLIENT_ID,
                "warp_enabled": False,
                "tos": f"{datetime.now().isoformat()[:-3]}+02:00",
                "type": "Android",
                "locale": "es_ES"
            }
            data = dumps(body).encode("utf8")
            headers = {
                "Content-Type": "application/json; charset=UTF-8",
                "Host": "api.cloudflareclient.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.12.1"
            }
            response = await send_request(url, data, headers)
        except Exception as error_code:
            print(error_code)

        if response == 200:
            SUCCESS_COUNT += 1
            message = f"PASSED: +1GB (total: {SUCCESS_COUNT}GB, failed: {FAIL_COUNT})"
            print(message)
        else:
            print(f"FAILED: {response}")
            FAIL_COUNT += 1

        # Cooldown
        cooldown_time = randint(10, 20)  # Adjusted cooldown time
        await cooldown(cooldown_time)


if __name__ == "__main__":
    asyncio.run(main())