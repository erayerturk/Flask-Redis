import json
import random
import string

from app import app, redis_client
import unittest


class APITest(unittest.TestCase):
    key = "test"
    value = "test"

    def setUp(self):
        self.tester = app.test_client()
        redis_client.set(self.key, self.value)

    def test_get_a_value(self):
        response = self.tester.get(f"/api/keys?key={self.key}", content_type="application/json")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["key"] == self.key
        assert data["value"] == self.value

    def test_get_a_value_with_non_exist_key(self):
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        response = self.tester.get(f"/api/keys/{random_string}", content_type="application/json")

        assert response.status_code == 404

    def test_get_all_values(self):
        response = self.tester.get(f"/api/keys/", content_type="application/json")

        assert response.status_code == 200

    def test_set_a_value(self):
        tester = app.test_client()
        response = tester.put("/api/keys/",
                              content_type="application/json",
                              data=json.dumps({"key": self.key, "value": self.value}))
        assert response.status_code == 201

    def test_set_a_value_with_empty_data(self):
        tester = app.test_client()
        response = tester.put("/api/keys/",
                              content_type="application/json",
                              data=json.dumps({"key": "", "value": ""}))
        assert response.status_code == 400

    def test_set_a_value_without_a_key(self):
        tester = app.test_client()
        response = tester.put("/api/keys/",
                              content_type="application/json",
                              data=json.dumps({"value": self.value}))
        assert response.status_code == 400

    def test_delete_a_value(self):
        response = self.tester.delete(f"/api/keys?key={self.key}")
        assert response.status_code == 204

    def test_delete_all_values(self):
        redis_client.set(self.key, self.value)
        response = self.tester.delete(f"/api/keys/")
        assert response.status_code == 204

    def tearDown(self):
        redis_client.delete(self.key)
