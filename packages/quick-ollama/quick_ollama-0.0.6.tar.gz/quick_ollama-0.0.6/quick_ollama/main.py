import shutil
import argparse
import requests
import subprocess as sp
from time import sleep
from datetime import datetime
from pyngrok import ngrok


OLLAMA_INSTALL_URL = 'https://ollama.ai/install.sh'
OLLAMA_INSTALL_FILE = 'ollama.sh'
DEFAULT_MODEL_NAME = 'mistral:instruct'
DEFAULT_OLLAMA_PORT = 11434 


def cmd(command):
    return sp.Popen(command, shell=True).wait()


def cmdb(command):
    return cmd(f"{command} &")


def install_ollama():
    with open(OLLAMA_INSTALL_FILE, 'w') as ollama:
        data = requests.get(OLLAMA_INSTALL_URL).text
        ollama.write(data)

    cmd(f"chmod +x {OLLAMA_INSTALL_FILE}")
    cmd(f"./{OLLAMA_INSTALL_FILE}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL_NAME,
        help="model name",
    )
    parser.add_argument(
        "--model-port",
        type=str,
        default=DEFAULT_OLLAMA_PORT,
        help="model port",
    )
    return parser.parse_args()


def check_ollama_command_exists():
    return shutil.which('ollama') is not None


def start_tunnel(args: argparse.Namespace):
    ngrok.kill()
    ngrok.connect(args.model_port, 'http')
    return ngrok.get_tunnels()


def start_infinit_loop_of_sleep():
    while True:
        print(datetime.now())
        sleep(60 * 2)


def main():
    args = parse_args()

    if not check_ollama_command_exists():
        install_ollama()

    cmd(f"ollama serve")

    if cmd(f"ollama list | grep {args.model}") != 0:
        cmd(f"ollama pull {args.model}")

    tunnels = start_tunnel(args)
    print(tunnels)

    start_infinit_loop_of_sleep()


if __name__ == "__main__":
    main()
    
