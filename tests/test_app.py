import importlib
from unittest import TestCase


class AppTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self):
        env_overrides = {}

        from . import main

        importlib.reload(main)
        self.app = main.app
        self.client = main.app.test_client()

    def test_md_compare(self):
        pass

    def test_pdf_compare(self):
        pass

    def test_py_compare(self):
        pass

    def test_ts_compare(self):
        pass

   