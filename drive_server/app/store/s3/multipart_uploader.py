# Этот файл не надо менять
from drive_server.app.config.dataclasses import S3ConfigSection


class MultipartUploader:
    def __init__(self, client, config: S3ConfigSection, key: str) -> None:
        self._client = client
        self._config = config
        self.key = key
        self._part_number = None
        self._parts = None
        self._mpu = None
        self.uploaded_size = 0

    async def __aenter__(self):
        await self.create_uploading()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.finish_uploading()
        except Exception as e:
            await self._client.abort_multipart_upload(
                Bucket=self._config.bucket_name,
                Key=self.key,
                UploadId=self._mpu["UploadId"],
            )
            raise e

    async def create_uploading(self, ) -> None:
        self._parts = []
        self._part_number = 1

        self._mpu = await self._client.create_multipart_upload(
            ACL=self._config.acl,
            Bucket=self._config.bucket_name,
            Key=self.key,
        )

    async def upload_part(self, chunk: bytes) -> None:
        part = await self._client.upload_part(
            Bucket=self._config.bucket_name,
            Key=self.key,
            PartNumber=self._part_number,
            UploadId=self._mpu["UploadId"],
            Body=chunk,
        )

        self._parts.append({"PartNumber": self._part_number, "ETag": part["ETag"]})
        self._part_number += 1

        self.uploaded_size += len(chunk)

    async def finish_uploading(self) -> None:
        part_info = {"Parts": self._parts}
        await self._client.complete_multipart_upload(
            Bucket=self._config.bucket_name,
            Key=self.key,
            UploadId=self._mpu["UploadId"],
            MultipartUpload=part_info,
        )
