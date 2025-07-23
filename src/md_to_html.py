
from htmlnode import HtmlNode, LeafNode, ParentNode
from textnode import TextNode, TextType

import re 
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {
                "src": text_node.url, "alt":text_node.text }, close_tag=False )
        case _:
            raise Exception("unknown text node type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ret_nodes = []
    for o_nod in old_nodes:
        if o_nod.text_type != TextType.PLAIN or len(o_nod.text) < 3:
            ret_nodes.append(o_nod)
            continue
        spliters =  o_nod.text.split(delimiter)
        #print(f"{spliters=}")
        if len(spliters) < 2:
            ret_nodes.append(o_nod)
            continue
        for spliters_indx in range(len(spliters)):
            if len(spliters[spliters_indx]) > 0:
                new_tn = TextNode(spliters[spliters_indx],
                    TextType.PLAIN if spliters_indx % 2 == 0 else text_type)
                ret_nodes.append(new_tn)
    return ret_nodes

def line_to_textnodes(str):
    ret_nodes = [ TextNode(str) ]
    ret_nodes = split_nodes_delimiter(ret_nodes, "**", TextType.BOLD)
    ret_nodes = split_nodes_delimiter(ret_nodes, "_", TextType.ITALIC)
    #print(f" after bold and ital {ret_nodes=}")
    ret_nodes = split_nodes_delimiter(ret_nodes, "`", TextType.CODE)
    #print(f" after bold and ital and code {ret_nodes=}")
    return ret_nodes

def extract_markdown_images(text):
    rege = re.compile(
        r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" )
    return rege.findall(text)
def extract_markdown_links(text):
    rege = re.compile(
       r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" )
    return rege.findall(text)

split_text_pat = re.compile(
    r"^((?:[^*_`\[\\!]|\\.|\*(?>[^*])|!(?>[^\[]))+)((?:[*_`\[!]|!\[|\*\*]).*)$")
split_bold_pat = re.compile(
    r"^\*\*((?:[^*]|\*(?>[^*]))*)\*\*(.*)$")
split_italic_pat = re.compile(
    r"^_([^_]*)_(.*)$")
split_code_pat = re.compile(
    r"^`([^`]*)`(.*)$")
split_image_pat = re.compile(
    r"^!\[([^\[\]]*)\]\(([^\(\)]*)\)(.*)$")
split_link_pat = re.compile(
    r"^\[([^\[\]]*)\]\(([^\(\)]*)\)(.*)$")
def text_to_textnodes(text):
    ret_nodes = []
    todo_text = text
    while  len(todo_text) > 0:
        mtch = split_text_pat.match(todo_text)
        if mtch:
            ret_nodes.append(TextNode(mtch.group(1)))
            todo_text = mtch.group(2)
            continue
        mtch = split_bold_pat.match(todo_text)
        if mtch:
            ret_nodes.append(TextNode(mtch.group(1), TextType.BOLD))
            todo_text = mtch.group(2)
            continue
        mtch = split_italic_pat.match(todo_text)
        if mtch:
            ret_nodes.append(TextNode(mtch.group(1), TextType.ITALIC))
            todo_text = mtch.group(2)
            continue
        mtch = split_code_pat.match(todo_text)
        if mtch:
            ret_nodes.append(TextNode(mtch.group(1), TextType.CODE))
            todo_text = mtch.group(2)
            continue
        mtch = split_link_pat.match(todo_text)
        if mtch:
            ret_nodes.append(TextNode(mtch.group(1), TextType.LINK, mtch.group(2) ))
            todo_text = mtch.group(3)
            continue
        mtch = split_image_pat.match(todo_text)
        if mtch:
            ret_nodes.append(TextNode(mtch.group(1), TextType.IMAGE, mtch.group(2) ))
            todo_text = mtch.group(3)
            continue
        ret_nodes.append(TextNode(todo_text))
        todo_text = ""
    return ret_nodes

def md_text_to_html_nodes(text):
    #tex_nods = []
    #for line in text.splitlines(): tex_nods.extend( text_to_textnodes(line))
    tex_nods = text_to_textnodes(text)
    return list(map(text_node_to_html_node, tex_nods))

def markdown_to_blocks(markdown):
    raw_sects = markdown.split("\n\n")
    ret_sects = []
    for sect in raw_sects:
        sect = sect.strip()
        if len(sect): ret_sects.append(sect)
    return ret_sects


def check_ordered_block(test):
    n = 1
    for line in text.splitlines():
        if not line.startswith(f"{n}. "): return False
        n+=1
    return True
def each_line_starts(text, prefix):
    for line in text.splitlines():
        if not line.startswith(prefix): return False
    return True

sniff_head_pat = re.compile(  r"^#{1,6} \S")
def block_to_block_type(text):
    if sniff_head_pat.match(text): return BlockType.HEADING
    if text.startswith("```") and text.endswith("```"): return BlockType.CODE
    if text.startswith(">"):
        return (BlockType.QUOTE if each_line_starts(text, '>') else BlockType.PARAGRAPH)
    if text.startswith("- "):
        #print("sniff a unorderdd mess")
        return (BlockType.UNORDERED_LIST if each_line_starts(text, '- ') else BlockType.PARAGRAPH)
        """  if each_line_starts(text, '- '):
            #print("returning  a unorderdd mess")
            return BlockType.UNORDERED_LIST
         #print("sniff a unorderdd mess  .... what")
         return BlockType.PARAGRAPH
         #return (BlockType.UNORDERED_LIST if each_line_starts(text, '- ') else BlockType.PARAGRAPH) """
    if text.startswith("1. "):
        return BlockType.ORDERED_LIST
    print("block_to_block_type default")
    return BlockType.PARAGRAPH

""" def paragraph_block_to_html_nodes(text):
    childs = []
    for line in text.splitlines():
        line_nodes = md_text_to_html_nodes(line)
        line_html = ParentNode("p", line_nodes)
        childs.append(line_html)
    return childs """

def special_block_to_html_node(text, line_split_pat, container_tag, sub_tag =None, keepends=False):
    childs = []
    for line in text.splitlines(keepends):
        mtch = line_split_pat.match(line)
        line_nodes = md_text_to_html_nodes(mtch.group(2))
        if sub_tag is not None:
            line_html = ParentNode(sub_tag, line_nodes)
            childs.append(line_html)
        else:
            childs.extend(line_nodes)
    top_container = ParentNode(container_tag, childs)
    return top_container

split_head_pat = re.compile(  r"^(#{1,6})\s+(.*)$")
line_split_pat = re.compile(  r"^(>|-\s|\d+\.\s)(.*)$", re.S) # re.M|re.S
def markdown_to_html_node(markdown):
    blks = markdown_to_blocks(markdown)
    top_div_childs = []
    md_block_props = { "class": "md_block"}
    for blck in blks:
        block_type= block_to_block_type(blck)
        match block_type:
            case BlockType.PARAGRAPH:
                smashed_txt = ' '.join(blck.splitlines())
                blck_nod = ParentNode("p", md_text_to_html_nodes(smashed_txt) )
                top_div_childs.append(blck_nod)
                #top_div_childs.extend(paragraph_block_to_html_nodes(blck))
                continue
            case BlockType.HEADING:
                mtch = split_head_pat(blck)
                h_lvl = len(mtch.group(1))
                blck_nod = ParentNode(f"h{h_lvl}", md_text_to_html_nodes(blck))
                top_div_childs.append(blck_nod)
                continue
            case BlockType.CODE:
                txt_nod = LeafNode(None, blck[4:-3])
                code_nod = ParentNode("code",  [txt_nod] )
                blck_nod = ParentNode("pre",  [code_nod] )
                top_div_childs.append(blck_nod)
                continue
            case BlockType.QUOTE:
                blck_nod = special_block_to_html_node(blck, line_split_pat, 'blockquote', keepends = True)
                top_div_childs.append(blck_nod)
                continue
            case BlockType.UNORDERED_LIST:
                blck_nod = special_block_to_html_node(blck, line_split_pat, 'ul', 'li')
                top_div_childs.append(blck_nod)
                continue
            case BlockType.ORDERED_LIST:
                blck_nod = special_block_to_html_node(blck, line_split_pat, 'ol', 'li')
                top_div_childs.append(blck_nod)
                continue
            case _:
                raise Exception("unknown text node type")
    top_div = ParentNode("div", top_div_childs)
    return top_div