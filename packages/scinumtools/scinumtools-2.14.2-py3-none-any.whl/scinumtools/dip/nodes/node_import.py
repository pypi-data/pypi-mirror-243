from .node_base import BaseNode
from ..environment import Environment
from ..settings import Sign

class ImportNode(BaseNode):
    keyword: str = 'import'
    names: list = None     # names of imported nodes

    def is_node(parser):
        parser.part_reference()
        if parser.is_parsed('part_reference'):
            parser.part_comment()
            return ImportNode(parser)
    
    def inject_value(self, env:Environment, node=None):
        pass
    
    def parse(self, env):
        # Parse import code
        nodes_new = []
        for node in env.request(self.value_ref):
            path = self.name.split(Sign.SEPARATOR + '{')
            path.pop()
            path.append(node.name)     
            node.name = Sign.SEPARATOR.join(path)
            node.indent = self.indent
            nodes_new.append(node)
        return nodes_new
