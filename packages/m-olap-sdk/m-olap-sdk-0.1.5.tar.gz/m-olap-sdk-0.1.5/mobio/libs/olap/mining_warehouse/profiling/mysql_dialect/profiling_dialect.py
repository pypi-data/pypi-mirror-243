import ast
import json

from mobio.libs.olap.mining_warehouse.profiling.mysql_dialect.base_dialect import (
    BaseDialect,
)

try:
    from mobio.libs.logging import MobioLogging

    m_log = MobioLogging()
except Exception:
    import logging as MobioLogging

    m_log = MobioLogging
from uuid import UUID
from sqlalchemy.exc import ProgrammingError
from mobio.libs.olap.mining_warehouse.profiling.mysql_dialect.profiling_session import (
    ProfilingSession,
)
from sqlalchemy import text


class ProfilingDialect(BaseDialect):
    def __init__(self, olap_uri):
        super().__init__(olap_uri)
        self.olap_uri = olap_uri
        self.session_class = ProfilingSession(olap_uri=self.olap_uri)

    def normalize_uuid(self, data: str) -> UUID:
        return UUID(data)

    def __parse_profile__(self, profile, fields, masking):
        response = {x: None for x in fields}
        if profile:
            for i in range(len(fields)):
                if fields[i] == "social_user" and profile[i]:
                    lst_social_user = ast.literal_eval(profile[i])
                    lst_social_response = []
                    for str_social_user in lst_social_user:
                        try:
                            arr_social_user = str_social_user.split("::")
                            lst_social_response.append(
                                {
                                    "social_id": arr_social_user[0],
                                    "social_type": int(arr_social_user[1]),
                                    "reachable": bool(arr_social_user[2]),
                                }
                            )
                        except Exception as ex:
                            m_log.warning(
                                f"fail when parse social_user {str_social_user}, {ex}"
                            )
                    response[fields[i]] = lst_social_response
                elif fields[i] == "profile_identify" and profile[i]:
                    lst_identify_response = []
                    lst_profile_identify = ast.literal_eval(profile[i])
                    for str_identify in lst_profile_identify:
                        try:
                            arr_identify = str_identify.split("::")
                            lst_identify_response.append(
                                {
                                    "identity_type": arr_identify[0],
                                    "identity_value": self.__masking_data__(
                                        arr_identify[1]
                                    )
                                    if masking
                                    else arr_identify[1],
                                }
                            )
                        except Exception as ex:
                            m_log.warning(
                                f"fail when parse profile_identify {str_identify}, {ex}"
                            )
                    response[fields[i]] = lst_identify_response
                elif fields[i] == "address_personal" and profile[i]:
                    lst_address_personal_response = []
                    lst_address_personal = ast.literal_eval(profile[i])
                    for str_address_personal in lst_address_personal:
                        try:
                            arr_address_personal = str_address_personal.split("::")
                            lst_address_personal_response.append(
                                {
                                    "type": arr_address_personal[0],
                                    "country_code": arr_address_personal[1],
                                    "state_code": arr_address_personal[2],
                                    "county_code": arr_address_personal[3],
                                    "city_code": arr_address_personal[4],
                                    "district_code": arr_address_personal[5],
                                    "subdistrict_code": arr_address_personal[6],
                                    "unique_value": arr_address_personal[7],
                                }
                            )
                        except Exception as ex:
                            m_log.warning(
                                f"fail when parse address_personal {str_address_personal}, {ex}"
                            )
                    response[fields[i]] = lst_address_personal_response
                elif fields[i] == "push_id" and profile[i]:
                    lst_push_id = ast.literal_eval(profile[i])
                    lst_push_id_response = []
                    for str_push_id in lst_push_id:
                        try:
                            arr_push_id = str_push_id.split("::")
                            lst_push_id_response.append(
                                {
                                    "push_id": self.__masking_data__(arr_push_id[0])
                                    if masking
                                    else arr_push_id[0],
                                    "os_type": int(arr_push_id[1]),
                                    "app_id": arr_push_id[2],
                                }
                            )
                        except Exception as ex:
                            m_log.warning(
                                f"fail when parse push_id {str_push_id}, {ex}"
                            )
                    response[fields[i]] = lst_push_id_response
                elif fields[i] in ["name", "cif"] and profile[i]:
                    response[fields[i]] = (
                        self.__masking_data__(profile[i]) if masking else profile[i]
                    )
                elif fields[i] in ["primary_email"] and profile[i]:
                    json_email = json.loads(profile[i])
                    response[fields[i]] = {
                        "status": json_email.get("status"),
                        "email": self.__masking_data__(json_email.get("email"))
                        if masking
                        else json_email.get("email"),
                        "last_check": json_email.get("last_check"),
                    }
                elif fields[i] in ["phone_number"] and profile[i]:
                    lst_phone = ast.literal_eval(profile[i])
                    response[fields[i]] = [
                        self.__masking_data__(str(x)) if masking else str(x)
                        for x in lst_phone
                    ]
                else:
                    response[fields[i]] = profile[i]
        return response

    def __get_profile__(
        self, merchant_id: str, profile_id: str, fields: list, masking: bool
    ) -> dict:
        lst_fields = ", ".join(fields)
        stmt = f"""
        select {lst_fields} from profiling.profile where merchant_id=:merchant_id and profile_id=:profile_id
        """
        with self.session_class.SessionLocal() as session:
            try:
                result = session.execute(
                    text(stmt),
                    {
                        "merchant_id": merchant_id,
                        "profile_id": profile_id,
                    },
                ).first()
            except ProgrammingError as pe:
                m_log.warning(
                    f"fail when fetch profile {merchant_id}, {profile_id}: {pe}"
                )
                result = None
        return self.__parse_profile__(profile=result, fields=fields, masking=masking)

    def __masking_data__(self, str_data: str) -> str:
        if str_data and type(str_data) == str:
            v = str(str_data)
            start = 2
            end = 1
            fill = 4
            if len(v) > fill + start + end:
                fill = len(v) - start - end
            v = (
                (v[:start] if start else "*" * start)
                + "*" * fill
                + (v[-end:] if end else "*" * end)
            )
            return v
        else:
            return "***"

    def __convert_criteria_to_field__(self, lst_criteria: list) -> list:
        # TODO phần này cần chuyển sang làm dạng code on fly. Criteria Mapping sẽ lấy từ DB ra để tránh update version SDK liên tục
        criteria_mapping = {
            "cri_merchant_id": {"field": "merchant_id"},
            "cri_profile_id": {"field": "profile_id"},
            "cri_birthday": {"field": "birthday"},
            "cri_name": {"field": "name"},
            "cri_gender": {"field": "gender"},
            "cri_address": {"field": "address"},
            "cri_city": {"field": "province_code"},
            "cri_province": {"field": "province_code"},
            "cri_province_code": {"field": "province_code"},
            "cri_job": {"field": "job"},
            "cri_operation": {"field": "operation"},
            "cri_hobby": {"field": "hobby"},
            "cri_created_account_type": {"field": "created_account_type"},
            "cri_marital_status": {"field": "marital_status"},
            "cri_birthday_period": {"field": "birthday"},
            "cri_created_time": {"field": "created_time"},
            "cri_nation": {"field": "nation"},
            "cri_card_level": {"field": "id", "path": "cards"},
            "cri_card_status": {"field": "status", "path": "cards"},
            "cri_tags_profile_multiple": {"field": "tags"},
            "cri_tags": {"field": "tags"},
            "cri_user_id": {"field": "profile_id"},
            "cri_phone": {"field": "phone_number"},
            "cri_email": {"field": "primary_email"},
            "cri_degree": {"field": "degree"},
            "cri_source": {"field": "source"},
            "cri_profile_group": {"field": "profile_group"},
            "cri_customer_created_time": {"field": "customer_created_time"},
            "cri_religiousness": {"field": "religiousness"},
            "cri_point": {"field": "point"},
            "cri_rank_point": {"field": "rank_point"},
            "cri_social_user": {"field": "social_user"},
            "cri_customer_id": {"field": "customer_id"},
            "cri_cif": {"field": "cif"},
            "cri_profile_identify": {"field": "profile_identify"},
            "cri_address_personal": {"field": "address_personal"},
            "cri_push_id": {"field": "push_id"},
        }
        lst_field = []
        for criteria in lst_criteria:
            if criteria and criteria in criteria_mapping:
                lst_field.append(
                    criteria_mapping.get(criteria).get("field")
                    if "path" not in criteria_mapping.get(criteria)
                    else "{}->'{}'".format(
                        criteria_mapping.get(criteria).get("path"),
                        criteria_mapping.get(criteria).get("field"),
                    )
                )
            elif criteria and criteria.startswith("cri_dyn_"):
                lst_field.append(str(criteria).replace("cri", ""))
            else:
                raise Exception(f"criteria {criteria} is not support now")
        return lst_field

    def __get_profiles__(
        self, merchant_id: str, profile_ids: list, fields: list, masking: bool
    ) -> list:
        lst_fields = ", ".join(fields)
        stmt = f"""
                select {lst_fields} from profiling.profile where merchant_id=:merchant_id and profile_id in (:profile_ids)
                """

        with self.session_class.SessionLocal() as session:
            try:
                result = session.execute(
                    text(stmt),
                    {
                        "merchant_id": merchant_id,
                        "profile_ids": ",".join(profile_ids),
                    },
                ).all()
            except ProgrammingError as pe:
                m_log.warning(
                    f"fail when fetch profiles {merchant_id}, {profile_ids}: {pe}"
                )
                result = []
        return [
            self.__parse_profile__(profile=x, fields=fields, masking=masking)
            for x in result
        ]

    def get_profile_by_criteria(
        self,
        merchant_id: str,
        profile_id: str,
        lst_criteria: list,
        masking: bool = True,
    ):
        lst_field = self.__convert_criteria_to_field__(lst_criteria=lst_criteria)
        if not lst_field:
            lst_field = ["merchant_id", "profile_id"]
        return self.__get_profile__(
            merchant_id=merchant_id,
            profile_id=profile_id,
            fields=lst_field,
            masking=masking,
        )

    def get_profiles_by_criteria(
        self,
        merchant_id: str,
        profile_ids: list,
        lst_criteria: list,
        masking: bool = True,
    ):
        lst_field = self.__convert_criteria_to_field__(lst_criteria=lst_criteria)
        if not lst_field:
            lst_field = ["merchant_id", "profile_id"]
        return self.__get_profiles__(
            merchant_id=merchant_id,
            profile_ids=profile_ids,
            fields=lst_field,
            masking=masking,
        )
