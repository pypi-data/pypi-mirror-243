import os
import hashlib

from ximilar.client.constants import *
from ximilar.client import RecognitionClient


PRODUCT_ENDPOINT = "product/v2/product/"
IMAGE_ENDPOINT = "product/v2/image/"
COLLECTION_ENDPOINT = "product/v2/collection/"


class ProductClient(RecognitionClient):
    """
    Ximilar API Client for Products management.
    """

    def __init__(
        self, token, endpoint=ENDPOINT, workspace=DEFAULT_WORKSPACE, max_image_size=0, resource_name=PRODUCTS_MANAGEMENT
    ):
        super().__init__(
            token=token,
            endpoint=endpoint,
            workspace=workspace,
            max_image_size=max_image_size,
            resource_name=resource_name,
        )

    def create_product(self, name, customer_product_id, product_collection, meta_data=None):
        data = {NAME: name, "customer_product_id": customer_product_id, "product_collection": product_collection}

        if meta_data:
            data[META_DATA] = meta_data

        product_json = self.post(PRODUCT_ENDPOINT, data=data, params=self.add_workspace(None, None))
        if ID not in product_json:
            return None, {STATUS: "unexpected error"}
        return Product(self.token, self.endpoint, self.workspace, product_json), RESULT_OK

    def create_image(self, record, name, product, meta_data={}, md5s=[]):
        assert product

        record = self._create_image_data(record, True, True, False, meta_data)
        
        record[NAME] = name
        record["product"] = product

        if "base64" in record and len(md5s):
            md5h = hashlib.md5(record["base64"].encode('utf-8')).hexdigest()
            if md5h in md5s:
                return None, {STATUS: "skipped"}

        image_json = self.post(IMAGE_ENDPOINT, data=record)
        if ID not in image_json:
            return None, {STATUS: "unexpected error"}
        return ProductImage(self.token, self.endpoint, self.workspace, image_json), RESULT_OK

    def get_product(self, product_id):
        product_json = self.get(PRODUCT_ENDPOINT + product_id)
        if ID not in product_json:
            return None, {STATUS: "Product with this id not found!"}
        return Product(self.token, self.endpoint, self.workspace, product_json), RESULT_OK

    def get_image(self, image_id):
        image_json = self.get(IMAGE_ENDPOINT + image_id)
        if ID not in image_json:
            return None, {STATUS: "Image with this id not found!"}
        return ProductImage(self.token, self.endpoint, self.workspace, image_json), RESULT_OK

    def remove_product(self, product_id):
        return self.delete(PRODUCT_ENDPOINT + product_id)

    def remove_image(self, image_id):
        return self.delete(IMAGE_ENDPOINT + image_id)

    def get_all_products(self, product_collection=None):
        url = PRODUCT_ENDPOINT

        if product_collection is not None:
            url = url + "?product_collection=" + str(product_collection)

        products, status = self.get_all_paginated_items(url)
        if not products and status[STATUS] == STATUS_ERROR:
            return None, status
        return [Product(self.token, self.endpoint, self.workspace, p_json) for p_json in products], RESULT_OK

    def get_all_images(self):
        images, status = self.get_all_paginated_items(IMAGE_ENDPOINT)
        if not images and status[STATUS] == STATUS_ERROR:
            return None, status
        return [ProductImage(self.token, self.endpoint, self.workspace, i_json) for i_json in images], RESULT_OK

    def get_products_url(self, page_url=None, product_collection=None, name=None, customer_product_id=None, collection_type=None):
        url = (
            page_url.replace(self.endpoint, "").replace(self.endpoint.replace("https", "http"), "")
            if page_url
            else PRODUCT_ENDPOINT + "?page=1"
        )

        if page_url is not None:
            return url
        if name is not None:
            url += "&search=" + str(name)
        if product_collection is not None:
            url += "&product_collection=" + str(product_collection)
        if customer_product_id is not None:
            url += "&customer_product_id=" + str(customer_product_id)
        if collection_type is not None:
            url += "&collection_type=" + str(collection_type)
        return url

    def get_products(self, page_url=None, product_collection=None, name=None, customer_product_id=None, collection_type=None):
        url = self.get_products_url(page_url, product_collection, name, customer_product_id, collection_type)
        result = self.get(url)
        return (
            [Product(self.token, self.endpoint, self.workspace, product_json) for product_json in result[RESULTS]],
            result[NEXT],
            {"count": result["count"], STATUS: "ok"},
        )


class Product(ProductClient):
    def __init__(self, token, endpoint, workspace, product_json):
        super().__init__(token, endpoint=endpoint, workspace=workspace, resource_name=None)

        self.id = product_json["id"]
        self.name = product_json["name"]
        self.product_collection = product_json["product_collection"]
        self.customer_product_id = product_json["customer_product_id"]
        self.meta_data = product_json.get("meta_data", None)
        self.thumb = product_json.get("thumb", None)

    def __str__(self):
        return self.name + ":" + self.id + ":" + str(self.product_collection)

    def remove(self):
        self.remove_product(self.id)

    def update_meta(self, new_data):
        result = self.patch(PRODUCT_ENDPOINT + self.id, data={META_DATA: new_data})


class ProductImage(ProductClient):
    def __init__(self, token, endpoint, workspace, image_json):
        super().__init__(token, endpoint=endpoint, workspace=workspace, resource_name=None)

        self.id = image_json["id"]
        self.name = image_json["name"]
        self.product = image_json["product"]
        self.meta_data = image_json.get("meta_data", None)
        self.objects = image_json["_objects"]

        self.img = image_json["file"]
        self.img_thumb = image_json["thumb"]

    def __str__(self):
        return self.name + ":" + self.id + ":" + str("" if not self.product else self.product.id)

    def remove(self):
        self.remove_image(self.id)
