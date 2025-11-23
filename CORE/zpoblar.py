import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='GalDot',
        tipo='Cliente', 
        nombre='Gal', 
        apellido='Gadot', 
        correo=test_user_email if test_user_email else 'GalDot@DCM.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='25.747.200-0',	
        direccion='123 Main Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/gal_gadot.jpeg')

    crear_usuario(
        username='HenVill',
        tipo='Cliente', 
        nombre='Henry', 
        apellido='Calvin', 
        correo=test_user_email if test_user_email else 'HenVill@DCM.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.202.357-5', 
        direccion='Albert Street, New York, \nNew York 10001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/Henry_Cavil.jpg')

    crear_usuario(
        username='joCena',
        tipo='Cliente', 
        nombre='John', 
        apellido='Cena', 
        correo=test_user_email if test_user_email else 'joCena@DCM.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11.991.600-3', 
        direccion='105 Apple Park Way, \nCupertino, CA 95014 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/john_cena.jpg')

    crear_usuario(
        username='Dwayson',
        tipo='Cliente', 
        nombre='Dwayne', 
        apellido='Johnson', 
        correo=test_user_email if test_user_email else 'Dwayson@DCM.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='16.469.725-8', 
        direccion='350 5th Ave, \nNew York, NY 10118 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/la-roca.jpg')

    crear_usuario(
        username='Brojas',
        tipo='Administrador', 
        nombre='Benjamin', 
        apellido='Rojas', 
        correo=test_user_email if test_user_email else 'Brojas@duoc.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.441.980-5', 
        direccion='10 Pine Road, Miami, \nFlorida 33101 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/benja.jpeg')
    
    crear_usuario(
        username='B3lkinHD',
        tipo='Administrador', 
        nombre='Osvaldo', 
        apellido='Ordoñez', 
        correo=test_user_email if test_user_email else 'B3lkinHD@duoc.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21.708.052-5', 
        direccion='1600 Pennsylvania Avenue NW, \nWashington, D.C. \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/chrisjames.jpg')

    crear_usuario(
        username='superHili',
        tipo='Superusuario',
        nombre='Hilary',
        apellido='Torres',
        correo=test_user_email if test_user_email else 'superHili@duoc.com',
        es_superusuario=True,
        es_staff=True,
        rut='13.029.317-4',
        direccion='15 Oak Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos',
        subscrito=False,
        imagen='perfiles/taylor.png')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción'},
        { 'id': 2, 'nombre': 'Aventura'},
        { 'id': 3, 'nombre': 'Estrategia'},
        { 'id': 4, 'nombre': 'RPG'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Acción"
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Bayonetta 3',
            'descripcion': 'La tercera entrega de la serie Bayonetta y continúa la historia de la bruja Bayonetta, conocida por su estilo de combate elegante y poderes mágicos. El juego combina secuencias de acción intensas con elementos de hack and slash, donde los jugadores controlan a Bayonetta mientras lucha contra hordas de enemigos angelicales y demoníacos. La jugabilidad se centra en combos fluidos, esquivas precisas y el uso estratégico de armas y magia. Con gráficos impresionantes y una narrativa rica en mitología y misterio.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/bayonetta_3.jpg'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Resident Evil 4 Remake',
            'descripcion': 'Versión modernizada del clásico juego de survival horror desarrollado por Capcom. La historia sigue a Leon S. Kennedy, quien es enviado a una aldea rural europea para rescatar a la hija del presidente de los Estados Unidos, Ashley Graham, secuestrada por un culto misterioso. El juego combina elementos de acción intensa con exploración y resolución de acertijos en entornos atmosféricos y a menudo claustrofóbicos.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/resident_evil_4_remake.jpg'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Rise Of The Tomb Raider',
            'descripcion': 'Juego de acción y aventuras desarrollado por Crystal Dynamics, continuando la historia de Lara Croft después de los eventos de su reboot en 2013. En esta entrega, Lara busca descubrir los secretos de la inmortalidad en Siberia, enfrentándose a peligros naturales y enemigos humanos. El juego combina exploración de mundo abierto con secuencias de acción intensas y resolución de acertijos ambientales.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/RiseoftheTombRaider.jpg'
        },
       
        # Categoría "Aventura"
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Oxenfree II: Lost Signals',
            'descripcion': 'Secuela del aclamado juego de aventuras y misterio "Oxenfree", desarrollado por Night School Studio. En esta continuación, los jugadores asumen el papel de Riley Poverly, una detective que regresa a su ciudad natal de Camena para investigar fenómenos paranormales relacionados con transmisiones de radio misteriosas y desapariciones inexplicables.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/Oxenfree_II_Lost_Signals_cover.jpg'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Silent Hill 2',
            'descripcion': '"Silent Hill 2" es un clásico juego de terror psicológico desarrollado por Konami. Lançado en 2001 para PlayStation 2, también disponible para Xbox, PC y más tarde para otras plataformas. el juego presenta deep storyline.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/sh2.jpg'
        },
        # Categoría "Estrategia" (4 juegos)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Alan Wake II',
            'descripcion': ' juego de terror psicológico desarrollado por Remedy Entertainment, conocido por su enfoque en narrativas complejas y experiencias atmosféricas. La secuela sigue la historia del escritor Alan Wake, quien se enfrenta a fuerzas oscuras y misteriosas en entornos surrealistas y perturbadores.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/AlanWake2.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Life Is Strange',
            'descripcion': 'Juego de aventuras episódico desarrollado por Dontnod Entertainment. La historia sigue a Max Caulfield, una estudiante de fotografía que descubre que puede retroceder en el tiempo. Ambientado en la ciudad ficticia de Arcadia Bay, el juego combina elementos de aventura gráfica con un fuerte enfoque en la narrativa y la toma de decisiones. Los jugadores exploran entornos detallados, interactúan con personajes memorables y enfrentan dilemas morales mientras Max intenta desentrañar los misterios de sus visiones premonitorias y salvar a su amiga Chloe Price.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/LifeIsStrange.jpeg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Beyond Two Souls',
            'descripcion': 'Juego interactivo de drama y acción desarrollado por Quantic Dream. La historia sigue la vida de Jodie Holmes, interpretada por Ellen Page, una mujer vinculada a una entidad sobrenatural llamada Aiden desde su nacimiento. Los jugadores alternan entre controlar a Jodie y a Aiden, explorando diferentes momentos de su vida mientras intentan entender el origen y el propósito de la entidad.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/Beyond.jpeg'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Phasmophobia',
            'descripcion': ' juego de terror cooperativo desarrollado por Kinetic Games. Los jugadores asumen el papel de investigadores paranormales que exploran lugares embrujados para recolectar evidencia de actividad paranormal. Utilizando una variedad de herramientas como detectores de EMF, cámaras de video y termómetros, los jugadores deben trabajar juntos para identificar el tipo de fantasma presente y cumplir con objetivos específicos para completar la misión.',
            'precio': 7990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/phasmophobia.jpg'
        },
        # Categoría "RPG"
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['25.747.200-0', '11.991.600-3']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

