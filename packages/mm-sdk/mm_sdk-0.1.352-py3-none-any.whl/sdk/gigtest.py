from datetime import date as datetime_date
from enum import Enum, IntEnum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl

from .client import Empty, SDKClient, SDKResponse


COMMON_GIGTEST_TIMEOUT = 10
LONG_GIGTEST_TIMEOUT = 60 + 2


class MedResearchType(IntEnum):
    exam = 0
    lab = 1


class MedResearchBlockType(Enum):
    exam = 0
    lab = 1
    vaccine = 2


class ActivityResponse(BaseModel):
    id: int = Field(description="id")
    key: str = Field(description="unique key")
    parent_id: Optional[int] = Field(description="id of parent activity")
    title: str = Field(description="unique key")


class SectionResponse(BaseModel):
    id: int = Field(description="id")
    activity_key: Optional[str] = Field(description="Тип деятельности из activities.key")
    title: str = Field(description="Название")
    image_url: Optional[str] = Field(description="Картинка типа")
    recommended: bool = Field(description="Рекомендовано или нет")


class CountryResponse(BaseModel):
    id: int = Field(description="id")
    name: str = Field(description="Название")


class MedResearchResult(BaseModel):
    id: int = Field(description="id")
    name: str = Field(description="Название")
    key: str = Field(description="Уникальный идентификатор")
    value: int = Field(description="Значение")


class MedicalResearchResponse(BaseModel):
    id: int = Field(description="id")
    name: str = Field(description="Название")
    key: str = Field(description="Уникальный идентификатор")
    activity_keys: List[str] = Field(description="Ключи типов деятельности")
    period: Optional[int] = Field(description="Периодичность в месяцах")
    important: bool = Field(
        description="Важность исследования. В случае положительно результата, "
        "заявитель будет заблокирован"
    )
    type: MedResearchType = Field(description="Тип исследования")
    block_type: MedResearchBlockType = Field(description="Тип группы исследований")
    results: List[MedResearchResult] = Field(
        description="Справочник возможных" " результатов"
    )

    class Config:
        use_enum_values = True


# КЛИЕНТ
class SearchClientRequest(BaseModel):
    medbook_number: str = Field(description="Номер ЛМК")
    lastname: str = Field(description="Фамилия")


class ClientInfo(BaseModel):
    home_address: Optional[str] = Field(description="Адрес")
    phone: Optional[str] = Field(description="Телефон")
    company_name: Optional[str] = Field(description="Название организации")
    position: Optional[str] = Field(description="Должность")
    birthday: Optional[datetime_date] = Field(description="Дата рождения")


class CreateClientRequest(ClientInfo):
    fio: str = Field(description="ФИО")
    birthday: datetime_date = Field(description="Дата рождения")
    country_id: int = Field(description="Id страны по справочнику")


class UpdateClientRequest(ClientInfo):
    pass


class ClientResponse(ClientInfo):
    id: int = Field(description="Id гигтест клиента")
    birthday: Optional[str] = Field(description="Дата рождения")


# МЕДКНИЖКА
class MedicalBookRequest(BaseModel):
    number: str = Field(description="Номер ЛМК")
    regnum: str = Field(description="Рег.номер ЛМК")
    date: datetime_date = Field(description="Дата выдачи ЛМК")
    user_id: int = Field(description="Id гигтест клиента")
    activity_keys: list = Field(description="Ключи типов деятельности")


class UserExtended(ClientInfo):
    fio: str = Field(description="ФИО")
    birth_date: str = Field(description="Дата рождения")


class MedicalBookSearchResponseOther(BaseModel):
    id: int = Field(description="Id ЛМК в гигтесте")
    number: str = Field(description="Номер ЛМК")
    regnum: str = Field(description="Рег. номер ЛМК")
    date: str = Field(description="Дата выдачи ЛМК")
    next_education_date: str = Field(description="Дата следующей аттестации")
    status: str = Field(description="Статус ЛМК: new, accepted, returned, completed")
    activity_names: list = Field(description="Тип деятельности")
    user: UserExtended = Field(description="Гигтест клиент")
    medical_direction_ids: list = Field(description="Гигтест id мед. направлений")


class User(BaseModel):
    fio: str


class MedicalBookSearchResponse(BaseModel):
    number: str = Field(description="Номер ЛМК")
    date: str = Field(description="Дата выдачи ЛМК")
    user: User = Field(description="ФИО гигтест клиента")
    id: int = Field(description="Id ЛМК в гигтесте")


