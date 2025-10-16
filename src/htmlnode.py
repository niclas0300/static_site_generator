class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        strings = []
        for key in self.props:
            strings.append(f' {key.strip("")}="{str(self.props[key])}"') 
        return "".join(strings)
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        
        if self.value == None:
            raise ValueError("A value is needed")
        elif self.tag == None:
            return self.value
        elif self.tag != "a" and self.tag != "img":
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            html_props = self.props_to_html()
            if len(html_props) != 0 and self.tag == "a":
                return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"
            elif len(html_props) != 0 and self.tag == "img":
                return f"<{self.tag}{html_props} />"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

                
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag")
        if self.children is None:
            raise ValueError("Child node is needed")
        
        html_string = ""
        for i in range(len(self.children)):
            child = self.children[i]
            html_string += child.to_html()
        
        return f"<{self.tag}>{html_string}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
            


