import zipfile
import typer
import logging

from ibdx.ibd_backup import ibd_backup
from ibdx.ibd_restore import ibd_restore
from ibdx.deps import complete_filename

logging.basicConfig(level='INFO')
cli = typer.Typer()


cli.command('backup')(ibd_backup)
cli.command('restore')(ibd_restore)


@cli.command()
def ls(zipfile_name: str = typer.Argument('', autocompletion=complete_filename)):
    try:
        if not zipfile.is_zipfile(zipfile_name):
            raise Exception('zipfile_name is not a zip file')
        zip_file = zipfile.ZipFile(zipfile_name, 'r', zipfile.ZIP_DEFLATED)

        for name in zip_file.namelist():
            typer.echo(name)
    except Exception as e:
        typer.echo(f'ibdx error: {e}')
