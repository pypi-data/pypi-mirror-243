from ximilar.client import RestClient
from ximilar.client.constants import *

GRADING_ENDPOINT = "card-grader/v2/grade"

COLLECTIBLES_PROCESS = "collectibles/v2/process"
COLLECTIBLES_CARD_ID = "collectibles/v2/card_id"
COLLECTIBLES_DETECT = "collectibles/v2/detect"
COLLECTIBLES_SLAB_ID = "collectibles/v2/slab_id"
COLLECTIBLES_OCR_ID = "collectibles/v2/ocr_id"
COLLECTIBLES_ANALYZE = "collectibles/v2/analyze"


class CardGradingClient(RestClient):
    def __init__(self, token, endpoint=ENDPOINT, resource_name="card-grader"):
        super().__init__(token=token, endpoint=endpoint, resource_name=resource_name)
        self.PREDICT_ENDPOINT = GRADING_ENDPOINT

    def construct_data(self, records=[]):
        if len(records) == 0:
            raise Exception("Please specify at least one record in detect method!")
        data = {RECORDS: self.preprocess_records(records)}
        return data

    def grade(self, records, endpoint=GRADING_ENDPOINT):
        records = self.preprocess_records(records)
        return self.post(endpoint, data={RECORDS: records})


class CollectiblesRecognitionClient(RestClient):
    def __init__(self, token, endpoint=ENDPOINT, resource_name=COLLECTIBLES_RECOGNITION):
        super().__init__(token=token, endpoint=endpoint, resource_name=resource_name)

    def process(self, records: list):
        data = {RECORDS: self.preprocess_records(records)}
        result = self.post(COLLECTIBLES_PROCESS, data=data)
        return result

    def card_id(self, records: list, lang: bool = False, slab_id: bool = False):
        data = {RECORDS: self.preprocess_records(records), "lang": lang, "slab_id": slab_id}
        result = self.post(COLLECTIBLES_CARD_ID, data=data)
        return result

    def detect(self, records: list):
        data = {RECORDS: self.preprocess_records(records)}
        result = self.post(COLLECTIBLES_DETECT, data=data)
        return result

    def slab_id(self, records: list):
        data = {RECORDS: self.preprocess_records(records)}
        result = self.post(COLLECTIBLES_SLAB_ID, data=data)
        return result

    def ocr_id(self, records: list):
        data = {RECORDS: self.preprocess_records(records)}
        result = self.post(COLLECTIBLES_OCR_ID, data=data)
        return result

    def analyze(self, records: list):
        data = {RECORDS: self.preprocess_records(records)}
        result = self.post(COLLECTIBLES_ANALYZE, data=data)
        return result
