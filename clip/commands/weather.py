import click
from clip.service import weather
import time 

class Context:
  def __init__(self, location):
    self.location = location
    self.weather = weather.Weather()


@click.group()
@click.option('-l', '--location', type=str, help='Weather at this location')
@click.pass_context
def cli(ctx, location):
  '''WEATHER INFO'''
  # click.echo(ctx.obj.location)
  ctx.obj = Context(location)
  pass

@cli.command()
@click.pass_context
def current(ctx):
  result = ctx.obj.weather.current(location=ctx.obj.location)
  click.echo(f' {result["location"]} - {result["status"].upper()}'.center(45, '='))
  click.echo(f'\U0001F525 Temp: {result["temp"]} - {result["min"]}/{result["max"]} (min/max)')
  click.echo(f'\U0001F32A Wind: {round(result["wind"], 1)}')
  click.echo(f'\U0001F4A7 Rain: {result["rain"]}')
  click.echo(
    f'\U0001F315 Sunrise: {time.strftime("%H:%m", time.localtime(result["sun_rise"]))} - '
    f'Sunset: {time.strftime("%H:%m", time.localtime(result["sun_set"]))} \U0001F311'
  )

def convert_epoch_to(epoch, fmt):
  return time.strftime(fmt, time.localtime(epoch))

def is_around_midday(epoch):
  return 11 <= int(convert_epoch_to(epoch, '%H')) <= 13

@cli.command()
@click.pass_context
def forecast(ctx, location=None, interval='3h'):
  result = ctx.obj.weather.current(location=ctx.obj.location)
  to_display = [wx for wx in ctx.obj.weather.forecast(location=ctx.obj.location) if is_around_midday(wx["time"])]

