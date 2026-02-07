from enum import Enum
from htmlnode import LeafNode
import re
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
class TextNode:
    def __init__(self,text,text_type,url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        return (self.text == other.text 
                and self.text_type == other.text_type
                     and self.url == other.url)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
def text_node_to_html_node(text_node):
    #We want to convert a TextNode into a LeafNode
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode('b',text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code',text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text,{'href':text_node.url})
        case TextType.IMAGE:
            return LeafNode('img','',{'src':text_node.url,'alt':text_node.text})
        case _:
            raise ValueError('Invalid TextType')
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections)%2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        
        for i in range(len(sections)):
            if sections[i] == '':
                continue
            if i%2 == 0:
                split_nodes.append(TextNode(sections[i],TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i],text_type))
        result.extend(split_nodes)
    return result
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
'''
def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if matches == []:
            result.append(node)
            continue
        split_nodes = []
        sections = []
        pivot = node.text
        for image_alt,image_link in matches:
            pivot = pivot.split(f"![{image_alt}]({image_link})")
            sections.append(pivot[0])
            pivot = pivot[1]
        sections.append(pivot)
        print(sections)
        print(matches[0],matches[0][0])
        j = 0
        for i in range(len(sections)):
            if sections[i] != '':
                split_nodes.append(TextNode(sections[i],TextType.TEXT))
            if j < len(matches):
                split_nodes.append(TextNode(matches[j][0],TextType.IMAGE, matches[j][1]))
                j+=1
        result.extend(split_nodes)
    return result
def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if matches == []:
            result.append(node)
            continue
        split_nodes = []
        sections = []
        pivot = node.text
        for image_alt,image_link in matches:
            pivot = pivot.split(f"[{image_alt}]({image_link})")
            sections.append(pivot[0])
            pivot = pivot[1]
        sections.append(pivot)
        print(sections)
        print(matches[0],matches[0][0])
        j = 0
        for i in range(len(sections)):
            if sections[i] != '':
                split_nodes.append(TextNode(sections[i],TextType.TEXT))
            if j < len(matches):
                split_nodes.append(TextNode(matches[j][0],TextType.LINK, matches[j][1]))
                j+=1
        result.extend(split_nodes)
    return result
'''