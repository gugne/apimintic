from fastapi import FastAPI, HTTPException, Response, status
from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID

app = FastAPI()


CONTENIDO = []
USUARIO = []
COMPRAS = []



# ----------------------------|GLOBALES|---------------------------

# Model mensaje para http response
class Message(BaseModel):
    message: str

#HTTP Respons code 404
def no_encontrado():
    return HTTPException(status_code=404, 
                        detail="Contenido no encontrado, el id no existe o está mal escrito",
                        headers={"X-header-error": "Nada para ver en el UUID"})



#                             ____________________________
# ----------------------------| Funciones para  CONTENIDO|---------------------------
#Usuario loggeado
class Usuario_Actual():
    usurio_actual= None


#Modelo enum para tipo
class TipoContenido(str,Enum):
    revista = "Revista"
    libro = "Libro"
    articulo = "Artículo"


######Modelo de Contenido
class Contenido (BaseModel):
    id: UUID
    titulo: str = Field(title="Nombre del libro:",
                        max_length=100,
                        min_length=1, )
    descripcion: str = Field(title="Descripción del libro:",
                        max_length=500,
                        min_length=1, )
    autor: str = Field(title="Autor del libro:",
                        max_length=50,
                        min_length=1, )
    isbn: str = Field(title="Código ISBN:",
                        max_length=50,
                        min_length=1, )
    genero: str = Field(title="Género del libro:",
                        max_length=25,
                        min_length=1, )
    editorial: str = Field(title="Nombre editorial",
                        max_length=50,
                        min_length=1, )
    año: int
    precio: float
    tipo: TipoContenido = Field(title= "Tipo de Contenido",default=TipoContenido.libro)
    listado: bool= Field(titel="Es listado?", default=True)
    
    class Config:
        schema_extra={
            "example" : {
                "id" : "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "titulo" : "La insoportable levedad del ser",
                "descripcion": "La insoportable levedad del ser trata de un hombre y sus dudas existenciales en torno a la vida en pareja, convertidas en conflictos sexuales y afectivos. La novela relata escenas de la vida cotidiana trazadas con un profundo sentido trascendental: la inutilidad de la existencia y la necesidad del eterno retorno.",
                "autor": "Milan Kundera",
                "isbn": "9871210752",
                "genero": "Novela",
                "editorial": "Tusquets",
                "año": 2008,
                "precio": 30,
                "tipo": "Libro",
                "listado": True       
                        }                
        }



######Get de Contenido por categoría
@app.get ("/categorias/{categoria}", tags=["Contenido"])
async def filtrar_categoria(categoria: TipoContenido):
    buscar_categoria= []
    for i in CONTENIDO:
         if i.tipo == categoria:
             buscar_categoria.append(i)
    return buscar_categoria



######Get de Contenido
@app.get("/", tags=["Contenido"], summary=["VER TODOS (GET): Muestra todos los contenidos."])
async def ver_todos():
    return CONTENIDO



######Get de Contenido por id
@app.get("/categorias/{contenido_id}", tags=["Contenido"],summary=["CONTENIDO POR ID (GET): Permite buscar un contenido especifico por el id."])
async def ver_un_contenido(contenido_id:UUID):
    for i in CONTENIDO:
        if i.id == contenido_id:
            return i



######Post de Contenido
@app.post("/", tags=["Contenido"], summary=["CREAR CONTENIDO (POST): Permite crear un nuevo contenido."])
async def crear_contenido(contenido : Contenido):
    CONTENIDO.append(contenido)
    if contenido.tipo == "Revista":
        pronombre= "La"
    else:
        pronombre= "El"
    return f"{pronombre} {contenido.tipo.lower()}: '{contenido.titulo}' de '{contenido.autor}' ha sido creado exitosamente"



######Put de Contenido
@app.put("/categorias/{contenido_id}", tags=["Contenido"], summary=["MODIFICAR CONTENIDO (PUT): Permite buscar un contenido por su id y modificarlo."])
async def modificar_contenido(contenido_id: UUID, contenido: Contenido):
    contador=0
    for i in CONTENIDO:
        contador +=1
        if i.id == contenido_id:
            CONTENIDO[contador-1]= contenido
            return f"""La entrada ha sido actualizada de forma exitosa:
        {contenido}"""
    return
    
 
      
