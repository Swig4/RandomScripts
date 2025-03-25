import os
import threading
import requests
import time
import json
import random
import string
from colorama import Fore, Style, init
import re
import ctypes
import aiohttp
import tls_client
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timezone, timedelta
from discord_interactions import verify_key
from PIL import Image

init()
COMMANDS = [
    "Close Script",
    "Join Server",
    "Leave Server",
    "Chat Spammer",
    "Nickname Changer",
    "Fake Typing",
    "Get Names With Tokens",
    "Message Reacter",
    "Join VC",
    "Soundboard Spam",
    "Scrape Members",
    "Check Server",
    "Check Tokens",
    "DM User",
    "Call User",
    "Reply Spammer",
    "Send Friend Request",
    "Login To Token",
    "Scan For tokens",
    "Check For Nitro",
    "Get Account Status"
]

default_color = Fore.CYAN
version = 1.0

init(autoreset=True)

def set_window_title(title): ctypes.windll.kernel32.SetConsoleTitleW(title)

G = Fore.GREEN; R = Fore.RED; Y = Fore.YELLOW; W = Fore.RESET

color_map = {
    "black": Fore.BLACK,
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
    "reset": Fore.RESET,
    "lightblack_ex": Fore.LIGHTBLACK_EX,
    "lightred_ex": Fore.LIGHTRED_EX,
    "lightgreen_ex": Fore.LIGHTGREEN_EX,
    "lightyellow_ex": Fore.LIGHTYELLOW_EX,
    "lightblue_ex": Fore.LIGHTBLUE_EX,
    "lightmagenta_ex": Fore.LIGHTMAGENTA_EX,
    "lightcyan_ex": Fore.LIGHTCYAN_EX,
    "lightwhite_ex": Fore.LIGHTWHITE_EX,
}

emoji_map = {
    "skull": "%F0%9F%92%80",
    "heart": "%E2%9D%A4%EF%B8%8F",
    "thumbs_up": "%F0%9F%91%8D",
    "nerd": "%F0%9F%A4%93",
    "speaking_head": "%F0%9F%97%BA",
    "gun": "%F0%9F%94%AB",
    "smile": "%F0%9F%98%83",
    "grin": "%F0%9F%98%80",
    "joy": "%F0%9F%98%82",
    "rofl": "%F0%9F%A4%A3",
    "wink": "%F0%9F%98%89",
    "blush": "%F0%9F%98%98",
    "yum": "%F0%9F%98%8B",
    "sunglasses": "%F0%9F%98%8E",
    "thinking": "%F0%9F%A4%94",
    "expressionless": "%F0%9F%98%90",
    "neutral_face": "%F0%9F%98%91",
    "smirk": "%F0%9F%98%8F",
    "unamused": "%F0%9F%98%92",
    "sweat_smile": "%F0%9F%98%85",
    "cold_sweat": "%F0%9F%98%93",
    "sob": "%F0%9F%98%AD",
    "angry": "%F0%9F%98%A0",
    "rage": "%F0%9F%98%A1",
    "thumbs_down": "%F0%9F%91%8E",
    "clap": "%F0%9F%91%8F",
    "pray": "%F0%9F%99%8F",
    "muscle": "%F0%9F%92%AA",
    "ok_hand": "%F0%9F%91%8C",
    "point_right": "%F0%9F%91%89",
    "point_left": "%F0%9F%91%88",
    "point_up": "%F0%9F%91%86",
    "point_down": "%F0%9F%91%87",
    "raised_hands": "%F0%9F%99%8C",
    "fist": "%F0%9F%91%8A",
    "facepunch": "%F0%9F%91%8A",
    "v": "%E2%9C%8C%EF%B8%8F",
    "wave": "%F0%9F%91%8B",
    "call_me_hand": "%F0%9F%91%95",
    "star": "%E2%AD%90",
    "star_struck": "%F0%9F%A4%A0",
    "fire": "%F0%9F%94%A5",
    "100": "%F0%9F%92%AF",
    "poop": "%F0%9F%92%A9",
    "alien": "%F0%9F%91%BD",
    "ghost": "%F0%9F%91%BB",
    "robot": "%F0%9F%A4%96",
    "skull_crossbones": "%E2%98%A0%EF%B8%8F",
    "devil": "%F0%9F%91%BF",
    "angel": "%F0%9F%99%8C",
    "see_no_evil": "%F0%9F%99%88",
    "hear_no_evil": "%F0%9F%99%89",
    "speak_no_evil": "%F0%9F%99%8A"
}

