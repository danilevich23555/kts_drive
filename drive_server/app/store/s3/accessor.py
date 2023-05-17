import typing
from datetime import datetime

from aiobotocore import get_session
from aiobotocore.session import AioSession
from aiohttp import BodyPartReader

from drive_server.app.api.utils.part_iterator import reader_iterator
from drive_server.app.base.connect_accessor import ConnectAccessor
from drive_server.app.config.dataclasses import S3ConfigSection
from drive_server.app.store.s3.multipart_uploader import MultipartUploader
from drive_server.app.settings.settings import settings

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

class S3Accessor(ConnectAccessor):
    def _init_(self):
        self._session: AioSession = get_session()
        self.config: S3ConfigSection = self.app.config.s3

    async def _connect(self) -> None:
        # TODO: проверить соединение с S3, вызвав список бакетов
        pass

    async def upload(self, key: str, reader: BodyPartReader, upload_callback: typing.Optional[callable] = None):
        # более подробное объяснения этого места в коде можно найти в уроке
        async with self._session.create_client('s3', **self.config.credentials) as client:
            async with MultipartUploader(client=client, config=self.config, key=key) as mpu:
                async for chunk in reader_iterator(reader):
                    await mpu.upload_part(chunk)
                    if upload_callback:
                        await upload_callback(mpu.uploaded_size)

    async def delete_object(self, key: str) -> None:
        # TODO: удалить объект из S3
        raise NotImplementedError

    async def list_objects(self) -> list[dict]:
        # TODO: получить список файлов из S3
        async with self._session.create_client('s3', **self.config.credentials) as client:
            paginator = client.get_paginator('list_objects')
            files = []
            async for result in paginator.paginate(Bucket=self.config.bucket_name):
                for c in result.get('Contents', []):
                    c['LastModified'] = serialize_datetime(c['LastModified'])
                    files.append(c)
                return files
