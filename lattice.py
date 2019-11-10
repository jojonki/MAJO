class Lattice(object):
    def __init__(self, sent=None):
        self.clear()
        if sent:
            self.setSentence(sent)

    def _newNode(self, begin, end, _surface_str=None):
        return {
            'surface': begin,
            'length': end - begin,
            '_surface': _surface_str
        }

    def setSentence(self, sent):
        self._sent = sent
        # +1 for BOS or EOS ndoe
        self._begin_nodes = [[] for _ in range(len(sent) + 1)]
        self._end_nodes = [[] for _ in range(len(sent) + 1)]

        bos_node = self._newNode(0, 0, '__BOS__')
        self._end_nodes[0].append(bos_node)
        eos_node = self._newNode(len(sent), 0, '__EOS__')
        self._begin_nodes[len(sent)].append(eos_node)

    def insert(self, begin, end, _surface_str=None):
        node = self._newNode(begin, end, _surface_str)
        self._begin_nodes[begin].append(node)
        self._end_nodes[end].append(node)
        return node

    def clear(self):
        self._sent = None
        self._begin_nodes = []
        self._end_nodes = []
        self._all_nodes = []

    def pprint(self):
        for i in range(len(self._sent) + 1):
            print([n['_surface'] for n in self._end_nodes[i]], end='')
            print(' ({}) '.format(i), end='')
            print([n['_surface'] for n in self._begin_nodes[i]])

    def plot(self):
        from graphviz import Digraph
        g = Digraph(format='png')
        g.attr('node', shape='circle')
        added_nodes = []
        for i in range(len(self._sent) + 1):
            for ct, n in enumerate(self._end_nodes[i]):
                if n['_surface'] not in added_nodes:
                    g.node(n['_surface'], n['_surface'])
                    added_nodes.append(n['_surface'])
            for ct, n in enumerate(self._begin_nodes[i]):
                if n['_surface'] not in added_nodes:
                    g.node(n['_surface'], n['_surface'])
                    added_nodes.append(n['_surface'])

            for en in self._end_nodes[i]:
                for bn in self._begin_nodes[i]:
                    g.edge(en['_surface'], bn['_surface'])

        print('Save this lattice image as png')
        g.render('lattice')
