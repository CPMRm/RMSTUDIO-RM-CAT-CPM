--#!/usr/bin/python

import os
import sys
import time
import signal
import random
import requests
from time import sleep
from pyfiglet import figlet_format
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.live import Live
from rich.align import Align
from rich.spinner import Spinner
from rich.progress import track
from pyfiglet import Figlet
from random import randint
import secrets
from rich.prompt import Prompt
from rich.progress import track
import json
from ryderchang2 import rmstudiocpm2  # Your game logic class

__CHANNEL_USERNAME__ = "𝘾𝙋𝙈𝟮 𝙏𝙤𝙤𝙡 𝙍𝙈𝙎𝙏𝙐𝘿𝙄𝙊 𝘾𝙝𝙖𝙣𝙣𝙚𝙡"
__GROUP_USERNAME__   = "𝑪𝑷𝑴𝟐 𝑻𝒐𝒐𝒍 𝑹𝑴𝑺𝑻𝑼𝑫𝑰𝑶 𝑪𝒉𝒂𝒕"


console = Console()
fig = Figlet(font='slant')

# Handle CTRL+C with smooth shutdown
def signal_handler(sig, frame):
    console.print("\n[bold red]✖ Program interrupted. Exiting...[/bold red]")
    time.sleep(0.5)
    console.print("[bold cyan]👑 See you next time, King.[/bold cyan]")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Create rainbow gradient for big text
def gradient_text(text, colors):
    lines = text.splitlines()
    colorful = Text()
    height = len(lines)
    width = max(len(line) for line in lines)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ' ':
                color_index = int(((x / (width - 1 if width > 1 else 1)) + (y / (height - 1 if height > 1 else 1))) * 0.5 * (len(colors) - 1))
                style = Style(color=colors[color_index])
                colorful.append(char, style=style)
            else:
                colorful.append(char)
        colorful.append("\n")
    return colorful

# Final sexy banner
def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')

    # Main VIP Gradient Header
    title_text = fig.renderText("CPM2 Tool RMSTUDIO [2]")
    gradient_colors = ["#FF0000", "#FF8000", "#FFFF00", "#00FF80", "#00FFFF", "#0055FF", "#8000FF"]
    
    with Live(console=console, refresh_per_second=6, transient=True) as live:
        for _ in range(3):  # Animate glowing text
            live.update(Align.center(gradient_text(title_text, gradient_colors)))
            time.sleep(0.2)
            live.update(Align.center(Text("")))
            time.sleep(0.1)

    # Info Panel
    info = Panel.fit(
        "[bold magenta]🧠 Tool:[/bold magenta] [white]Car Parking Multiplayer 2 VIP 工具[/white]\n"
        "[bold magenta]📢 Telegram:[/bold magenta] [bold cyan]@ryderchang666[/bold cyan]  |  [bold cyan]@RMSTUDIO MAIN[/bold cyan]\n"
        "[bold magenta]⚠ 記得:[/bold magenta] [yellow]使用此工具前請先把帳號儲存登出[/yellow]",
        title="[bold blue]🚀 RMSTUDIO VIP Termux[/bold blue]",
        border_style="bright_magenta",
        padding=(1, 3),
    )

    # VIP Bar
    vip_line = Text("═" * 60, style="bold red")

    # Print Final Layout
    console.print(vip_line, justify="center")
    console.print(info, justify="center")
    console.print(vip_line, justify="center")

# Signal handler
def signal_handler(sig, frame):
    console.print("\n[bold red]✖ Program interrupted. Exiting...[/bold red]")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Save profile to file
def save_player_profile(data):
    with open("player_profile.json", "w") as f:
        json.dump(data, f, indent=4)
    console.print("[green]📁 Profile saved as [bold]player_profile.json[/bold][/green]")

