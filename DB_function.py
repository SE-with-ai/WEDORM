import json
import sqlite3
import logging
from flask import session, redirect
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def login_required(f):
    """
    Decorate routes to require login.

    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def create_conn():
    """
    Get connection from SQLite database.

    Returns:
        [type]: SQLite connection object
    """
    conn = sqlite3.connect("database.db")
    return conn

def insert_user(conn, arg) -> int:
    """添加用户
    分别添加一行user和一行virtue
    uid自增生成， arg需要传入name， dorm， email为key的字典
    Args:
        conn (sqlite3.Connection): 数据库连接对象
        arg (dict): 用户数据
    Returns:
        int: 插入的用户ID
    """
    usersql = "INSERT INTO USERS (NAME, DORM, EMAIL) VALUES (?, ?, ?);"
    virsql = "INSERT INTO VIRTUE (UID, VIRTUE) VALUES (?, ?);"
    with conn:
        cursor = conn.cursor()
        cursor.execute(usersql, (arg['name'], arg['dorm'], arg['email']))
        uid = cursor.lastrowid
        cursor.execute(virsql, (uid, 0))  # 功德初始值为0
        logger.info(f"添加数据<{uid}>到数据库")
        conn.commit()
    return uid

def insert_share(conn, uid, iid, modi, ddl, commit=True) -> int:
    """插入共享数据
    Args:
        conn (sqlite3.Connection): 数据库连接对象
        uid (int): 用户ID
        iid (int): 项ID
        modi (str): 修改信息
        ddl (str): 截止日期
        commit (bool, optional): 是否提交事务. Defaults to True.
    Returns:
        int: 插入的共享数据ID
    """
    sql = "INSERT INTO SHARE (UID, IID, MODIFIED, DDL) VALUES (?, ?, ?, ?);"
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (uid, iid, modi, ddl))
        sid = cursor.lastrowid
        logger.info(f"添加数据<{sid}>到数据库")
        if commit:
            conn.commit()
    return sid

def insert_item(conn, arg, commit=True) -> int:
    """插入项数据
    Args:
        conn (sqlite3.Connection): 数据库连接对象
        arg (dict): 项数据
        commit (bool, optional): 是否提交事务. Defaults to True.
    Returns:
        int: 插入的项ID
    """
    sql = "INSERT INTO ITEMS (NAME, BRAND, DESCRIPTION, QTY, IS_CONSUME) VALUES (?, ?, ?, ?, ?);"
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (arg['name'], arg['brand'], arg['description'], arg['qty'], arg['is_consume']))
        iid = cursor.lastrowid
        logger.info(f"添加数据<{iid}>到数据库")
        if commit:
            conn.commit()
    return iid

def insert_own(conn, uid, iid, commit=True) -> int:
    """插入拥有数据
    Args:
        conn (sqlite3.Connection): 数据库连接对象
        uid (int): 用户ID
        iid (int): 项ID
        commit (bool, optional): 是否提交事务. Defaults to True.
    Returns:
        int: 插入的拥有数据ID
    """
    sql = "INSERT INTO OWN (UID, IID) VALUES (?, ?);"
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (uid, iid))
        oid = cursor.lastrowid
        logger.info(f"添加数据<{oid}>到数据库")
        if commit:
            conn.commit()
    return oid

def insert_tag(conn, cid, iid, commit=True) -> int:
    """插入标签数据
    Args:
        conn (sqlite3.Connection): 数据库连接对象
        cid (int): 标签ID
        iid (int): 项ID
        commit (bool, optional): 是否提交事务. Defaults to True.
    Returns:
        int: 插入的标签数据ID
    """
    sql = "INSERT INTO TAGS (NAME, IID) VALUES (?, ?);"
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (cid, iid))
        tid = cursor.lastrowid
        logger.info(f"添加数据<{tid}>到数据库")
        if commit:
            conn.commit()
    return tid

def insert_virlog(conn, uid, log_content, commit=True) -> int:
    """插入功德日志
    Args:
        conn (sqlite3.Connection): 数据库连接对象
        uid (int): 用户ID
        log_content (str): 日志内容
        commit (bool, optional): 是否提交事务. Defaults to True.
    Returns:
        int: 插入的功德日志ID
    """
    sql = "INSERT INTO VIRLOG (VIRLOG, uid) VALUES (?, ?);"
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (log_content, uid))
        vid = cursor.lastrowid
        logger.info(f"添加数据<{vid}>到功德日志")
        if commit:
            conn.commit()
    return vid

def get_item_by_id(conn, id):
    """Fetch data by id from ITEMS table"""
    sql = "SELECT * FROM ITEMS WHERE iid = ?;"
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        logger.info(f"Select data<{result}> from item")
    return result

def get_owner_by_iid(conn, id):
    """Fetch owner info by iid from OWN table"""
    sql = "SELECT * FROM OWN WHERE iid = ?;"
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        logger.info(f"Select data<{result}> from own")
    return result

def get_tag_by_id(conn, id):
    """Fetch data by id from TAGS table"""
    sql = "SELECT NAME FROM TAGS WHERE iid = ?;"
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        result = cursor.fetchall()
        logger.info(f"Select data<{result}> from tags")
    return result

def get_user_by_id(conn, id):
    """Fetch data by id from USERS table"""
    sql = "SELECT * FROM USERS WHERE uid = ?;"
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        logger.info(f"Select data<{result}> from user")
    return result

def get_sharing_by_item_id(conn, id):
    """Fetch data by id from SHARE table"""
    sql = "SELECT * FROM SHARE WHERE iid = ?;"
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        logger.info(f"Select data<{result}> from share")
    return result

def get_data_by_name(conn, item_name, table_name):
    """Fetch data by item_name from specified table"""
    if table_name not in ["USERS", "ITEMS", "TAGS"]:
        return
    sql = f"SELECT * FROM {table_name} WHERE NAME = ?;"
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (item_name,))
        result = cursor.fetchall()
        logger.info(f"Select data<{result}> from database")
    return result

def update_virtue(conn, uid, num, commit=True):
    """
    num is the virtue change amount, if subtracting, use negative value
    """
    sql = "SELECT * FROM VIRTUE WHERE uid = ?;"
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (uid,))
        virtue_old = cursor.fetchone()[1]
        logger.info(f"Select data<{virtue_old}> from virtue")

    sql = "UPDATE VIRTUE SET VIRTUE = ? WHERE uid = ?;"
    with conn:
        cursor = conn.cursor()
        result = cursor.execute(sql, (virtue_old + num, uid))
        logger.info(f"Update data<{result}> to the virtue")
        if commit:
            conn.commit()

# if __name__ == '__main__':
#     conn = create_conn()
#     print(insert_tag(conn,'药','2',True))
#     print(get_user_by_id(conn, 1))