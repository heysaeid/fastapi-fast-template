from enum import StrEnum


class EnumMixin:
    
    @classmethod
    def get_names(cls):
        result = []
        for item in cls:
            result.append(item.name)
        return list(result)
    
    @classmethod
    def get_values(cls):
        result = []
        for item in cls:
            result.append(item.value)
        return list(result)


class ConfigTypeEnum(EnumMixin, StrEnum):
    MULTIPLE = "multiple"
    SINGLE =  "simple"


class ArgumentDefaultValueEnum(StrEnum):
    APP_NAME = "Fast Template"
    CONFIG_TYPE = ConfigTypeEnum.MULTIPLE