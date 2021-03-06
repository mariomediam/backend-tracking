from sqlalchemy.sql.schema import ForeignKey
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types



class ClienteModel(base_de_datos.Model):
    __tablename__ = "clientes"

    clienteId = Column(name="cliente_id", type_=types.Integer, primary_key=True, autoincrement=True, nullable=False)

    clienteNombre = Column(name="nombre", type_=types.String(50), nullable=False)

    clienteCorreo = Column(name="correo", type_=types.String(50), nullable=False, unique=True)

    clienteTelefono = Column(name="telefono", type_=types.String(20), nullable=True)

    clienteDireccion = Column(name="direccion", type_=types.String(50), nullable=False)

    clienteDistrito = Column(ForeignKey(column="distritos.distr_id"), name="distr_id", type_=types.Integer, nullable=False)

    def save(self, nombre, correo, telefono, direccion, distrito):
        
        cliente_buscado : ClienteModel = base_de_datos.session.query(ClienteModel).filter(ClienteModel.clienteCorreo==correo).first()

        if not cliente_buscado:
            cliente_buscado = ClienteModel()
            cliente_buscado.clienteCorreo = correo
            base_de_datos.session.add(cliente_buscado)

        cliente_buscado.clienteNombre = nombre
        cliente_buscado.clienteTelefono = telefono
        cliente_buscado.clienteDireccion = direccion
        cliente_buscado.clienteDistrito = distrito        
        
        base_de_datos.session.commit()

        return cliente_buscado

        
        



    