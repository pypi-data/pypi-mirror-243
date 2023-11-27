from .pxlogger import CustomLogger
from pyspark.sql import SparkSession
from .spark_session import get_spark_session
from .resource_manager import ResourceManager
#from .order_manager import OrderManager
from .util import Timer
from .util import parseSourceObject
from functools import reduce
from pyspark.sql.functions import collect_list, struct, split
from pyspark.sql.functions import col, lit
from datetime import datetime
import time
import math


class EltManager:
    def __init__(self, spark, config_file="config.yaml"):
        self.spark = spark
        self.logger = CustomLogger("EltManager")
        #self.odm = OrderManager(spark)
        self.config_file = config_file
      
    def init_rsm(
        self,
        source_type, source_topic, source_dpath,
        target_type, target_topic, target_dpath,
        chunk_size=50000, lowercase=True):

        self.source_type = source_type
        self.source_topic = source_topic
        self.source_dpath = source_dpath
        self.target_type = target_type
        self.target_topic = target_topic
        self.target_dpath = target_dpath

        self.chunk_size = chunk_size
        self.lowercase = lowercase
    
        # 소스 타겟 대상 초기화 
        rsm = ResourceManager(self.spark, self.config_file)
        
        # 소스 대상 정의
        self.source_tm = rsm.get_resource_manager(source_type, source_topic, dpath=source_dpath) #oracle

        # 타셋 대상 정의
        self.target_tm = rsm.get_resource_manager(target_type, target_topic, dpath=target_dpath) #delta

        
    def getSourceManager(self) :
        return self.source_tm 
        
    def getTargetManager(self) :
        return self.target_tm
        
    def _getSourceInfo(self, source_objects) :
        return (
            f"{self.source_type} {self.source_topic} {self.source_dpath} {source_objects}"
            if self.source_dpath is not None
            else f"{self.source_type} {self.source_topic} _ {source_objects}"
        )
    
    def _getTargetInfo(self, target_object) :
        return (
            f"{self.target_type} {self.target_topic} {self.target_dpath} {target_object}"
            if self.target_dpath is not None
            else f"{self.target_type} {self.target_topic} _ {target_object}"
        )
    
    # Single tables full load
    def ingest_fulls(self, source_objects, target_object, source_customSchema=None, target_customSchema=None, count=True, offset=0, cleansing_conditions=None) :    
        sourceTables = parseSourceObject(tableNames)
        dataframes = {}

        for sourceTable in sourceTables: 
            (source_df, cleaned_target_df, valid) = self.ingest_full(sourceTable, target_object, sourceTables, sourceTables, count, offset, cleansing_conditions)
            dataframes[sourceTable] = (source_df, cleaned_target_df, valid)

        return dataframes        


    def ingest_full(self, source_object, target_object, source_customSchema=None, target_customSchema=None, count=True, offset=0, cleansing_conditions=None, delemeter=None, append_mode=False) :
        # 소스 > 타겟 Ingestion (chunk load)
        sourceTable = source_object[0]   # 단일 테이블에 대해서만 ingest_full 처리, 복수 테이블은 increment 기반 처리
        targetTable = target_object

        sourceInfo = self._getSourceInfo(source_object)
        targetInfo = self._getTargetInfo(target_object)

        timer = Timer()
        self.logger.info(f"ETL/FL Started : [ {targetInfo} ]")

        source_df = None
        chunk_size = self.chunk_size

        target_df_org_count = 0
        if append_mode :
            target_df = self.target_tm.loadTable(targetTable)
            if target_df is not None :
                target_df_org_count = target_df.count()
            self.logger.info(f"Target count before append : {targetInfo} ({target_df_org_count})")

        if count is True:  # For RDBMS option
            source_df = self.source_tm.loadTable(sourceTable)
            if source_df is None :
                self.logger.error(f"ETL/FL Done : [ {targetInfo} / True (0, 0) / {timer.tab():.2f} ]")
                return (None, None, True)

            size = source_df.count()

            if self.source_tm.getType() == "delta" and self.target_tm.getType() == "delta":
                chunk_size = source_df.count()

            self.logger.info(f"Source count = {size} / expected loop {math.ceil(size / chunk_size)} / {timer.tab():.2f}")


        offset = offset
        chunk_read_size = chunk_size
        tot_cleaned_count = 0

        while chunk_read_size == chunk_size:

            # Oracle 데이터 읽기
            source_df = None
            if self.source_tm.getType() == "delta" and self.target_tm.getType() == "delta": # in case of delta to delta, we don't calculate row_num
                source_df = self.source_tm.loadTable(sourceTable, offset=None, customSchema=source_customSchema)  # Full load
            elif self.source_tm.getType() == "csv":
                source_df = self.source_tm.loadTable(sourceTable, offset=offset, chunk_size=chunk_size, customSchema=source_customSchema, delemeter=delemeter)
            else:
                source_df = self.source_tm.loadTable(sourceTable, offset=offset, chunk_size=chunk_size, customSchema=source_customSchema)

            # 데이터가 없으면 종료
            if source_df is None :
                self.logger.error(f"ETL/FL Done : [ {targetInfo} / True (0, 0) / {timer.tab():.2f} ]")
                return (None, None, True)

            #source_df.cache()

            chunk_read_size = source_df.count()

            self.logger.info(f"Source Loading Chunk : {sourceInfo} / seq={math.ceil(offset / chunk_size + 1)} offset={offset} chunk_size={chunk_read_size} / elipsed={timer.tab():.2f}")

            cleaned_source_df = source_df
            if cleansing_conditions is not None:
                cleaned_count, cleaned_source_df = self.cleansing(source_df, cleansing_conditions)
                self.logger.info(f"Source  Cleaning : {sourceInfo} / cleaned_size={cleaned_count} / elipsed={timer.tab():.2f}")
                tot_cleaned_count += cleaned_count

            # Save to Delta
            if offset == 0 and append_mode is not True:
                # 컬럼 이름을 소문자로 변환
                if self.lowercase is True:
                    cleaned_source_df = cleaned_source_df.toDF(*[col.lower() for col in cleaned_source_df.columns])

                self.target_tm.saveTable(cleaned_source_df, targetTable, mode="overwrite")
            else:
                self.target_tm.saveTable(cleaned_source_df, targetTable, mode="append")

            self.logger.info(f"Target  Saving Chunk : {targetInfo} / elipsed={timer.tab():.2f}")

            offset += chunk_read_size

            if self.source_tm.getType() == "csv":
                self.source_tm.archive(sourceTable)

            if self.source_tm.getType() == "delta" and self.target_tm.getType() == "delta":  # Full loaded already
                chunk_read_size = 0

        self.logger.info(f"Source Loading Count : {sourceInfo} ({offset})")

        target_df = self.target_tm.loadTable(targetTable)
        self.logger.info(f"Target Saving Count : {targetInfo} ({target_df.count()})")

        valid = offset == target_df.count() + tot_cleaned_count - target_df_org_count

        self.logger.info(f"ETL/FL Done : [ {targetInfo} / {valid} ({offset}, {target_df.count() - target_df_org_count}, {tot_cleaned_count}) / {timer.elapsed():.2f} ]")

        source_df = self.source_tm.loadTable(sourceTable)

        return (source_df, target_df, valid)
  
    # (Bronze: Oracle > Delta) 
    # source_inc_query = """
    #     SELECT * FROM BCPARKING.TB_TMINOUT 
    #     WHERE IN_DTTM < TO_DATE('2023-06-02', 'YYYY-MM-DD')
    #     -- WHERE IN_DTTM >= TO_DATE('2023-06-02','YYYY-MM-DD') AND IN_DTTM < TO_DATE('2023-06-03','YYYY-MM-DD')
    # """
    #
    # (Silver / Gold / Mart) 
    # source_inc_query = """
    #     SELECT * FROM tb_tminout 
    #     WHERE IN_DTTM < DATE '2023-06-02'
    # """ 
    # target_condition = "`IN_DTTM` < DATE '2023-06-02'"
    #

    # Multiple tables incremental load 
    def ingest_increment(self, source_objects, target_object, source_inc_query, target_condition,  
                         source_df=None, source_customSchema=None, target_customSchema=None, cleansing_conditions=None) :    

        sourceInfo = self._getSourceInfo(source_objects)
        targetInfo = self._getTargetInfo(target_object)
        
        timer = Timer()
        self.logger.info(f"ETL/IC Started : [ {targetInfo} ]")

        if source_df is None:
            source_df = self.source_tm.queryTable(source_inc_query, tableNames=source_objects, customSchemas=source_customSchema)

        # 데이터가 없으면 종료
        if source_df is None :
            self.logger.error(f"ETL/IC Error : [ {targetInfo} / True (0, 0) / {timer.tab():.2f} ]")
            return (None, None, True)

        #source_df.cache()

        source_read_size = source_df.count()
        self.logger.info(f"Source Loading : {sourceInfo} / source_size={source_read_size} / elipsed={timer.tab():.2f}")

        if target_customSchema:
            for column_name, data_type in target_customSchema.items():
                source_df = source_df.withColumn(column_name, source_df[column_name].cast(data_type))

        cleaned_source_df = source_df
        cleaned_count = 0
        if cleansing_conditions is not None:
            cleaned_count, cleaned_source_df = self.cleansing(source_df, cleansing_conditions)
            self.logger.info(f"Source  Cleaning : {sourceInfo} / cleaned_size={cleaned_count} / elipsed={timer.tab():.2f}")

        # Save to Delta Incrementally
        before_count, after_count, del_count, target_df = self.target_tm.delSert(cleaned_source_df, target_condition, target_object)

        self.logger.info(f"Target  Saving : {targetInfo} / delsert_size={after_count - before_count + del_count} (before={before_count}, after={after_count}, del={del_count}) / elipsed={timer.tab():.2f}")

        target_read_size = self.target_tm.countTableCondition(target_condition, target_object)
        valid = source_read_size == target_read_size + cleaned_count
        self.logger.info(f"ETL/IC Done : [ {targetInfo} / {valid} ({source_read_size}, {target_read_size}, {cleaned_count}) / {timer.elapsed():.2f} ]")

        # insert_log(spark, schema_name, table_name, datetime.now(), rundate)
        # logger.info(f" Update Job logs : {targetTopic}]")   ac

        return (source_df, target_df, valid)
        
    # condition1 = ~col("aaa").like("%.%")
    # cleansing_condition = F.col("vehno").isNotNull()  # Null 아닌것만 저장
    # condition2 = col("bbb") != "xyz"
    def cleansing(self, target_df,  cleansing_conditions=None):
        if cleansing_conditions is None:
            return (0, target_df)

        cleaned_df = target_df.filter(cleansing_conditions)
        count = target_df.count() - cleaned_df.count()
        self.logger.debug(f"Cleansed count={count} (before={target_df}, after={cleaned_df})")

        return (count, cleaned_df)