class MedicalBookResponse(BaseModel):
    id: int = Field(description="Id ЛМК в гигтесте")


# АТТЕСТАЦИЯ
class AttestationRequest(BaseModel):
    date: datetime_date = Field(description="Дата первичной/периодической аттестации")
    section_id: int = Field(description="Id раздела")
    questions: dict = Field(description="Объект из id вопрос-ответ")
    medbook_id: Optional[int] = Field(description="Id ЛМК в гигтесте")
    medbook_number: Optional[str] = Field(description="Номер ЛМК")
    mb_regnum: str = Field(description="Рег.номер ЛМК")
    mb_date: datetime_date = Field(description="Дата выдачи ЛМК")
    attestation_number: int = Field(description="1 или 0 (первичная или периодическая)")
    user_id: int = Field(description="Id гигтест клиента")


class AttestationResponse(BaseModel):
    id: int = Field(description="Id фттестации в гигтесте")
    passed: bool = Field(description="Сдал или нет")
    result: str = Field(description="Результат")
    percent: int = Field(description="Процент сдачи")


# МЕДИЦИНА
class MedicineCreateRequest(BaseModel):
    user_id: int = Field(description="Id гигтест клиента")
    medbook_number: str = Field(description="Номер ЛМК")
    activity_key: str = Field(description="Ключи типов деятельности")
    medical_type: str = Field(
        description="Тип медосмотра (preliminary-предварительный, periodic-периодический"
    )
    direction_date: datetime_date = Field(description="Дата направления медосмотра")
    date_completion: Optional[datetime_date] = Field(
        description="Дата завершения медосмотра"
    )


class MedicineUpdateRequest(BaseModel):
    medbook_number: str = Field(description="Номер ЛМК")
    date_completion: datetime_date = Field(description="Дата завершения медосмотра")
    results: dict = Field(description="Исследования")


class MedDirectionResultData(BaseModel):
    result_id: str = Field(description="Id исследования в гигтест")
    date_med_result: datetime_date = Field(description="Дата исследования")
    description: str = Field(description="Описание")
    self_explored: int = Field(description="0/1 (проведено у нас или нет)")


class AdditionalMedDirectionResultRequest(MedDirectionResultData):
    medical_research_id: int = Field(description="Id исследования в гигтест")
    medical_direction_id: int = Field(description="Id медобследования в гигтест")


class MedicineCreateOrUpdateResponseResults(BaseModel):
    medical_research_id: int = Field(description="Id исследования в гигтест")
    id: int = Field(description="Id медобследования в гигтест")


class MedicineCreateOrUpdateResponseResultsExtended(
    MedicineCreateOrUpdateResponseResults
):
    medical_research_name: str = Field(description="Название услуги")
    date_med_result: str = Field(description="Дата обследования")
    medical_research_result: int = Field(
        description="Результат обследования. Предположительно 1 - нет противопоказаний"
    )
    medical_research_key: str = Field(description="Код услуги по справочнику гигтест")


class MedicineCreateResponse(BaseModel):
    id: int = Field(description="Id медобследования в гигтест")
    results: List[MedicineCreateOrUpdateResponseResults] = Field(
        description="Исследования"
    )


class MedicineCreateResponseExtended(MedicineCreateResponse):
    results: List[MedicineCreateOrUpdateResponseResultsExtended] = Field(
        description="Исследования"
    )


class MedicineUpdateResponse(BaseModel):
    results: List[MedicineCreateOrUpdateResponseResults] = Field(
        description="Исследования"
    )
    sticker_links: Optional[list] = Field(description="Ссылки на исследования")


class AdditionalMedDirectionResultResponse(BaseModel):
    id: int = Field(description="Id исследования в гигтест")


