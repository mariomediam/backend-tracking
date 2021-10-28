from flask_cors.core import try_match
from flask_restful import Resource, reqparse
from sqlalchemy.orm import session
from sqlalchemy.sql.expression import text, true
from sqlalchemy.sql.sqltypes import ARRAY, Integer
from models.distrito import DistritoModel
from models.pedido import PedidoModel
from models.cliente import ClienteModel
from models.producto import ProductoModel
from config.conexion_bd import base_de_datos
from flask_jwt import jwt_required
import uuid
from datetime import datetime, timedelta

from models.pedido_producto import PedidoProductoModel
from models.pedido_ruta import PedidoRutaModel
from models.plantilla_rutas import PlantillaRutasModel
from controllers.to_pdf import pdf_template

from config.enviar_correo import enviarCorreo

class PedidosController(Resource):
    serializador = reqparse.RequestParser(bundle_errors=True)

    #@jwt_required()
    def post(self):

        self.serializador.add_argument(
            'pedidoDireccion',
            required=True,
            location='json',
            help='Debe ingresar dirección de entrega',
            type=str
        )
        self.serializador.add_argument(
            'pedidoDistrDestino',
            required=True,
            location='json',
            help='Debe ingresar distrito de entrega',
            type=int
        )
        self.serializador.add_argument(
            'clienteNombre',
            required=True,
            location='json',
            help='Debe ingresar nombre de cliente',
            type=str
        )
        self.serializador.add_argument(
            'clienteCorreo',
            required=True,
            location='json',
            help='Debe ingresar correo de cliente',
            type=str
        )
        self.serializador.add_argument(
            'clienteTelefono',
            required=False,
            location='json',
            type=str
        )
        self.serializador.add_argument(
            'pedProductos',
            required=True,
            location='json',
            type=list
        )
        self.serializador.add_argument(
            'pedidoGeo',
            required=True,
            location='json',
            type=list
        )

        data = self.serializador.parse_args()
      
        try:

              
            
            nuevo_cliente = ClienteModel().save(
                data.get('clienteNombre'), 
                data.get('clienteCorreo'), 
                data.get('clienteTelefono'), 
                data.get('pedidoDireccion'), 
                data.get('pedidoDistrDestino')
            )            

            #punto_guardado = base_de_datos.session.begin_nested()  

            nuevo_pedido : PedidoModel = PedidoModel()
            nuevo_pedido.pedidoToken = str(uuid.uuid4())[0:6]  #"6ac21f"
            nuevo_pedido.pedidoDireccion = data.get('pedidoDireccion')
            nuevo_pedido.pedidoDistrDestino = data.get('pedidoDistrDestino')
            nuevo_pedido.pedidoGeo = data.get("pedidoGeo")
            nuevo_pedido.cliente = nuevo_cliente.clienteId
                    
            base_de_datos.session.add(nuevo_pedido)

            base_de_datos.session.flush()

            pedProductos = data.get('pedProductos')
            productos = []
            for producto in pedProductos:
                producto_buscado : ProductoModel = base_de_datos.session.query(ProductoModel).filter(ProductoModel.productoId==producto.get("producto")).first()

                if not producto_buscado:
                    raise Exception("El producto con id {} no existe".format(producto.get("producto")))

                if producto_buscado.productoStock < producto.get("pedProdCantidad"):
                    raise Exception("El producto {} solo tiene en stock {} unidades".format(producto_buscado.productoNombre, producto_buscado.productoStock))
                else:
                    producto_buscado.productoStock -= producto.get("pedProdCantidad")


                nuevo_pedProducto = PedidoProductoModel.agregar(nuevo_pedido.pedidoId, producto.get("producto"), producto.get("pedProdCantidad"))

                productos.append(
                    {
                        "productoNombre":producto_buscado.productoNombre,
                        "productoDescripcion":producto_buscado.productoDescripcion,
                        "pedProdCantidad":producto.get("pedProdCantidad")
                    }
                )

                base_de_datos.session.add(nuevo_pedProducto)

            rutas = base_de_datos.session.query(PlantillaRutasModel).filter(PlantillaRutasModel.distrDestino==data.get('pedidoDistrDestino')).all()

            fecha_base = datetime.now()
            rutas_template = []
            for ruta in rutas:
                pedido_ruta = PedidoRutaModel()
                pedido_ruta.pedido = nuevo_pedido.pedidoId
                pedido_ruta.pedRutPasoNro = ruta.plantPasoNro
                pedido_ruta.pedRutPasoTipo = ruta.plantPasoTipo.name
                pedido_ruta.pedRutTiempoEst = ruta.plantTiempoEst
                fecha_base += timedelta(days=ruta.plantTiempoEst)
                pedido_ruta.pedRutFechaEst = fecha_base

                rutas_template.append(
                    {
                        "paso":ruta.plantPasoTipo.name,
                        "tiempoEstimado":ruta.plantTiempoEst,
                        "fechaEstimada": pedido_ruta.pedRutFechaEst.strftime("%d/%m/%Y")
                    }
                )
                base_de_datos.session.add(pedido_ruta)

            base_de_datos.session.commit()

            #GENERA PDF
            distrito_destino : DistritoModel =  base_de_datos.session.query(DistritoModel).filter(DistritoModel.distritoId == data.get('pedidoDistrDestino')).first()

            
            pdf_template(
                template="formato_compra.html", 
                output=nuevo_pedido.pedidoToken, 
                pedidoToken=nuevo_pedido.pedidoToken,
                clienteNombre=data.get('clienteNombre'), 
                clienteCorreo=data.get('clienteCorreo'), 
                clienteTelefono=data.get('clienteTelefono'), 
                pedidoDireccion=data.get('pedidoDireccion'),
                dptoNombre = distrito_destino.dptoNombre,
                provNombre = distrito_destino.provNombre,
                distrNombre = distrito_destino.distrNombre,
                productos = productos,
                rutas=rutas_template
            )

            enviarCorreo(data.get('clienteCorreo'), '''Estimado {} se ha registrado su compra la cual podrás consultar en la página web https://trackingapp.vercel.app/ con el número de tracking {}'''.format(data.get('clienteNombre'), nuevo_pedido.pedidoToken),  '''./static/pdfs/{}.pdf'''.format(nuevo_pedido.pedidoToken))
        
            
            return {
                "message": "Pedido agregado exitosamente",
                "content": {
                    "pedidoId": nuevo_pedido.pedidoId,
                    "pedidoToken": nuevo_pedido.pedidoToken                    
                }

            }, 201
        except Exception as e:
            base_de_datos.session.rollback()
            return {
                "message": "Hubo un error al guardar el pedido, intentelo nuevamente",
                "content": e.args[0]
            }, 500

    #@jwt_required()
    def get(self):
        pedidos = base_de_datos.session.query(PedidoModel).all()
        resultado = []
        # for pedido in pedidos:
        #     pedido_dicc = pedido.__dict__            
        #     del pedido_dicc['_sa_instance_state']
        #     pedido_dicc['pedidoFecha'] = str(pedido_dicc['pedidoFecha'])
        #     resultado.append(pedido_dicc)

        for pedido in pedidos:
            pedido_dicc = pedido.__dict__ 

            cliente_buscado : ClienteModel = base_de_datos.session.query(ClienteModel).filter(ClienteModel.clienteId==pedido_dicc["cliente"]).first()     

            del pedido_dicc['_sa_instance_state']
            pedido_dicc['pedidoFecha'] = str(pedido_dicc['pedidoFecha'])
            pedido_dicc['clienteNombre'] = cliente_buscado.clienteNombre
            pedido_dicc['clienteTelefono'] = cliente_buscado.clienteTelefono
            pedido_dicc['clienteCorreo'] = cliente_buscado.clienteCorreo            
            resultado.append(pedido_dicc)

        return {
            "message": None,
            "content": resultado
        }

