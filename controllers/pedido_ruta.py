from sqlalchemy.sql.sqltypes import DECIMAL
from config.conexion_bd import base_de_datos
from flask_restful import Resource, reqparse
from models.pedido import PedidoModel
from models.pedido_ruta import PedidoRutaModel


class PedidoRutaControllerPorPedidoId(Resource):

    def __init__(self):
        self.serializadorFiltro = reqparse.RequestParser()
        self.serializadorFiltro.add_argument(
            'pedidoId',
            location='args',
            required=True,
            type=str
        )
        

    def get(self):
        filtros = self.serializadorFiltro.parse_args()
        resultado = base_de_datos.session.query(PedidoRutaModel).filter(PedidoRutaModel.pedido==filtros["pedidoId"]).all()
        
        resultado_final = []
        if resultado:
            
            for registro in resultado:
                resultado = registro.__dict__
                del resultado['_sa_instance_state']

                resultado['pedRutPasoTipo'] = resultado['pedRutPasoTipo'].name
                resultado['pedRutFechaEst'] = str(resultado['pedRutFechaEst'])
                resultado['pedRutFechaReal'] = str(resultado['pedRutFechaReal'])
                resultado_final.append(resultado)                            
            return {
                "message": "Registros encontrados",
                "content": resultado_final
            }
        else:
            return {
                "message": "No se encontraron registros coincidentes",
                "content": resultado_final
            }, 200