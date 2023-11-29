import click


def prog(cnt=3, mark="."):
    click.secho(mark * cnt, nl=False)


def success():
    click.secho("OK", bold=True, fg="green", nl=False)
    click.secho("")


def fail():
    click.secho("FAIL", bold=True, fg="red", nl=False)
    click.secho("")


def start(name, nl=False):
    click.secho(name, nl=nl)
