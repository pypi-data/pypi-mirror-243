# drf api test case
from concurrent.futures import ThreadPoolExecutor

from rest_framework.test import APITestCase, APITransactionTestCase

from .models import Sample, User


class SampleTestCase(APITestCase):
    def setUp(self):
        pass

    @classmethod
    def setUpTestData(cls):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_성공__sample(self):
        self.assertEqual(1, 1)
        self.assertFalse(False)
        self.assertTrue(True)
        self.assertIn("a", "abc")
        self.assertNotIn("d", "abc")
        self.assertIsInstance("abc", str)
        self.assertNotIsInstance("abc", int)
        self.assertLess(1, 2)
        self.assertLessEqual(1, 2)
        self.assertGreater(2, 1)
        self.assertGreaterEqual(2, 1)
        self.assertRegex("abc", "^abc$")
        self.assertNotRegex("abc", "^ab$")
        self.assertCountEqual("abc", "cba")
        self.assertListEqual([1, 2, 3], [1, 2, 3])
        self.assertTupleEqual((1, 2, 3), (1, 2, 3))
        self.assertSetEqual({1, 2, 3}, {1, 2, 3})
        self.assertDictEqual({"a": 1, "b": 2}, {"a": 1, "b": 2})
        self.assertNumQueries(1, lambda: Sample.objects.create())

    def test_실패__sample(self):
        try:
            self.assertEqual(1, 2)
        except AssertionError:
            pass
        else:
            self.fail("AssertionError not raised")
        try:
            self.assertFalse(True)
        except AssertionError:
            pass
        else:
            self.fail("AssertionError not raised")

    def test_성공__리스트_조회(self):
        response = self.client.get("/sample/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})

    def test_성공__로그인_후_리스트_조회(self):
        self.client.login(username="test", password="test")
        response = self.client.get("/sample/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})

    def test_성공__생성(self):
        user = User.objects.create_user(username="test", password="test")
        self.client.force_authenticate(user=user)
        response = self.client.post("/sample/", {})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {})
        self.assertEqual(Sample.objects.count(), 1)

    def test_성공__대량_생성(self):
        user = User.objects.create_user(username="test", password="test")
        self.client.force_authenticate(user=user)
        for _ in range(100):
            self.client.post("/sample/", {})
        self.assertEqual(Sample.objects.count(), 100)


class TestAsync(APITransactionTestCase):
    """비동기 호출 테스트"""

    def setUp(self):
        self.user = None

    def _호출할_API(self):
        resp = self.client.get("/v1/...")
        self.assertEqual(resp.status_code, 200)

    def test_성공__연속_리스트_조회(self):
        self.client.force_login(self.user)
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._호출할_API) for _ in range(100)]
            for future in futures:
                future.result()