global found, files, tokens, contents
global invalids, lockeds, checked
found = []; files = []; tokens = []; contents = []
invalids = 0; lockeds = 0; checked = 0

def convert_emoji(emoji_name): return emoji_map.get(emoji_name.lower(), emoji_name)

def has_nitro(token):
    try:
        url = "https://discord.com/api/v9/users/@me/billing/subscriptions"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            subscriptions = response.json()
            for subscription in subscriptions:
                if subscription.get("type") == 1:
                    return True
            return False
        elif response.status_code == 400:
            printwee(f"captcha required for token: {token}", "yellow")
        else:
            printwee(f"Failed to check Nitro status for token. Status code: {response.status_code}", "red")
            return False
    except Exception as e:
        printwee(f"An error occurred while checking Nitro status: {e}", "red")
        return False
    
def check_tokens_for_nitro(tokens):
    nitro_tokens = []
    for token in tokens:
        if has_nitro(token):
            nitro_tokens.append(token)
    return nitro_tokens

def printwee(msg, color):
    ti = f'{Fore.LIGHTBLACK_EX}{time.strftime("%H:%M:%S")}{Style.RESET_ALL}'
    color_code = color_map.get(color.lower(), Fore.RESET)
    colored_msg = f"{color_code}{msg}{Style.RESET_ALL}"
    print(f"{ti} {colored_msg}")

def log(mode, msg, token=None):
    redstart = 'failed to '
    greenstart = 'successfully '
    messeige = ''
    if token != None:
        token = token.split('.')[0]
    if mode == 'green':
        messeige = greenstart + msg
    elif mode == 'red':
        messeige = redstart + msg
    messeige = messeige.capitalize()
    ti = f'{Fore.LIGHTBLACK_EX}{time.strftime("%H:%M:%S")}'
    if token == None:
        if mode == 'green':
            print(ti + f' {G}{msg}{W}')
        elif mode == 'red':
            print(ti + f' {R}{msg}{W}')
        elif mode == 'yellow':
            print(ti + f' {Y}{msg}{W}')
    else:
        if mode == 'green':
            print(ti + f' {G}{msg} {W}{token}****{G}')
        elif mode == 'red':
            print(ti + f' {R}{msg} {W}{token}****{R}')
        elif mode == 'yellow':
            print(ti + f' {Y}{msg} {W}{token}****{Y}')

async def check_token(token: str):
    global invalids, lockeds, checked
    try:
        token = str(token).replace('\n', '')
        headers = {'Authorization': token}
        async with aiohttp.ClientSession() as client:
            r = await client.get('https://discord.com/api/v9/users/@me', headers=headers)
            tuken = token.split('.')[0]
            try:
                message = await r.json()
                message = json.dumps(message, indent=2)
                ti = f'{Fore.LIGHTBLACK_EX}{time.strftime("%H:%M:%S")}'
                if r.status == 200:
                    log('green', f"valid: [{r.status}]", token)
                    tokens.append(token)
                elif r.status == 403:
                    log('yellow', f"locked: [{r.status}]", token)
                    lockeds += 1
                elif r.status == 429:
                    log('yellow', f"ratelimited: [{r.status}]")
                    await asyncio.sleep(15)
                    await check_token(token)
                else:
                    log('red', f"invalid: [{r.status}]", token)
                    invalids += 1
                checked += 1
            except:
                await check_token(token)
    except:
        pass

def token_locator(path):
    global found, files, tokens, contents
    for root, dirs, balls in os.walk(path):
        if 'discord' in root.lower() or 'token' in root.lower():
            for ball in balls:
                ball = ball.lower()
                if 'token' in ball and ball.endswith('.txt'):
                    found.append(os.path.join(root, ball))
                    ti = f'{Fore.LIGHTBLACK_EX}{time.strftime("%H:%M:%S")}'
                    print(ti + f' Found tokens file (#{len(found)})', end='\r')
    print()

    if not os.path.isdir('files'):
        os.mkdir('files')
        log('green', "Created 'files' folder since it wasn't found")
    else:
        for f in os.listdir('files'):
            os.remove(os.path.join('files', f))
        os.rmdir('files')
        os.mkdir('files')
        log('green', "Replaced 'files' folder")

    count = 0
    for xx in found:
        count += 1
        with open(xx) as ff:
            con = ff.read()
        with open(f'files/Tokens_{count}.txt', 'w+') as ff:
            ff.write(con)

    log('yellow', 'Saved scraped tokens.txt files')
    obj = os.scandir('files')
    for i in obj:
        name = i.name.lower()
        if 'token' in name or 'discord' in name:
            if '.txt' in name:
                files.append(i.name)
    amtfound = len(files)
    if amtfound != 0:
        log('green', f'Amount of tokens files found: {amtfound}')
    else:
        log('red', 'No tokens files found, please try another path')
        time.sleep(3)
        return
    for file in files:
        with open(f'files/{file}', 'r') as file:
            content = file.read().splitlines()
            for c in content:
                if c and (c.startswith('MTE') or c.startswith('MTA') or c.startswith('OT') or c.startswith('OD') or c.startswith('Nj') or c.startswith('Nz') or c.startswith('MTI') or c.startswith('Mj') or c.startswith('ND')):
                    contents.append(c)
    async def runtask():
        tasks = [check_token(c) for c in contents]
        await asyncio.gather(*tasks)
    asyncio.run(runtask())
    with open('tokens.txt', 'w+') as f:
        cum = '\n'.join(tokens)
        f.write(cum)
    log('yellow', 'Saved all valid tokens to tokens.txt')
    unique = set()
    with open('tokens.txt', 'r') as file:
        for line in file.read().splitlines():
            unique.add(line)
    with open('tokens.txt', 'w') as file:
        for line in unique:
            file.write(line + '\n')
    log('yellow', 'Removed all duplicated tokens from tokens.txt')
    time.sleep(2)

