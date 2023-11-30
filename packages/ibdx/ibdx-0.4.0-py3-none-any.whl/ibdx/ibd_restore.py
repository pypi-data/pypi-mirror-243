import zipfile
from pathlib import Path
from contextlib import suppress
import fnmatch
import typer
import logging

from ibdx.mysql_db_quick import MysqlConn
from ibdx.deps import complete_filename

logger = logging.getLogger(__name__)


def ibd_restore(
    dbname: str = typer.Option(..., '--db', '-d'),
    host: str = typer.Option('127.0.0.1', '--host', '-h'),
    port: int = typer.Option(3306, '--port', '-p'),
    user: str = typer.Option('root', '--user', '-u'),
    password: str = typer.Option('', '--password', '-P'),
    tables_pattern: str = typer.Option('*', '--tables', '-t'),
    fin_path: str = typer.Option(..., '--file', '-f', autocompletion=complete_filename),
    datadir: str = typer.Option(''),
) -> None:
    db = MysqlConn(dbname, host, port, user, password)

    if not zipfile.is_zipfile(fin_path):
        logger.error('--file is not a valid archive file')
        return

    if not datadir:
        res = db.query("show variables like 'datadir';").fetchone()
        if res is None:
            logger.error('cannot get datadir')
            return
        datadir = res[1]

    db_path = Path(datadir) / dbname
    assert db_path.is_dir()

    with zipfile.ZipFile(fin_path, 'r', zipfile.ZIP_DEFLATED) as zip_file:
        target_ibd_files = fnmatch.filter(
            zip_file.namelist(),
            f'{tables_pattern}.ibd',
        )
        target_sql_files = fnmatch.filter(
            zip_file.namelist(),
            f'{tables_pattern}.sql',
        )

        for sql_file in target_sql_files:
            table = sql_file.rsplit('.')[0]
            logger.info(f'executing sql: {table}')

            with suppress(Exception):
                sql_create = zip_file.read(sql_file)
                db.query(sql_create)

        for ibd_file in target_ibd_files:
            table = ibd_file.rsplit('.')[0]
            logger.info(f'importing tablespace: {table}')

            try:
                db.query(f'alter table `{table}` discard tablespace')
                logger.info(f'. alter table `{table}` discard tablespace')

                zip_file.extract(f'{table}.ibd', db_path)
                (db_path / f'{table}.ibd').chmod(0o666)
                logger.info(f'.. extract {table}.ibd')
                with suppress(Exception):
                    zip_file.extract(f'{table}.cfg', db_path)
                    logger.info(f'.. extract {table}.cfg')

                db.query(f'alter table `{table}` import tablespace')
                logger.info(f'... alter table `{table}` import tablespace')

            except Exception as e:
                (db_path / f'{table}.ibd').unlink(missing_ok=True)
                (db_path / f'{table}.cfg').unlink(missing_ok=True)

                # db.query(f'drop table if exists `{table}`;')

                logger.error('failed when importing tablespace: ' + str(e))
