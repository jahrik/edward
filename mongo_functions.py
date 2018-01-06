#!/usr/bin/env python
"""
Manage mongo db
"""
# import edward
import os
import pymongo


def export(filename=None):
    """
    * export the database
    * mongoexport -d bot_db -c statements
    """
    # return filename
    # from os.path import join
    # from bson.json_utils import dumps
    username = 'root'
    password = 'root'
    host = 'mongodb://{}:{}@127.0.0.1'.format(username, password)
    port = 27017
    # database = 'bot_db'

    def backup_db(backup_db_dir, filename):
        """
        backup database
        """
        if filename is None:
            filename = 'export.yml'
        else:
            filename = filename

        if backup_db_dir is None:
            backup_db_dir = os.environ['PWD']
        else:
            backup_db_dir = backup_db_dir

        client = pymongo.MongoClient(host=host, port=port)
        database = client['bot_db']
        print(authenticated=database.authenticate())
        # assert authenticated, "Could not authenticate to database!"
        collections = database.collection_names()
        print(collections)
        # for i, collection_name in enumerate(collections):
        # col = getattr(database,collections[i])
        # collection = col.find()
        # jsonpath = collection_name + ".json"
        # jsonpath = join(backup_db_dir, jsonpath)
        # with open(jsonpath, 'wb') as jsonfile:
        # jsonfile.write(dumps(collection))
    # bot = chat_bot()
    backup_db(backup_db_dir=os.environ['PWD'], filename=filename)


# ex
# db.statements.find( { "text" : "stuff" } )
# db.statements.deleteOne( { "text" : "stuff" } )
# db.statements.deleteMany( { "text" : "stuff" } )

# Twitter cleanup
# db.statements.deleteMany( { text: { $regex: /@/ } } )
# db.statements.deleteMany( { text: { $regex: /#/ } } )
# Reddit cleanup
# db.statements.deleteMany( { text: { $regex: /reddit/ } } )
# db.statements.deleteMany( { text: { $regex: /gold/ } } )
# db.statements.deleteMany( { text: { $regex: /[removed]/ } } )
# db.statements.deleteMany( { text: { $regex: /[deleted]/ } } )
