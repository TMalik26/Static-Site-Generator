from textnode import TextType, TextNode, copy_static, generate_page, generate_pages_recursive

def main():
    copy_static("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    text_node_1 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node_1)


if __name__ == "__main__":
    main()