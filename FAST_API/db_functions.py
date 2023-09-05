import sqlite3
import json

DATABASE = 'test.db'

async def addImage(title, type, description, url, metadata, groupID, groupNAME):
    sql = '''INSERT INTO IMAGES (TITLE, TYPE, DESCRIPTION, METADATA, GROUPNAME, GROUPID, URL) VALUES (?, ?, ?, ?, ?, ?, ?)'''
    arg = (title, type, description, metadata, groupNAME, groupID, url)

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql, arg)
    conn.commit()
    conn.close()
    return

async def addGroup(groupID, groupNAME):
    sql = '''INSERT INTO GROUPS (GROUPNAME, GROUPID) VALUES (?, ?)'''
    arg = (groupNAME, groupID)
    print(groupID)
    isAlready = await GetGroupById(groupID)
    print(isAlready)
    if(len(isAlready) != 0):
        return

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql, arg)
    conn.commit()
    conn.close()
    return

async def updateMetadata(id, metadata):
    sql = '''UPDATE IMAGES SET METADATA='?' WHERE ID = ?'''
    arg = (metadata, id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql, arg)
    conn.commit()
    conn.close()
    return

async def deleteImage(id):
    sql = '''DELETE FROM IMAGES WHERE ID = ?'''
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    conn.close()
    return

async def deleteGroup(id):
    sql = '''DELETE FROM GROUPS WHERE GROUPID = ?'''
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    conn.close()
    return

async def GetImageById(id):
    sql = '''SELECT * FROM IMAGES WHERE ID = ?'''
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    result = cur.fetchall()
    conn.close()
    return result

async def GetGroupById(id):
    sql = '''SELECT * FROM GROUPS WHERE GROUPID = ? '''
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    result = cur.fetchall()
    conn.close()
    return result

async def GetAllImages():
    sql = '''SELECT * FROM IMAGES'''
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    result = cur.fetchall()
    conn.close()
    return result

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d