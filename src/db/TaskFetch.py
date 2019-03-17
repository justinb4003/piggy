import uuid
import json
import sqlalchemy as sa

conn_str = 'mysql+pymysql://piggy:oinkoink@localhost:3306/ircon'
engine = sa.create_engine(conn_str)
conn = engine.connect()
md = sa.MetaData()
task_config = sa.Table('task_config', md, autoload=True, autoload_with=engine)


def display_tasks():
    print("task_config columns: ")
    print(task_config.columns.keys())
    print("BEGIN displaying tasks from DB.")
    qry = sa.select([task_config])
    rs = conn.execute(qry).fetchall()
    print(rs)
    print("END displaying tasks from DB.")


def get_random_uuid():
    return str(uuid.uuid4())


def to_db_json(d):
    return json.dumps(d, indent=4, sort_keys=True, default=str) + "\n"


def get_tasks():
    qry = sa.select([task_config])
    rs = conn.execute(qry).fetchall()
    return [dict(row) for row in rs]


def save_tasks(task_list):
    # Clear out all the current configs.
    # Probably need to be more precise about this eventually...
    conn.execute(sa.delete(task_config))

    for task in task_list:
        print("saving... {}".format(task))
        ins = sa.insert(task_config).values(
                    task_config_id=get_random_uuid(),
                    task_type=type(task).__name__,
                    task_name=task.name,
                    priority=task.get_priority(),
                    json_config=to_db_json(task.export_as_dict()))
        rp = conn.execute(ins)
