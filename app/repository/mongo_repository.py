from pymongo import MongoClient


class MongoRepository:
    """
    MongoRepository Class

    Receives an adress to the database and a database name on instantiation.

    getAllDocs() - receives collection name as string.
                            - returns a list of documents, with the internal MongoDB _id absent.

    insertOne() - receives a collection name as string, and a document as dict.
                            - returns a status string.

    insertOneUnique() - receives a collection name as string, and a document as dict.
                                    - checks if there is an identical document in the collection before inserting.
                                    - returns a status string.
                                    - optionally, it receives a set with strings as the 3th argument:
                                            - this set is meant to filter for identical documents in a more specific case.
                                            - only the columns described in the set will be considered as unique.
                                            - the function then will check if there is a document in the collection with
                                            these columns identical before inserting.
                                            - returns a status string.
    """

    def __init__(self, db_address, db_name):
        self.db_address = db_address
        self.db_name = db_name
        self.db = None

        self.connect()

    def connect(self):
        client = MongoClient(self.db_address)
        self.db = client[self.db_name]

    def getAllDocs(self, collection_name):
        result = self.db[collection_name].find({}, {'_id': False})

        return list(result)

    def insertOne(self, collection_name, document):
        result = self.db[collection_name].insert_one(document)

        return True

    def insertOneUnique(self, collection_name, document, unique_columns=False):
        all_docs = self.getAllDocs(collection_name)
        if unique_columns:
            if all_docs:
                all_filtered_for_unique_columns = []
                for doc in all_docs:
                    all_filtered_for_unique_columns.append({key: doc[key] for key in doc.keys() and unique_columns})
                doc_filtered_for_unique_columns = {key: document[key] for key in document.keys() and unique_columns}

                if doc_filtered_for_unique_columns in all_filtered_for_unique_columns:
                    print("\nDocument already exists in the collection.")
                    return "Document already exists in the collection."
                else:
                    result = self.insertOne(collection_name, document)
                    return result
            else:
                result = self.insertOne(collection_name, document)
                return result
        elif document in all_docs:
            print("\nDocument already exists in the collection.")
            return "Document already exists in the collection."
        else:
            result = self.insertOne(collection_name, document)
            return result