# Load and display player data
def load_player_data(cpm, access_key=None):
    response = cpm.get_player_data()

    if isinstance(response, dict) and response.get('ok'):
        data = response.get('data')
        if isinstance(data, dict):
            WalletData = data.get('WalletData', {})
            PlayerStorage = data.get('PlayerStorage', {})

            if all(k in WalletData for k in ('Money', 'Coins')) and all(k in PlayerStorage for k in ('LocalID', 'Name', 'Brakes')):
                name = PlayerStorage.get('Name', 'UNDEFINED')
                local_id = PlayerStorage.get('LocalID', 'UNDEFINED')
                money = WalletData.get('Money', 0)
                coins = WalletData.get('Coins', 0)

                # Animated coin/money count
                console.print("\n[bold cyan]🔄 Fetching Wallet...[/bold cyan]")
                for _ in track(range(20), description="Loading Money & Coins..."):
                    time.sleep(0.02)

                table = Table(title="🚗 [bold yellow]Player Profile[/bold yellow]", box=box.SQUARE, border_style="bright_blue")
                table.add_column("Field", style="bold green", justify="right")
                table.add_column("Value", style="bold white", justify="left")

                table.add_row("👤 名字", str(name))
                table.add_row("🆔 ID", str(local_id))
                table.add_row("💸 綠鈔", f"{money:,}")
                table.add_row("🪙 C幣", f"{coins:,}")
                if access_key:
                    table.add_row("🔐 密鑰", access_key)

                panel = Panel.fit(
                    table,
                    title="[bold green]✓ 玩家資料載入",
                    subtitle="CPM2 VIP Data Viewer",
                    border_style="bold magenta"
                )
                console.print(panel)

                # Save to file
                save_player_profile({
                    "Name": name,
                    "LocalID": local_id,
                    "Money": money,
                    "Coins": coins,
                    "AccessKey": access_key
                })

                # Reload Prompt
                reload = Prompt.ask("\n[bold cyan]🔁 你想要重新載入資料?[/bold cyan]", choices=["y", "n"], default="n")
                if reload.lower() == "y":
                    load_player_data(cpm, access_key)

            else:
                console.print("[bold red]❌ Missing required player fields.[/bold red]")
        else:
            console.print(f"[bold red]❌ Invalid format in response data.[/bold red] → {data}")
    else:
        console.print(f"[bold red]❌ Server response error or 'ok' is False.[/bold red] → {response}")
  
# Show access key info with fallback
def load_key_data(cpm):
    data = cpm.get_key_data()

    access_key = data.get('access_key', 'N/A')
    telegram_id = data.get('telegram_id', 'N/A')
    balance = 'Unlimited' if data.get('is_unlimited') else str(data.get('coins', 0))

    table = Table(box=box.ROUNDED, border_style="bold green", show_header=False)
    table.add_row("🔑 [bold yellow]Access Key[/bold yellow]", str(access_key))
    table.add_row("🆔 [bold yellow]Telegram ID[/bold yellow]", str(telegram_id))
    table.add_row("💰 [bold yellow]Balance[/bold yellow]", str(balance))

    panel = Panel(table, title="🔐 Access Info", border_style="green", padding=(1, 2))
    console.print(panel)

# Show client location with smooth loader
def load_client_details():
    console.print("[cyan]🌍 Fetching client location info...[/cyan]")
    for _ in track(range(15), description="Locating..."):
        time.sleep(0.02)

    try:
        response = requests.get("http://ip-api.com/json", timeout=5)
        data = response.json()
    except Exception as e:
        console.print(f"[bold red]⚠️ Failed to fetch location info: {e}[/bold red]")
        return

    ip = data.get("query", "Unknown")
    city = data.get("city", "Unknown")
    region = data.get("regionName", "")
    country = data.get("country", "")
    isp = data.get("isp", "Unknown")

    location = f"{city}, {region}, {country}"

    table = Table(box=box.SQUARE, border_style="cyan", show_header=False)
    table.add_row("📍 [bold yellow]Location[/bold yellow]", location)
    table.add_row("🌐 [bold yellow]ISP[/bold yellow]", isp)
    table.add_row("🧠 [bold yellow]IP[/bold yellow]", ip)

    panel = Panel(table, title="🌍 Client Details", subtitle="Fetched via IP", border_style="cyan", padding=(1, 2))
    console.print(panel)

    console.print(Panel("[bold magenta]🛠️ Services Loaded Successfully[/bold magenta]", border_style="magenta"))

