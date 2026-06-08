"""
Alohomora — RSA file/directory encryptor
Upgraded version: Rich UI · env-var key loading · crash-safe .bak backups
"""

import sys
import os

# Allow importing from RSA/ subfolder
sys.path.insert(0, os.path.dirname(__file__))

from RSA.rsa_cryptography import RSA, RSAError
from banner import print_banner

import shutil
from math import ceil
from time import sleep, time

from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    FileSizeColumn,
    TotalFileSizeColumn,
    TransferSpeedColumn,
    TaskProgressColumn,
)
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.text import Text
from rich.align import Align
from rich.rule import Rule
from rich.columns import Columns
from rich import box

console = Console()


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header(subtitle: str = ""):
    clear()
    print_banner()
    if subtitle:
        console.print(Rule(f"[bold cyan]{subtitle}[/]", style="cyan"))
        console.print()


def abort(msg: str):
    console.print(f"\n[bold red]  ✖  {msg}[/]")
    sleep(10)


def success(msg: str):
    console.print(f"\n[bold green]  ✔  {msg}[/]")
    sleep(2)


def warn(msg: str):
    console.print(f"\n[bold yellow]  ⚠  {msg}[/]")
    sleep(3)


def key_status_panel(rsa: RSA) -> Panel:
    """Small panel showing current key state."""
    if rsa.keys_loaded():
        bits = rsa.PRIVATE_KEY.key_size
        body = Text.assemble(
            ("  Status : ", "dim"),
            ("Loaded ✔\n", "bold green"),
            ("  Size   : ", "dim"),
            (f"{bits}-bit\n", "bold cyan"),
            ("  Source : ", "dim"),
            (f"{rsa._key_source}\n" if hasattr(rsa, "_key_source") else "—\n", "italic"),
        )
    else:
        body = Text("  No keys loaded yet", style="bold red")
    return Panel(body, title="[bold]Key Pair[/]", border_style="dim", padding=(0, 1))


# ─────────────────────────────────────────────
#  Main Application
# ─────────────────────────────────────────────

