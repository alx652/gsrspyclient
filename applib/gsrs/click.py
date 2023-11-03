import click

manager = None
cli = None

def get_manager():
    return manager

def set_manager(m):
    manager=m

def get_cli():
    return cli

def set_cli(c):
    cli=c