def get_headers(token):
    xSuper = "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI2LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6Imh0dHBzOi8vd3d3Lmdvb2dsZS5jb20vIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50Ijoid3d3Lmdvb2dsZS5jb20iLCJzZWFyY2hfZW5naW5lX2N1cnJlbnQiOiJnb29nbGUiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjozMDczOTIsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGwsImRlc2lnbl9pZCI6MH0="
    return {
        'Authorization': token,
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0',
        'X-Debug-Options': 'bugReporterEnabled',
        'X-Discord-Locale': 'en-US',
        'X-Super-Properties': xSuper
    }

def load_tokens():
    try:
        tokens_option = input("Load tokens from file (F) or use custom token (C)? ").strip().lower()
        if tokens_option == "f":
            tokens_file = os.path.join(os.path.dirname(__file__), "tokens.txt")
            if not os.path.isfile(tokens_file):
                printwee(f"File 'tokens.txt' not found in the script's directory.", "red")
                return []

            with open(tokens_file, 'r') as file:
                tokens = [line.strip() for line in file if line.strip()]
        elif tokens_option == "c":
            token = input("Enter your token: ").strip()
            tokens = [token]
        else:
            print("Invalid option. Please choose 'F' for file or 'C' for custom token.")
            tokens = []
        return tokens
    except Exception as e:
        printwee(f"An error occurred while loading tokens: {e}", "red")
        return []


def get_random_string(length): return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def solve_captcha(invite_code, token):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        url = f"https://discord.com/invite/{invite_code}"
        driver.get(url)
        
        script = f'''
        function login(token) {{
            setInterval(() => {{
                document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"{token}"`
            }}, 50);
            setTimeout(() => {{
                location.reload();
            }}, 2500);
        }}
        login("{token}");
        '''

        driver.execute_script(script)

        input("Press Enter To Exit...")


    finally:
        driver.quit()

def mass_messenger(tokens, user_id, message, add_random_string, count, tokens_count):
    successful_messages = 0

    try:
        if tokens_count == "all":
            tokens_count = len(tokens)
        else:
            tokens_count = int(tokens_count)

        for token in tokens[:tokens_count]:
            session = tls_client.Session(
                client_identifier='chrome112',
                random_tls_extension_order=True
            )
            session.headers = get_headers(token)
            session.cookies = session.get('https://discord.com').cookies

            dm_channel_url = "https://discord.com/api/v9/users/@me/channels"
            payload = {"recipient_id": user_id}
            dm_channel_response = session.post(dm_channel_url, json=payload)

            if dm_channel_response.status_code == 200:
                channel_id = dm_channel_response.json()["id"]
                message_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

                for _ in range(count):
                    data = {"content": f"**{message}**"}
                    if add_random_string.lower() == 'y':
                        data["content"] += f" | {get_random_string(15)}"

                    message_response = session.post(message_url, json=data)

                    if message_response.status_code == 200:
                        successful_messages += 1
                        printwee(f"Successfully sent message with token: {token}", "green")
                    elif message.status_code == 400:
                        printwee(f"captcha required for token: {token}", "yellow")
                    else:
                        printwee(f"Failed to send message with token {token}: {message_response.status_code}", "red")
            else:
                printwee(f"Failed to create DM channel with token {token}: {dm_channel_response.status_code}", "red")

    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        printwee(f"An error occurred: {e}", "red")

    printwee(f"Successfully sent {successful_messages} messages.", "green")
    return successful_messages

