from textnode import TextNode, TextType


def main():
    text_type = TextType.LINK
    node = TextNode("this is some text", text_type, "https://www.boot.dev")
    print(repr(node))

main()