from app import app
from unittest import TestCase

class TestClienteControllers(TestCase):
    def setUp(self):        
        self.app = app.test_client()

    def test_get_clientes(self):
        respuesta =  self.app.get("/clientes")
        self.assertEqual(respuesta.json["message"], "clientes")
        self.assertEqual(respuesta.status_code, 200)

    def test_fail_get_distrito(self):
        respuesta =  self.app.get("/cliente/2000")
        self.assertEqual(respuesta.json, dict(message="El cliente no existe", content=None))
        self.assertEqual(respuesta.status_code, 404)