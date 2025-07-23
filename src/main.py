from textnode import TextNode , TextType

def main():
    #tn = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    tn = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(tn)

main()

