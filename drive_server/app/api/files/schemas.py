from marshmallow import Schema, fields


class FileSchema(Schema):
    # TODO: файл должен содержать поля key, size и last_modified.
    #  S3 отдает их немного с другими названиями, поэтому можно посмотреть в сторону параметра attribute для поля
    #  https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Field
    pass


class FilesSchema(Schema):
    # TODO: список файлов в поле items
    pass


class FilesUploadSchema(Schema):
    # TODO: сделать, из чего состоит можно посмотреть в Swagger, приложенном к заданию
    pass


class FilesDeleteSchema(Schema):
    # TODO: удаление происходит по ключу
    key = fields.Str()
