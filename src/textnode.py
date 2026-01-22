from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
	TEXT = None
	BOLD =  "b"
	ITALIC = "i"
	CODE = "code"
	LINK = "a"
	IMAGE = "img"
	STRIKETHROUGH = "s"
	SUPERSCRIPT = "sup"
	SUBSCRIPT = "sub"

	@property
	def label(self):
		# pretty display name
		return self.name.lower() if self is not TextType.TEXT else "text"

#Middleman in the conversion from Blocks to HTMLNodes
#Records the text and text type of a particular portion of text, and url for images and links
class TextNode:
	def __init__(self, text, text_type, url = None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		return self.text == other.text and self.text_type == other.text_type and self.url == other.url

	def __repr__(self):
		return f'TextNode("{self.text}",{self.text_type.label},{self.url})'

def text_node_to_html_node(text_node):
	if text_node.text_type not in set(TextType):
		raise ValueError(f"Invalid TextType: {text_node.text_type!r}")
	elif text_node.text_type == TextType.TEXT:
		return LeafNode(None, text_node.text)
	elif text_node.text_type == TextType.IMAGE:
		props = {"src": text_node.url, "alt": text_node.text}
		return LeafNode("img", "", props)
	
	props = None
	if text_node.text_type == TextType.LINK:
		props = {"href": text_node.url}
	tag = text_node.text_type.value
	return LeafNode(tag, text_node.text, props)

#splits old nodes based on an inputted delimiter
#input: list of textnodes, a markdown delimiter, and the texttype of each delimiter
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        node_text_type = node.text_type
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise SyntaxError("Invalid Markdown Syntax; either an extra delimiter was added or one is missing")
        use_node_text_type = True
        for text in split_text:
            #this line will be revamped to support bold + italic etc. later
            current_text_type = node_text_type if use_node_text_type else text_type
            use_node_text_type = not use_node_text_type
            if text != "":
                new_nodes.append(TextNode(text, current_text_type))
    return new_nodes

#detects markdown image syntax in text
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

#detects markdown link syntax in text
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

#splits a list nodes with undetected images into a list of nodes takes account of the image
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type in [TextType.IMAGE, TextType.LINK]:
            new_nodes.append(node)
            continue
        split_text = re.split(r"(!\[[^\[\]]*\]\([^\(\)]*\))", node.text)
        image_data = extract_markdown_images(node.text)
        for i in range(0, len(split_text)):
            if split_text[i] != "":
                if i%2 == 0:
                    new_nodes.append(TextNode(split_text[i], node.text_type))
                else:
                    new_nodes.append(TextNode(image_data[(i-1)//2][0], TextType.IMAGE, image_data[(i-1)//2][1]))
    return new_nodes

#splits a list nodes with undetected links into a list of nodes takes account of the links
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type in [TextType.IMAGE, TextType.LINK]:
            new_nodes.append(node)
            continue
        split_text = re.split(r"((?<!!)\[[^\[\]]*\]\([^\(\)]*\))", node.text)
        link_data = extract_markdown_links(node.text)
        for i in range(0, len(split_text)):
            if split_text[i] != "":
                if i%2 == 0:
                    new_nodes.append(TextNode(split_text[i], node.text_type))
                else:
                    new_nodes.append(TextNode(link_data[(i-1)//2][0], TextType.LINK, link_data[(i-1)//2][1]))
    return new_nodes

def text_to_textnodes(text): #Note: does not support nested delimiters yet!
    nodes = [TextNode(text, TextType.TEXT)] #The whole text is set under a textnode but we split those below
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC) #We want to support both italic syntaxes
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "~~", TextType.STRIKETHROUGH)
    nodes = split_nodes_delimiter(nodes, "^", TextType.SUPERSCRIPT)
    nodes = split_nodes_delimiter(nodes, "~", TextType.SUBSCRIPT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes