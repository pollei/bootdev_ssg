from textnode import TextNode , TextType

import publish

def main():
    publish.clean_public()
    publish.publish_static()
    #publish.generate_page("content/index.md", "template.html", "public/index.html")
    publish.generate_pages_recursive()
    #tn = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    #tn = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(tn)

main()

