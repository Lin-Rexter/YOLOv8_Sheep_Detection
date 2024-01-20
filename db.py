import json
import os
from bson import json_util
from pprint import PrettyPrinter
from typing import Union, Optional

# import asyncio

# 讀取.env檔
from dotenv import load_dotenv, find_dotenv

# https://github.com/mongodb/motor
import motor.motor_asyncio as Motor
from pymongo.server_api import ServerApi

# 解決asyncio無法嵌套循環問題 https://github.com/erdewit/nest_asyncio
import nest_asyncio

# 從.env載入環境變數
env_path = find_dotenv(raise_error_if_not_found=True)
load_dotenv(env_path)

# Mongodb連線資訊
Mongo_UserName = os.getenv("MongoDB_USERNAME") or None
Mongo_PassWord = os.getenv("MongoDB_PASSWORD") or None
Mongo_ClusterName = os.getenv("MongoDB_CLUSTERNAME") or None

if None in [Mongo_UserName, Mongo_PassWord, Mongo_ClusterName]:
    raise ValueError("❌[Error] .env檔的MongoDB連線設置是否有誤或缺少!")


# 與MongoDB Atlas連線
def connect():
    try:
        global client
        client = Motor.AsyncIOMotorClient(
            f"mongodb+srv://{Mongo_UserName}:{Mongo_PassWord}@{Mongo_ClusterName}/?retryWrites=true&w=majority",
            server_api=ServerApi("1"),
        )

        client.admin.command("ping")
        print("\n✅已成功連接MongoDB資料庫!\n")

        # Coroutine 協程 asyncio
        global loop
        loop = client.get_io_loop()
    except Exception as e:
        print("\n❌[Error] 發生錯誤: ", e, "\n")


# 斷開MongoDB Atlas連線
def disconnect():
    client.close()


# 執行命令
def run(command):
    nest_asyncio.apply()
    return loop.run_until_complete(command)


# MongoDB CRUD 模組
class Mongodb:
    def __init__(self, database: str, collection: str):
        self.database = client[f"{database}"]
        self.collection = self.database[f"{collection}"]

    # 尋找資料(單筆)
    async def find_one(self, query: Optional[dict] = None):
        """
        ### 尋找資料(單筆)
        ---
        #### Args:
            - query (Optional[dict], optional): _description_. Defaults to None.
                - 可選，資料篩選
        """

        if query is None:
            query = {}

        document = await self.collection.find_one(query)
        return document

    # 尋找資料(多筆)
    async def find(
        self,
        query: Optional[dict] = None,
        projection: Optional[dict] = None,
        sort_key: Optional[list] = None,
        limit: Optional[int] = None,
        skip_index: Optional[int] = None,
    ) -> list | None:
        """
        ### find 尋找資料(多筆)
        ---
        #### Args:
            - query (Optional[dict], optional): _description_. Defaults to None.
                - 資料篩選
            - projection (Optional[dict], optional): _description_. Defaults to None.
                - 提取特定Field，https://www.mongodb.com/docs/manual/tutorial/project-fields-from-query-results/#return-the-specified-fields-and-the-_id-field-only
            - sort_key (Optional[list], optional): _description_. Defaults to None.
                - 指定要排序的Key值(ex:sort_key(lId)
            - limit (Optional[int], optional): _description_. Defaults to None.
                - 限制資料數量
            - skip_index (Optional[int], optional): _description_. Defaults to None.
                - 指定從哪裡開始取得的資料索引值
        """

        if query is None:
            query = {}

        if projection:
            cursor = self.collection.find(query, projection)
        else:
            cursor = self.collection.find(query)

        if sort_key:
            cursor = cursor.sort(*sort_key)

        if skip_index:
            cursor = cursor.skip(skip_index)

        if limit:
            cursor = cursor.limit(limit)

        result = []
        async for document in cursor:
            # pprint.pprint(document)
            result.append(document)

        return result

    # 新增資料(可多筆)
    async def insert(self, document: list):
        """
        ### insert 新增資料(可多筆)
        ---
        #### Args:
            - document (list): _description_
                - 字典格式，外面要包一層list[{}, {}]: 要新增的資料
        """

        if len(document) > 1:
            result = await self.collection.insert_many([item for item in document])
        else:
            result = await self.collection.insert_one(document[0])

        return result

    # 更新資料
    async def update(self, filter: dict, update: dict, all: Optional[bool] = None):
        """
        ### update 更新資料
        ---
        #### Args:
            - filter (dict): _description_
                - 篩選資料
            - update (dict): _description_
                - 更新的資料{key: values}
            - all (Optional[bool], optional): _description_. Defaults to None.
                - (True, False): 是否更新所有符合的資料
        """

        if all:
            result = await self.collection.update_many(filter, update)
        else:
            result = await self.collection.update_one(filter, update)

        return result

    # 刪除資料
    async def delete(self, filter: Optional[dict] = None, all: Optional[bool] = None):
        """
        ### delete 刪除資料
        ---
        #### Args:
            - filter (Optional[dict], optional): _description_. Defaults to None.
                - 篩選資料
            - all (Optional[bool], optional): _description_. Defaults to None.
                - (True, False): 是否刪除所有符合的資料
        """

        if filter is None:
            filter = {}

        if all:
            result = await self.collection.delete_many(filter)
        else:
            result = await self.collection.delete_one(filter)

        return result

    # 取得資料數量
    async def count(self, filter: Optional[dict] = None) -> int:
        """
        ### filter: 篩選資料
        ---
        #### Args:
            - filter (Optional[dict], optional): _description_. Defaults to None.
                - 篩選資料
        Returns:
            int: _description_
        """

        if filter is None:
            filter = {}
        n = await self.collection.count_documents(filter)

        return n


