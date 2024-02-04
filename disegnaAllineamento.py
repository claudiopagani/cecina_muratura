import math
from Maschio import Maschio


def disegnaAllineamento(
    nf, xyOrigine: list[float], angoloOrientamento: float, maschi: list[Maschio]
):
    #
    x0 = xyOrigine[0]
    y0 = xyOrigine[1]
    phi = angoloOrientamento
    #
    for maschio in maschi:
        # Definisci coordinate nodi
        x1 = maschio.x - maschio.L / 2
        x2 = maschio.x + maschio.L / 2
        y1 = 0
        y2 = maschio.H
        # Aggiungi nodi
        n1 = nf.addNode(x0 + x1 * math.cos(phi), y0 + x1 * math.sin(phi), y1)
        n2 = nf.addNode(x0 + x2 * math.cos(phi), y0 + x2 * math.sin(phi), y1)
        n3 = nf.addNode(x0 + x2 * math.cos(phi), y0 + x2 * math.sin(phi), y2)
        n4 = nf.addNode(x0 + x1 * math.cos(phi), y0 + x1 * math.sin(phi), y2)
        # crea maschio
        maschio = nf.addQuad(n1, n2, n3, n4, maschio.sezione, maschio.materiale)
        nf.setMacroelement(maschio, 5)
    return nf
