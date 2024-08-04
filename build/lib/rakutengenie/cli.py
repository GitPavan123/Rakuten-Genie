import click
from InquirerPy import inquirer
import sys


BRIGHT_BLUE = '\033[94m'
RESET = '\033[0m'

ASCII_ART = """
.------------------------------------------------------------------.
|   ____       _          _                ____            _       |
|  |  _ \ __ _| | ___   _| |_ ___ _ __    / ___| ___ _ __ (_) ___  |
|  | |_) / _` | |/ / | | | __/ _ \ '_ \  | |  _ / _ \ '_ \| |/ _ \ |
|  |  _ < (_| |   <| |_| | ||  __/ | | | | |_| |  __/ | | | |  __/ |
|  |_| \_\__,_|_|\_\___,_|\__\___|_| |_|  \____|\___|_| |_|_|\___| |
|                                                                  |
'------------------------------------------------------------------'

Welcome to Rakuten Genie. Your CLI assistant for automated Dockerfile related tasks.

Type 'rakutengenie help' for more info!
"""

CUSTOM_HELP = """
Rakuten Genie CLI

Usage: rakutengenie [OPTIONS] COMMAND [ARGS]...

Commands:
  init    Initialize a new Dockerfile setup
  help    Display this help information

For more information on a specific command, use:
  rakutengenie help
"""

def print_welcome():
    click.echo(f"{BRIGHT_BLUE}{ASCII_ART}{RESET}")

@click.group(invoke_without_command=True, help=CUSTOM_HELP, add_help_option=False, context_settings=dict(help_option_names=['--help']))
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        if '--help' in sys.argv or '-h' in sys.argv:
            click.echo(CUSTOM_HELP)
        else:
            print_welcome()

@cli.command()
def init():
    options = ["Template docker", "Custom docker"]

    selected_option = inquirer.select(
        message="Select an option:",
        choices=options,
        default=options[0] 
    ).execute()

    if selected_option == "Template docker":
        click.echo("Template option selected. Not implemented yet.")  
    else:
        click.echo("Custom option selected. Not implemented yet.")

@cli.command()
def help():
    """Display help information for Rakuten Genie CLI"""
    click.echo(CUSTOM_HELP)

if __name__ == '__main__':
    cli()
