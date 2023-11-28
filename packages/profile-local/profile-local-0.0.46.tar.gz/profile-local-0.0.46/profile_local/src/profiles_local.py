from typing import Dict

from circles_local_database_python.generic_crud import GenericCRUD  # noqa: E402
from circles_number_generator.number_generator import NumberGenerator  # noqa: E402
from logger_local.Logger import Logger  # noqa: E402

from .constants_profiles_local import OBJECT_TO_INSERT_CODE

logger = Logger.create_logger(object=OBJECT_TO_INSERT_CODE)


class ProfilesLocal(GenericCRUD):

    def __init__(self):
        super().__init__(default_schema_name="profile", default_table_name="profile_table",
                         default_view_table_name="profile_view", default_id_column_name="profile_id")

    '''
    person_id: int,
    data: Dict[str, any] = {
        'name': name,
        'name_approved': name_approved,
        'lang_code': lang_code,
        'user_id': user_id,                             #Optional
        'is_main': is_main,                             #Optional
        'visibility_id': visibility_id,
        'is_approved': is_approved,
        'profile_type_id': profile_type_id, #Optional
        'preferred_lang_code': preferred_lang_code,     #Optional
        'experience_years_min': experience_years_min,   #Optional
        'main_phone_id': main_phone_id,                 #Optional
        'is_rip': is_rip,                                     #Optional
        'gender_id': gender_id,                         #Optional
        'stars': stars,
        'last_dialog_workflow_state_id': last_dialog_workflow_state_id
    },
    profile_id: int
    '''

    def insert(self, person_id: int, profile_dict: Dict[str, any]) -> int:
        """Returns the new profile_id"""
        logger.start(object={'data': str(profile_dict)})

        profile_table_json = {
            "`number`": NumberGenerator.get_random_number("profile", "profile_table", "`number`"),
            "user_id": profile_dict.get('user_id'),
            "person_id": person_id,
            "is_main": profile_dict.get('is_main'),
            "visibility_id": profile_dict.get('visibility_id'),
            "is_approved": profile_dict.get('is_approved'),
            "profile_type_id": profile_dict.get('profile_type_id'),
            "preferred_lang_code": profile_dict.get('preferred_lang_code'),
            "experience_years_min": profile_dict.get('experience_years_min'),
            "main_phone_id": profile_dict.get('main_phone_id'),
            "is_rip": profile_dict.get('is_rip'),
            "gender_id": profile_dict.get('gender_id'),
            "stars": profile_dict.get('stars'),
            "last_dialog_workflow_state_id": profile_dict.get('last_dialog_workflow_state_id')
        }
        super().insert(data_json=profile_table_json)

        profile_id = self.cursor.lastrowid()
        profile_ml_table_json = {
            "profile_id": profile_id,
            "lang_code": profile_dict.get('lang_code'),
            "name": profile_dict.get('name'),
            "name_approved": profile_dict.get('name_approved'),
            "about": profile_dict.get('about')
        }
        super().insert(table_name="profile_ml_table", data_json=profile_ml_table_json)

        logger.end(object={'profile_id': profile_id})
        return profile_id

    '''
    profile_id: int,
    data: Dict[str, any] = {
        'name': name,
        'name_approved': name_approved,
        'lang_code': lang_code,
        'user_id': user_id,                             #Optional
        'is_main': is_main,                             #Optional
        'visibility_id': visibility_id,
        'is_approved': is_approved,
        'profile_type_id': profile_type_id, #Optional
        'preferred_lang_code': preferred_lang_code,     #Optional
        'experience_years_min': experience_years_min,   #Optional
        'main_phone_id': main_phone_id,                 #Optional
        'is_rip': is_rip,                                     #Optional
        'gender_id': gender_id,                         #Optional
        'stars': stars,
        'last_dialog_workflow_state_id': last_dialog_workflow_state_id
    }
    person_id: int                                      #Optional
    '''

    def update(self, profile_id: int, profile_dict: Dict[str, any]) -> None:
        logger.start(object={'profile_id': profile_id,
                     'data': str(profile_dict)})
        profile_table_json = {
            "person_id": profile_dict.get('person_id'),
            "user_id": profile_dict.get('user_id'),
            "is_main": profile_dict.get('is_main'),
            "visibility_id": profile_dict.get('visibility_id'),
            "is_approved": profile_dict.get('is_approved'),
            "profile_type_id": profile_dict.get('profile_type_id'),
            "preferred_lang_code": profile_dict.get('preferred_lang_code'),
            "experience_years_min": profile_dict.get('experience_years_min'),
            "main_phone_id": profile_dict.get('main_phone_id'),
            "is_rip": profile_dict.get('is_rip'),
            "gender_id": profile_dict.get('gender_id'),
            "stars": profile_dict.get('stars'),
            "last_dialog_workflow_state_id": profile_dict.get('last_dialog_workflow_state_id')
        }
        super().update_by_id(id_column_value=profile_id, data_json=profile_table_json)

        profile_ml_table_json = {
            "profile_id": profile_id,
            "lang_code": profile_dict['lang_code'],
            "`name`": profile_dict['name'],
            "name_approved": profile_dict['name_approved'],
            "about": profile_dict.get('about')
        }
        super().update_by_id(table_name="profile_ml_table",
                             id_column_value=profile_id, data_json=profile_ml_table_json)
        logger.end()

    # TODO develop get_profile_object_by_profile_id( self, profile_id: int ) -> Profile[]:
    def get_profile_dict_by_profile_id(self, profile_id: int) -> Dict[str, any]:
        logger.start(object={'profile_id': profile_id})
        profile_ml_dict = self.select_one_dict_by_id(
            view_table_name="profile_ml_view", id_column_value=profile_id)
        profile_dict = self.select_one_dict_by_id(id_column_value=profile_id)
        logger.end(object={'profile_ml_dict': str(
            profile_ml_dict), 'profile_view': str(profile_dict)})
        if not profile_ml_dict or not profile_dict:
            return {}
        return {**profile_ml_dict, **profile_dict}

    def delete_by_profile_id(self, profile_id: int):
        logger.start(object={'profile_id': profile_id})
        self.delete_by_id(id_column_value=profile_id)
        logger.end()
