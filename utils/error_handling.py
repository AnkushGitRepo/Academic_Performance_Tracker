from rich.console import Console

console = Console()

def log_error(message, error):
    console.print(f"[red]{message}: {error}[/red]")
