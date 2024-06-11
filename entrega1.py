from simpleai.search import astar, SearchProblem
from simpleai.search.viewers import WebViewer


class Frasco:
    def __init__(self, *colores):
        self.colores = colores


class ProblemSortEmAll(SearchProblem):
    def __init__(self, frascos, dificil):
        super(ProblemSortEmAll, self).__init__()
        self.frascos = frascos
        self.dificil = dificil

    def is_goal(self, state):
        color_elegido = None
        cantidad = 0
        cantidad_frascos_llenos = 0
        for frasco in state:
            for indice, color in enumerate(frasco):
                if indice == 1:
                    color_elegido = color
                    cantidad = 1
                elif color == color_elegido:
                    cantidad += 1
                if cantidad == 4:
                    cantidad_frascos_llenos += 1
        if cantidad_frascos_llenos == 6:
            return True
        else:
            return False

    def heuristic(self,state):
        colores_disponibles = len(state) - 1
        frascos_cerrados = 0

        for frasco in state:
            completo = all(x == frasco[0] for x in frasco)
            if completo:
                frascos_cerrados += 1

        return colores_disponibles - frascos_cerrados
