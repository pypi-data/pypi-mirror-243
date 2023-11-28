import click
from .image_handler import ImageHandler

def print_version(ctx, param, value):
    """Print the version of the program"""
    if not value or ctx.resilient_parsing:
        return
    click.echo('pyencry version 0.2.0')
    ctx.exit()

@click.command()
@click.option('-v', '--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.option('-f', '--file', help='The file to use to encode/decode the data\n should be a PNG image', required=True)
@click.option('-e', '--encode', help='Encode data into the image', is_flag=True, default=False)
@click.option('-d', '--decode', help='Decode data from the image', is_flag=True, default=False)
@click.option('-m', '--method', type=click.Choice(['rail_fence_cipher', 'random_spacing'], case_sensitive=False), help='The method to use to encode/decode the data', default='rail_fence_cipher', required=True)
@click.option('-d', '--data', help='The data to encode\n Only used if the --encode flag are used')
@click.option('--new-file', help='The file to write the encoded image to\n Only used if the --encode flag are used')
@click.argument('key')
def cli(key, file, encode, decode, method, data, new_file):
    """Encode and decode data into and from images"""
    if not file:
        raise click.BadParameter('No file was given')

    if not key:
        raise click.BadParameter('No key was given')

    if not encode and not decode:
        raise click.BadParameter('No encode or decode flag was given')

    if encode and decode:
        raise click.BadParameter('Both encode and decode flags was given')

    if encode:
        if not data:
            raise click.BadParameter('No data was given')

        if not new_file:
            raise click.BadParameter('No new file was given')

        image = ImageHandler(file)
        image.encode(method, data=data, key=int(key))
        image.write(new_file)
    else:
        image = ImageHandler(file)
        click.echo(image.decode(method, key=int(key)))
