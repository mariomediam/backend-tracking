from app import app
from unittest import TestCase

class TestProductoControllers(TestCase):
    def setUp(self):        
        self.app = app.test_client()

    def test_get_productos(self):
        respuesta =  self.app.get("/productos")
        self.assertEqual(respuesta.json["message"], "productos")
        self.assertEqual(respuesta.status_code, 200)