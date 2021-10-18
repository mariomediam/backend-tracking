from config.conexion_bd import base_de_datos
from flask_restful import Resource, reqparse
from models.distrito import DistritoModel

class DistritosController(Resource):
    serializador = reqparse.RequestParser(bundle_errors=True)

    def post(self):
        self.serializador.add_argument(
            'dptoNombre',
            required=True,
            location='json',
            help='Debe ingresar Departamento',
            type=str
        )
        self.serializador.add_argument(
            'provNombre',
            required=True,
            location='json',
            help='Debe ingresar Provincia',
            type=str
        )
        self.serializador.add_argument(
            'distrNombre',
            required=True,
            location='json',
            help='Debe ingresar Distrito',
            type=str
        )
        self.serializador.add_argument(
            'distrGeo',
            required=True,
            location='json',
            help='Debe ingresar ubicación georeferencial ',
            type=list
        )

        data = self.serializador.parse_args()
        try:
            nuevo_distrito : DistritoModel = DistritoModel()
            nuevo_distrito.dptoNombre = data.get('dptoNombre')
            nuevo_distrito.provNombre = data.get('provNombre')
            nuevo_distrito.distrNombre = data.get('distrNombre')
            nuevo_distrito.distrGeo = data.get('distrGeo')
            
            
            base_de_datos.session.add(nuevo_distrito)
            base_de_datos.session.commit()
            return {
                "message": "Distrito agregado exitosamente",
                "content": {
                    "distrId": nuevo_distrito.distritoId,
                    "distrNombre": nuevo_distrito.distrNombre
                }

            }, 201
        except Exception as e:
            return {
                "message": "Hubo un error al guardar el distrito, intentelo nuevamente",
                "content": e.args[0]
            }, 500


    def get(self):
        distritos = base_de_datos.session.query(DistritoModel).all()
        resultado = []
        for distrito in distritos:
            distrito_dicc = distrito.__dict__
            del distrito_dicc['_sa_instance_state']
            resultado.append(distrito_dicc)

        return {
            "message": "distritos",
            "content": resultado
        }

class DistritoController(Resource):
    def get(self, id):
        resultado = base_de_datos.session.query(
            DistritoModel).filter(DistritoModel.distritoId == id).first()

        if resultado:
            data = resultado.__dict__
            del data['_sa_instance_state']
            return {
                "message": "distrito",
                "content": data
            }
        else:
            return {
                "message": "El distrito no existe",
                "content": resultado
            }, 404



class DistritosControllerFiltrar(Resource):

    def __init__(self):
        self.serializadorFiltro = reqparse.RequestParser()
        self.serializadorFiltro.add_argument(
            'dpto',
            location='args',
            required=False,
            type=str
        )
        self.serializadorFiltro.add_argument(
            'prov',
            location='args',
            required=False,
            type=str
        )
        self.serializadorFiltro.add_argument(
            'dist',
            location='args',
            required=False,
            type=str
        )
        

    def get(self):
        consulta = base_de_datos.session.query(DistritoModel)
        filtros = self.serializadorFiltro.parse_args()

        if filtros.dpto:
            consulta = consulta.filter(DistritoModel.dptoNombre == filtros['dpto'])
        if filtros.prov:
            consulta = consulta.filter(DistritoModel.provNombre == filtros['prov'])
        if filtros.dist:
            consulta = consulta.filter(DistritoModel.distrNombre == filtros['dist'])

        resultado = consulta.all()
        
        if resultado:
            resultado_final = []
            for registro in resultado:
                resultado = registro.__dict__
                del resultado['_sa_instance_state']
                resultado_final.append(resultado)                            
            return {
                "message": "Registros encontrados",
                "content": resultado_final
            }
        else:
            return {
                "message": "No se encontraron registros coincidentes",
                "content": resultado
            }, 404