import shutil
from colors import *

TERMINAL_WIDTH = shutil.get_terminal_size().columns
LEFT_PADDING = (TERMINAL_WIDTH - 55) // 2
RIGHT_PADDING = TERMINAL_WIDTH - 55 - LEFT_PADDING

BANNER_TEXT = BLUE + f'''
{" "*LEFT_PADDING} ▄▄▄· ▄▄▌         ▄ . ▄      • ▌ ▄ ·.       ▄▄▄   ▄▄▄· {" "*RIGHT_PADDING}
{" "*LEFT_PADDING}▐█ ▀█ ██•  ▪     ██▪ ▐█▪     ·██ ▐███▪▪     ▀▄ █·▐█ ▀█ {" "*RIGHT_PADDING}
{" "*LEFT_PADDING}▄█▀▀█ ██▪   ▄█▀▄ ██▀▀▐█ ▄█▀▄ ▐█ ▌▐▌▐█· ▄█▀▄ ▐▀▀▄ ▄█▀▀█ {" "*RIGHT_PADDING}
{" "*LEFT_PADDING}▐█ ▪▐▌▐█▌▐▌▐█▌.▐▌██▌ ▐▀▐█▌.▐▌██ ██▌▐█▌▐█▌.▐▌▐█•█▌▐█ ▪▐▌{" "*RIGHT_PADDING}
{" "*LEFT_PADDING} ▀  ▀ .▀▀▀  ▀█▄▀▪▀▀▀  · ▀█▄▀▪▀▀  █▪▀▀▀ ▀█▄▀▪.▀  ▀ ▀  ▀ {" "*RIGHT_PADDING}\n
{" "*((TERMINAL_WIDTH - 18)//2)+YELLOW+BOLD}🔐 hide secrets 🔐{" "*((TERMINAL_WIDTH - (TERMINAL_WIDTH - 18)//2) -18)}{END}\n
'''