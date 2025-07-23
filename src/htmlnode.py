
#from textnode import TextNode , TextType
import html

class HtmlNode():

    def __init__(self, tag=None, value=None, children=None, props=None, close_tag=True ):
        self.tag =tag
        self.value= value
        self.children = children
        self.props = props
        self.close_tag = close_tag
    
    def __repr__(self):
        if self.tag is None:
            return f"HtmlNode_#Text#({self.value})"
        html_tag = self.tag
        if self.value is not None: 
            return f"HtmlNode_{html_tag}({self.value=})({self.props=})"
        return f"HtmlNode_{html_tag}({self.children=})({self.props=})"
    
    def to_html(self):
        raise NotImplementedError("can not convert node to html yet")
    def props_to_html(self):
        if self.props is None: return ""
        prop_arr = []
        for prop_name, prop_val in self.props.items():
            prop_esc = html.escape(prop_val)
            prop_arr.append(f'{prop_name}="{prop_esc}"')
        return ' '.join(prop_arr)


class LeafNode(HtmlNode):
    def __init__(self, tag=None, value="", props=None, close_tag=True ):
        super().__init__( tag, value, None, props, close_tag)
    def to_html(self):
        if self.value is None: raise ValueError("LeafNode must have a value")
        if self.children is not None: raise ValueError("LeafNode must NOT have children")
        esc_val = html.escape(self.value)
        if self.tag is None: return html.escape(esc_val)
        html_tag = self.tag
        if self.close_tag:
            if self.props is None:
                return f"<{html_tag}>{esc_val}</{html_tag}>"
            props_snip = self.props_to_html()
            return f"<{self.tag} {props_snip}>{esc_val}</{self.tag}>"
        if self.props is None:
            return f"<{html_tag}>"
        props_snip = self.props_to_html()
        return f"<{self.tag} {props_snip}>"
        

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None ):
        super().__init__( tag, None, children, props, True)
    def to_html(self):
        if self.tag is None: raise ValueError("ParentNode must have a tag")
        if self.value is not None: raise ValueError("ParentNode must NOT have a value")
        if self.children is None: raise ValueError("ParentNode must have children")
        child_arr = []
        for chld in self.children:
            child_arr.append( chld.to_html() )
        html_tag = self.tag
        if self.props is None:
            return f"<{html_tag}>{''.join(child_arr)}</{html_tag}>"
        props_snip = self.props_to_html()
        return f"<{html_tag} {[props_snip]}>{''.join(child_arr)}</{html_tag}>"



