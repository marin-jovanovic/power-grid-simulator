import pymongo


def get_database():
    # print(len(rows))

    from collections import namedtuple
    Config = namedtuple('Config', ["username", "password", "cluster-name", "database-name"])

    # config = {
    #     "username": "",
    #     "password": "",
    #     "cluster-name": "",
    #     "database-name": "myFirstDatabase",
    # }



    # create connection using mongo client
    # mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mongo_client = pymongo.MongoClient(f"mongodb+srv://{config['username']}:<password>@<cluster-name>.mongodb.net/myFirstDatabase")
    # CONNECTION_STRING =+"mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myFirstDatabase"
    mongo_database = mongo_client["mydatabase"]
    collection = mongo_database["tmp"]

    # for i in collection:
    #     print(i)

    print(
        mongo_database.list_collection_names()

    )

    # start_time = time.time()
    # x = collection.insert_many(rows)
    # end_time = time.time()

    # print(end_time - start_time, "seconds")

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # CONNECTION_STRING = "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myFirstDatabase"

    # Create the database for our example (we will use the same database throughout the tutorial
    # return client['user_shopping_list']


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = get_database()