# from lib.elt_manager import EltManager
# em = EltManager(spark)        
#
# (Bronze Config)
# source_type = "oracle"
# source_topic = "bcparking"
# source_objects = ["tb_tminout"]
# target_type = "delta"
# target_topic = "bronze-bcparking"
# target_object = "tb_tminout"
#
# (Bronze Full Load)
# em.init_rsm(source_type, source_topic, target_type, target_topic, 500000)
# source_df, target_df = em.ingest_full(source_objects, target_object)
#
# (Bronze Incremental Load)
# source_inc_query = """
#     SELECT * FROM BCPARKING.TB_TMINOUT 
#     WHERE IN_DTTM < TO_DATE('2023-06-02', 'YYYY-MM-DD')
#     -- WHERE IN_DTTM >= TO_DATE('2023-06-02','YYYY-MM-DD') AND IN_DTTM < TO_DATE('2023-06-03','YYYY-MM-DD')
# """
# target_condition = "`IN_DTTM` < DATE '2023-06-02'"
# source_df, target_df = em.ingest_increment(source_objects, target_object, source_inc_query, target_condition)
#
# (Mart Config)
# source_type = "delta"
# source_topic = "gold"
# source_objects = ["tb_tminout"]
# target_type = "postgresql"
# target_topic = "mart"
# target_object = "public.tb_tminout"
#
# (Bronze Full Load)
# em.init_rsm(source_type, source_topic, target_type, target_topic, 500000)
# source_df, target_df = em.ingest_full(source_objects, target_object)
#
# (Incremental Load)
# source_inc_query = """
#     SELECT * FROM tb_tminout 
#     WHERE IN_DTTM < DATE '2023-06-02'
# """ 
# target_condition = "`IN_DTTM` < DATE '2023-06-02'"
# source_df, target_df = em.ingest_increment(source_objects, target_object, source_inc_query, target_condition)

                                
