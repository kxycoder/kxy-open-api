# coding=UTF-8

from kxy.framework.base_entity import BaseEntity as kxyBaseEntity
from kxy.framework.id_generator import SnowflakeIDGenerator
idgenerator = SnowflakeIDGenerator()

class BaseEntity(kxyBaseEntity):
    def InitInsertEntityWithJson(self, json_data):
        self.__init_require__(json_data, self.InsertRequireFields)
        self.__init_fileds__(json_data, self.InsertOtherFields)
        if self.__AutoId__ and not self.id:
            self.setId()
    def setId(self):
        if self._id_type == 'str':
            self.id = str(idgenerator.get_next_id())
        else:
            self.id = idgenerator.get_next_id()