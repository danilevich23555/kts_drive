# Этот файл не надо менять

from aiohttp.web_request import BodyPartReader


async def reader_iterator(reader: BodyPartReader, chunk_size: int = 5 * 1024 * 1024):
    while not reader.at_eof():
        chunk = b''
        while not reader.at_eof() and len(chunk) < chunk_size:
            chunk += await reader.read_chunk(size=chunk_size)
        yield chunk

