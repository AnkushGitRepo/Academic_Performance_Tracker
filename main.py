from rich.console import Console
from cli.faculty_cli import faculty_menu
from cli.student_cli import student_menu


def main():
    console = Console()
    while True:
        console.print("\n[bold blue]Welcome to the Academic Performance Tracker[/bold blue]")
        console.print("Select a login option:")
        console.print("1. Log In as Faculty")
        console.print("2. Log In as Student")
        console.print("3. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            faculty_menu()
        elif choice == "2":
            student_menu()
        elif choice == "3":
            console.print("[green]Exiting the application. Goodbye![/green]")
            break
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")


if __name__ == '__main__':
    main()
