
from simpleai.search import SearchProblem,astar,greedy

class ProblemSortEmAll(SearchProblem):

    def is_goal(self, state):
            color_frascos = {}
            for frasco in state:
                if len(frasco) > 0:
                    if len(set(frasco)) != 1:
                        return False
                    color = frasco[0]
                    if color in color_frascos:
                        return False
                    color_frascos[color] = True
            return True
    
    def cost(self,state1,action,state2):
        return 1 
    
    def heuristic(self, state):
            incompletos = 0
            for frasco in state:
                if frasco and (len(frasco) != 4 or len(set(frasco)) != 1):
                    incompletos += 1
            return incompletos

    def actions(self, state):
        actions = []
        for i, frasco_origen in enumerate(state):
            if not frasco_origen or (len(frasco_origen) == 4 and len(set(frasco_origen)) == 1):
                continue  # Frasco vacío o frasco lleno de un solo color
            for j, frasco_destino in enumerate(state):
                if i != j:
                    if not frasco_destino or frasco_origen[-1] == frasco_destino[-1]:
                        if len(frasco_destino) < 4:
                            actions.append((i+1, j+1))
        return actions

    def result(self, state, action):
        new_state = [list(frasco) for frasco in state]
        origen, destino = action
        destino -= 1
        origen -= 1
        color = new_state[origen][-1]

        # Transferimos todo el líquido del color superior posible
        while new_state[origen] and new_state[origen][-1] == color and len(new_state[destino]) < 4:
            new_state[destino].append(new_state[origen].pop())
        return tuple(tuple(frasco) for frasco in new_state)

def jugar(frascos, dificil=False):
    problema = ProblemSortEmAll(frascos)

    if dificil:
        solucion = greedy(problema, graph_search=True)
    else:
        solucion = astar(problema, graph_search = True)
        
    if solucion:
        pasos_solucion = solucion.path()
        solucion_final = []
        for act in pasos_solucion:
            solucion_final.append(act[0])
        solucion_final_no_none = solucion_final[1:]
        return solucion_final_no_none
    else:
        return []
 

if __name__ == "__main__":
     pasos = jugar(
        frascos=(
            ("verde", "azul", "rojo", "naranja",),     # frasco 1, notar el orden de los colores
            ("azul", "rosa", "naranja",),              # frasco 2, notar que es de largo 3, queda un espacio vacío
            ("rosa", "celeste", "verde", "verde",),    # frasco 3, notar cómo "verde" se repite 2 veces por los 2 cuartos iguales
            ("rosa", "rojo", "celeste", "celeste",),   # frasco 4
            ("rojo", "azul", "lila",),                 # frasco 5
            ("verde", "naranja", "celeste", "rojo",),  # frasco 6
            ("azul", "naranja", "rosa",),              # frasco 7
            ("lila", "lila", "lila",),                 # frasco 8, notar la repetición de colores para cada cuarto
            (),                                       # frasco 9, notar que una tupla de largo 0 es un frasco vacío
        ),
        dificil=True,
)
     for paso in pasos:
        print(paso)
