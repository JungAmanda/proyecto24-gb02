from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import models, crud 
import os 

"""
Autor: Grupo GA01 - ASEE - AmandaMerino Tapia para Sonar
Versión: 2.0
Descripción: Conexión a la base de datos contenidos.db y creación de sesión

"""

# URL de la base de datos (SQLite en este caso)
# Acceso antes de DOCKER!!! SQLALCHEMY_DATABASE_URL = "sqlite:///./Microservicio_Contenidos/contenidos.db"

#Acceso a la base de datos tras realizar los cambios con Docker
DB_PATH = os.getenv("DB_PATH", "/app/contenidos.db")  # /app es el directorio de trabajo del contenedor
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Crear el motor para interactuar con la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear una fábrica de sesiones para hacer queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos de SQLAlchemy
Base = declarative_base()

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def initialize_database():
    if not os.path.exists(DB_PATH):
        # Crea las tablas si no existen
        Base.metadata.create_all(bind=engine)
        print("Base de datos creada y tablas inicializadas.")

        db = SessionLocal()
        try:
            insertar_datos_iniciales(db)
            db.commit()
            print("Valores iniciales insertados.")
        finally:
            db.close()


def insertar_datos_iniciales(db):
    insertar_subtitulos(db)
    insertar_doblajes(db)
    insertar_generos(db)
    insertar_contenidos(db)
    insertar_temporadas(db)
    insertar_episodios(db)
    insertar_actores_y_reparto(db)
    insertar_directores_y_contenidos(db)


def insertar_subtitulos(db):
    if db.query(models.Subtitulo).count() == 0:
        subtitulos = [
            models.Subtitulo(idSubtitulo="1", idioma="Inglés"),
            models.Subtitulo(idSubtitulo="2", idioma="Español"),
            models.Subtitulo(idSubtitulo="3", idioma="Italiano"),
            models.Subtitulo(idSubtitulo="4", idioma="Portugués")
        ]
        db.bulk_save_objects(subtitulos)


def insertar_doblajes(db):
    if db.query(models.Doblaje).count() == 0:
        doblajes = [
            models.Doblaje(idDoblaje="1", idioma="Inglés"),
            models.Doblaje(idDoblaje="2", idioma="Español"),
            models.Doblaje(idDoblaje="3", idioma="Italiano"),
            models.Doblaje(idDoblaje="4", idioma="Portugués")
        ]
        db.bulk_save_objects(doblajes)


def insertar_generos(db):
    if db.query(models.Genero).count() == 0:
        genero = models.Genero(id="1", nombre="Drama", descripcion="Descripcion de drama: llorar")
        db.add(genero)


def insertar_contenidos(db):
    if db.query(models.Contenido).count() == 0:
        contenidos = [
            models.Contenido(
                id="ContenidoPrueba1", tipoContenido="Pelicula", titulo="ContenidoPrueba", descripcion="Descripcion de prueba",
                fechaLanzamiento="0000-00-00", idGenero="1", valoracionPromedio=0, idSubtitulosContenido="1",
                idDoblajeContenido="1", duracion=120, idDirector="1"
            ),
            models.Contenido(
                id="1", tipoContenido="Serie", titulo="Los Soprano", descripcion="Descripcion de los soprano",
                fechaLanzamiento="0000-00-00", idGenero="1", valoracionPromedio=0, idSubtitulosContenido="1",
                idDoblajeContenido="1"
            )
        ]
        db.bulk_save_objects(contenidos)


def insertar_temporadas(db):
    if db.query(models.Temporada).count() == 0:
        temporadas = [
            models.Temporada(idContenido="1", idTemporada="1", numeroTemporada="1"),
            models.Temporada(idContenido="1", idTemporada="2", numeroTemporada="3"),
            models.Temporada(idContenido="1", idTemporada="3", numeroTemporada="3")
        ]
        db.bulk_save_objects(temporadas)


def insertar_episodios(db):
    if db.query(models.Episodio).count() == 0:
        episodios = [
            models.Episodio(idContenido="1", idTemporada="1", idEpisodio="1", idDirector="1", numeroEpisodio="1", duracion="15"),
            models.Episodio(idContenido="1", idTemporada="1", idEpisodio="2", idDirector="1", numeroEpisodio="2", duracion="16"),
            models.Episodio(idContenido="1", idTemporada="2", idEpisodio="3", idDirector="1", numeroEpisodio="1", duracion="17"),
            models.Episodio(idContenido="1", idTemporada="2", idEpisodio="4", idDirector="1", numeroEpisodio="2", duracion="11"),
            models.Episodio(idContenido="1", idTemporada="3", idEpisodio="5", idDirector="1", numeroEpisodio="1", duracion="20"),
            models.Episodio(idContenido="1", idTemporada="3", idEpisodio="6", idDirector="1", numeroEpisodio="2", duracion="21")
        ]
        db.bulk_save_objects(episodios)


def insertar_actores_y_reparto(db):
    if db.query(models.Actor).count() == 0:
        actores = [
            models.Actor(id="1", nombre="Robert Deniro", nacionalidad="EstadoUnidense", fechaNacimiento="1943-08-17"),
            models.Actor(id="2", nombre="Tom Cruise", nacionalidad="EstadoUnidense", fechaNacimiento="1962-07-03"),
            models.Actor(id="3", nombre="Tom Hardy", nacionalidad="Britanico", fechaNacimiento="1977-09-15"),
            models.Actor(id="4", nombre="George Clooney", nacionalidad="EstadoUnidense", fechaNacimiento="1961-05-06")
        ]
        db.bulk_save_objects(actores)

        contenido_vinculado = models.Contenido(
            id="ContenidoActores1", tipoContenido="Pelicula", titulo="PeliculaActores", descripcion="prueba",
            fechaLanzamiento="0000-00-00", idGenero="1", valoracionPromedio=0, idSubtitulosContenido="1",
            idDoblajeContenido="1", duracion=120, idDirector="1"
        )
        db.add(contenido_vinculado)

        reparto = [models.Reparto(idContenido="ContenidoActores1", idActor=str(i)) for i in range(1, 5)]
        db.bulk_save_objects(reparto)


def insertar_directores_y_contenidos(db):
    if db.query(models.Director).count() == 0:
        directores = [
            models.Director(id="1", nombre="Francis Ford Coppola", nacionalidad="EstadoUnidense", fechaNacimiento="1939-04-07"),
            models.Director(id="2", nombre="Stanley Kubrik", nacionalidad="Estadounidense", fechaNacimiento="1928-07-26"),
            models.Director(id="3", nombre="Jean Luc Godard", nacionalidad="Frances", fechaNacimiento="1930-12-03"),
            models.Director(id="4", nombre="David Lynch", nacionalidad="EstadoUnidense", fechaNacimiento="1946-01-20")
        ]
        db.bulk_save_objects(directores)

        contenidos = [
            models.Contenido(
                id=f"ContenidoDirectores{i}", tipoContenido="Pelicula", titulo=f"PeliculaDirectores{i}", descripcion="prueba",
                fechaLanzamiento="0000-00-00", idGenero="1", valoracionPromedio=0, idSubtitulosContenido="1",
                idDoblajeContenido="1", duracion=120, idDirector=str(i)
            ) for i in range(1, 5)
        ]
        db.bulk_save_objects(contenidos)