def friend_request(tokens, username, number):
    try:
        session = tls_client.Session(
            client_identifier='chrome112',
            random_tls_extension_order=True
        )
        successful_requests = 0

        if number == "all":
            number = len(tokens)
        else:
            number = int(number)

        for token in tokens[:number]:
            session.headers = get_headers(token)
            data = {
                "username": username
                # Removing "discriminator" since it's no longer used
            }
            response = session.post('https://discord.com/api/v10/users/@me/relationships', json=data)
            
            if response.status_code == 204:
                printwee(f"Friend request sent with token: {token}", "green")
                successful_requests += 1
            elif response.status_code == 429:
                retry_after = response.json().get('retry_after', 5)
                printwee(f"Rate limited with token {token}. Waiting {retry_after} seconds...", "yellow")
                time.sleep(retry_after)
                response = session.post('https://discord.com/api/v10/users/@me/relationships', json=data)
                if response.status_code == 204:
                    printwee(f"Friend request sent after retry with token: {token}", "green")
                    successful_requests += 1
                else:
                    printwee(f"Failed to send friend request after retry with token {token}: {response.status_code}", "red")
            elif response.status_code == 400:
                    printwee(f"captcha required for token: {token}", "yellow")
            else:
                printwee(f"Failed to send friend request with token {token}: {response.status_code}", "red")

        return successful_requests

    except Exception as e:
        printwee(f"An error occurred: {str(e)}", "red")
        return 0

def extract_invite_code(invite_code):
    match = re.match(r'(?:https?://)?discord\.gg/([^/]+)', invite_code)
    if match:
        return match.group(1)
    else:
        return invite_code
    
def join_server(tokens, invite_code, number):
    try:
        session = tls_client.Session(
            client_identifier='chrome112',
            random_tls_extension_order=True
        )
        session.headers = get_headers(tokens[0])
        session.cookies = session.get('https://discord.com').cookies
        successful_joins = 0

        if number == "all":
            number = len(tokens)
        else:
            number = int(number)

        invite_code = extract_invite_code(invite_code)

        for token in tokens[:number]:
            session.headers = get_headers(token)
            data = {"invite_code": invite_code}
            response = session.post(f'https://discord.com/api/v10/invites/{invite_code}', json=data, headers=get_headers(token))
            
            if response.status_code == 200:
                printwee(f"Successfully joined with token: {token}", "green")
                successful_joins += 1
            elif response.status_code == 400:
                    printwee(f"captcha required for token: {token}", "yellow")
            else:
                printwee(f"Failed to join server with token {token}: {response.status_code}", "red")

        return successful_joins
    except Exception as e:
        printwee(f"An error occurred while joining server: {e}", "red")
        return 0

def leave_server(tokens, guild_id, number):
    try:
        successful_leaves = 0
        
        if number == "all":
            number = len(tokens)
        else:
            number = int(number)
        
        for token in tokens[:number]:
            url = f"https://discord.com/api/v9/users/@me/guilds/{guild_id}"
            headers = get_headers(token)
            data = {}
            
            response = requests.delete(url, headers=headers, json=data)
            
            if response.status_code == 204:
                printwee(f"Successfully left server {guild_id} with token: {token}", "green")
                successful_leaves += 1
            elif response.status_code == 400:
                    printwee(f"captcha required for token: {token}", "yellow")
            else:
                printwee(f"Failed to leave server {guild_id} with token {token}: {response.status_code}", "red")
        
        return successful_leaves
    
    except Exception as e:
        printwee(f"An error occurred while leaving server: {e}", "red")
        return 0

def react_to_message(tokens, invite_code, channel_id, message_id, emoji_name, number):
    join_server(tokens, invite_code, number)
    
    emoji = convert_emoji(emoji_name)
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
    successful_reactions = 0
    
    if number == "all":
        number = len(tokens)
    else:
        number = int(number)
    
    try:
        for i in range(number):
            token = tokens[i]
            headers = get_headers(token)
            
            response = requests.put(url, headers=headers)
            
            if response.status_code == 204:
                successful_reactions += 1
                printwee(f"Successfully reacted to message with token: {token}", "green")
            elif response.status_code == 400:
                    printwee(f"captcha required for token: {token}", "yellow")
            else:
                printwee(f"Failed to react to message with token {token}: {response.status_code}", "red")
            
    except Exception as e:
        printwee(f"An error occurred while reacting to message: {e}", "red")

    return successful_reactions