# PrettyPrinter indent:縮排, width:寬度, depth:最大層級限制, sort_dicts:是否根據key值排序
pp = PrettyPrinter(
    indent=2,
    width=100,
    depth=None,
    sort_dicts=False,
)


# MongoDB CRUD範例
async def main():
    print("= = = = = = = = = = = = = = = = = = = = = = = =")
    # data = Mongodb(database="YOLO_羊圈管理", collection="Sheep_ID")

    # n = loop.run_until_complete(data.count({"age": 6}))
    """
    # 取得資料表內的資料數量
    n = data.count({"age": 6})
    pp.pprint(n)
    
    # 資料查找(返回全部)
    n = await data.find(query={"age": "6"}, sort_key=["deposit", -1])
    pp.pprint(n)
    
    # 資料查找(返回一筆資料)
    n = await data.find_one()
    pp.pprint(n)
    """

    """
    sheep_list = [
        {
            "picture": "../static/images/sheep/sheep_1.png", # 照片
            "Id_name": "sheep1", # ID名稱
            "sex": "male", # 性別
            "age": 5, # 年齡
            "Weight": 112, # 體重
            "date": "2023-12-25", # 新增日期
        },
        {
            "picture": "../static/images/sheep/sheep_2.png",
            "Id_name": "class 1",
            "sex": "female",
            "age": 7,
            "Weight": 95,
            "date": "2023-12-25",
        },
    ]
    """

    """
    # 新增資料(可多筆，使用all=True)
    n = await data.insert(document=sheep_list)
    pp.pprint(f"新增的資料id: {n.inserted_id}")
    """

    """
    # 更新資料(可多筆，使用all=True)
    n = await data.update(filter={"sex": "male", "Id_name": "sheep1"}, update={"$set": {"age": 3}})
    pp.pprint(f"更新了{n.modified_count}筆資料!")
    """

    """
    # 刪除資料(可多筆)
    n = await data.delete(filter={"age": 3})
    pp.pprint(f"刪除了: {n.deleted_count}筆資料!")
    pp.pprint(f"剩餘資料量: {await data.count()}")
    """

    # json_util.dumps: 序列化Bson格式, ensure_ascii為False，不使用ascii編碼
    # result = json_util.dumps(n, indent=4, ensure_ascii=False)
    # print(result)

    # pp.pprint(n)


"""
if __name__ == "__main__":
    asyncio.run(main())
"""
