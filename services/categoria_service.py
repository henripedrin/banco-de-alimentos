from repository.categoria_repository import CategoriaRepository

class CategoriaService:
    def __init__(self):
        self.repository = CategoriaRepository()

    def get_all_categorias(self):
        result = self.repository.get_all()
        return result if result else []
