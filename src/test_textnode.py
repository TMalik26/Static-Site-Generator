import unittest
from textnode import TextNode, TextType, BlockType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, text_to_children, markdown_to_html_node, extract_title
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_content(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_without_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://example1.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example1.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://exampl2.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node") 

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example1.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {'href': "https://example1.com"})

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://example1.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example1.com", "alt": "This is a text node"})

    def test_unknown_type(self):
        node = TextNode("This is a text node", "Unknown_type", "https://example1.com")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_split_nodes_delimiter_bold_1(self):
        old_nodes = [
            TextNode("This is a text", TextType.BOLD),
            TextNode("This is a **text**", TextType.TEXT),
            TextNode("This is a text", TextType.ITALIC)
        ]
        delimiter = "**"
        text_type = TextType.BOLD
        lst = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(lst, [
            TextNode("This is a text", TextType.BOLD),
            TextNode("This is a ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode("This is a text", TextType.ITALIC)
        ])

    def test_split_nodes_delimiter_bold_2(self):
        old_nodes = [
            TextNode("This is a text", TextType.BOLD),
            TextNode("This is **bold** and **fat**", TextType.TEXT),
            TextNode("This is a text", TextType.ITALIC)
        ]
        delimiter = "**"
        text_type = TextType.BOLD
        lst = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(lst, [
            TextNode("This is a text", TextType.BOLD),
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("fat", TextType.BOLD),
            TextNode("This is a text", TextType.ITALIC)
        ])

    def test_split_nodes_delimiter_exception(self):
        old_nodes = [
            TextNode("This is a text", TextType.BOLD),
            TextNode("This is **bold text", TextType.TEXT),
            TextNode("This is a text", TextType.ITALIC)
        ]
        delimiter = "**"
        text_type = TextType.BOLD
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, delimiter, text_type)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://example.com/1.png)"
        )
        self.assertListEqual([("image", "https://example.com/1.png")], matches)

    def test_extract_markdown_images_several(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](https://example.com/1.png) and an ![image2](https://example.com/2.png)"
        )
        self.assertListEqual([("image1", "https://example.com/1.png"), ("image2", "https://example.com/2.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [site](https://example1.com)"
            )
        self.assertListEqual([("site", "https://example1.com")], matches)
    
    def test_extract_markdown_links_several(self):
        matches = extract_markdown_links(
            "This is text with a link [site](https://example1.com) and [site2](https://example2.com)"
            )
        self.assertListEqual([("site", "https://example1.com"), ("site2", "https://example2.com")], matches)

    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image1](https://example.com/1.png) and another ![image2](https://example.com/2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://example.com/1.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "image2", TextType.IMAGE, "https://example.com/2.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with an [link1](https://example1.com) and another [link2](https://example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://example1.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link2", TextType.LINK, "https://example2.com"
                ),
            ],
            new_nodes,
        ) 

    def test_split_nodes_image_1(self):
        node = TextNode(
            "This is text with an ![image1](https://example.com/1.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://example.com/1.png")
            ],
            new_nodes,
        )

    def test_split_nodes_link_1(self):
        node = TextNode(
            "This is text with an [link1](https://example1.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://example1.com")
            ],
            new_nodes,
        )

    def test_split_nodes_image_first(self):
        node = TextNode(
            "![image1](https://example.com/1.png) and then text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://example.com/1.png"),
                TextNode(" and then text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_nodes_link_first(self):
        node = TextNode(
            "[link1](https://example1.com) and then text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://example1.com"),
                TextNode(" and then text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_nodes_image_only(self):
        node = TextNode(
            "image1", TextType.IMAGE, "https://example.com/1.png"
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image1", TextType.IMAGE, "https://example.com/1.png")],
            new_nodes,
        )

    def test_split_nodes_link_only(self):
        node = TextNode(
            "link1", TextType.LINK, "https://example1.com"
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link1", TextType.LINK, "https://example1.com")],
            new_nodes,
        )

    def test_split_nodes_image_text_only(self):
        node = TextNode(
            "Only text", TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("Only text", TextType.TEXT)],
            new_nodes,
        )

    def test_split_nodes_link_text_only(self):
        node = TextNode(
            "Only text", TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("Only text", TextType.TEXT)],
            new_nodes,
        )

    def test_split_nodes_image_without_links(self):
        node = TextNode(
            "Only code", TextType.CODE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("Only code", TextType.CODE)],
            new_nodes,
        )

    def test_split_nodes_link_without_links(self):
        node = TextNode(
            "Only code", TextType.CODE,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("Only code", TextType.CODE)],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://example.com/1.png) and a [link](https://example1.com)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/1.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example1.com"),
            ],
            nodes,
        )
        
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        expected = []
        result = markdown_to_blocks(md)
        self.assertListEqual(result, expected)

    def test_markdown_to_blocks_extra_whitespace(self):
        md = "    \n\nThis is a first block\n\n\n\n\n\n\n    Second block         \n\n  "
        expected = ["This is a first block", "Second block"]
        result = markdown_to_blocks(md)
        self.assertListEqual(result, expected)

    def test_markdown_to_blocks_sigle_block(self):
        md = "This is a single block"
        expected = ["This is a single block"]
        result = markdown_to_blocks(md)
        self.assertListEqual(result, expected)

    def test_markdown_to_blocks_multiple_empty_lines(self):
        md = "Block 1\n\n\n\n\nBlock 2\n\nBlock 3   \n\n\n"
        expected = ["Block 1", "Block 2", "Block 3"]
        result = markdown_to_blocks(md)
        self.assertListEqual(result, expected)

    def test_markdown_to_blocks_only_whitespace(self):
        markdown = "   \n\n   \n\n   "
        expected = []
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_mixed_content(self):
        markdown = "# Header\n\n* List item 1\n* List item 2\n\n```\ncode block\n```"
        expected = ["# Header", "* List item 1\n* List item 2", "```\ncode block\n```"]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_block_to_block_type_heading(self):
        markdown_block = "###### Heading"
        result = block_to_block_type(markdown_block)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_heading_1(self):
        markdown_block = "######Heading"
        result = block_to_block_type(markdown_block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        markdown_block = "```\ncode here\n```"
        result = block_to_block_type(markdown_block)
        self.assertEqual(result, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        markdown_block = "> This is a quote\n> Second line"
        result = block_to_block_type(markdown_block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        markdown_block = "- Item 1\n- Item 2"
        result = block_to_block_type(markdown_block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        markdown_block = "1. Item 1\n2. Item 2"
        result = block_to_block_type(markdown_block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        markdown_block = "Just regular text"
        result = block_to_block_type(markdown_block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

def test_extract_title(self):
    markdown = "# This is a header h1.\nThis is not a header."
    result = extract_title(markdown)
    expected = "This is a header h1."
    self.assertEqual(result, expected)

def test_extract_title_further_in_text(self):
    markdown = "This is not a header.\n## This is a header h2.\n# This is a header h1."
    result = extract_title(markdown)
    expected = "This is a header h1."
    self.assertEqual(result, expected)

def test_extract_title_extra_whitespaces(self):
    markdown = "#   This is a header h1.   "
    result = extract_title(markdown)
    expected = "This is a header h1."
    self.assertEqual(result, expected)

def test_extract_title_whithout_title(self):
    markdown = "This is not a header.\n## This is a header h2.\n### This is a header h3."
    with self.assertRaises(Exception):
        extract_title(markdown)

def test_extract_title_empty_string(self):
    markdown = ""
    with self.assertRaises(Exception):
        extract_title(markdown)

if __name__ == "__main__":
    unittest.main()