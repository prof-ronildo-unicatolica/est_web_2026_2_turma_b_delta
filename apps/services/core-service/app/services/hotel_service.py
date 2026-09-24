from sqlalchemy.orm import Session

from app.models.hotel import Cidade, Hotel
from app.repositories.hotel_repository import CidadeRepository, HotelRepository


class RegraDeNegocioError(Exception):
    pass


class CidadeJaExisteError(RegraDeNegocioError):
    pass


class CidadeNaoEncontradaError(RegraDeNegocioError):
    pass


class CidadeService:
    def __init__(self, db: Session):
        self.repository = CidadeRepository(db)

    def criar(self, nome: str) -> Cidade:
        nome = nome.strip()
        if self.repository.get_by_nome(nome):
            raise CidadeJaExisteError(f"Ja existe uma cidade chamada '{nome}'.")
        return self.repository.create(nome=nome)

    def listar(self) -> list[Cidade]:
        return self.repository.list()


class HotelService:
    def __init__(self, db: Session):
        self.repository = HotelRepository(db)
        self.cidades = CidadeRepository(db)

    def criar(self, nome: str, cidade_id) -> Hotel:
        nome = nome.strip()
        if not self.cidades.get_by_id(cidade_id):
            raise CidadeNaoEncontradaError(f"Nao existe cidade com id '{cidade_id}'.")
        return self.repository.create(nome=nome, cidade_id=cidade_id)

    def listar(self, cidade_id=None) -> list[Hotel]:
        if cidade_id is not None:
            if not self.cidades.get_by_id(cidade_id):
                raise CidadeNaoEncontradaError(f"Nao existe cidade com id '{cidade_id}'.")
            return self.repository.list_by_cidade(cidade_id)
        return self.repository.list()