class PedidoController(Resource):
    def get(self, id):
        resultado = base_de_datos.session.query(
            PedidoModel).filter(PedidoModel.pedidoId == id).first()

        if resultado:
            data = resultado.__dict__
            del data['_sa_instance_state']
            data['pedidoFecha'] = str(data['pedidoFecha'])
            return {
                "message": "pedido",
                "content": data
            }
        else:
            return {
                "message": "El pedido no existe",
                "content": resultado
            }, 404        

class PedidoControllerFiltrar(Resource):

    def __init__(self):
        self.serializadorFiltro = reqparse.RequestParser()
        self.serializadorFiltro.add_argument(
            'token',
            location='args',
            required=False,
            type=str
        )
        

    def get(self):
        consulta = base_de_datos.session.query(PedidoModel)
        filtros = self.serializadorFiltro.parse_args()

        try:
            if filtros.token:
                consulta = consulta.filter(PedidoModel.pedidoToken == filtros['token'])

            resultado = consulta.all()
            
            resultado_final = []
            if resultado:
                for registro in resultado:
                    resultado = registro.__dict__

                    cliente_buscado : ClienteModel = base_de_datos.session.query(ClienteModel).filter(ClienteModel.clienteId==resultado["cliente"]).first()
                    
                    del resultado['_sa_instance_state']
                    resultado['pedidoFecha'] = str(resultado['pedidoFecha'])
                    resultado['clienteNombre'] = cliente_buscado.clienteNombre
                    resultado['clienteTelefono'] = cliente_buscado.clienteTelefono
                    resultado['clienteCorreo'] = cliente_buscado.clienteCorreo
                    resultado_final.append(resultado)                            
                return {
                    "message": "Registros encontrados",
                    "content": resultado_final
                }, 200
            else:
                return {
                    "message": "0 Registros encontrados",
                    "content": resultado_final
                } , 200           
        
        except Exception as error:
            return {
                    "message": "Error realizando la consulta",
                    "content": error
                }, 404            



        