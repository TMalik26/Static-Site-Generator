class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("it will be later")
    
    def props_to_html(self):
        target = ""
        if self.props is not None:
            for key, value in self.props.items():
                target += ' ' + key + '=\"' + value + '\"'
        return target

    def __repr__(self):
        return f"HTMLNode: tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a non-empty value")
        if self.tag is None:
            return self.value
        if not self.props:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            attrs = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
            return f'<{self.tag} {attrs}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a non-empty tag")
        if not self.children:
            raise ValueError("ParentNode must have a non-empty children")
        else:
            att = ''
            for child in self.children:
                att += child.to_html()
            return f'<{self.tag}>{att}</{self.tag}>'