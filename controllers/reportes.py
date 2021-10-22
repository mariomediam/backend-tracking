from sqlalchemy.sql.sqltypes import DECIMAL, Text
from config.conexion_bd import base_de_datos
from flask_restful import Resource, reqparse
from sqlalchemy import text
import json


class ReporteControllerVentasPorDistrito(Resource):

    def get(self):
        sql_query = text('''SELECT distritos.distr_id,
        distritos.dpto_nombre,
        distritos.prov_nombre,
        distritos.distr_nombre,
        COALESCE(TPedidos.total,0) total
        FROM distritos
        LEFT JOIN (SELECT distr_id, count(*) as total
        FROM pedidos
        GROUP BY distr_id) AS TPedidos
        ON distritos.distr_id = TPedidos.distr_id
        ORDER BY 5 DESC, distritos.dpto_nombre,
        distritos.prov_nombre,
        distritos.distr_nombre;''')        

        result = base_de_datos.session.execute(sql_query)
        data = []
        for row in result:
            data.append({
                "distr_id": row['distr_id'],
                "dpto_nombre": row['dpto_nombre'],
                "prov_nombre": row['prov_nombre'],
                "distr_nombre": row['distr_nombre'],
                "total": row['total']
            })            

        return {
                "message": "Registros encontrados",
                "content": data
            }
        

class ReporteControllerVentasPorProducto(Resource):

    def get(self):
        sql_query = text('''select productos.prod_id,
            productos.nombre,
            productos.descripcion,
            productos.imagen,
            productos.oferta,
            productos.stock,
            coalesce(tventas.cantidad,0) as cantidad,
            coalesce(tventas.monto, 0) as monto
        from productos
        left join (select prod_id, sum(cantidad) as cantidad, sum(cantidad*precio_unit) as monto
        from pedidos_productos
        group by prod_id) as tventas
        on productos.prod_id = tventas.prod_id
        order by monto desc, cantidad desc, nombre;''')        

        result = base_de_datos.session.execute(sql_query)
        data = []
        for row in result:        
            data.append({
                "prod_id": row['prod_id'],
                "nombre": row['nombre'],
                "descripcion": row['descripcion'],
                "imagen": row['imagen'],
                "oferta": row['oferta'],
                "stock": row['stock'],
                "cantidad": float(row['cantidad']),
                "monto": float(row['monto'])
            })            

        return {
                "message": "Registros encontrados",
                "content": data
            }
                

class ReporteControllerVentasPorCliente(Resource):

    def get(self):
        sql_query = text('''select clientes.cliente_id,
            clientes.nombre,
            clientes.correo,
            clientes.telefono,
            TCompras.nro_compras,
            TCompras.monto
        from clientes
        inner join (select pedidos.cliente_id,
                    count(*) as nro_compras,
                    sum(tproductos.monto) as monto
        from pedidos
        inner join (select pedido_id,
                    sum(cantidad*precio_unit) as monto
        from pedidos_productos
        group by pedido_id) as tproductos
        on pedidos.pedido_id = tproductos.pedido_id
        group by pedidos.cliente_id) as TCompras
        on clientes.cliente_id = TCompras.cliente_id
        order by TCompras.monto desc;''')        

        result = base_de_datos.session.execute(sql_query)
        data = [] 

        for row in result:        
            data.append({
                "cliente_id": row['cliente_id'],
                "nombre": row['nombre'],
                "correo": row['correo'],
                "telefono": row['telefono'],
                "nro_compras": row['nro_compras'],
                "monto": float(row['monto'])
            })            

        return {
                "message": "Registros encontrados",
                "content": data
            }
                                