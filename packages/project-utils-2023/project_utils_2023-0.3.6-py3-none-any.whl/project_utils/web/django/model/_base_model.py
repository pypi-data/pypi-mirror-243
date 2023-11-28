import traceback

from asgiref.sync import sync_to_async
from django.db.models import Model, Manager, CharField, BooleanField

from project_utils.exception import ModelException
from ._id_model import IDModel
from ._base_meta import BaseMeta


class BaseModel(Model):
    objects: Manager = Manager()

    id: CharField = CharField(max_length=30, verbose_name="ID", blank=True, primary_key=True,
                              default=IDModel.create_id())
    is_delete: BooleanField = BooleanField(verbose_name="删除标记", blank=True, default=False)

    @classmethod
    async def async_filter(cls, *args: ..., **kwargs: ...):
        return await sync_to_async(cls.objects.filter)(*args, **kwargs)

    @classmethod
    def get_fields(cls):
        return [field.name for field in cls._meta.get_fields()]

    @classmethod
    async def async_get_field(cls):
        return [field.name for field in cls._meta.get_fields()]

    @classmethod
    def get_one(cls, *args, **kwargs):
        try:
            return cls.objects.get(*args, **kwargs)
        except Exception as e:
            raise ModelException(str(e), error_detail=traceback.format_exc())

    @classmethod
    async def async_get_one(cls, *args, **kwargs):
        try:
            return await cls.objects.aget(*args, **kwargs)
        except Exception as e:
            raise ModelException(str(e), traceback.format_exc())

    class Meta(BaseMeta):
        abstract: bool = True
