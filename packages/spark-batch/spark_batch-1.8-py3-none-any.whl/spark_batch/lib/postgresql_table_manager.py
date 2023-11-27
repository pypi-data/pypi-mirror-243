from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from .pxlogger import CustomLogger
from .util import parseSourceObject
import psycopg2
import re

"""
PostgreSQL 테이블을 로드하고 저장하는 클래스.

:param spark: Spark 세션.
:param default_bucket: Delta 테이블이 저장된 기본 S3 버킷.
:param default_dpath: Delta 테이블의 기본 dpath 또는 하위 디렉토리.

사용 예시)
    # Oracle database connection settings
    connection_url = "jdbc:postgresql://<host>:<port>/<database>"
    connection_properties = {
        "user": "<username>",
        "password": "<password>",
        "driver": "org.postgresql.Driver"
    }
    
    # Initialize OracleTableManager
    manager = OracleTableManager(spark, connection_url, connection_properties)
"""

class PostgreSQLTableManager:
    def __init__(self, spark, connection_url, connection_properties, dbname=None):
        self.spark = spark
        self.connection_url = connection_url
        self.connection_properties = connection_properties
        self.dbname = dbname
        self.logger = CustomLogger("PostgreSQLTableManager")

    def __add_public_domain(self, input_string):
        # 문자열에서 "."을 기준으로 분리
        parts = input_string.split(".")

        # 분리된 부분의 길이 확인
        if len(parts) == 1:
            # 도메인이 없는 경우, "public."를 추가
            return "public." + input_string
        else:
            # 도메인이 있는 경우, 원래 문자열 그대로 반환
            return input_string

    def getType(self) :
        return "postgresql"
            
    def getTablePath(self, tableName):
        tableName = self.__add_public_domain(tableName)
        return tableName if self.dbname is None else self.dbname + "." + tableName
    
    def loadTable(self, tableName, offset=None, chunk_size=100000, dpath=None, customSchema=None):
        self.logger.debug(("loadTable = ", tableName, offset, chunk_size))
        
        target_table = self.getTablePath(tableName)
        self.logger.debug(("target_table = ", target_table))
        
        if offset == None:
            query = f"(SELECT * FROM {target_table}) tbl"
        else:
            query = f"(SELECT * FROM {target_table} OFFSET {offset} LIMIT {chunk_size}) tbl"
            
        self.logger.debug(("connection_url = ", self.connection_url))    

        df = self.spark.read \
            .format("jdbc") \
            .option("url", self.connection_url) \
            .option("dbtable", query) \
            .option("fetchsize", chunk_size) 

        for key, value in self.connection_properties.items():
            df = df.option(key, value)

        if customSchema:
            df = df.schema(toCustomSchema(customSchema)) 

        df = df.load()

        return df

    def saveTable(self, dataFrame, tableName, mode="append", dpath=None):
        self.logger.debug(("saveTable = ", tableName, self.connection_url))

        # 테이블을 삭제하지 않고, 데이터만 삭제. Delta 테이블과 동일한 방식으로 동작
        if mode == "overwrite" :
           delete_query = f"DELETE FROM {tableName}"
           self._executeDB(delete_query)

        df = dataFrame.write \
            .mode("append") \
            .format("jdbc") \
            .option("url", self.connection_url) \
            .option("dbtable", tableName) \
            .option("isolationLevel", "NONE") 
        
        for key, value in self.connection_properties.items():
            df = df.option(key, value)
        df.save()


    def loadTables(self, tableNames, dpath=None, customSchemas=None):
        tableNames = parseSourceObject(tableNames)

        if customSchemas is None:
            customSchemas = [None] * len(tableNames)  # 기본적으로 None 스키마를 사용

        dataframes = {}

        for tableName, customSchema in zip(tableNames, customSchemas):
            target_table = self.getTablePath(tableName)

            # JDBC 연결 속성 설정
            properties = self.properties
            if customSchema:
                properties["customSchema"] = customSchema

            # Spark DataFrame 로딩 및 등록
            df = self.spark.read.jdbc(self.connection_url, table=target_table, properties=properties)
            df.createOrReplaceTempView(tableName)
            dataframes[tableName] = df

        return dataframes    

    def _get_connect(self) :
        match = re.match(r"jdbc:postgresql://([\w.]+):(\d+)/(\w+)", self.connection_url)
        if match:
            host = match.group(1)
            port = int(match.group(2))
            database = match.group(3)
        else:
            raise ValueError("Invalid jdbc_url")

        # connection_properties에서 사용자 이름 및 비밀번호 추출
        user = self.connection_properties["user"]
        password = self.connection_properties["password"]

        # 추출된 정보를 사용하여 PostgreSQL 연결 설정
        conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )    
    
        return conn
    
    def _executeDB(self, delete_query) :
        conn = self._get_connect()
        cur = conn.cursor()
        
        cur.execute(delete_query)
        conn.commit()

        cur.close()
        conn.close()
 
    def delSert(self, dataFrame, condition, tableName, dpath=None):
        self.logger.debug(("delSert = ", condition, tableName))
        
        df = self.loadTable(tableName)

        before_count = df.count()

        if condition.lower().startswith("where "): 
            condition = condition[6:].lstrip()    # WHERE 시작인 경우 제거 

        del_count = df.filter(condition).count()   # spark_condition :  "IN_DTTM < DATE '2023-06-02'"

        # DELTE Target
        query_condition = condition.replace("`", "\"")
        delete_query = f"DELETE FROM {tableName} WHERE {query_condition}" # query_condition : "\"IN_DTTM\" < DATE '2023-06-02'"
        self._executeDB(delete_query)

        # INSERT Target
        self.saveTable(dataFrame, tableName)

        after_count = df.count()

        target_table = self.getTablePath(tableName)

        self.logger.debug(f"delSert : before = {before_count}, after = {after_count}, del = {del_count} [ {target_table} / {condition} ]")

        return (before_count, after_count, del_count, df)

    
    def countTableCondition(self, condition, tableName, dpath=None):
        df = self.loadTable(tableName)
        count = df.filter(condition).count()   # spark_condition :  "IN_DTTM < DATE '2023-06-02'"
        
        return count

    def queryTable(self, query, tableNames=None, dpath=None, customSchemas=None):
        self.logger.debug(("queryTable = ", query, tableNames))

        df = self.spark.read \
            .format("jdbc") \
            .option("url", self.connection_url) \
            .option("query", query) 
        
        for key, value in self.connection_properties.items():
            df = df.option(key, value)

        if customSchemas:
            df = df.schema(toCustomSchema(customSchemas)) 

        df = df.load()

        return df    