class GigtestService:
    def __init__(self, client: SDKClient, url: HttpUrl, token: str):
        self._client = client
        self._url = url
        self._token = token
        # СПРАВОЧНИКИ
        self._get_activities_url = "/api/v2/activities"
        self._get_sections_url = "/api/v2/sections"
        self._get_countries_url = "/api/v2/countries"
        self._get_medical_researches_url = "/api/v2/medical-researches"
        # КЛИЕНТ
        self._search_client_url = "/api/v2/users/search"
        self._create_or_update_client_url = "/api/v2/users"
        # МЕДКНИЖКА
        self._medbook_url = "/api/v2/medical-books"
        self._medbook_url_search = "/api/v2/medical-books/search"
        # АТТЕСТАЦИЯ
        self._attestation_url = "/api/v2/protocols"
        # МЕДИЦИНА
        self._create_update_medicine_url = "/api/v2/medical-directions"
        self._additional_medicine_results_url = "/api/v2/medical-research-results"

    # СПРАВОЧНИКИ
    def activities(self) -> SDKResponse[List[ActivityResponse]]:
        return self._client.get(
            self._full_url(self._get_activities_url),
            ActivityResponse,
            timeout=COMMON_GIGTEST_TIMEOUT,
        )

    def sections(self) -> SDKResponse[List[SectionResponse]]:
        return self._client.get(
            self._full_url(self._get_sections_url),
            SectionResponse,
            timeout=COMMON_GIGTEST_TIMEOUT,
        )

    def countries(self) -> SDKResponse[List[CountryResponse]]:
        return self._client.get(
            self._full_url(self._get_countries_url),
            CountryResponse,
            timeout=COMMON_GIGTEST_TIMEOUT,
        )

    def medical_research(self) -> SDKResponse[List[MedicalResearchResponse]]:
        return self._client.get(
            self._full_url(self._get_medical_researches_url),
            MedicalResearchResponse,
            timeout=COMMON_GIGTEST_TIMEOUT,
        )

    # КЛИЕНТ
    def search_client(self, query: SearchClientRequest) -> SDKResponse[ClientResponse]:
        return self._client.get(
            self._full_url(self._search_client_url),
            ClientResponse,
            params=query.dict(),
            timeout=COMMON_GIGTEST_TIMEOUT,
        )

    def create_client(self, query: CreateClientRequest) -> SDKResponse[ClientResponse]:
        return self._client.post(
            self._full_url(self._create_or_update_client_url),
            ClientResponse,
            data=query.json(exclude_none=True),
            timeout=LONG_GIGTEST_TIMEOUT,
            headers={"Content-Type": "application/json"},
        )

    def update_client(
        self, query: UpdateClientRequest, client_gig_test_id: int
    ) -> SDKResponse[ClientResponse]:
        return self._client.put(
            self._full_url(
                self._create_or_update_client_url + "/" + str(client_gig_test_id)
            ),
            ClientResponse,
            data=query.json(exclude_none=True),
            timeout=LONG_GIGTEST_TIMEOUT,
            headers={"Content-Type": "application/json"},
        )

    def get_client(self, client_gig_test_id: int) -> SDKResponse[ClientResponse]:
        return self._client.get(
            self._full_url(
                self._create_or_update_client_url + "/" + str(client_gig_test_id)
            ),
            ClientResponse,
            timeout=COMMON_GIGTEST_TIMEOUT,
        )

    # этот метод для ручного использования!
    def delete_client(self, client_gig_test_id: int) -> SDKResponse[Empty]:
        return self._client.delete(
            self._full_url(
                self._create_or_update_client_url + "/" + str(client_gig_test_id)
            ),
            Empty,
            timeout=LONG_GIGTEST_TIMEOUT,
        )

    # МЕДКНИЖКИ
    def search_medbook_when_other_department(
        self, medbook_number: int
    ) -> SDKResponse[MedicalBookSearchResponseOther]:
        return self._client.get(
            self._full_url(self._medbook_url_search),
            MedicalBookSearchResponseOther,
            params={"number": medbook_number},
            timeout=COMMON_GIGTEST_TIMEOUT,
        )

    def search_medbook(
        self, medbook_number: int
    ) -> SDKResponse[List[MedicalBookSearchResponse]]:
        return self._client.get(
            self._full_url(self._medbook_url),
            MedicalBookSearchResponse,
            params={"MedicalBooksSearch[number]": medbook_number},
            timeout=COMMON_GIGTEST_TIMEOUT,
        )

    def create_medbook(
        self, query: MedicalBookRequest
    ) -> SDKResponse[MedicalBookResponse]:
        return self._client.post(
            self._full_url(self._medbook_url),
            MedicalBookResponse,
            data=query.json(exclude_none=True),
            timeout=LONG_GIGTEST_TIMEOUT,
            headers={"Content-Type": "application/json"},
        )

    def update_medbook(
        self, query: MedicalBookRequest, medbook_gig_test_id: int
    ) -> SDKResponse[MedicalBookResponse]:
        return self._client.put(
            self._full_url(self._medbook_url + "/" + str(medbook_gig_test_id)),
            MedicalBookResponse,
            data=query.json(exclude_none=True),
            timeout=LONG_GIGTEST_TIMEOUT,
            headers={"Content-Type": "application/json"},
        )

    # АТТЕСТАЦИЯ
    def create_attestation(
        self, query: AttestationRequest
    ) -> SDKResponse[AttestationResponse]:
        return self._client.post(
            self._full_url(self._attestation_url),
            AttestationResponse,
            data=query.json(exclude_none=True),
            timeout=LONG_GIGTEST_TIMEOUT,
            headers={"Content-Type": "application/json"},
        )

    def update_attestation(
        self, query: AttestationRequest, gigtest_att_id: int
    ) -> SDKResponse[AttestationResponse]:
        return self._client.put(
            self._full_url(self._attestation_url + "/" + str(gigtest_att_id)),
            AttestationResponse,
            data=query.json(exclude_none=True),
            timeout=LONG_GIGTEST_TIMEOUT,
            headers={"Content-Type": "application/json"},
        )

    # этот метод для ручного использования!
    def delete_attestation(self, gigtest_att_id: int) -> SDKResponse[Empty]:
        return self._client.delete(
            self._full_url(self._attestation_url + "/" + str(gigtest_att_id)),
            Empty,
            timeout=LONG_GIGTEST_TIMEOUT,
        )

    # МЕДИЦИНА
    def get_med_direction(
        self, gigtest_med_direction_id: int
    ) -> SDKResponse[MedicineCreateResponseExtended]:
        return self._client.get(
            self._full_url(
                self._create_update_medicine_url + "/" + str(gigtest_med_direction_id)
            ),
            MedicineCreateResponseExtended,
            timeout=COMMON_GIGTEST_TIMEOUT,
        )

    def create_med_direction(
        self, query: MedicineCreateRequest
    ) -> SDKResponse[MedicineCreateResponse]:
        return self._client.post(
            self._full_url(self._create_update_medicine_url),
            MedicineCreateResponse,
            data=query.json(exclude_none=True),
            timeout=LONG_GIGTEST_TIMEOUT,
            headers={"Content-Type": "application/json"},
        )

    def update_med_direction(
        self, query: MedicineUpdateRequest, gigtest_med_direction_id: int
    ) -> SDKResponse[MedicineUpdateResponse]:
        return self._client.put(
            self._full_url(
                self._create_update_medicine_url + "/" + str(gigtest_med_direction_id)
            ),
            MedicineUpdateResponse,
            data=query.json(exclude_none=True),
            timeout=LONG_GIGTEST_TIMEOUT,
            headers={"Content-Type": "application/json"},
        )

    def delete_med_direction(self, gigtest_med_direction_id: int) -> SDKResponse[Empty]:
        return self._client.delete(
            self._full_url(
                self._create_update_medicine_url + "/" + str(gigtest_med_direction_id)
            ),
            Empty,
            timeout=LONG_GIGTEST_TIMEOUT,
        )

    # TODO выше метод get_med_direction объединить с этим, проверив апи
    def search_med_direction(
        self, gigtest_med_direction_id: int
    ) -> SDKResponse[MedicineUpdateResponse]:
        return self._client.get(
            self._full_url(
                self._create_update_medicine_url + "/" + str(gigtest_med_direction_id)
            ),
            MedicineUpdateResponse,
            timeout=COMMON_GIGTEST_TIMEOUT,
        )

    def delete_med_direction_result(
        self, gigtest_med_direction_result_id: int
    ) -> SDKResponse[Empty]:
        return self._client.delete(
            self._full_url(
                self._additional_medicine_results_url
                + "/"
                + str(gigtest_med_direction_result_id)
            ),
            Empty,
            timeout=LONG_GIGTEST_TIMEOUT,
        )

    def add_additional_result_to_med_direction(
        self, query: AdditionalMedDirectionResultRequest
    ) -> SDKResponse[AdditionalMedDirectionResultResponse]:
        return self._client.post(
            self._full_url(self._additional_medicine_results_url),
            AdditionalMedDirectionResultResponse,
            data=query.json(exclude_none=True),
            timeout=LONG_GIGTEST_TIMEOUT,
            headers={"Content-Type": "application/json"},
        )

    def _full_url(self, url):
        return f"{self._url}{url}?access-token={self._token}"
