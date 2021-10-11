from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types

class UsuarioModel(base_de_datos.Model):
    __tablename__ = "usuarios"

    usuarioId = Column(name="usuario_id", type_=types.Integer, primary_key=True, autoincrement=True, nullable=False)

    usuarioNombre = Column(name="nombre", type_=types.String(50), nullable=False)

    usuarioCorreo = Column(name='correo', type_=types.Text,
                           nullable=False, unique=True)

    usuarioPassword = Column(name='password', type_=types.Text, nullable=False)

    usuarioTelefono = Column(
        name='telefono', type_=types.String(15), nullable=True)

    usuarioActivo = Column(name="activo", type_=types.Boolean, nullable=False, default=True)