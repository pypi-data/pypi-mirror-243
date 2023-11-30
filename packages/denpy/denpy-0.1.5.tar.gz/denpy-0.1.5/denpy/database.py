import sqlite3
import inspect

def get(table: str, value: str, where: str = None, and_where: list = None, fetchone: bool = True, cog_file: bool = True, filename: str = 'database.db') -> str | None | list:
    # Get database file path
    path = inspect.getmodule(inspect.currentframe().f_back).__file__.replace('\\', '/').split('/')
    path.pop(-1)
    if cog_file is True:
        path.pop(-1)
    path.append(filename)
    path = '/'.join(path)

    # Connect with database
    database = sqlite3.connect(path)
    cursor = database.cursor()

    # Get data
    if where is None:
        if fetchone is True:
            item = cursor.execute(f'SELECT {value} FROM {table}').fetchone()
        else:
            item = cursor.execute(f'SELECT {value} FROM {table}').fetchall()
    else:
        if fetchone is True:
            if and_where is not None:
                execute = f'SELECT {value} FROM {table} WHERE {where.split(" = ")[0]} = ?'
                var = (where.split(' = ')[1],)
                for and_where_item in and_where:
                    execute += f' AND {and_where_item.split(" = ")[0]} = ?'
                    var += (and_where_item.split(' = ')[1],)
                item = cursor.execute(execute, var).fetchone()
            else:
                item = cursor.execute(f'SELECT {value} FROM {table} WHERE {where.split(" = ")[0]} = ?', (where.split(' = ')[1],)).fetchone()
        else:
            if and_where is not None:
                execute = f'SELECT {value} FROM {table} WHERE {where.split(" = ")[0]} = ?'
                var = (where.split(' = ')[1],)
                for and_where_item in and_where:
                    execute += f' AND {and_where_item.split(" = ")[0]} = ?'
                    var += (and_where_item.split(' = ')[1],)
                item = cursor.execute(execute, var).fetchall()
            else:
                item = cursor.execute(f'SELECT {value} FROM {table} WHERE {where.split(" = ")[0]} = ?', (where.split(' = ')[1],)).fetchall()

    # Disconnect database
    cursor.close()
    database.close()

    # Returning the data
    if item is None:
        return None
    else:
        if fetchone is True:
            return item[0]
        else:
            return item


def insert(table: str, parameter: list, values: list, cog_file: bool = True, filename: str = 'database.db'):
    # Get database file path
    path = inspect.getmodule(inspect.currentframe().f_back).__file__.replace('\\', '/').split('/')
    path.pop(-1)
    if cog_file is True:
        path.pop(-1)
    path.append(filename)
    path = '/'.join(path)

    # Connect with database
    database = sqlite3.connect(path)
    cursor = database.cursor()

    # Insert data
    fragezeichen = ['?' for _ in parameter]
    cursor.execute(f'INSERT INTO {table}({", ".join(parameter)}) VALUES({", ".join(fragezeichen)})', tuple(values))

    # Overwrite data & disconnect database
    database.commit()
    cursor.close()
    database.close()


def edit(table: str, parameter: str, value: str, where: str = None, cog_file: bool = True, filename: str = 'database.db'):
    # Get database file path
    path = inspect.getmodule(inspect.currentframe().f_back).__file__.replace('\\', '/').split('/')
    path.pop(-1)
    if cog_file is True:
        path.pop(-1)
    path.append(filename)
    path = '/'.join(path)

    # Connect with database
    database = sqlite3.connect(path)
    cursor = database.cursor()

    # Edit data
    if where is None:
        cursor.execute(f'UPDATE {table} SET {parameter} = ?', (value,))
    else:
        cursor.execute(f'UPDATE {table} SET {parameter} = ? WHERE ? = ?', (value, where.split(' = ')[0], where.split(' = ')[1]))

    # Overwrite data & disconnect database
    database.commit()
    cursor.close()
    database.close()


def delete(table: str, value: str = None, where: str = None, and_where: list = None, cog_file: bool = True, filename: str = 'database.db'):
    # Get database file path
    path = inspect.getmodule(inspect.currentframe().f_back).__file__.replace('\\', '/').split('/')
    path.pop(-1)
    if cog_file is True:
        path.pop(-1)
    path.append(filename)
    path = '/'.join(path)

    # Connect with database
    database = sqlite3.connect(path)
    cursor = database.cursor()

    # Delete data
    if where is None:
        if value is None:
            cursor.execute(f'DELETE FROM {table}')
        else:
            cursor.execute(f'DELETE {value} FROM {table}')
    else:
        if value is None:
            if and_where is not None:
                execute = f'DELETE FROM {table} WHERE {where.split(" = ")[0]} = ?'
                var = (where.split(' = ')[1],)
                for and_where_item in and_where:
                    execute += f' AND {and_where_item.split(" = ")[0]} = ?'
                    var += (and_where_item.split(' = ')[1],)
                cursor.execute(execute, var)
            else:
                cursor.execute(f'DELETE FROM {table} WHERE {where.split(" = ")[0]} = ?', (where.split(' = ')[1],))
        else:
            if and_where is not None:
                execute = f'DELETE {value} FROM {table} WHERE {where.split(" = ")[0]} = ?'
                var = (where.split(' = ')[1],)
                for and_where_item in and_where:
                    execute += f' AND {and_where_item.split(" = ")[0]} = ?'
                    var += (and_where_item.split(' = ')[1],)
                cursor.execute(execute, var)
            else:
                cursor.execute(f'DELETE {value} FROM {table} WHERE {where.split(" = ")[0]} = ?', (where.split(' = ')[1],))

    # Overwrite data & disconnect database
    database.commit()
    cursor.close()
    database.close()