######Delete de Contenido
@app.delete("/categorias/{contenido_id}",tags=["Contenido"], summary=["BORRAR UN CONTENIDO (DELETE): Permite buscar un contenido por su id y borrarlo."])
async def borrar_contenido(contenido_id: UUID):
    for i in CONTENIDO:
        if i.id == contenido_id:
            CONTENIDO.remove(i)
            return f"Contenido  con id '{contenido_id}' fue eliminado de forma exitosa."
    raise no_encontrado()





#                             __________________________      
# ----------------------------|Funciones para  USUARIO|---------------------------

######Modelo de Usuario
class Usuario (BaseModel):
    id : UUID
    nombre : str = Field(title="Nombre completo:",
                        max_length=50,
                        min_length=1, )
    apellido : str = Field(title="Apellidos:",
                        max_length=50,
                        min_length=1, )
    email : EmailStr
    
    contraseña : str = Field(title="Contraseña:",
                        max_length=25,
                        min_length=8, )
    telefono : str =Field(title="Teléfono celular:",
                        max_length=11,
                        min_length=1, )
    
    class Config:
        schema_extra={
            "example" : {
                "id" : "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "nombre" : "Angie Elizabeth",
                "apellido": "León",
                "email": "angie@elizabeth.com",
                "contraseña": "123456789",
                "telefono": "3113323458",
                        }                
        }



######Get de de login
@app.get("/user/login", tags=["Usuario"], summary=["LOGIN (GET): Permite iniciar sesión."],
         responses={
             400: {"model": Message, "description": "Contraseña incorrecta"},
             404: {"model": Message, "description": "El usuario no existe"},
             })
async def login (nombre_usuario: EmailStr, contraseña : str ):
    for i in USUARIO:
        if i.email == nombre_usuario:
            if i.contraseña == contraseña:
                Usuario_Actual.usurio_actual= nombre_usuario                
                return f"Sesión iniciada de forma exitosa como: {Usuario_Actual.usurio_actual}"
            else:
                raise HTTPException(status_code=400, detail="Lo sentimos, las credenciales de inicio de sesión no coinciden.")
    raise HTTPException(status_code=404, detail="El usuario con el que está intentando iniciar sesión no existe o está mal escrito.")



######Get de de logout
@app.get("/user/logout", tags=["Usuario"], summary=["LOGOUT (GET): Permite cerrar sesión."])
async def logout():
    global usurio_actual
    if Usuario_Actual.usurio_actual != None:
        Usuario_Actual.usurio_actual= None
        return "Sesión cerrada exitosamente."
    return "Aún no ha iniciado sesión con ningún usuario."



######Get de usuario
@app.get("/users", tags=["Usuario"], summary=["VER TODOS (GET): Muestra todos los usuarios."])
async def ver_usuarios():
    return USUARIO



######Get de Usuario por nombre de usuario
@app.get("/user/{nombre_usuario}", tags=["Usuario"], summary=["VER UN USUARIO (GET): Busca y muestra un usuario específico por el username(correo electrónico)."],
         responses={
              404: {"model": Message, "description": "El usuario no existe"},
              })
async def ver_un_usuario(nombre_usuario: EmailStr):
    for i in USUARIO:
        if i.email == nombre_usuario:
            return i
    raise HTTPException(status_code=404, detail="El usuario que está buscando no existe o está mal escrito.")



######Post de Usuario
@app.post("/user", tags=["Usuario"], summary=["CREAR USUARIO (POST): Crea un nuevo usuario."], 
          responses={
              409: {"model": Message, "description": "Correo electrónico ya registrado"},
              })
async def nuevo_usuario(usuario: Usuario):
    for i in USUARIO:
        if i.email == usuario.email:
            raise HTTPException(status_code=409, detail="Este correo electrónico ya ha sido registrado")
    USUARIO.append(usuario)
    return "Usuario nuevo creado de forma exitosa"



