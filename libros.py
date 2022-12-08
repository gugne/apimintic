import os 
from fastapi import FastAPI, HTTPException, Body,  status
from fastapi.responses import Response, JSONResponse
from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from uuid import UUID
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from typing import Optional, List


# ----------------------------|Base de Datos|---------------------------
MONGODB_URL= "mongodb+srv://berna:1090450623@cluster0.vlf3xco.mongodb.net/test"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db= client.misiontic


app = FastAPI()



# CONTENIDO = []
# USUARIO = []
# COMPRAS = []



# ----------------------------|GLOBALES|---------------------------

# Modelo para asignar id
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
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
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra={
            "example" : {
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



class Actualizar_Contenido (BaseModel):
    titulo: Optional[str]
    descripcion: Optional[str]
    autor: Optional[str]
    isbn: Optional[str]
    genero: Optional[str]
    editorial: Optional[str]
    año: int
    precio: float
    tipo: TipoContenido = Field(title= "Tipo de Contenido",default=TipoContenido.libro)
    listado: bool= Field(titel="Es listado?", default=True)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra={
            "example" : {
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

# ######Get de Contenido por categoría
# @app.get ("/categorias/{categoria}", tags=["Contenido"])
# async def filtrar_categoria(categoria: TipoContenido):
#     buscar_categoria= []
#     for i in CONTENIDO:
#          if i.tipo == categoria:
#              buscar_categoria.append(i)
#     return buscar_categoria



######Get de Contenido
@app.get("/", tags=["Contenido"], summary=["VER TODOS (GET): Muestra todos los contenidos."])
async def ver_todos():
    contenidos= await db["contenidos"].find().to_list(1000)
    return contenidos
    # return CONTENIDO



######Get de Contenido por id
@app.get("/categorias/{id}", tags=["Contenido"],summary=["CONTENIDO POR ID (GET): Permite buscar un contenido especifico por el id."], response_model=Contenido)
async def ver_un_contenido(id: str):
    if (contenido := await db["contenidos"].find_one({"_id": id})) is not None:
        return contenido
    raise HTTPException(status_code=404, detail=f"Contenido {id} no encontrado, no existe o está mal escrito. Verifique e intente de nuevo")
    # for i in CONTENIDO:
    #     if i.id == contenido_id:
    #         return i



######Post de Contenido
@app.post("/", tags=["Contenido"], summary=["CREAR CONTENIDO (POST): Permite crear un nuevo contenido."], response_model=Contenido)
async def crear_contenido(contenido : Contenido):
    contenido = jsonable_encoder(contenido)
    nuevo_contenido= await db["contenidos"].insert_one(contenido)
    contenido_creado = await db["contenidos"].find_one({"_id": nuevo_contenido.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=contenido_creado)
    # if contenido.tipo == "Revista":
    #     pronombre= "La"
    # else:
    #     pronombre= "El"
    # return f"{pronombre} {contenido.tipo.lower()}: '{contenido.titulo}' de '{contenido.autor}' ha sido creado exitosamente"




######Put de Contenido
@app.put("/categorias/{id}", tags=["Contenido"], summary=["MODIFICAR CONTENIDO (PUT): Permite buscar un contenido por su id y modificarlo."], response_model=Contenido)
async def modificar_contenido(id: str, contenido: Actualizar_Contenido = Body(...)):
    contenido = {k: v for k, v in contenido.dict().items() if v is not None}
    if len(contenido) >= 1:
        actualizar_resultado = await db["contenidos"].update_one({"_id": id}, {"$set": contenido})
        if actualizar_resultado.modified_count == 1:
            if (actualizar_contenido := await db["contenidos"].find_one({"_id": id})) is not None:
                return actualizar_contenido
    if (contenido_existente := await db["contenidos"].find_one({"_id": id})) is not None:
        return contenido_existente
    raise HTTPException(status_code=404, detail=f"Contenido {id} no encontrado, no existe o está mal escrito. Verifique e intente de nuevo")   
    # contador=0
    # for i in CONTENIDO:
    #     contador +=1
    #     if i.id == contenido_id:
    #         CONTENIDO[contador-1]= contenido
    #         return f"""La entrada ha sido actualizada de forma exitosa:
    #     {contenido}"""
    # return
    
 
      
######Delete de Contenido
@app.delete("/categorias/{id}", tags=["Contenido"], summary=["BORRAR UN CONTENIDO (DELETE): Permite buscar un contenido por su id y borrarlo."])
async def borrar_contenido(id: str):
    borrar_resultado = await db["contenidos"].delete_one({"_id": id})
    if borrar_resultado.deleted_count == 1:
        return f"Contenido: {id}, eliminado de forma exitosa."
    raise HTTPException(status_code=404, detail=f"Contenido {id} no encontrado, no existe o está mal escrito. Verifique e intente de nuevo")
    # for i in CONTENIDO:
    #     if i.id == contenido_id:
    #         CONTENIDO.remove(i)
    #         return f"Contenido  con id '{contenido_id}' fue eliminado de forma exitosa."
    # raise no_encontrado()





#                             __________________________      
# ----------------------------|Funciones para  USUARIO|---------------------------


######Modelo de Usuario
class Usuario (BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    nombre : str = Field(title="Nombre completo:",
                        max_length=50,
                        min_length=1, )
    apellido : str = Field(title="Apellidos:",
                        max_length=50,
                        min_length=1, )
    email : EmailStr = Field(alias="_id")
    
    contraseña : str = Field(title="Contraseña:",
                        max_length=25,
                        min_length=8, )
    telefono : str =Field(title="Teléfono celular:",
                        max_length=11,
                        min_length=1, )
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra={
            "example" : {
                "nombre" : "Angie Elizabeth",
                "apellido": "León",
                "email": "angie@elizabeth.com",
                "contraseña": "123456789",
                "telefono": "3113323458",
                        }                
        }

######Get de de login
# @app.get("/user/login", tags=["Usuario"], summary=["LOGIN (GET): Permite iniciar sesión."],
#          responses={
#              400: {"model": Message, "description": "Contraseña incorrecta"},
#              404: {"model": Message, "description": "El usuario no existe"},
#              })
# async def login (nombre_usuario: EmailStr, contraseña : str ):
#     for i in USUARIO:
#         if i.email == nombre_usuario:
#             if i.contraseña == contraseña:
#                 Usuario_Actual.usurio_actual= nombre_usuario                
#                 return f"Sesión iniciada de forma exitosa como: {Usuario_Actual.usurio_actual}"
#             else:
#                 raise HTTPException(status_code=400, detail="Lo sentimos, las credenciales de inicio de sesión no coinciden.")
#     raise HTTPException(status_code=404, detail="El usuario con el que está intentando iniciar sesión no existe o está mal escrito.")



######Get de de logout
# @app.get("/user/logout", tags=["Usuario"], summary=["LOGOUT (GET): Permite cerrar sesión."])
# async def logout():
#     global usurio_actual
#     if Usuario_Actual.usurio_actual != None:
#         Usuario_Actual.usurio_actual= None
#         return "Sesión cerrada exitosamente."
#     return "Aún no ha iniciado sesión con ningún usuario."



######Get de usuario
@app.get("/users", tags=["Usuario"], summary=["VER TODOS (GET): Muestra todos los usuarios."], response_model=List[Usuario])
async def ver_usuarios():
    usuarios= await db["usuarios"].find().to_list(1000)
    return usuarios



######Get de Usuario por nombre de usuario
@app.get("/user/{nombre_usuario}", tags=["Usuario"], summary=["VER UN USUARIO (GET): Busca y muestra un usuario específico por el username(correo electrónico)."],
         responses={
              404: {"model": Message, "description": "El usuario no existe"},
              })
async def ver_un_usuario(nombre_usuario: EmailStr):
    if (nombre_usuario := await db["usuarios"].find_one({"_id": nombre_usuario})) is not None:
        return nombre_usuario
    raise HTTPException(status_code=404, detail=f"Contenido {nombre_usuario} no encontrado, no existe o está mal escrito. Verifique e intente de nuevo")
# async def ver_un_usuario(nombre_usuario: EmailStr):
#     for i in USUARIO:
#         if i.email == nombre_usuario:
#             return i
#     raise HTTPException(status_code=404, detail="El usuario que está buscando no existe o está mal escrito.")



######Post de Usuario
@app.post("/user", tags=["Usuario"], summary=["CREAR USUARIO (POST): Crea un nuevo usuario."], 
          responses={
              409: {"model": Message, "description": "Correo electrónico ya registrado"},
              })
async def nuevo_usuario(usuario : Usuario):
    usuario = jsonable_encoder(usuario)
    nuevo_usuario= await db["usuarios"].insert_one(usuario)
    usuario_creado = await db["usuarios"].find_one({"_id": nuevo_usuario.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=usuario_creado)
    
# async def nuevo_usuario(usuario: Usuario):
#     for i in USUARIO:
#         if i.email == usuario.email:
#             raise HTTPException(status_code=409, detail="Este correo electrónico ya ha sido registrado")
#     USUARIO.append(usuario)
#     return "Usuario nuevo creado de forma exitosa"



######Put de Usuario
@app.put("/user/{id}",tags=["Usuario"], summary=["MODIFICAR UN USUARIO (POST): Permite buscar un usuario por su username(email) y modificarlo."],
         responses={
              404: {"model": Message, "description": "El usuario no existe"},
              })
async def modificar_usuario(id: EmailStr, usuario: Usuario = Body(...)):
    usuario = {k: v for k, v in usuario.dict().items() if v is not None}
    if len(usuario) >= 1:
        actualizar_usuario = await db["usuarios"].update_one({"_id": id}, {"$set": usuario})
        if actualizar_usuario.modified_count == 1:
            if (actualizar_usuario := await db["usuarios"].find_one({"_id": id})) is not None:
                return actualizar_usuario
    if (usuario_existente := await db["usuarios"].find_one({"_id": id})) is not None:
        return usuario_existente
    raise HTTPException(status_code=404, detail=f"Usuario: {id} no encontrado. Este usuario no existe o está mal escrito. Verifique e intente de nuevo")   
# async def modificar_usuario(nombre_usuario: EmailStr, usuario : Usuario):
#     contador=0
#     for i in USUARIO:
#         contador+=1
#         if i.email == nombre_usuario:
#             USUARIO[contador-1]= usuario
#             return usuario
#     raise HTTPException(status_code=404, detail="El usuario que está buscando no existe o está mal escrito.")



######Delete de Usuario
@app.delete("/user/{nombre_usuario}", tags=["Usuario"], summary=["BORRAR UN USUARIO (DELETE): Permite buscar un usuario por su username(email) y eliminarlo."],
            responses={
              404: {"model": Message, "description": "El usuario no existe"},
              })
async def borrar_usuario(id: EmailStr):
    borrar_usuario = await db["usuarios"].delete_one({"_id": id})
    if borrar_usuario.deleted_count == 1:
        return f"Usuario: {id}, eliminado de forma exitosa."
    raise HTTPException(status_code=404, detail=f"Usuario: {id} no encontrado. Este usuario no existe o está mal escrito. Verifique e intente de nuevo")
    # for i in USUARIO:
    #     if i.email == nombre_usuario:
    #         USUARIO.remove(i)
    #         return f"El usuario {i.email} ha sido borrado exitosamente"
    # raise HTTPException(status_code=404, detail="El usuario que está buscando no existe o está mal escrito.")





# #                              ________________________
# # -----------------------------|Funciones para  ORDEN|-----------------------------

# class Compra (BaseModel):
#     id : UUID
#     usuarioId : EmailStr
#     pagado : bool = Field(default=False)
#     class Config:
#         schema_extra={
#             "example" : {
#                 "id" : "4fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "usuarioId" : "angie@elizabeth.com",
#                 "pagado" : False
#                         }                
#         }



# ######Get de TODAS las Compras
# @app.get("/compras", tags=["Compras"], summary=["VER TODOS (GET): Muestra todas las compras de todos los usuarios."])
# async def ver_todo_compras():
#     return COMPRAS



# ######Get de Compra por nombre de usuario
# @app.get("/compras/{nombre_usuario}", tags=["Compras"], summary=["VER COMPRAS DE USUARIO (GET): Busca y muestra un TODAS las compras de un usuario específico por el username(correo electrónico)."],
#          responses={
#               404: {"model": Message, "description": "El usuario no existe"},
#               })
# async def ver_compras_usuario(nombre_usuario: EmailStr):
#     for i in COMPRAS:
#         if i.usuarioId == nombre_usuario:
#             return i
#     raise HTTPException(status_code=404, detail="El usuario que está buscando no existe o no ha realizado ninguna compra.")



#  ######Get compras del usuario loggeado
# # @app.get("/usuario/{usuario}/compras", tags=["Compras"], summary=["VER COMPRAS DE USUARIO LOGEADO (GET): Muestra TODAS las compras del usuario actual por el username(correo electrónico)."],
# #          responses={
# #               404: {"model": Message, "description": "No hay compras de este usuario"},
# #               })
# # async def ver_compras_usuario(usuario: EmailStr= Field(default=Usuario_Actual.usurio_actual)):
# #     for i in COMPRAS:
# #         if i.usuarioId == Usuario_Actual.usurio_actual:
# #             return i
# #     raise HTTPException(status_code=404, detail="Aún no has realizado ninguna compra.")


# ######Post de Compra
# @app.post("/compras", tags=["Compras"], summary=["CREAR COMPRA (POST): Permite crear una nueva orden."])
# async def crear_compra( orden: Compra):
#     orden.usuarioId = Usuario_Actual.usurio_actual
#     COMPRAS.append(orden)
#     return f"Compra realizada con exito."



# ######Delete de Compra
# @app.delete("/compras/{id_compra}", tags=["Compras"], summary=["BORRAR COMPRA (POST): Permite borrar una orden existente."])
# async def borrar_compra( id_compra: UUID):
#     for i in COMPRAS:
#         if i.id == id_compra:
#             COMPRAS.remove(i)
#             return f"La compra {i.id} ha sido borrado exitosamente"
#     raise HTTPException(status_code=404, detail="No existe una orden con el id {id_compra}")
            
            
            

#     COMPRAS.append(orden)
#     return f"Compra realizada con exito."

    