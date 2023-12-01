from myutils import graph
from pytest import approx
import igraph
import os

##########################################################
def test_haversine():
    # Coords from GMaps. Results from GMaps directions.

    # Singularity
    assert graph.haversine(0, 0, 0, 0) == 0

    # Washington Sq. Park
    lat1, lon1 = 40.730723, -73.995599 # NE corner
    lat2, lon2 = 40.729575, -73.996594 # SE corner
    assert graph.haversine(lon1, lat1, lon2, lat2) == approx(152, 3)

    # Sao Paulo
    lat1, lon1 = -23.520179, -46.630318 # north
    lat2, lon2 = -23.626811, -46.641013 # south
    assert graph.haversine(lon1, lat1, lon2, lat2) == approx(12600, 200)

    # Paris
    lat1, lon1 = 48.856261, 2.325350 # north
    lat2, lon2 = 48.834000, 2.332598 #south
    assert graph.haversine(lon1, lat1, lon2, lat2) == approx(2600, 100)

##########################################################
def test_add_lengths():
    # singularity
    g = igraph.Graph(0)
    g = graph.add_lengths(g) # no error should happen

    # Using above values
    g = igraph.Graph(4)
    g.add_edges([[0, 1], [2, 3]])
    g.vs['x'] = [-73.995599, -73.996594, -46.630318, -46.641013]
    g.vs['y'] = [40.730723, 40.729575, -23.520179, -23.626811]
    g = graph.add_lengths(g)
    assert g.es[0]['length'] == approx(152, 3)
    assert g.es[1]['length'] == approx(12600, 200)

##########################################################
def test_get_larget_component_from_file(tmp_path):
    tmpdir = tmp_path.as_posix()
    g1path = os.path.join(tmpdir, 'g1.graphml')
    g1 = igraph.Graph(4, directed=True)
    g1.add_edges([[0, 0], [0, 1], [2, 3], [2, 3],])
    g1.vs['x'] = [-73.995599, -73.996594, -46.630318, -46.641013]
    g1.vs['y'] = [40.730723, 40.729575, -23.520179, -23.626811]
    g1.write(g1path)

    g2 = graph.get_largest_component_from_file(g1path, undirect=False, simplify=False)
    assert g2.is_directed() == True

    g2 = graph.get_largest_component_from_file(g1path, undirect=True, simplify=False)
    assert g2.is_directed() == False
    assert g2.is_simple() == False

    g2 = graph.get_largest_component_from_file(g1path, undirect=False, simplify=True)
    assert g2.is_simple() == True
    assert g2.es[0]['length'] == approx(152, 3)
