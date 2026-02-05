class HTMLNode:
    def __init__(self,tag = None,value = None,children = None,props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("Not implemented yet.")
    def props_to_html(self):
        sol = ''
        if self.props is not None:
            for key in self.props.keys():
                sol += f'" {key}":"{self.props[key]}"'
        return sol
    def __repr__(self):
        return f"Tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props}"
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        else:
            return (self.tag == other.tag and 
                       self.value == other.value and
                        self.children == other.children and
                        self.props == other.props)
    
    