'''
@author:chenzhan
@date:2020-10-30
@desc:工具函数，用来将mysql里面数据插入到elasticsearch
'''


from utils.dal import database
from elasticsearch import helpers
from elasticsearch import Elasticsearch


def insert_elasticsearch(start=1,interval=1000):
    mysql_instance = database.Database.get_instance()
    sql = "select title,description from shrimp_question where id >={} and id < {}".format(start,interval)
    results = mysql_instance.query(sql)
    data = []
    limit = 1
    es = Elasticsearch([{'host':'localhost','port':9200}], timeout=3600)

    while results:
        for result in results:
            print(result[0])
            data.append({
                "_index":"shrimp",
                "_source":{ "title":result[0],
                "description":result[1]}

            })

            if len(data) > limit:
                helpers.bulk(es, data)
                data = []

        start += interval
        interval += interval
        sql = "select title,description from shrimp_question where id >={} and id < {}".format(start,interval)
        results = mysql_instance.query(sql)



if __name__ == "__main__":
    insert_elasticsearch()








