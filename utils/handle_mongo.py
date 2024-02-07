import pymongo

from configs.conf import MongoConfig

class MongoConnection:
    def __init__(self,host=MongoConfig.HOST,port=MongoConfig.PORT,user=MongoConfig.USER,
                 pwd=MongoConfig.PWD,db=MongoConfig.DB):

        #1创建连接
        client = pymongo.MongoClient(f"mongodb://{user}:{pwd}@{host}:{port}")
        #2指定数据库
        self.db = client[db]

    #插入
    def insert(self,collection,query,many=False):
        '''
        插入方法
        :param collection: 集合
        :param query: 字典语句
        :param many: 控制是匹配更多还是一个
        :return:
        '''
        try:
            data_collection = self.db[collection]
            if many:
                data_collection.insert_many(query)
            else:
                data_collection.insert_one(query)
        except Exception as e:
            raise e

    #查询
    def find(self,collection,query,many=True):
        data_collection = self.db[collection]
        if many:
            result = [data for data in data_collection.find(query)]
            return result
        else:
            result = data_collection.insert_one(query)
            return result

    def update(self,collection,query,new_value,many=False):
        data_collection = self.db[collection]
        if many:
            data_collection.update_many(query,{"$set":new_value})
        else:
            data_collection.update_one(query,{"$set":new_value})

    def delete(self,collection,query,many=False):
        data_collection = self.db[collection]
        if many:
            data_collection.delete_many(query)
        else:
            data_collection.delete_one(query)


if __name__ == '__main__':
    # res = [one for one in range(10)]
    # print(res)
    db  = MongoConnection()
    db.insert('categories',{"count":10,"level":1,"name":"快餐便当","abc":6})