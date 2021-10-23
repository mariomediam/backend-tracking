from app import app
from unittest import TestCase

class TestDistritoControllers(TestCase):
    def setUp(self):        
        self.app = app.test_client()

    def test_get_distritos(self):
        respuesta =  self.app.get("/distritos")
        self.assertEqual(respuesta.json["message"], "distritos")
        self.assertEqual(respuesta.status_code, 200)

    def test_get_distrito(self):
        respuesta =  self.app.get("/distrito/5")
        self.assertEqual(respuesta.json, dict(message="distrito", content={
            "distritoId": 5,
            "provNombre": "Arequipa",
            "distrGeo": [
                "-16.3988032",
                "-71.5390943"
            ],
            "distrNombre": "Arequipa",
            "dptoNombre": "Arequipa"
        }))
        self.assertEqual(respuesta.json["message"], "distrito")
        self.assertEqual(respuesta.status_code, 200)