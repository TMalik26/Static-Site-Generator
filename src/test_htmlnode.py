import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node= HTMLNode("h1", "HELLO", None, {'class': 'text'})
        result = node.props_to_html()
        expected = ' class=\"text\"'      
        self.assertEqual(result, expected)
        
        
    def test_props_to_html_multiple_prop(self):
        node = HTMLNode("p", "Goog morning!", None, {'class': 'text', 'class2': 'text2'})
        result = node.props_to_html()
        expected = ' class=\"text\" class2=\"text2\"'
        self.assertEqual(result, expected)

    def test_props_to_html_None_prop(self):
        node = HTMLNode("a", "Goodbye", None, None)
        result = node.props_to_html()
        expected = ''
        self.assertEqual(result, expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_None_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_empty_value(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_single_prop(self):
        node = LeafNode("p", "Hello, world!", {'class': 'text'})
        self.assertEqual(node.to_html(), '<p class="text">Hello, world!</p>')

    def test_leaf_to_html_multiple_prop(self):
        node = LeafNode("p", "Hello, world!", {'class': 'text', 'class2': 'text2'})
        self.assertEqual(node.to_html(), '<p class="text" class2="text2">Hello, world!</p>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Text")
        self.assertEqual(node.to_html(), "Text")

    def test_to_html_with_string_child(self):
        parent = ParentNode("div", ["Text"])
        with self.assertRaises(AttributeError):
            parent.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    

if __name__ == "__main__":
    unittest.main()