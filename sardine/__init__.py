import asyncio
import importlib
import os
import sys
from pathlib import Path
from sys import argv

from rich import print
from rich.panel import Panel

try:
    import uvloop
except ImportError:
    print("[yellow]UVLoop is not installed. Not supported on Windows![/yellow]")
    print("[yellow]Rhythm accuracy may be impacted[/yellow]")
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    uvloop.install()

from .base import *
from .clock import *
from .fish_bowl import *
from .handlers import *
from .io.UserConfig import (
    pretty_print_configuration_file,
    read_user_configuration,
)
from .sequences.SardineParser.ListParser import ListParser
from .utils.Messages import config_line_printer, sardine_intro

config = read_user_configuration()

# | INITIALISATION |#
CRASH_TEST = False

# Reading user configuration
config = read_user_configuration()

hook_path = argv[0]
if "__main__.py" in hook_path:
    os.environ["SARDINE_INIT_SESSION"] = "YES"

if (
    os.getenv("SARDINE_INIT_SESSION") is not None
    and os.getenv("SARDINE_INIT_SESSION") == "YES"
):
    print(sardine_intro)
    print(config_line_printer(config))

    # Load user config
    if Path(f"{config.user_config_path}").is_file():
        spec = importlib.util.spec_from_file_location(
            "user_configuration", config.user_config_path
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        from user_configuration import *
    else:
        print(f"[red]No user provided configuration file found...")

    # Real initialisation takes place here ############################
    bowl = FishBowl(
        clock=InternalClock(tempo=config.bpm, bpb=config.beats),
    )

    # Adding a parser
    # bowl.swap_parser(ListParser)

    # Adding Senders
    # bowl.add_handler(MidiHandler())
    # bowl.add_handler(OSCHandler())
    # bowl.add_handler(SuperColliderHandler(name="Custom SuperCollider Connexion"))
    # bowl.add_handler(SuperDirtHandler())

    if CRASH_TEST:
        @swim
        def dummy_swimming_function():
            print('Hello there, I am swimming again!')
            M('60').out()
            S('bd').out()
            O('/hello/', value=1, other=2, otherother=3).out()

        Pa >> play('bd')
        Pb >> play_midi('60,67')
        Pc >> play_osc('/hello/surf/', value=1, other=2, otherother=3)