def send_spammer(tokens, invite_code, channel_id, message, add_random_string, count):
    join_server(tokens, invite_code, "all")
    
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    successful_spams = 0
    token_index = 0
    
    try:
        for _ in range(count):
            token = tokens[token_index]
            headers = get_headers(token)
            data = {
                "content": f"**{message}** | {get_random_string(15) if add_random_string.lower() == 'y' else ''}"
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                successful_spams += 1
                printwee(f"Successfully sent message with token: {token}", "green")
            elif response.status_code == 400:
                    printwee(f"captcha required for token: {token}", "yellow")
            else:
                printwee(f"Failed to send message with token {token}: {response.status_code}", "red")
            
            token_index = (token_index + 1) % len(tokens)
            # time.sleep(1)
            
    except Exception as e:
        printwee(f"An error occurred while spamming messages: {e}", "red")

    return successful_spams

def nickname_changer(tokens, nickname, number):
    try:
        url = f"https://discord.com/api/v9/users/@me/nick"
        successful_changes = 0
        if number == "all":
            number = len(tokens)
        else:
            number = int(number)

        for token in tokens[:number]:
            headers = get_headers(token)
            data = {"nick": nickname}
            response = requests.patch(url, headers=headers, json=data)
            if response.status_code == 200:
                successful_changes += 1
                printwee(f"Successfully Changed Nickname For Token: {token}: {response.status_code}", "green")
            elif response.status_code == 400:
                    printwee(f"captcha required for token: {token}", "yellow")
            else:
                printwee(f"Failed To Change Nickname For Token: {token}: {response.status_code}", "red")
        return successful_changes
    except Exception as e:
        printwee(f"An error occurred while changing nickname: {e}", "red")
        return 0

def fake_typing(tokens, channel_id, duration, invite_code, number):
    try:
        url = f"https://discord.com/api/v9/channels/{channel_id}/typing"
        headers_list = [get_headers(token) for token in tokens]

        join_server(tokens, invite_code, number)

        if number == "all":
            number = len(tokens)
        else:
            number = int(number)
        
        end_time = time.time() + duration
        while time.time() < end_time:
            for headers in headers_list[:number]:
                response = requests.post(url, headers=headers)
                if response.status_code != 204:
                    printwee(f"Failed to start typing with status code {response.status_code}", "red")
                    return False
            printwee("Typing...", "red")
            time.sleep(3)

            printwee("Stopped typing...", "red")
            time.sleep(3)

        return True
    except Exception as e:
        printwee(f"An error occurred while simulating typing: {e}", "red")
        return False

def online_tokens(tokens):
    try:
        online_accounts = []
        for token in tokens:
            headers = get_headers(token)
            response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                username = user_data['username'] + '#' + user_data['discriminator']
                online_accounts.append(f"{username} | {token}")
        return online_accounts
    except Exception as e:
        printwee(f"An error occurred while checking online tokens: {e}", "red")
        return []
    
def get_status(tokens):
    try:
        online_accounts = []
        offline_accounts = []
        for token in tokens:
            headers = get_headers(token)
            response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                username = user_data['username'] + '#' + user_data['discriminator']
                online_accounts.append(f"{username} | Online")
            else:
                user_data = response.json()
                username = user_data['username'] + '#' + user_data['discriminator']
                offline_accounts.append(f"{username} | Offline")
        return online_accounts, offline_accounts
    except Exception as e:
        printwee(f"An error occurred while checking online tokens: {e}", "red")
        return []

def join_vc(tokens, channel_id, invite_code, number):
    try:
        join_server(tokens, invite_code, number)

        session = tls_client.Session(
            client_identifier='chrome112',
            random_tls_extension_order=True
        )

        if number == "all":
            number = len(tokens)
        else:
            number = int(number)

        successful_vc_joins = 0

        for token in tokens[:number]:
            session.headers = get_headers(token)
            session.cookies = session.get('https://discord.com').cookies

            join_channel_url = f"https://discord.com/api/v9/channels/{channel_id}/join"
            response = session.post(join_channel_url)

            if response.status_code == 200:
                printwee(f"Joined voice channel successfully with token: {token}", "red")
                successful_vc_joins += 1
            elif response.status_code == 400:
                    printwee(f"captcha required for token: {token}", "yellow")
            else:
                printwee(f"Failed to join voice channel with token {token}: {response.status_code}", "red")

            time.sleep(0.5)  

        return successful_vc_joins

    except Exception as e:
        printwee(f"An error occurred while joining voice channel: {e}", "red")
        return 0

def soundboard_spam(tokens, invite_code, channel_id, sound_id, count=10):
    try:
        join_server(tokens, invite_code, 1)

        successful_spams = 0
        for token in tokens:
            url = f"https://discord.com/api/v9/channels/{channel_id}/call/soundboard/{sound_id}"
            headers = get_headers(token)
            for _ in range(count):
                response = requests.post(url, headers=headers)
                if response.status_code == 204:
                    successful_spams += 1
                time.sleep(1)
        return successful_spams
    except Exception as e:
        printwee(f"An error occurred while spamming soundboard: {e}", "red")
        return 0

def scrape_members(invite_code):
    try:
        invite_code = extract_invite_code(invite_code)
        url = f"https://discord.com/api/v9/invites/{invite_code}?with_counts=true"
        response = requests.get(url)
        
        if response.status_code == 200:
            try:
                invite_data = response.json()
                server_name = invite_data['guild']['name']
                members_count = invite_data.get('approximate_member_count', 'Unknown')
                
                print(f"Server Name: {server_name}")
                print(f"Members Count: {members_count}")
                if 'members' in invite_data['guild']:
                    for member in invite_data['guild']['members']:
                        print(f"{member['user']['username']} | {member['user']['id']}")
                else:
                    printwee(f"No members data found for server '{server_name}'.", "red")
            
            except KeyError as e:
                printwee(f"KeyError: {e}. Response content: {response.content}", "red")
            
            except Exception as e:
                printwee(f"An error occurred: {e}", "red")
        
        else:
            printwee(f"Failed to scrape members. Status code: {response.status_code}. Response content: {response.content}", "red")
    except Exception as e:
        print(f"An error occurred while scraping members: {e}")

def check_server(invite_code):
    try:
        invite_code = extract_invite_code(invite_code)
        url = f"https://discord.com/api/v9/invites/{invite_code}"
        response = requests.get(url)
        return response.status_code == 200
    except Exception as e:
        print(f"An error occurred while checking server: {e}")
        return False

def check_tokens(tokens, result_holder):
    try:
        valid_tokens = []
        invalid_tokens = []
        
        for token in tokens:
            headers = get_headers(token)
            response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
            if response.status_code == 200:
                valid_tokens.append(token)
            else:
                invalid_tokens.append(token)

        result_holder['valid_tokens'] = valid_tokens
        result_holder['invalid_tokens'] = invalid_tokens
    except Exception as e:
        print(f"An error occurred while checking tokens: {e}")
        result_holder['valid_tokens'] = []
        result_holder['invalid_tokens'] = []

def call_user(tokens, user_id):
    try:
        successful_calls = 0
        for token in tokens:
            url = f"https://discord.com/api/v9/users/{user_id}/call"
            headers = get_headers(token)
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                successful_calls += 1
            elif response.status_code == 400:
                    printwee(f"captcha required for token: {token}", "yellow")
        return successful_calls
    except Exception as e:
        print(f"An error occurred while calling user: {e}")
        return 0

def get_recent_messages(token, channel_id, limit=50):
    try:
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}"
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"An error occurred while getting recent messages: {e}")
        return []

