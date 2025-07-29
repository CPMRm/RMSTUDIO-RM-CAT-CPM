#!/usr/bin/python

import random
import requests
from time import sleep
import os, signal, sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
import pystyle
from pystyle import Colors, Colorate

from funny import Funny

__CHANNEL_USERNAME__ = "cpmrmstudio"
__GROUP_USERNAME__   = "cpmrmstudiochat"

def signal_handler(sig, frame):
    print("\n Bye Bye...")
    sys.exit(0)

def gradient_text(text, colors):
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ' ':
                color_index = int(((x / (width - 1 if width > 1 else 1)) + (y / (height - 1 if height > 1 else 1))) * 0.5 * (len(colors) - 1))
                color_index = min(max(color_index, 0), len(colors) - 1)  # Ensure the index is within bounds
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text

def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')
    brand_name =  "Car Parking Multiplayer 1 Tool - RMSTUDIO"
    colors = [
        "rgb(255,0,0)", "rgb(255,69,0)", "rgb(255,140,0)", "rgb(255,215,0)", "rgb(173,255,47)", 
        "rgb(0,255,0)", "rgb(0,255,255)", "rgb(0,191,255)", "rgb(0,0,255)", "rgb(139,0,255)",
        "rgb(255,0,255)"
    ]
    colorful_text = gradient_text(brand_name, colors)
    console.print(colorful_text)
    print(Colorate.Horizontal(Colors.rainbow, '======================================================='))
    print(Colorate.Horizontal(Colors.rainbow, '\t         在帳號登入腳本前請先在CPM1登出帳號'))
    print(Colorate.Horizontal(Colors.rainbow, '    密鑰僅可在一個裝置登入使用 分享密鑰不被允許'))
    print(Colorate.Horizontal(Colors.rainbow, f' ‌   𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦: @{__CHANNEL_USERNAME__} 𝐎𝐫 @{__GROUP_USERNAME__}'))
    print(Colorate.Horizontal(Colors.rainbow, '======================================================='))

def load_player_data(cpm):
    response = cpm.get_player_data()
    if response.get('ok'):
        data = response.get('data')
        if 'floats' in data and 'localID' in data and 'money' in data and 'coin' in data:
        
            print(Colorate.Horizontal(Colors.rainbow, '==========[ PLAYER DETAILS ]=========='))
            
            print(Colorate.Horizontal(Colors.rainbow, f'名字   : {(data.get("Name") if "Name" in data else "UNDEFINED")}.'))
                
            print(Colorate.Horizontal(Colors.rainbow, f'帳號ID : {data.get("localID")}.'))
            
            print(Colorate.Horizontal(Colors.rainbow, f'綠鈔   : {data.get("money")}.'))
            
            print(Colorate.Horizontal(Colors.rainbow, f'C幣    : {data.get("coin")}.'))

        else:
            print(Colorate.Horizontal(Colors.rainbow, '! ERROR: new accounts most be signed-in to the game at least once !.'))
            sleep(1)
    else:
        print(Colorate.Horizontal(Colors.rainbow, '! ERROR: seems like your login is not properly set !.'))
        exit(1)


def load_key_data(cpm):

    data = cpm.get_key_data()
    
    print(Colorate.Horizontal(Colors.rainbow, '========[ ACCESS KEY DETAILS ]========'))
    
    print(Colorate.Horizontal(Colors.rainbow, f'Access Key : {data.get("access_key")}.'))
    
    print(Colorate.Horizontal(Colors.rainbow, f'Telegram ID: {data.get("telegram_id")}.'))
    
    print(Colorate.Horizontal(Colors.rainbow, f'代幣 $     : {(data.get("coins") if not data.get("is_unlimited") else "Unlimited")}.'))
        
    

def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            print(Colorate.Horizontal(Colors.rainbow, f'{tag} cannot be empty or just spaces. Please try again.'))
        else:
            return value
            
def load_client_details():
    response = requests.get("http://ip-api.com/json")
    data = response.json()
    print(Colorate.Horizontal(Colors.rainbow, '=============[ 𝐋𝐎𝐂𝐀𝐓𝐈𝐎𝐍 ]============='))
    print(Colorate.Horizontal(Colors.rainbow, f'Ip Address : {data.get("query")}.'))
    print(Colorate.Horizontal(Colors.rainbow, f'Location   : {data.get("city")} {data.get("regionName")} {data.get("countryCode")}.'))
    print(Colorate.Horizontal(Colors.rainbow, f'國家       : {data.get("country")} {data.get("zip")}.'))
    print(Colorate.Horizontal(Colors.rainbow, '===============[ 𝐌𝐄𝐍𝐔 ]==============='))

