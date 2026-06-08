from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich import print as rprint

ASCII_ART = """\
 ▄▄▄· ▄▄▌         ▄ . ▄      • ▌ ▄ ·.       ▄▄▄   ▄▄▄·
▐█ ▀█ ██•  ▪     ██▪ ▐█▪     ·██ ▐███▪▪     ▀▄ █·▐█ ▀█
▄█▀▀█ ██▪   ▄█▀▄ ██▀▀▐█ ▄█▀▄ ▐█ ▌▐▌▐█· ▄█▀▄ ▐▀▀▄ ▄█▀▀█
▐█ ▪▐▌▐█▌▐▌▐█▌.▐▌██▌ ▐▀▐█▌.▐▌██ ██▌▐█▌▐█▌.▐▌▐█•█▌▐█ ▪▐▌
 ▀  ▀ .▀▀▀  ▀█▄▀▪▀▀▀  · ▀█▄▀▪▀▀  █▪▀▀▀ ▀█▄▀▪.▀  ▀ ▀  ▀\
"""

def print_banner():
    art = Text(ASCII_ART, style="bold blue", justify="center")
    subtitle = Text("🔐  hide secrets  🔐", style="bold yellow", justify="center")
    content = Text.assemble(art, "\n\n", subtitle)
    panel = Panel(Align.center(content), border_style="blue", padding=(0, 2))
    rprint(panel)