######Put de Usuario
@app.put("/user/{nombre_usuario}",tags=["Usuario"], summary=["MODIFICAR UN USUARIO (POST): Permite buscar un usuario por su username(email) y modificarlo."],
         responses={
              404: {"model": Message, "description": "El usuario no existe"},
              })
async def modificar_usuario(nombre_usuario: EmailStr, usuario : Usuario):
    contador=0
    for i in USUARIO:
        contador+=1
        if i.email == nombre_usuario:
            USUARIO[contador-1]= usuario
            return usuario
    raise HTTPException(status_code=404, detail="El usuario que está buscando no existe o está mal escrito.")



######Delete de Usuario
@app.delete("/user/{nombre_usuario}", tags=["Usuario"], summary=["BORRAR UN USUARIO (DELETE): Permite buscar un usuario por su username(email) y eliminarlo."],
            responses={
              404: {"model": Message, "description": "El usuario no existe"},
              })
async def borrar_usuario(nombre_usuario: EmailStr):
    for i in USUARIO:
        if i.email == nombre_usuario:
            USUARIO.remove(i)
            return f"El usuario {i.email} ha sido borrado exitosamente"
    raise HTTPException(status_code=404, detail="El usuario que está buscando no existe o está mal escrito.")





#                              ________________________
# -----------------------------|Funciones para  ORDEN|-----------------------------

class Compra (BaseModel):
    id : UUID
    usuarioId : EmailStr
    pagado : bool = Field(default=False)
    class Config:
        schema_extra={
            "example" : {
                "id" : "4fa85f64-5717-4562-b3fc-2c963f66afa6",
                "usuarioId" : "angie@elizabeth.com",
                "pagado" : False
                        }                
        }



######Get de TODAS las Compras
@app.get("/compras", tags=["Compras"], summary=["VER TODOS (GET): Muestra todas las compras de todos los usuarios."])
async def ver_todo_compras():
    return COMPRAS



######Get de Compra por nombre de usuario
@app.get("/compras/{nombre_usuario}", tags=["Compras"], summary=["VER COMPRAS DE USUARIO (GET): Busca y muestra un TODAS las compras de un usuario específico por el username(correo electrónico)."],
         responses={
              404: {"model": Message, "description": "El usuario no existe"},
              })
async def ver_compras_usuario(nombre_usuario: EmailStr):
    for i in COMPRAS:
        if i.usuarioId == nombre_usuario:
            return i
    raise HTTPException(status_code=404, detail="El usuario que está buscando no existe o no ha realizado ninguna compra.")



 ######Get compras del usuario loggeado
# @app.get("/usuario/{usuario}/compras", tags=["Compras"], summary=["VER COMPRAS DE USUARIO LOGEADO (GET): Muestra TODAS las compras del usuario actual por el username(correo electrónico)."],
#          responses={
#               404: {"model": Message, "description": "No hay compras de este usuario"},
#               })
# async def ver_compras_usuario(usuario: EmailStr= Field(default=Usuario_Actual.usurio_actual)):
#     for i in COMPRAS:
#         if i.usuarioId == Usuario_Actual.usurio_actual:
#             return i
#     raise HTTPException(status_code=404, detail="Aún no has realizado ninguna compra.")


######Post de Compra
@app.post("/compras", tags=["Compras"], summary=["CREAR COMPRA (POST): Permite crear una nueva orden."])
async def crear_compra( orden: Compra):
    orden.usuarioId = Usuario_Actual.usurio_actual
    COMPRAS.append(orden)
    return f"Compra realizada con exito."



######Delete de Compra
@app.delete("/compras/{id_compra}", tags=["Compras"], summary=["BORRAR COMPRA (POST): Permite borrar una orden existente."])
async def borrar_compra( id_compra: UUID):
    for i in COMPRAS:
        if i.id == id_compra:
            COMPRAS.remove(i)
            return f"La compra {i.id} ha sido borrado exitosamente"
    raise HTTPException(status_code=404, detail="No existe una orden con el id {id_compra}")
            
            
            

    COMPRAS.append(orden)
    return f"Compra realizada con exito."

    