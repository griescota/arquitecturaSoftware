from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Articulo(BaseModel):
    id: int
    titulo: str
    contenido: str

class BaseDatosArticulos:
    def __init__(self):
        self.articulos = []

    def crear_articulo(self, articulo: Articulo):
        self.articulos.append(articulo)

    def leer_articulo(self, id: int) -> Articulo:
        for articulo in self.articulos:
            if articulo.id == id:
                return articulo
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    def modificar_articulo(self, id: int, articulo_actualizado: Articulo):
        for idx, articulo in enumerate(self.articulos):
            if articulo.id == id:
                self.articulos[idx] = articulo_actualizado
                return
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    def borrar_articulo(self, id: int):
        for idx, articulo in enumerate(self.articulos):
            if articulo.id == id:
                del self.articulos[idx]
                return
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

base_datos_articulos = BaseDatosArticulos()

@app.post("/articulos/", response_model=Articulo)
def crear_articulo(articulo: Articulo):
    base_datos_articulos.crear_articulo(articulo)
    return articulo

@app.get("/articulos/{id}", response_model=Articulo)
def leer_articulo(id: int):
    return base_datos_articulos.leer_articulo(id)

@app.put("/articulos/{id}")
def modificar_articulo(id: int, articulo: Articulo):
    base_datos_articulos.modificar_articulo(id, articulo)
    return {"mensaje": "Artículo modificado correctamente"}

@app.delete("/articulos/{id}")
def borrar_articulo(id: int):
    base_datos_articulos.borrar_articulo(id)
    return {"mensaje": "Artículo eliminado correctamente"}