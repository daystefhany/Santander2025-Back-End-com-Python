# main.py
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///./workout.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo Atleta
class Atleta(Base):
    __tablename__ = "atletas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    centro_treinamento = Column(String, nullable=True)
    categoria = Column(String, nullable=True)

# Criar tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workout API")

# Endpoint para listar atletas (sem filtros ainda)
@app.get("/atletas")
def listar_atletas():
    db = SessionLocal()
    atletas = db.query(Atleta).all()
    db.close()
    return atletas

# Endpoint para criar atleta
@app.post("/atletas")
def criar_atleta(nome: str, cpf: str, centro_treinamento: str = None, categoria: str = None):
    db = SessionLocal()
    atleta = Atleta(nome=nome, cpf=cpf, centro_treinamento=centro_treinamento, categoria=categoria)
    db.add(atleta)
    db.commit()
    db.refresh(atleta)
    db.close()
    return atleta
