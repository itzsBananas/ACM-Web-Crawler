import crawl
import sqlalchemy
from dotenv import load_dotenv
import os
from flask import Flask, Response


app = Flask(__name__)


load_dotenv()

# logger = logging.getLogger()

def init_db_connection():
    db_config = {
        'pool_size': 5,
        'max_overflow': 2,
        'pool_timeout': 30,
        'pool_recycle': 1800,
    }
    return init_unix_connection_engine(db_config)

def init_unix_connection_engine(db_config):
    username=os.environ.get('DB_USER')
    password=os.environ.get('DB_PASS')
    # database=os.environ.get('DB_NAME')
    host=os.environ.get('DB_HOST')
    port=os.environ.get('DB_PORT')
    pool = sqlalchemy.create_engine(
        "postgresql://{}:{}@{}:{}/postgres".format(
            username,
            password,
            host,
            port
        ),
        **db_config
    )
    pool.dialect.description_encoding = None
    return pool

db = init_db_connection()


@app.route('/', methods=['POST'])
def main():
    stmt = sqlalchemy.text("INSERT INTO records(link, name, due_date, desc, prize)"
                    "VALUES (:link, :name, :due_date, :desc, :prize)")
    data = crawl.crawl()
    try:
        with db.connect() as conn:
            for d in data[0:1]:
                conn.execute(stmt,
                            link = d["link"],
                            name = d["name"],
                            due_date = d["due_date"],
                            desc = d["desc"],
                            prize = d["prize"])
        pass
    except Exception as e:
        return Response(
            status=500,
            response="Unable to successfully enter information!"
        )
    return Response(
        status=200,
        response="Succesfully entered information"
    )



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)