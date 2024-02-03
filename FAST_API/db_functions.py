import os
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
    # isAlready = await GetGroupById(groupID)
    # if(len(isAlready) != 0):
    #     return

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql, arg)
    conn.commit()
    conn.close()
    return

# async def updateMetadata(id, metadata):
#     sql = '''UPDATE IMAGES SET METADATA='?' WHERE ID = ?'''
#     arg = (metadata, id)
#     conn = sqlite3.connect(DATABASE)
#     cur = conn.cursor()
#     cur.execute(sql, arg)
#     conn.commit()
#     conn.close()
#     return

async def UpdateImagesGroup(ids, groupID, groupNAME):
    sql = '''UPDATE IMAGES SET GROUPID=? WHERE ID IN '''
    sql2 = '''UPDATE IMAGES SET GROUPNAME=? WHERE ID IN '''
    ids_str = '(' + str(ids)[1:-1] + ');'
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql + ids_str, (groupID,))
    cur.execute(sql2 + ids_str, (groupNAME,))
    conn.commit()
    conn.close()
    return 

async def UpdateImagesURL(imgs, pathToGroup):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    for img in imgs:
        newURL = os.path.join(pathToGroup, img['TITLE'])
        sql = '''UPDATE IMAGES SET URL = ? WHERE ID = ? '''
        arg = (newURL, img['ID'])
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

async def deleteImages(ids):
    ids = [(i,) for i in ids]
    sql = '''DELETE FROM IMAGES WHERE ID = ?'''
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.executemany(sql, ids)
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
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    result = cur.fetchall()
    conn.close()
    return result[0]

async def GetUrlById(id):
    sql = '''SELECT URL FROM IMAGES WHERE ID = ?'''
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    result = cur.fetchall()
    conn.close()
    return result

async def GetImagesByGroupId(id):
    sql = '''SELECT * FROM IMAGES WHERE GROUPID = ?  '''
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    result = cur.fetchall()
    conn.close()
    return result

async def GetUrlsByIds(ids):
    sql = '''SELECT URL FROM IMAGES WHERE ID IN '''
    ids_str = '(' + str(ids)[1:-1] + ')'
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql + ids_str)
    conn.commit()
    result = cur.fetchall()
    conn.close()
    return result

async def GetGroupById(id):
    sql = '''SELECT * FROM GROUPS WHERE GROUPID = ? '''
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    result = cur.fetchall()
    conn.close()
    return result[0]

async def GetImages(ids):
    sql = '''SELECT * FROM IMAGES WHERE ID IN '''
    ids_str = '(' + str(ids)[1:-1] + ')'
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql + ids_str)
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

async def GetAllGroups():
    sql = '''SELECT * FROM GROUPS'''
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    result = cur.fetchall()
    conn.close()
    return result

async def UpdateImagesDesc(id, desc):
    sql = '''UPDATE IMAGES SET DESCRIPTION=? WHERE ID=?'''
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql, (desc, id))
    conn.commit()
    conn.close()
    return

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d