import graphviz


def create_example_diagram():
    dot = graphviz.Digraph(comment='Example Process')

    dot.attr(bgcolor='black')
    dot.attr('node', style='filled', fillcolor='black', fontcolor='white')
    dot.attr('edge', color='white', fontcolor='white')

    dot.node('A1', 'Image 1: BB1 (10,10,50,50)')
    dot.node('A2', 'Image 1: BB2 (60,60,100,100)')
    dot.node('B1', 'Image 2: BB1 (12,12,52,52)')
    dot.node('B2', 'Image 2: BB2 (58,58,98,98)')
    dot.node('B3', 'Image 2: BB3 (150,150,200,200)')

    dot.node('G1', 'Factor Graph for Image 1')
    dot.node('G2', 'Factor Graph for Image 2')
    dot.node('C', 'Histogram Comparison')
    dot.node('D', 'Graph Calibration and Belief Propagation')
    dot.node('E', 'Results: BB1->BB1, BB2->BB2, BB3->-1 (new)')

    dot.edge('A1', 'G1')
    dot.edge('A2', 'G1')
    dot.edge('B1', 'G2')
    dot.edge('B2', 'G2')
    dot.edge('B3', 'G2')

    dot.edge('G1', 'C', label='Histogram Comparison')
    dot.edge('G2', 'C')
    dot.edge('C', 'D', label='Graph Calibration and Belief Propagation')
    dot.edge('D', 'E', label='Results')

    return dot

diagram = create_example_diagram()
diagram.render('example_process_diagram', format='png', view=True)
