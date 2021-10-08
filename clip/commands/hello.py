import click 

from clip.service import weather 

class Context:
  def __init__(self, location):
    self.location = location 
    self.weather = weather.Weather()


@click.group()
@click.option('-l', '--location', type=str, help='weather at this location')
@click.pass_context
def cli(ctx, location):
  '''Weather info'''
  ctx.object = Context(location)

@cli.command()
def cli(ctx):
  click.echo(ctx.obj.location)