def reply_spammer(tokens, invite_code, channel_id, message, add_random_string, count):
    join_server(tokens, invite_code, "all")

    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    successful_spams = 0
    token_index = 0
    
    try:
        for _ in range(count):
            token = tokens[token_index]
            headers = get_headers(token)
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                messages = response.json()
                
                if messages:
                    for msg in messages:
                        reply_to_id = msg["id"]
                        data = {
                            "content": f"**{message}** | {get_random_string(15) if add_random_string.lower() == 'y' else ''}",
                            "message_reference": {"message_id": reply_to_id}
                        }
                        
                        response = requests.post(url, headers=headers, json=data)
                        
                        if response.status_code == 200:
                            successful_spams += 1
                            printwee(f"Successfully replied with token: {token}", "green")
                        elif response.status_code == 400:
                            printwee(f"captcha required for token: {token}", "yellow")
                        else:
                            printwee(f"Failed to reply with token {token}: {response.status_code}", "red")
                
                else:
                    printwee(f"No messages found to reply in channel {channel_id} with token {token}", "red")
            
            else:
                printwee(f"Failed to get messages for token {token}: {response.status_code}", "red")
            
            token_index = (token_index + 1) % len(tokens)

    except ValueError:
        print("Invalid input. Please enter a valid number.")

    return successful_spams

def get_input():
    import msvcrt
    key = b""
    while True:
        key = msvcrt.getch()
        if key in b'\x00\xe0':  
            key = msvcrt.getch()
            if key == b'H': 
                return 'up'
            elif key == b'P':
                return 'down'
        elif key == b'\r': 
            return 'enter'
        elif key == b'\x1b': 
            return 'escape'

