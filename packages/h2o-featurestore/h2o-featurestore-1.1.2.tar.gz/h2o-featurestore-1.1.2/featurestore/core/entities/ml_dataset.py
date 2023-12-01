import datetime
import json
import re
import time
from typing import Optional

from google.protobuf.timestamp_pb2 import Timestamp

import ai.h2o.featurestore.api.v1.CoreService_pb2 as pb
import ai.h2o.featurestore.api.v1.OnlineApi_pb2 as OnlineApi
from ai.h2o.featurestore.api.v1.CoreService_pb2_grpc import CoreServiceStub

from ...rest_stub import RestStub
from ..job_info import JobInfo
from ..utils import Utils
from .ml_data_feature import MLDatasetFeature


class OnlineToken:
    def __init__(self, ml_dataset_id, token, signature, valid_to: datetime.datetime):
        self.ml_dataset_id = ml_dataset_id
        self.token = token
        self.signature = signature
        self.valid_to = valid_to

    def is_valid_for(self, ml_dataset_id):
        return (
            self.valid_to > (datetime.datetime.utcnow() - datetime.timedelta(minutes=1))
            and self.ml_dataset_id == ml_dataset_id
        )


class MLDataset:
    def __init__(self, stub: CoreServiceStub, rest_stub: RestStub, ml_dataset_proto):
        self._online_retrieval_token: Optional[OnlineToken] = None
        ml_dataset = pb.MLDataset()
        ml_dataset.CopyFrom(ml_dataset_proto)
        self._ml_dataset = ml_dataset
        self._stub = stub
        self._rest_stub = rest_stub

    @property
    def id(self):
        return self._ml_dataset.id

    @property
    def name(self):
        return self._ml_dataset.name

    @property
    def description(self):
        return self._ml_dataset.description

    @property
    def primary_keys(self):
        return self._ml_dataset.primary_keys

    @description.setter
    def description(self, value):
        update_request = pb.UpdateMLDatasetRequest(
            ml_dataset_id=self.id,
            description=value,
        )
        ml_dataset_proto = self._stub.UpdateMLDataset(update_request)
        ml_dataset = pb.MLDataset()
        ml_dataset.CopyFrom(ml_dataset_proto)
        self._ml_dataset = ml_dataset

    @property
    def start_date_time(self):
        timestamp: Timestamp = self._ml_dataset.start_date_time
        if timestamp:
            return datetime.datetime.fromtimestamp(timestamp.ToMilliseconds() / 1000, tz=datetime.timezone.utc)
        else:
            return None

    @property
    def end_date_time(self):
        timestamp: Timestamp = self._ml_dataset.end_date_time
        if timestamp:
            return datetime.datetime.fromtimestamp(timestamp.ToMilliseconds() / 1000, tz=datetime.timezone.utc)
        else:
            return None

    @property
    def features(self):
        return [MLDatasetFeature(feature) for feature in self._ml_dataset.features]

    def delete(self):
        """Deletes ML Dataset."""
        request = pb.DeleteMLDatasetRequest(ml_dataset_id=self.id)
        self._stub.DeleteMLDataset(request)

    def download(self, output_dir=None):
        """Download files to the specified directory location.

        Args:
            output_dir: (str) A directory location as string. Default is None.

        Returns:
            str: A directory path where the files are downloaded.

        Typical usage example:
            dir = ml_dataset.download()

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/feature_view_api.html#downloading-the-files-from-feature-store-from-the-ml-dataset
        """
        request = pb.RetrieveMLDatasetAsAsLinksRequest(ml_dataset_id=self.id)
        job_id = self._stub.StartRetrieveMLDatasetAsLinksJob(request)

        info = JobInfo(self._stub, job_id)
        while not self._stub.GetJob(job_id).done:
            info.show_progress()
            time.sleep(2)
        info.show_progress()  # there is possibility that some progress was pushed before finishing job
        response = self._stub.GetRetrieveMLDatasetAsLinksJobOutput(job_id)

        return Utils.download_files(output_dir, response.download_links)

    def as_spark_frame(self, spark_session):
        """Return a spark data frame.

        This generates a data frame of the retrieved data using a spark session.

        Args:
            spark_session: (SparkSession) Represents a spark session.

        Returns:
            DataFrame: Represents a spark data frame.

            The frame is made up of columns as features and rows as records.
            Rows contain data within retrieve scope (filtered).

        Typical usage example:
            data_frame = ml_dataset.as_spark_frame(sparkSession)

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/feature_view_api.html#obtaining-data-as-a-spark-frame-from-the-ml-dataset
        """
        from ..commons.spark_utils import SparkUtils

        session_id = spark_session.conf.get("ai.h2o.featurestore.sessionId", "")
        request = pb.RetrieveMLDatasetAsSparkRequest(ml_dataset_id=self.id, session_id=session_id)

        response = self._stub.RetrieveMLDatasetAsSpark(request)
        spark_session.conf.set("ai.h2o.featurestore.sessionId", response.session_id)

        SparkUtils.configure_user_spark(spark_session)
        if response.offline_storage_format == pb.OfflineStorageFormat.OFFLINE_STORAGE_FORMAT_SNOWFLAKE:
            df = self.__load_data_from_snowflake(response, spark_session)
        else:
            df = self.__load_data_from_parquet(response, spark_session)

        return df

    def __load_data_from_parquet(self, response, spark_session):
        for k, v in response.options.items():
            spark_session.conf.set(k, v)
        df = spark_session.read.format("parquet").load(response.path)
        return df

    def __load_data_from_snowflake(self, response, spark_session):
        df = (
            spark_session.read.format("net.snowflake.spark.snowflake")
            .options(**response.options)
            .option("dbtable", response.path)
            .load()
        )
        for col_name in df.schema.names:
            df = df.withColumnRenamed(col_name, re.sub(r"(^_|_$)", "", col_name.replace('"', "")))

        return df

    def retrieve_online(self, *keys):
        """Retrieve data from the online Feature Store.

        Args:
            keys: (Any) A specific primary key value for which the entry is obtained.

        Returns:
            dict: A dictionary of specific instance (JSON row).

            For example:

            {'id': '01', 'department': 'Engineering', 'name': 'Test'}

        Typical example:
            ml_dataset.retrieve_online(1)

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/feature_view_api.html#retrieving-data-from-online-feature-store
        """
        if self._online_retrieval_token is None or not self._online_retrieval_token.is_valid_for(self.id):
            request = OnlineApi.OnlineMLDataSetRetrieveTokenRequest(ml_dataset_id=self.id)

            response: OnlineApi.OnlineRetrieveTokenResponse = self._stub.GenerateMLDatasetOnlineRetrievalToken(request)
            self._online_retrieval_token = OnlineToken(
                ml_dataset_id=self.id,
                token=response.token,
                signature=response.signature,
                valid_to=Utils.timestamp_to_datetime(response.valid_to),
            )

        response = self._rest_stub.online_store.get(
            f"/v1/retrieve/ml-datasets/{self.id}",
            params={
                "token": self._online_retrieval_token.token,
                "signature": self._online_retrieval_token.signature,
                "key": map(lambda x: str(x), keys),
            },
        )
        json_row = response["row"]

        return json.loads(json_row)

    def __repr__(self):
        return Utils.pretty_print_proto(self._ml_dataset)

    def __str__(self):
        nl = "\n"
        return (
            f"Name                  : {self.name} \n"
            f"Description           : {self.description} \n"
            f"Feature view version  : {self._ml_dataset.feature_view_version} \n"
            f"State                 : {self._ml_dataset.state} \n"
            f"Primary keys          : {self.primary_keys} \n"
            f"Features              : \n{nl.join(self._custom_feature_fields())} \n"
        )

    def _custom_feature_fields(self):
        tmp_list = list()
        for feature in self.features:
            s = (
                "   {\n"
                f"     Name             : {feature.name} \n"
                f"     Data type        : {feature.data_type} \n"
                f"     Is primary key?  : {feature.is_primary_key} \n"
                "   }"
            )
            tmp_list.append(s)
        return tmp_list