# Prompt with safe validation
def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(f"[bold cyan]{content}[/bold cyan]", password=password)
        if not value or value.isspace():
            warning = Text(f"⚠️  {tag} cannot be empty or just spaces. Please try again.", style="bold red")
            console.print(warning)
        else:
            return value

# Rainbow interpolator for text
def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (0, 2, 4))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (0, 2, 4))
    interpolated = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
    return '{:02x}{:02x}{:02x}'.format(*interpolated)

# Generate colored text string from name
def rainbow_gradient_string(customer_name):
    modified = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))

    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated = interpolate_color(start_color, end_color, fraction)
        modified += f"[#{interpolated}]{char}"
    return Text.from_markup(modified)

# Cool animated banner splash
def animated_intro(console):
    title = "[bold cyan]🚀 RM Tool[/bold cyan]"
    subtitles = [
        "🔒 Secure. ⚙️ Powerful. 🎮 Game-On!",
        "👑 Powered by RMSTUDIO Ryder Chang",
        f"📡 Connecting to servers..."
    ]
    with Live(console=console, refresh_per_second=10) as live:
        for subtitle in subtitles:
            panel = Panel(Align.center(Text(subtitle, style="bold white"), vertical="middle"),
                          title=title,
                          border_style="green")
            live.update(panel)
            sleep(1)

# Cool loading spinner text
def loading_spinner(console, message="Processing..."):
    with console.status(f"[bold cyan]{message}[/bold cyan]", spinner="dots"):
        sleep(random.uniform(1.2, 2.2))