logo = r"""
__________       __                __        
\______   \____ |  | _____ _______|__| ______
 |     ___/  _ \|  | \__  \\_  __ \  |/  ___/
 |    |  (  <_> )  |__/ __ \|  | \/  |\___ \ 
 |____|   \____/|____(____  /__|  |__/____  >
                          \/              \/ 
"""

def anim_logo():
    lines = logo.split('\n')
    width = os.get_terminal_size().columns
    centered_logo = '\n'.join(line.center(width) for line in lines)
    for i, char in enumerate(centered_logo):
        if char.strip():
            color = Fore.MAGENTA if i % 2 == 0 else Fore.CYAN
            print(color + char, end='', flush=True)
        else:
            print(char, end='', flush=True)
        time.sleep(0.004)
    print()

def print_logo():
    lines = logo.split('\n')
    width = os.get_terminal_size().columns
    centered_logo = '\n'.join(line.center(width) for line in lines)
    print(Fore.CYAN + centered_logo + Style.RESET_ALL)

def main():
    Keyauth()


    set_window_title("Polaris")
    tokens = load_tokens()
    set_window_title("Loading...")
    
    result_holder = {}
    
    logo_thread = threading.Thread(target=anim_logo)
    tokens_thread = threading.Thread(target=check_tokens, args=(tokens, result_holder))
    
    logo_thread.start()
    tokens_thread.start()
    
    logo_thread.join()
    tokens_thread.join()

    valid_tokens = result_holder.get('valid_tokens', [])
    invalid_tokens = result_holder.get('invalid_tokens', [])

    set_window_title(f"Polaris | Valid Tokens: {len(valid_tokens)} | Invalid Tokens: {len(invalid_tokens)} | Version: {version}")

    choice = 0
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_logo()
        menu_lines = []
        for idx, cmd in enumerate(COMMANDS):
            menu_lines.append(Fore.CYAN + f"{idx}. {cmd}".center(os.get_terminal_size().columns) + Style.RESET_ALL)

        menu_text = '\n'.join(menu_lines)
        print(menu_text.center(os.get_terminal_size().lines))

        try:
            user_input = int(input("\nYour Choice: "))
        except ValueError:
            printwee("Invalid input. Please enter a number corresponding to the command.", "red")
            input("\nPress Enter to continue...")
            continue
        
        if user_input == 0:
            printwee("Exiting Polaris. Goodbye!", "green")
            break
        
        if user_input < 0 or user_input >= len(COMMANDS):
            printwee("Invalid choice. Please enter a valid number corresponding to the command.", "red")
            input("\nPress Enter to continue...")
            continue
        
        choice = user_input

        if choice == 1:
            invite_code = input("Enter invite code: ")
            number = input("Enter number of tokens to use (type 'all' for all tokens): ")
            successful_joins = join_server(valid_tokens, invite_code, number)
            printwee(f"Successfully joined with {successful_joins} accounts.", "green")
        elif choice == 2:
            guild_id = input("Enter guild ID to leave: ")
            number_or_all = input("Enter 'all' to leave all servers or specify a number: ")
            success_count = leave_server(valid_tokens, guild_id, number_or_all)

            if success_count > 0:
                printwee(f"Successfully left {success_count} server(s).", "green")
            else:
                printwee("Failed to leave any servers.", "red")
        elif choice == 3:
            invite_code = input("Enter invite code of the server to spam: ")
            channel_id = input("Enter channel ID to spam messages: ")
            message = input("Enter message to spam: ")
            add_random_string = input("Add random string? (Y/N): ")
            count = int(input("Enter number of messages to send: "))
            successful_spams = send_spammer(valid_tokens, invite_code, channel_id, message, add_random_string, count)
            printwee(f"Successfully sent {successful_spams} messages.", "green")
        elif choice == 4:
            nickname = input("Enter new nickname: ")
            number = input("Enter number of tokens to use (type 'all' for all tokens): ")
            successful_changes = nickname_changer(valid_tokens, nickname, number)
            printwee(f"Successfully changed nickname for {successful_changes} users.", "green")
        elif choice == 5:
            invite_code = input("Enter invite code: ")
            channel_id = input("Enter channel ID to fake typing: ")
            duration = int(input("Enter duration (in seconds) to fake typing: "))
            number = input("Enter number of tokens to use (type 'all' for all tokens): ")
            success = fake_typing(valid_tokens, channel_id, duration, invite_code, number)
            if success:
                printwee("Successfully faked typing.", "green")
            else:
                printwee("Failed to fake typing.", "red")
        elif choice == 6:
            printwee("Working On It...", "green")
            online_accounts = online_tokens(valid_tokens)
            printwee(f"Online tokens: {len(online_accounts)}", "green")
            for account in online_accounts:
                print(account)
        elif choice == 7:
            invite_code = input("Enter invite code of the server: ")
            channel_id = input("Enter channel ID: ")
            message_id = input("Enter message ID: ")
            emoji = input("emoji: ")
            number = input("Enter number of tokens to use (type 'all' for all tokens): ")
            successful_reactions = react_to_message(tokens, invite_code, channel_id, message_id, emoji, number)
            printwee(f"Successfully reacted {successful_reactions} times.", "green")
        elif choice == 8:
            invite_code = input("Enter invite code of the server to join VC: ")
            channel_id = input("Enter channel ID to join VC: ")
            number = input("Enter number of tokens to use (type 'all' for all tokens): ")
            successful_joins = join_vc(valid_tokens, channel_id, invite_code, number)
            printwee(f"Successfully joined VC in {successful_joins} servers.", "green")
        elif choice == 9:
            invite_code = input("Enter invite code of the server to spam soundboard: ")
            channel_id = input("Enter channel ID to spam soundboard: ")
            sound_id = input("Enter sound ID to spam: ")
            count = int(input("Enter number of times to spam: "))
            successful_spams = soundboard_spam(valid_tokens, invite_code, channel_id, sound_id, count)
            printwee(f"Successfully spammed soundboard {successful_spams} times.", "green")
        elif choice == 10:
            invite_code = input("Enter invite code of the server to scrape members: ")
            scrape_members(invite_code)
        elif choice == 11:
            invite_code = input("Enter invite code to check server availability: ")
            success = check_server(invite_code)
            if success:
                printwee("Server is valid and joinable.", "green")
            else:
                printwee("Server is invalid or not joinable.", "red")
        elif choice == 12:
            printwee(f"Valid tokens: {len(valid_tokens)}", "green")
            printwee(f"Invalid tokens: {len(invalid_tokens)}", "red")
        elif choice == 13:
            user_id = input("Enter user ID to send DM: ")
            message = input("Enter message to send: ")
            add_random_string = input("Add random string? (Y/N): ")
            count = int(input("Enter number of times to send: "))
            number = input("Enter number of tokens to use (type 'all' for all tokens): ")
            successful_messages = mass_messenger(valid_tokens, user_id, message, add_random_string, count, number)
            printwee(f"Successfully sent {successful_messages} messages.", "green")
        elif choice == 14:
            user_id = input("Enter user ID to call: ")
            successful_calls = call_user(valid_tokens, user_id)
            printwee(f"Successfully called {successful_calls} users.", "green")
        elif choice == 15:
            invite_code = input("Enter invite code of the server to reply: ")
            channel_id = input("Enter channel ID to reply: ")
            message = input("Enter message to reply: ")
            add_random_string = input("Add random string? (Y/N): ")
            count = int(input("Enter number of times to reply: "))
            successful_spams = reply_spammer(valid_tokens, invite_code, channel_id, message, add_random_string, count)
            printwee(f"Successfully replied {successful_spams} times.", "green")
        elif choice == 16:
            user_id = input("Enter username to send friend request: ")
            number = input("Enter number of tokens to use (type 'all' for all tokens): ")
            successful_requests = friend_request(valid_tokens, user_id, number)
            printwee(f"Successfully sent {successful_requests} friend requests.", "green")
        elif choice == 17:
            user_id = input("Enter Token You Want To Login To: ")
            printwee(f"Logging In...", "green")
            successful_requests = solve_captcha("mushroom", user_id)
        elif choice == 18:
            mother_folder = input("Enter the mother folder path: ")
            printwee(f"Working On It...", "green")
            token_locator(mother_folder)
            printwee(f"Done!", "green")
        elif choice == 19:
            printwee("Working On It...", "green")
            nitro_tokens = check_tokens_for_nitro(valid_tokens)
            print(f"Tokens with Nitro: {len(nitro_tokens)}")
            for token in nitro_tokens:
                print(token)
        elif choice == 20:
            printwee("Working On It...", "green")
            online_accounts, offline_accounts = get_status(valid_tokens)
            printwee(f"Online tokens: {len(online_accounts)}", "green")
            printwee(f"Offline tokens: {len(offline_accounts)}", "green")
            for account in online_accounts:
                print(account)
            for account in offline_accounts:
                print(account)
        else:
            printwee("Invalid choice. Please select a valid option from the menu.", "red")

        input("\nPress Enter to continue...")

if __name__ == "__main__": 
    main()