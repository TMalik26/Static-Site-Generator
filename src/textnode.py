from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
import re
import textwrap
import os
import shutil

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

        
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text                # The text content of the node
        self.text_type = text_type      # The type of text this node contains, which is a member of the TextType enum.
        self.url = url                  # The URL of the link or image, if the text is a link. Default to None if nothing is passed in.

    def __eq__(self, obj):
        return (
            isinstance(obj, TextNode) and
            self.text == obj.text and 
            self.text_type == obj.text_type and 
            self.url == obj.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    valid_types = [TextType.TEXT, TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.LINK, TextType.IMAGE]
    if text_node.text_type not in valid_types:
        raise Exception("Unknown text type")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text, None)
    if text_node.text_type == TextType.BOLD:
        return LeafNode('b', text_node.text, None)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode('i', text_node.text, None)
    if text_node.text_type == TextType.CODE:
        return LeafNode('code', text_node.text, None)
    if text_node.text_type == TextType.LINK:
        return LeafNode('a', text_node.text, {'href': text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            total = node.text.count(delimiter)
            if total % 2 != 0:
                raise Exception('closing delimiter missing')
            parts = node.text.split(delimiter)
            for idx, part in enumerate(parts):
                if not part:
                    continue
                if idx % 2 == 0:
                    result.append(TextNode(part, TextType.TEXT))
                else:
                    result.append(TextNode(part, text_type))
        else:
            result.append(node)
    return result

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            current_text_to_process = node.text
            while len(extract_markdown_images(current_text_to_process)) > 0:
                images = extract_markdown_images(current_text_to_process)
                image_first = images[0]
                full_markdown_image = f"![{image_first[0]}]({image_first[1]})"
                texts = current_text_to_process.split(full_markdown_image, 1)
                text_before_image = texts[0]
                if text_before_image:
                    result.append(TextNode(text_before_image, TextType.TEXT))
                result.append(TextNode(image_first[0], TextType.IMAGE, image_first[1]))
                current_text_to_process = texts[1]
            if current_text_to_process:
                result.append(TextNode(current_text_to_process, TextType.TEXT))
        else:
            result.append(node)
    return result                       
        
def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            current_text_to_process = node.text
            while len(extract_markdown_links(current_text_to_process)) > 0:
                links = extract_markdown_links(current_text_to_process)
                link_first = links[0]
                full_markdown_link = f"[{link_first[0]}]({link_first[1]})"
                texts = current_text_to_process.split(full_markdown_link, 1)
                text_before_link = texts[0]
                if text_before_link:
                    result.append(TextNode(text_before_link, TextType.TEXT))
                result.append(TextNode(link_first[0], TextType.LINK, link_first[1]))
                current_text_to_process = texts[1]
            if current_text_to_process:
                result.append(TextNode(current_text_to_process, TextType.TEXT))
        else:
            result.append(node)
    return result

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
             cleaned_blocks.append(stripped_block)
    return cleaned_blocks 

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block):
    if markdown_block.startswith("#"):
        count = 0
        for char in markdown_block:
            if char == "#":
                count += 1
            else:
                break
        if 1 <= count <= 6 and markdown_block[count] == " ":
            return BlockType.HEADING
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    lines = markdown_block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            heading_line = block.strip().split('\n')[0]
            i = 0
            while i < len(heading_line) and heading_line[i] == "#":
                i += 1
            if 1 <= i <= 6:
                tag = f"h{i}" 
            else:
                tag = "h6"
            value = heading_line[i:].strip()
            children = text_to_children(value)
            parent_node = ParentNode(tag, children)
            block_nodes.append(parent_node)

        if block_type == BlockType.QUOTE:
            tag = "blockquote"
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                if line.startswith(">"):
                    new_line = line[1:].strip()
                else:
                    new_line = line.strip()
                if new_line:
                    new_lines.append(new_line)
            value = " ".join(new_lines)
            children = text_to_children(value)
            parent_node = ParentNode(tag, children)
            block_nodes.append(parent_node)

        if block_type == BlockType.PARAGRAPH:
            tag = "p"
            lines = block.strip().splitlines()
            clean_lines = []
            for line in lines:
                clean_line = line.strip()
                if clean_line:
                    clean_lines.append(clean_line)
            value = " ".join(clean_lines)
            children = text_to_children(value)
            parent_node = ParentNode(tag, children)
            block_nodes.append(parent_node)

        if block_type == BlockType.CODE:
            tag = "code"
            clean_block = block.strip().removeprefix("```").removesuffix("```").strip("\n")
            value = textwrap.dedent(clean_block)
            text_node = TextNode(value, TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            parent_node = ParentNode("pre", [html_node])
            block_nodes.append(parent_node)

        if block_type == BlockType.UNORDERED_LIST:
            tag = "ul"
            list_items_html_nodes = []
            lines = block.strip().splitlines()
            for line in lines:
                line = line.lstrip()
                if line.startswith("-") or line.startswith("*"):
                    value = line[1:].lstrip()
                else:
                    value = line
                children = text_to_children(value)
                html_node = ParentNode("li", children)
                list_items_html_nodes.append(html_node)
            parent_node = ParentNode(tag, list_items_html_nodes)
            block_nodes.append(parent_node)

        elif block_type == BlockType.ORDERED_LIST:
            tag = "ol"
            list_items_html_nodes = []
            lines = block.strip().splitlines()
            for line in lines:
                line = line.lstrip()
                idx = line.find('.')
                if idx != -1:
                    value = line[idx + 1:].lstrip()
                else:
                    value = line
                children_li = text_to_children(value)
                html_node = ParentNode("li", children_li)
                list_items_html_nodes.append(html_node)
            parent_node = ParentNode(tag, list_items_html_nodes)
            block_nodes.append(parent_node)
    html = ParentNode("div", block_nodes)
    return html


    
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes


def copy_static(source_dir: str, destination_dir: str):
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.makedirs(destination_dir)
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("H1 header doesn't exsist in this file")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    html_page = template_content.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", html_content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(html_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    def recurse(current_path, current_dest_path):
        for entry in os.listdir(current_path):
            full_path = os.path.join(current_path, entry)
            dst_path = os.path.join(current_dest_path, entry.replace('.md', '.html') if entry.endswith('.md') else entry)
            if os.path.isfile(full_path):
                if entry.endswith('.md'):
                    os.makedirs(current_dest_path, exist_ok=True)
                    generate_page(full_path, template_path, dst_path)
                
            else:
                os.makedirs(dst_path, exist_ok=True)
                recurse(full_path, dst_path)

    recurse(dir_path_content, dest_dir_path)