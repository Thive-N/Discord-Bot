import json
import os
import shutil
import sqlite3


class ConfigParser:
    """
    config parser to load most of the bot configuration
    """

    def __init__(self) -> None:
        self.config_file = './src/config/config.json'
        self.load_config()

    def load_config(self) -> None:
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

    def push_config(self) -> None:
        with open(self.config, 'w') as f:
            json.dump(self.config_file, f, indent=4, sort_keys=True)

    def get_prefix(self) -> str:
        return self.config['prefix']

    def get_db_columns(self) -> [str, str]:
        return self.config['guild_db_columns']

    def push_db_column(self, column: [str, str]) -> None:
        self.load_config()
        self.config['guild_db_columns'].append(column)
        self.push_config()


class DatabaseManager:
    def __init__(self):
        self.config_parser = ConfigParser()
        self.update_columns()
        print(self.columns)
        self._dbjson = './src/databases/databases.json'
        self._database_path = os.path.dirname(self._dbjson)

        if not os.path.exists(self._dbjson):
            self.make_database_json()
        with open(self._dbjson, 'r') as f:
            self.database_config = json.load(f)

    def update_columns(self) -> None:
        self.columns = self.config_parser.get_db_columns()

    def add_column(self, name: str, col_type: str) -> None:
        self.config_parser.push_db_column([name, col_type])
        self.update_columns()

    def get_guilds(self) -> [str]:
        with open(self._dbjson, 'r') as f:
            return json.load(f)['guilds']

    def add_guild_entry_json(self, guild_id: str) -> None:
        with open(self._dbjson, 'r') as f:
            temp = json.load(f)
            temp['guilds'].append(guild_id)
        with open(self._dbjson, 'w') as f:
            json.dump(temp, f, indent=4, sort_keys=True)

    def add_guild_entry(self, guild_id: str) -> None:
        try:
            os.mkdir('./src/databases/{}'.format(guild_id))
        except FileExistsError:
            print('guild entry already exists')
            return
        self.add_guild_entry_json(guild_id)
        self.create_guild_entry_database(guild_id)

    def create_guild_entry_database(self, guild_id) -> None:
        with open('{0}/{1}/guild.json'.format(self._database_path, guild_id), 'w') as f:
            json.dump('', f)

        sql = self.connect_db(guild_id)
        sql_cursor = sql.cursor()
        sql_cursor.execute(
            "CREATE TABLE IF NOT EXISTS Users (UserID int PRIMARY KEY,{})".format(self.columns_format_for_table_creation()))

    def columns_format_for_table_creation(self) -> str:
        """
        do not use this anywhere with userinput unless your stupid and want to be sql injected
        only for use inside this class
        """
        temp = []
        for x in self.columns:
            temp.append(x[0] + ' ' + x[1])

        return ','.join(temp)

    def columns_format_for_user_add(self, user_id: int) -> None:
        """
        do not use this anywhere with userinput unless your stupid and want to be sql injected
        only for use inside this class
        """
        return '('+(','.join([x[0] for x in self.columns]))+') VALUES (' + ','.join(['NULL' for _ in range(len(self.columns))]) + ')'

    def connect_db(self, guild_id: str) -> sqlite3.Connection:
        return sqlite3.connect(
            '{0}/{1}/guild.db'.format(self._database_path, guild_id))

    def set_value(self, guild_id: str, user_id: int, value: int, value_type: str) -> None:
        sql = self.connect_db(guild_id)
        sql_cursor = sql.cursor()
        sql_cursor.execute("UPDATE Users set {0} = {1} where userid = {2}"
                           .format(value_type, value, user_id))
        sql.commit()

    def get_value(self, guild_id: str, user_id: int, value_type: str) -> int:
        sql = self.connect_db(guild_id)
        sql_cursor = sql.cursor()
        sql_cursor.execute(
            'SELECT {1} FROM Users WHERE userid = {0}; '.format(user_id, value_type))
        return sql_cursor.fetchall()[0][0]

    def add_to_int_value(self, guild_id: str, user_id: int, value: int, value_type: str):
        value += self.get_value(guild_id, user_id, value_type)
        self.set_value(guild_id, user_id, value, value_type)

    def add_to_database(self, guild_id: str, user_id: int) -> None:
        sql = self.connect_db(guild_id)
        sql_cursor = sql.cursor()
        sql_cursor.execute(
            "INSERT INTO Users (UserID,Money) VALUES (?,?)", (user_id, 0))
        sql.commit()

    def make_database_json(self) -> None:
        """
        this function will completly reset the database/database.json with the template below
        """

        with open(self._dbjson, 'w') as f:
            template = {"guilds": []}
            json.dump(template, f, indent=4, separators=(", ", ": "))

    def clean_databases(self) -> None:
        """
        cleans the databases directory completly
        """
        shutil.rmtree(self._database_path)
        os.mkdir(self._database_path)
        self.make_database_json()


if __name__ == '__main__':
    dbm = DatabaseManager()
    dbm.clean_databases()

    dbm.add_guild_entry('1111111111')
    dbm.add_to_database('1111111111', 898989089)
    print(dbm.get_value('1111111111', 898989089, 'money'))
    dbm.add_to_int_value('1111111111', 898989089, 23, 'money')
    print(dbm.get_value('1111111111', 898989089, 'money'))


# conn.execute("UPDATE COMPANY set SALARY = 25000.00 where ID = 1")
# conn.commit()
# indent=4, separators=(", ", ": "), sort_keys=True
# INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country)
# VALUES ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger', '4006', 'Norway');