class Alohomora:
    def __init__(self):
        self.rsa = RSA()

    # ── Main menu ────────────────────────────

    def run(self):
        header()
        console.print(key_status_panel(self.rsa))
        console.print()

        menu = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
        menu.add_column("key", style="bold cyan", width=1)
        menu.add_column("action", style="bold")

        rows = [
            ("1", "Generate new key pair"),
            ("2", "Load key pair from file / env"),
            ("3", "Encrypt  file or directory"),
            ("4", "Decrypt  file or directory"),
            ("5", "Exit"),
        ]
        for k, v in rows:
            menu.add_row(k, v)

        console.print(Align.left(menu))

        choice = Prompt.ask(
            "\n[bold]Choose option[/]",
            choices=["1", "2", "3", "4", "5"],
            show_choices=True,
        )

        dispatch = {
            "1": self.generate_new_key_pairs,
            "2": self.load_keys_from_file,
            "3": lambda: self.lock(decrypt=False),
            "4": lambda: self.lock(decrypt=True),
            "5": self.exit_app,
        }
        dispatch[choice]()

    # ── Exit ─────────────────────────────────

    def exit_app(self):
        clear()
        console.print(
            Panel(
                Align.center(
                    Text.assemble(
                        ("💀  Don't forget to DELETE your private key!  💀\n\n", "bold red"),
                        ("Thanks for using Alohomora 💖", "bold green italic"),
                    )
                ),
                border_style="yellow",
                padding=(1, 4),
            )
        )
        sleep(1.5)

    # ── Key generation ────────────────────────

    def generate_new_key_pairs(self):
        header("Generate New Key Pair")

        console.print(
            Panel(
                "[dim]Valid range:[/] [bold cyan]530 – 4096[/] bits\n"
                "[dim]Recommended:[/] [bold green]2048[/] or [bold green]4096[/] bits",
                border_style="dim",
                padding=(0, 2),
            )
        )
        console.print()

        try:
            bits = IntPrompt.ask("[bold]Key size (bits)")
            if bits < 530 or bits > 4096:
                abort("Key size out of allowed range [530, 4096].")
                return self.generate_new_key_pairs()
        except (KeyboardInterrupt, EOFError):
            return self.run()

        with console.status(
            f"[bold cyan]Generating {bits}-bit RSA key pair …[/]", spinner="dots"
        ):
            try:
                self.rsa.generate_keys(bits)
                self.rsa._key_source = ".KEYS directory"
            except RSAError as e:
                abort(str(e))
                return self.run()

        success(f"{bits}-bit key pair generated and saved to [cyan].KEYS/[/]")
        self.run()

    # ── Key loading ───────────────────────────

    def load_keys_from_file(self):
        header("Load Key Pair")

        env_priv = os.environ.get("ALOHOMORA_PRIVATE_KEY")
        env_pub  = os.environ.get("ALOHOMORA_PUBLIC_KEY")

        info = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        info.add_column("label", style="dim", width=20)
        info.add_column("value", style="cyan")

        if env_priv and env_pub:
            info.add_row("ALOHOMORA_PRIVATE_KEY", env_priv)
            info.add_row("ALOHOMORA_PUBLIC_KEY",  env_pub)
            info.add_row("Source", "[bold green]Environment variables[/]")
        else:
            info.add_row("Private key", ".KEYS/PRIVATE_KEY.pem")
            info.add_row("Public key",  ".KEYS/PUBLIC_KEY.pem")
            info.add_row("Source", "[bold yellow]Fallback: .KEYS/ directory[/]")

        console.print(info)
        console.print()

        with console.status("[bold cyan]Loading keys …[/]", spinner="dots"):
            try:
                source = self.rsa.load_keys_from_file()
                self.rsa._key_source = source
            except RSAError as e:
                abort(str(e))
                if Confirm.ask("\n[bold]Generate a new 4096-bit key pair instead?"):
                    with console.status("[bold cyan]Generating keys …[/]", spinner="dots"):
                        try:
                            self.rsa.generate_keys(4096)
                            self.rsa._key_source = ".KEYS directory (auto-generated)"
                        except RSAError as e2:
                            abort(str(e2))
                return self.run()

        success(f"Keys loaded from [cyan]{source}[/]  ([green]{self.rsa.PRIVATE_KEY.key_size}[/]-bit)")
        self.run()

    # ── Lock / Unlock entry point ─────────────

    def lock(self, decrypt: bool = False):
        verb = "Decrypt" if decrypt else "Encrypt"
        header(f"{verb} File or Directory")

        if not self.rsa.keys_loaded():
            abort("No keys loaded! Generate or load a key pair first.")
            return self.run()

        path = Prompt.ask("[bold]Absolute path to file or directory")

        if not os.path.exists(path):
            abort(f"Path does not exist: [cyan]{path}[/]")
            return self.lock(decrypt)

        is_dir = os.path.isdir(path)
        self.encrypt_decrypt_dashboard(path, decrypt=decrypt, is_dir=is_dir)

    # ── Core enc/dec engine ───────────────────

    def encrypt_decrypt_dashboard(
        self, root_path: str, decrypt: bool = False, is_dir: bool = False
    ):
        verb    = "Decrypt" if decrypt else "Encrypt"
        verb_ed = "Decrypted" if decrypt else "Encrypted"
        header(f"{verb}ing {'Directory' if is_dir else 'File'}")

        # ── Collect files ──
        with console.status("[bold cyan]Scanning files …[/]", spinner="dots"):
            if is_dir:
                file_list = list(self._get_all_files(root_path))
            else:
                file_list = [root_path]
            total_size = sum(os.path.getsize(p) for p in file_list)

        # ── Show summary table ──
        summary = Table(show_header=False, box=box.ROUNDED, padding=(0, 2), border_style="cyan")
        summary.add_column("k", style="dim")
        summary.add_column("v", style="bold")
        summary.add_row("Operation", f"[{'red' if decrypt else 'green'}]{verb}[/]")
        summary.add_row("Files",     str(len(file_list)))
        summary.add_row("Total size", _fmt_size(total_size))
        summary.add_row("Key size",  f"{self.rsa.PRIVATE_KEY.key_size}-bit")
        if is_dir:
            summary.add_row("Directory", root_path)
        console.print(summary)
        console.print()

        # ── Pre-flight: check for leftover .bak files ──
        stale_baks = [p + ".bak" for p in file_list if os.path.exists(p + ".bak")]
        if stale_baks:
            console.print(
                Panel(
                    "[bold red]Stale backup (.bak) files detected from a previous crash:[/]\n\n"
                    + "\n".join(f"  [cyan]{b}[/]" for b in stale_baks)
                    + "\n\n[yellow]Please inspect these files before proceeding.\n"
                    "They may contain your last uncorrupted data.[/]",
                    title="[bold red]⚠  Aborted[/]",
                    border_style="red",
                    padding=(1, 2),
                )
            )
            sleep(3)
            return self.run()

        if not Confirm.ask(f"[bold]Proceed with {verb.lower()}ion of {len(file_list)} file(s)?"):
            return self.run()

        # ── Process each file ──
        block_size = self.rsa.MAX_CIPHER_LENGTH if decrypt else self.rsa.MAX_BYTES

        progress = Progress(
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(bar_width=30),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console,
            expand=True,
        )

        overall_task = None
        file_task    = None

        errors = []

        with progress:
            overall_task = progress.add_task(
                f"[bold]{verb}ing …", total=len(file_list)
            )

            for idx, file_path in enumerate(file_list, 1):
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                bak_path  = file_path + ".bak"

                file_task = progress.add_task(
                    f"[dim]{file_name[:40]}",
                    total=file_size,
                )

                try:
                    # 1) Create backup
                    shutil.copy2(file_path, bak_path)

                    # 2) Read original
                    with open(file_path, "rb") as fh:
                        data = fh.read()

                    input_size = len(data)

                    # 3) Write encrypted/decrypted output directly over original
                    with open(file_path, "wb") as fh:
                        offset = 0
                        while offset < input_size:
                            chunk = data[offset : offset + block_size]
                            if decrypt:
                                fh.write(self.rsa.decrypt(chunk))
                            else:
                                fh.write(self.rsa.encrypt(chunk))
                            offset += block_size
                            progress.advance(file_task, min(block_size, input_size - (offset - block_size)))

                    # 4) Remove backup — we're safe now
                    os.remove(bak_path)

                except Exception as exc:
                    errors.append((file_path, str(exc)))
                    # Restore from backup if it exists
                    if os.path.exists(bak_path):
                        try:
                            shutil.copy2(bak_path, file_path)
                            os.remove(bak_path)
                            errors[-1] = (file_path, f"{exc}  [backup restored]")
                        except Exception:
                            errors[-1] = (file_path, f"{exc}  [⚠ backup restore FAILED — .bak kept]")

                progress.advance(overall_task, 1)
                progress.remove_task(file_task)

        # ── Results ──
        console.print()
        if errors:
            err_table = Table(
                "File", "Error",
                title="[bold red]Errors[/]",
                box=box.ROUNDED,
                border_style="red",
            )
            for fp, msg in errors:
                err_table.add_row(fp, msg)
            console.print(err_table)
        else:
            console.print(
                Panel(
                    f"[bold green]✔  {verb_ed} {len(file_list)} file(s) successfully.[/]",
                    border_style="green",
                    padding=(0, 2),
                )
            )

        sleep(2)
        self.run()

    # ── Utilities ─────────────────────────────

    def _get_all_files(self, directory: str):
        for root, _dirs, files in os.walk(directory):
            for fname in files:
                yield os.path.join(root, fname)


# ─────────────────────────────────────────────
#  Misc helpers
# ─────────────────────────────────────────────

def _fmt_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    try:
        app = Alohomora()
        app.run()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Interrupted. Exiting.[/]")
        sys.exit(0)