if __name__ == "__main__":
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        animated_intro(console)
        banner(console)

        acc_email = prompt_valid_value("[bold][?] Account Email[/bold]", "Email", password=False)
        acc_password = prompt_valid_value("[bold][?] Account Password[/bold]", "Password", password=False)
        acc_access_key = prompt_valid_value("[bold][?] Access Key[/bold]", "Access Key", password=False)

        loading_spinner(console, "🔐 Attempting Login")
        cpm = rmstudiocpm2(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)

        if login_response != 0:
            if login_response == 100:
                console.print("[bold red]✖ 找不到此帳號[/bold red]")
            elif login_response == 101:
                console.print("[bold red]✖ 錯誤密碼[/bold red]")
            elif login_response == 103:
                console.print("[bold red]✖ 無效密鑰[/bold red]")
            else:
                console.print("[bold red]✖ 未知錯誤[/bold red]")
                console.print("[bold yellow]! Note[/bold yellow]: Make sure all fields are correctly filled.")
            sleep(2)
            continue
        else:
            console.print("[bold green]✅ 登入成功[/bold green]")
            sleep(1.5)

        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()

            console.rule("[bold cyan]💻 選擇一個服務[/bold cyan]")

            menu_items = [
                "離開",  # 0
                "更改gmail - 10000",
                "更改密碼 - 5000",
                "增加綠鈔 - 4000",
                "自訂名字 - 1000",
                "刪除所有好友 - 2000",
                "皇冠等級 - 6000",
                "解鎖警燈 - 10000",
                "解鎖所有房子 - 10000",
                "解鎖所有煞車 - 5000",
                "解鎖所有輪框 - 6000",
                "解鎖所有男性服裝 - 9000",
                "解鎖所有卡鉗 - 5000",
                "解鎖所有車輛顏色材質 - 5000",
                "解鎖所有人物動作 - 5000",
                "解鎖所有女性服裝 - 9000",
                "解鎖所有車輛警燈 - 7000",
                "解鎖20個車位 - 7000",  # 17
                "解鎖所有車輛的氣壓懸吊 - 6000",  # 18
                "解鎖所有旗子 - 9000",
                "解鎖所有警燈套件 - 20000",
                "每日任務 300C幣 24小時 重置 - 10000",         
                "測試",
]

            choices = [str(i) for i in range(len(menu_items))]

            for index, item in enumerate(menu_items):
                color = "green" if item != "Exit" else "red"
                console.print(f"[bold cyan]({index:02}):[/bold cyan] [{color}]{item}[/{color}]")

            console.print()  # Add spacing
            service = IntPrompt.ask(
                f"[bold][?] 選擇一個服務 [red][0-{choices[-1]}][/red][/bold]",
                choices=choices,
                show_choices=False
            )

            if service == 0:
                console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                break
            elif service == 1: # Change Email
                console.print("[bold cyan][!] 你正在更換你的帳號gmail[/bold cyan]")
                new_email = Prompt.ask("[bold cyan][?] 輸入新的Gmail[/bold cyan]", default="")

                # Basic email format validation (can be more robust)
                if "@" not in new_email or "." not in new_email:
                    console.print("[bold red][!] 錯誤gmail格式. 請重新嘗試[/bold red]")
                    sleep(2)
                    continue

                    console.print(f"[bold cyan][%] Changing Email to {new_email}[/bold cyan]: ", end="")
                if cpm.change_email(new_email):
                    console.print("[bold green]成功[/bold green]")
                    console.print("==================================")
                    console.print(f"[bold yellow][!] 你的gmail已被更換[/bold yellow]")
                else:
                    console.print("[bold red]失敗.[/bold red]")
                    console.print("[bold red][!] 你輸入的gmail已經被另一個帳號註冊過或者發生錯誤[/bold red]")
                sleep(2)
                continue
            elif service == 2: # Change Password
                console.print("[bold cyan][!] 你正在更換你的帳號的密碼[/bold cyan]")
                new_password = Prompt.ask("[bold cyan][?] 輸入新的密碼[/bold cyan]", password=True)

                # Add password strength validation (e.g., minimum length, complexity)
                if len(new_password) < 6:
                    console.print("[bold red][!] 密碼要至少8個字以上[/bold red]")
                    sleep(2)
                    continue

                console.print(f"[bold cyan][%] Changing Password[/bold cyan]: ", end="")
                if cpm.change_password(new_password):
                    console.print("[bold green]成功[/bold green]")
                    console.print("==================================")
                    console.print(f"[bold yellow][!] 你的密碼已更新[/bold yellow]")
                else:
                    console.print("[bold red]失敗.[/bold red]")
                    console.print("[bold red][!] An error occurred while changing your password. Please try again.[/bold red]")
                    sleep(2)
                    continue 
            elif service == 3: # Increase Money
                console.print("[bold cyan][!] 輸入你要的綠鈔數量[/bold cyan]")
                amount = IntPrompt.ask("[bold][?] 數量[/bold]")
                console.print("[bold cyan][%] Saving your data[/bold cyan]: ", end=None)
                if amount > 0 and amount <= 5000000000:
                    if cpm.set_player_money(amount):
                        console.print("[bold green]成功[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] 你想要離開腳本嗎?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]FAILED.[/bold red]")
                        console.print("[bold yellow][!] Please try again.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please use valid values.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 4: # Change Name
                console.print("[bold cyan][!] 輸入你新的名字[/bold cyan]")
                new_name = Prompt.ask("[bold][?] Name[/bold]")
                console.print("[bold cyan][%] Saving your data[/bold cyan]: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 30:
                    if cpm.set_player_name(new_name):
                        console.print("[bold green]成功[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] 你想要離開工具？[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]FAILED.[/bold red]")
                        console.print("[bold yellow][!] Please try again.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please use valid values.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 5: # Delete Friends
                console.print("[bold cyan][%] 正在刪除所有好友[/bold cyan]: ", end=None)
                if cpm.delete_player_friends():
                    console.print("[bold green]成功[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 6: # King Rank
                console.print("[bold red][!] Note:[/bold red]: 如果皇冠等級在遊戲內沒有顯示, 請把帳號登出登入多次")
                console.print("[bold red][!] Note:[/bold red]: 請不要用皇冠等級在你的帳號兩次.", end="\n\n")
                sleep(2)
                console.print("[bold cyan][%] Upgrading Rank[/bold cyan]: ", end=None)
                if cpm.set_player_rank():
                    console.print("[bold green]成功.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 7: # Unlock police 
                console.print("[bold cyan][%] 正在解鎖警燈[/bold cyan]: ", end=None)
                if cpm.unlock_police():
                    console.print("[bold green]成功.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue                    
            elif service == 8: # Unlock Apartments
                console.print("[bold cyan][%] 正在解鎖所有房子[/bold cyan]: ", end=None)
                if cpm.unlock_apartments():
                    console.print("[bold green]成功.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 9: # Unlock Brakes
                console.print("[bold cyan][%] 正在就解鎖煞車[/bold cyan]: ", end=None)
                if cpm.unlock_brakes():
                    console.print("[bold green]成功[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 10: # Unlock Wheels
                console.print("[bold cyan][%] 正在解鎖輪框[/bold cyan]: ", end=None)
                if cpm.unlock_wheels():
                    console.print("[bold green]成功.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 11: # Unlock Clothes
                console.print("[bold cyan][%] 正在解鎖衣服[/bold cyan]: ", end=None)
                if cpm.unlock_clothes():
                    console.print("[bold green]成功.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 12: # Unlock Calipers
                console.print("[bold cyan][%] 正在解鎖卡鉗[/bold cyan]: ", end=None)
                if cpm.unlock_calipers():
                    console.print("[bold green]成功[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue       
            elif service == 13: # Unlock Paint
                console.print("[bold cyan][%] 正在解鎖車輛顏色材質[/bold cyan]: ", end=None)
                if cpm.unlock_paints():
                    console.print("[bold green]成功.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue                     
            elif service == 14: # Unlock animation
                console.print("[bold cyan][%] 正在解鎖所有人物動畫[/bold cyan]: ", end=None)
                if cpm.unlock_animation():
                    console.print("[bold green]成功[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue 
            elif service == 15: # Unlock female
                console.print("[bold cyan][%] 正在解鎖女性角色衣服[/bold cyan]: ", end=None)
                if cpm.unlock_clothess():
                    console.print("[bold green]成功[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 16:  # Unlock All Cars Siren
                console.print("[bold cyan][%] 正在解鎖所有車輛警燈[/bold cyan]: ", end=None)
                if cpm.unlock_all_cars_siren():            
                    console.print("[bold green]成功[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 17: # Unlock Slots
                console.print("[bold cyan][%] 正在解鎖20個車位[/bold cyan]: ", end=None)
                if cpm.unlock_slots():
                    console.print("[bold green]成功[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 18: # Unlock suspension 
                console.print("[bold cyan][%] 解鎖所有車輛氣壓懸吊[/bold cyan]: ", end=None)
                if cpm.unlock_all_suspension():
                    console.print("[bold green]成功[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 19: # Unlock All Flags
                console.print("[bold cyan][%] 正在解鎖所有旗子[/bold cyan]: ", end=None)
                if cpm.unlock_all_flags():
                    console.print("[bold green]成功[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue   
            elif service == 20: # Unlock All PoliceBody
                console.print("[bold cyan][%] 正在解鎖所有車輛套件[/bold cyan]: ", end=None)
                if cpm.unlock_all_police_bodykits():
                    console.print("[bold green]成功[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")  
                    sleep(2)
                    continue                       
            elif service == 21: # Unlock All PoliceBody
                console.print("[bold cyan][%]正在獲取的每日任務300C幣[/bold cyan]: ", end=None)
                if cpm.king_and_daily_rewards():
                    console.print("[bold green]成功.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")  
                    sleep(2)
                    continue
            elif service == 22: # Unlock All PoliceBody
                console.print("[bold cyan][%]正在獲取的每日任務300C幣[/bold cyan]: ", end=None)
                if cpm.generate_localid():
                    console.print("[bold green]成功.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] 你想要離開工具嗎？[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] 感謝您使用我們的工具, 請加入我們的Telegram頻道[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")  
                    sleep(2)
                    continue                    
            else: continue
            break
        break