def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
    return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)

def rainbow_gradient_string(customer_name):
    modified_string = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f'[{interpolated_color}]{char}'
    return modified_string

if __name__ == "__main__":
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        banner(console)
        acc_email = prompt_valid_value("[bold][?] 帳號Gmail[/bold]", "Email", password=False)
        acc_password = prompt_valid_value("[bold][?] 密碼[/bold]", "Password", password=False)
        acc_access_key = prompt_valid_value("[bold][?] 密鑰[/bold]", "Access Key", password=False)
        console.print("[bold cyan][%] Trying to Login[/bold cyan]: ", end=None)
        cpm = Funny(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)
        if login_response != 0:
            if login_response == 100:
                print(Colorate.Horizontal(Colors.rainbow, 'ACCOUNT NOT FOUND.'))
                sleep(2)
                continue
            elif login_response == 101:
                print(Colorate.Horizontal(Colors.rainbow, 'WRONG PASSWORD.'))
                sleep(2)
                continue
            elif login_response == 103:
                print(Colorate.Horizontal(Colors.rainbow, 'INVALID ACCESS KEY.'))
                sleep(2)
                continue
            else:
                print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                print(Colorate.Horizontal(Colors.rainbow, '! Note: make sure you filled out the fields !.'))
                sleep(2)
                continue
        else:
            print(Colorate.Horizontal(Colors.rainbow, 'SUCCESSFUL.'))
            sleep(2)
        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()
            choices = ["0", "1", "2", "3"]
            print(Colorate.Horizontal(Colors.rainbow, '{01}: 皇冠等級                 100k'))
            print(Colorate.Horizontal(Colors.rainbow, '{02}: 自訂ID                  4.5K'))
            print(Colorate.Horizontal(Colors.rainbow, '{03}: 更改目前遊戲帳號綁定的Gmail 50K'))
            print(Colorate.Horizontal(Colors.rainbow, '{04}: 更改目前遊戲帳號的密碼      50K'))
            print(Colorate.Horizontal(Colors.rainbow, '{05}: 車輛資訊(用車輛id查看      5k'))
            print(Colorate.Horizontal(Colors.rainbow, '{0} : 退出腳本'))
            
            print(Colorate.Horizontal(Colors.rainbow, '===============[ 𝐂𝐏𝐌 ]==============='))
            
            service = IntPrompt.ask(f"[bold][?] 選擇一個服務 [red][1-{choices[-1]} or 0][/red][/bold]", choices=choices, show_choices=False)
            
            print(Colorate.Horizontal(Colors.rainbow, '===============[ 𝐂𝐏𝐌 ]==============='))
            
            if service == 0: # Exit
                print(Colorate.Horizontal(Colors.rainbow, f'Thank You for using our tool, please join our telegram channel: @{__CHANNEL_USERNAME__}.'))
            
            elif service == 1: # King Rank
                console.print("[bold red][!] Note:[/bold red]: if the king rank doesn't appear in game, close it and open few times.", end=None)
                console.print("[bold red][!] Note:[/bold red]: please don't do King Rank on same account twice.", end=None)
                sleep(2)
                console.print("[%] Giving you a King Rank: ", end=None)
                if cpm.set_player_rank():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESSFUL'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'Thank You for using our tool, please join our telegram channe: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Please try again.'))
                    sleep(2)
                    continue
            elif service == 2: # Change ID
                print(Colorate.Horizontal(Colors.rainbow, '[?] Enter your new ID.'))
                new_id = Prompt.ask("[?] ID")
                console.print("[%] Saving your data: ", end=None)
                if len(new_id) >= 0 and len(new_id) <= 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999 and (' ' in new_id) == False:
                    if cpm.set_player_localid(new_id.upper()):
                        print(Colorate.Horizontal(Colors.rainbow, 'SUCCESSFUL'))
                        print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'Thank You for using our tool, please join our telegram channe: @{__CHANNEL_USERNAME__}.'))
                        else: continue
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                        print(Colorate.Horizontal(Colors.rainbow, 'Please try again.'))
                        sleep(2)
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Please use valid ID.'))
                    sleep(2)
                    continue
            elif service == 3:#change email
                console.print("[bold]Enter New Email![/bold]")
                new_email = prompt_valid_value("[bold cyan][?] Account New Email[/bold cyan]", "Email", password=False)
                console.print(
                      "[bold red]C[/bold red][bold dark_orange]H[/bold dark_orange][bold yellow]A[/bold yellow]"
                      "[bold green]N[/bold green][bold cyan]G[/bold cyan][bold blue]I[/bold blue]"
                      "[bold magenta]N[/bold magenta][bold violet]G[/bold violet] "
                      "[bold red]E[/bold red][bold dark_orange]M[/bold dark_orange][bold yellow]A[/bold yellow]"
                      "[bold green]I[/bold green][bold cyan]L[/bold cyan][bold blue].[/bold blue]"
                      "[bold magenta].[/bold magenta][bold violet].[/bold violet]",
                       end="")
                if cpm.change_email(new_email):
                    console.print("\n[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold]Thank You for using our tool[/bold]")
                    else: continue            
                else:
                    console.print("\n[bold red]FAILED[/bold red]")
                    console.print("[bold]EMAIL IS ALREADY REGISTERED[/bold]")
                    sleep(2)
                    continue
            elif service == 4:
                console.print("[bold]Enter New Password![/bold]")
                new_password = prompt_valid_value("[bold][?] Account New Password[/bold]", "Password", password=False)
                console.print("[bold red][%] Changing Password [/bold red]: ", end=None)
                if cpm.change_password(new_password):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold white]Thank You for using my tool[/bold white]")
                    else: continue
                else:
                    console.print("[bold cyan]FAILED[/bold cyan]")
                    console.print("[bold cyan]PLEASE TRY AGAIN[/bold cyan]")
                    sleep(2)
                    continue
            elif service == 5:  # Car Info Service
                console.print("[bold cyan][!] Car Info Lookup[/bold cyan]")
                car_id = IntPrompt.ask("[bold][?]Enter Car ID[/bold]")
                car = cpm.car_info(car_id)
                if car:
                    if car.get("ok"):
                        console.print("[bold][red]========[/red][ CAR INFORMATION ][red]========[/red][/bold]")
                        console.print(f"[bold white]   >> Car ID           : {car.get('id')}[/bold white]")
                        console.print(f"[bold white]   >> Spoiler          : {car.get('sp')}[/bold white]")
                        console.print(f"[bold white]   >> HP               : {car.get('hp')} ({car.get('ihp')})[/bold white]")
                        console.print(f"[bold white]   >> NM               : {car.get('nm')} ({car.get('tq')})[/bold white]")
                        console.print(f"[bold white]   >> Front Bumper     : {car.get('fb')}[/bold white]")
                        console.print(f"[bold white]   >> Rear Bumper      : {car.get('rb')}[/bold white]")
                        console.print(f"[bold white]   >> Bodykit          : {car.get('bk')}[/bold white]")
                        console.print(f"[bold white]   >> Incline Rear     : {car.get('ir')}[/bold white]")
                        console.print(f"[bold white]   >> Incline Front    : {car.get('if')}[/bold white]")
                        console.print(f"[bold white]   >> Steering Angle   : {car.get('ang')}[/bold white]")
                        console.print(f"[bold white]   >> Wheel Percentage : {car.get('wtp')}[/bold white]")
                        console.print(f"[bold white]   >> Mileage (km)     : {car.get('km')}[/bold white]")
                        console.print(f"[bold white]   >> Wheel Front      : {car.get('wf')}[/bold white]")
                        console.print(f"[bold white]   >> Wheel Rear       : {car.get('wr')}[/bold white]")
                        console.print(f"[bold white]   >> Police Unlock    : {car.get('pol')}[/bold white]")
                        console.print(f"[bold white]   >> Tyre             : {car.get('tr')}[/bold white]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold white] Thank You for using my tool[/bold white]")
                        else: continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print("[bold red]Not found[/bold red]")
                        sleep(2)
                        continue
                else: continue
                break
            break
            
        
            
              
   
              
