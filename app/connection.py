from sqlalchemy import create_engine, exc
import time

def test_connection(conn_url):
    while 1:
        try:
            e = create_engine(conn_url)
            e.execute('select 1')
        except exc.OperationalError:
            print('Waiting for database...')
            time.sleep(1)
        else:
            break
    print('Connected!')

def commit_tables(db):
    db.create_all()
    db.session.commit()