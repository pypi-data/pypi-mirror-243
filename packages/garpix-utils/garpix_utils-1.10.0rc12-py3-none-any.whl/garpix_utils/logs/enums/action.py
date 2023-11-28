from enum import Enum

from garpix_utils.logs.enums.get_enums import ActionType, ActionLevel
from garpix_utils.logs.services.logger_iso import ActionElement


class ActionDefault(Enum):
    # 100-109 | Управление учетными записями пользователей
    user_registration = ActionElement(100, ActionType.user_account, 'Регистрация', ActionLevel.info)
    user_create = ActionElement(101, ActionType.user_account, 'Создание пользователя', ActionLevel.info)
    user_change = ActionElement(102, ActionType.user_account, 'Изменение параметров пользователя', ActionLevel.warning)
    user_delete = ActionElement(103, ActionType.user_account, 'Удаление пользователя', ActionLevel.warning)

    # 110-119 | Идентификация и аутентификация субъекта доступа
    user_login = ActionElement(110, ActionType.authentication, 'Вход в систему', ActionLevel.info)
    user_logout = ActionElement(111, ActionType.authentication, 'Выход из системы', ActionLevel.info)

    # 120-129 | Управление атрибутами доступа
    user_access = ActionElement(120, ActionType.user_access_attribute, 'Изменение привилегий пользователя', ActionLevel.warning)

    # 130-139 | Доступ к защищаемой информации
    user_exist = ActionElement(130, ActionType.access_information, 'Проверка существования пользователя', ActionLevel.info)

    # 140-149 | Удаление информации
    any_entity_delete = ActionElement(140, ActionType.delete_information, 'Удаление сущностей', ActionLevel.info)

    # 150-159 | Добавление информации
    any_entity_create = ActionElement(150, ActionType.create_information, 'Создание сущностей', ActionLevel.info)

    # 160-169 | Изменение информации
    any_entity_change = ActionElement(160, ActionType.change_information, 'Изменение сущностей', ActionLevel.info)

    # 170-179 | Изменение конфигураций
    configuration_change = ActionElement(170, ActionType.change_configuration, 'Изменение конфигураций', ActionLevel.info)

    '''
        100-109 | Управление учетными записями пользователей
        110-119 | Идентификация и аутентификация субъекта доступа
        120-129 | Управление атрибутами доступа
        130-139 | Доступ к защищаемой информации
        140-149 | Удаление информации
        150-159 | Добавление информации
        160-169 | Изменение информации
        170-179 | Изменение конфигураций
    '''
