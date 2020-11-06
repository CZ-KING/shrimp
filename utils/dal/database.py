import MySQLdb

from utils.config import settings
from elasticsearch import Elasticsearch
from elasticsearch import helpers


class Database:
    """
    对数据库
    """

    __db_instances={}

    @classmethod
    def get_instance(cls, db_type=settings.DatabaseType.MYSQL):
        """
        定义get_instance类方法，用来获取数据库对象的单例
        所谓的单例就是一个类只有一个实例，调用该方法每次获取
        到的都是同一个数据库实例，type_默认为MYSQL类型，表示
        默认获取的是mysql的数据实例
        """

        if db_type not in cls.__db_instances:
            # 如果不存在，就构造一个Datebase的实例对象
            cls.__db_instances[db_type] = Database(db_type)
        return  cls.__db_instances[db_type]

    def __init__(self,db_type=settings.DatabaseType.MYSQL):
        """

        :param db_type:数据库的类型在DatabaseType中进行了定义
        默认为MYSQL类型,表示创建mysql类型的数据库实例
        """

        self.__db_type = db_type
        self.__db = self.__get_database()
        self.__cursors={}

    def __get_database(self):
        db = None
        # 根据类型字段，来创建对应的数据库实例
        if self.__db_type == settings.DatabaseType.MYSQL:
            try:
                db = MySQLdb.connect(settings.DATABASE["mysql"]["host"],
                                     settings.DATABASE["mysql"]["username"],
                                     settings.DATABASE["mysql"]["password"],
                                     settings.DATABASE["mysql"]["db"],charset="utf8")
            except :
                db = None
        elif self.__db_type == settings.DatabaseType.ELASTICSEARCH:
            try:
                db = Elasticsearch([{'host':settings.DATABASE["elasticsearch"]["host"],
                                     'port':settings.DATABASE["elasticsearch"]["port"]}],
                                   timeout=3600)
            except :
                db = None
        return  db


    def query(self, ql,*args, **kwargs):
        """

        :param ql: 表示查询语句
        :param args: 表示查询的参数
        :return: 查询的数据
        """
        data = None

        if self.__db_type == settings.DatabaseType.MYSQL:
            if settings.DatabaseType.MYSQL not in self.__cursors:
                self.__cursors[settings.DatabaseType.MYSQL] = self.__db.cursor()

            if not args:
                self.__cursors[settings.DatabaseType.MYSQL].execute(ql)
            else:
                self.__cursors[settings.DatabaseType.MYSQL].execute(ql,args)

            data = self.__cursors[settings.DatabaseType.MYSQL].fetchall()

        elif self.__db_type == settings.DatabaseType.ELASTICSEARCH:
            data = self.__db.search(index=kwargs["es_index"],body=ql)

        return data








