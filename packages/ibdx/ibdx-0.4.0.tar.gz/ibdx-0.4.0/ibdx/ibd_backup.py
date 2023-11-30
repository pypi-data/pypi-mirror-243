import zipfile
from pathlib import Path
import fnmatch
import typer
import logging

from ibdx import __version__
from ibdx.deps import complete_filename
from ibdx.mysql_db_quick import MysqlConn

logger = logging.getLogger(__name__)


def ibd_backup(
    dbname: str = typer.Option(..., '--db', '-d'),
    host: str = typer.Option('127.0.0.1', '--host', '-h'),
    port: int = typer.Option(3306, '--port', '-p'),
    user: str = typer.Option('root', '--user', '-u'),
    password: str = typer.Option('', '--password', '-P'),
    tables_pattern: str = typer.Option('*', '--tables', '-t'),
    fout_path: str = typer.Option(..., '--file', '-f', autocompletion=complete_filename),
    datadir: str = typer.Option(''),
) -> None:
    db = MysqlConn(dbname, host, port, user, password)

    if not datadir:
        res = db.query("show variables like 'datadir';").fetchone()
        if res is None:
            logger.error('cannot get datadir')
            return
        datadir = res[1]
        if not Path(datadir).exists():
            logger.error('datadir does not exists')
            return

    db_dpath = Path(datadir) / dbname
    assert db_dpath.is_dir()

    _out_fpath = Path(fout_path)

    tables = fnmatch.filter(db.get_tables(), tables_pattern)
    if not tables:
        logger.error('no table macthes')
        return

    host_info = db.get_version()
    if _out_fpath.exists():
        logger.error('can not write to an exists archive')
        return

    arc = zipfile.ZipFile(_out_fpath, 'w', zipfile.ZIP_DEFLATED)
    try:
        for table in tables:
            logger.info(f'backing up table: {table}')

            db.query(f'flush tables `{table}` for export;')
            try:
                sql_create = db.query(f'show create table `{table}`;').fetchall()[0][1]
                arc.writestr(f'{table}.sql', sql_create)
                arc.write(db_dpath / f'{table}.ibd', f'{table}.ibd')
                arc.write(db_dpath / f'{table}.cfg', f'{table}.cfg')
                arc.writestr(f'{table}.ibdx', f'ibdx.v{__version__}\n{host_info}')
            finally:
                db.query('unlock tables;')
    finally:
        arc.close()
