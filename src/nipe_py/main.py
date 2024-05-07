import click
from nipe_py import Stop, Start, Restart
from nipe_py import Status, Install, Status

@click.group()
def cli():
    pass

@cli.command()
def install():
    """Install dependencies"""
    install = Install()

@cli.command()
def start():
    """Start routing"""
    Start()

@cli.command()
def stop():
    """Stop routing"""
    Stop()

@cli.command()
def restart():
    """Restart the Nipe circuit"""
    Restart()

@cli.command()
def status():
    """See status"""
    Status()


if __name__ == "__main__":
    cli()
