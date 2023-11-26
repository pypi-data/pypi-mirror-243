from .db import get_db
from datetime import datetime
from sqlite3 import Connection


# Define CONFIG Constants
EMPTY_STRING: str = ''
ZERO_INTEGER: int = 0
TYPE_AFFINITY_NONE: int = 0
TYPE_AFFINITY_INTEGER: int = 1
TYPE_AFFINITY_TEXT: int = 2
TYPE_AFFINITY_BLOB: int = 3
TYPE_AFFINITY_REAL: int = 4
TYPE_AFFINITY_NUMERIC: int = 5


class CONFIG:
    # CONFIG table fields
    id: int
    name: str
    description: str
    config_value: str
    config_value_type: int
    user_id: int
    created_dt_tm: datetime
    updated_dt_tm: datetime
    is_active: bool

    def __init__(self, **fields) -> None:
        self.id = fields.get('id', ZERO_INTEGER)
        self.name = fields.get('name', EMPTY_STRING)
        self.description = fields.get('description', EMPTY_STRING)
        self.config_value = fields.get('config_value', EMPTY_STRING)
        self.config_value_type = fields.get('config_value_type', TYPE_AFFINITY_NONE)
        self.user_id = fields.get('user_id', ZERO_INTEGER)
        self.created_dt_tm = fields.get('created_dt_tm', datetime.now())
        self.updated_dt_tm = fields.get('updated_dt_tm', datetime.now())
        self.is_active = fields.get('is_active', True)

    def __repr__(self) -> str:
        config: dict = {
            'id': self.id
            , 'name': self.name
            , 'description': self.description
            , 'config_value': self.config_value
            , 'config_value_type': self.config_value_type
            , 'user_id': self.user_id
            , 'created_dt_tm': self.created_dt_tm.isoformat()
            , 'updated_dt_tm': self.updated_dt_tm.isoformat()
            , 'is_active': self.is_active
        }

        return str(config)

    def get(self) -> None:
        get_config: str = ''

        if self.id > 0:
            get_config: str = 'SELECT * FROM CONFIG WHERE id = ? AND is_active = ?'
        elif self.name and self.user_id:
            get_config: str = 'SELECT * FROM CONFIG WHERE name = ? AND user_id = ? AND is_active = ?'
        else:
            raise Exception("Config class requires id or name and user_id.")

        db: Connection = get_db()

        try:
            config = db.execute(get_config, [
                self.name,
                self.user_id,
                self.is_active
            ]).fetchone()

            self.id = config['id']
            self.description = config['description']
            self.config_value = config['config_value']
            self.config_value_type = config['config_value_type']
            self.user_id = config['user_id']
            self.created_dt_tm = datetime.fromisoformat(config['created_dt_tm'])
            self.updated_dt_tm = datetime.fromisoformat(config['updated_dt_tm'])
            self.is_active = config['is_active']
        except Exception as e:
            print(e)

        db.close()
