from pymongo import MongoClient, collection


class DBClient:
    conn = MongoClient('localhost', 27018)
    db = conn.insta
    coll: collection.Collection = db.insta

    def insert_doc(self, data):
        data['watched'] = False
        self.coll.insert_one(data)

    def get_all_cats(self):
        res = self.coll.find({"is_cat": True})
        for r in res:
            r['id'] = str(r['_id'])
            del r['_id']
        self.set_all_watched()
        return res

    def get_all_unwatched_cats(self):
        res = self.coll.find({"is_cat": True, "watched": False})
        for r in res:
            r['id'] = str(r['_id'])
            del r['_id']
        self.set_all_watched()
        return res

    def set_all_watched(self):
        self.coll.update_many({"watched": False}, {"watched": True})

    def insta_id_exists(self, inst_id):
        res = self.coll.find_one({"inst_id": inst_id})
        return res is not None
