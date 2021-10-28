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
        resultado = base_de_datos.session.query(PedidoRutaModel).filter(PedidoRutaModel.pedido==filtros["pedidoId"]).order_by(PedidoRutaModel.pedRutPasoNro).all()
        
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

class PedidoRutaController(Resource):    

    def put(self, id):
        serializador = reqparse.RequestParser()
        serializador.add_argument(
            'pedidoRuta_fecReal',
            required=True, 
            location='json',
            help='Debe ingresar fecha de movimiento',
            type=str,
        )
        serializador.add_argument(
            'pedRutaComent',
            required=True, 
            location='json',
            help='Debe ingresar comentario',
            type=str,
        )
        data = serializador.parse_args()
        resultado = base_de_datos.session.query(PedidoRutaModel).filter(
            PedidoRutaModel.pedRutaId == id).update(
                {
                    PedidoRutaModel.pedRutFechaReal: data['pedidoRuta_fecReal'],
                    PedidoRutaModel.pedRutaComent: data['pedRutaComent'],
                    PedidoRutaModel.pedRutRecibido: True
                }, synchronize_session='fetch')

        base_de_datos.session.commit()
        print(resultado)
        if resultado == 0:
            return {
                "message": "No hubo xxxxxx a actualizar",
                "content": None
            }, 404
        else:
            return {
                "message": "El xxxxxx fue actualizado exitosamente",
                "content": None
            }
