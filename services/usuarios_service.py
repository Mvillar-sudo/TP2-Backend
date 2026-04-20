from repositories import usuarios_repository

def crear_usuario(nombre, email):
    return usuarios_repository.crear_usuario(nombre, email)

def listar_usuarios(limit, offset):
    return usuarios_repository.listar_usuarios(limit, offset)

def obtener_usuario(id):
    return usuarios_repository.obtener_usuario(id)

def actualizar_usuario(id, nombre, email):
    return usuarios_repository.actualizar_usuario(id, nombre, email)

def borrar_usuario(id):
    return usuarios_repository.borrar_usuario(id)
