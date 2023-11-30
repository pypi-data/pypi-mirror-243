""" standard imports """
from pydantic import BaseModel, Field


class RegScaleModel(BaseModel):
    """RegScale Base Model"""

    extra_data: dict = Field(default={}, hidden=True)

    def dict(self, **kwargs):
        """
        Override the default dict method to exclude hidden fields
        :param kwargs: kwargs
        :return: dict
        """
        hidden_fields = set(
            attribute_name
            for attribute_name, model_field in self.__fields__.items()
            if model_field.field_info.extra.get("hidden") is True
        )
        kwargs.setdefault("exclude", hidden_fields)
        return super().dict(**kwargs)
