from flask_restful import Resource, reqparse
from config.conexion_bd import base_de_datos
from models.cliente import ClienteModel

class ClientesController(Resource):
    serializador = reqparse.RequestParser(bundle_errors=True)

    def post(self):
        self.serializador.add_argument(
            'clienteNombre',
            required=True,
            location='json',
            help='Debe ingresar nombre',
            type=str    
        )
        self.serializador.add_argument(
            'clienteCorreo',
            required=True,
            location='json',
            help='Debe ingresar correo',
            type=str    
        )
        self.serializador.add_argument(
            'clienteTelefono',
            required=False,
            location='json',            
            type=str    
        )
        self.serializador.add_argument(
            'clienteDireccion',
            required=True,
            location='json',
            help='Debe ingresar dirección',
            type=str    
        )
        self.serializador.add_argument(
            'clienteDistrito',
            required=True,
            location='json',
            help='Debe ingresar distrito',
            type=int    
        )

        data = self.serializador.parse_args()
        try:
            cliente_buscado = base_de_datos.session.query(
            ClienteModel).filter(ClienteModel.clienteCorreo == data.get('clienteCorreo')).first()            
            if not cliente_buscado:
                nuevo_cliente : ClienteModel = ClienteModel()
                nuevo_cliente.clienteNombre = data.get('clienteNombre')
                nuevo_cliente.clienteCorreo = data.get('clienteCorreo')
                nuevo_cliente.clienteTelefono = data.get('clienteTelefono')
                nuevo_cliente.clienteDireccion = data.get('clienteDireccion')
                nuevo_cliente.clienteDistrito = data.get('clienteDistrito')
                base_de_datos.session.add(nuevo_cliente)
                base_de_datos.session.commit()
                return {
                    "message": "Cliente agregado exitosamente",
                    "content": {
                        "clienteId": nuevo_cliente.clienteId,
                        "clienteNombre": nuevo_cliente.clienteNombre                    
                    }
                }, 201
            else:
                raise Exception("El cliente ya existe")
        except Exception as e:
            return {
                "message": "Hubo un error al guardar el cliente",
                "content": e.args[0]
            }, 500

    def get(self):
        clientes = base_de_datos.session.query(ClienteModel).all()
        resultado = []
        for cliente in clientes:
            cliente_dicc = cliente.__dict__
            del cliente_dicc['_sa_instance_state']
            resultado.append(cliente_dicc)

        return {
            "message": "clientes",
            "content": resultado
        }

class ClienteController(Resource):
    def get(self, id):
        resultado = base_de_datos.session.query(
            ClienteModel).filter(ClienteModel.clienteId == id).first()

        if resultado:
            data = resultado.__dict__
            del data['_sa_instance_state']
            return {
                "message": "cliente",
                "content": data
            }
        else:
            return {
                "message": "El cliente no existe",
                "content": resultado
            }, 404

class ClientesControllerFiltrar(Resource):

    def __init__(self):
        self.serializadorFiltro = reqparse.RequestParser()
        self.serializadorFiltro.add_argument(
            'nombre',
            location='args',
            required=False,
            type=str
        )
        self.serializadorFiltro.add_argument(
            'correo',
            location='args',
            required=False,
            type=str
        )
        

    def get(self):
        consulta = base_de_datos.session.query(ClienteModel)
        filtros = self.serializadorFiltro.parse_args()

        if filtros.nombre:
            consulta = consulta.filter(ClienteModel.clienteNombre.ilike('%' + filtros['nombre'] + '%'))
        if filtros.correo:
            consulta = consulta.filter(ClienteModel.clienteCorreo == filtros['correo'])

        print(consulta)
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