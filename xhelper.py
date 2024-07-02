import re
from lxml import etree

class XpathHelper():
    """
    A class that allows changes and updates on Xpath expressions.
    For index parameters used in methods; each "/" symbol represents an index.
    """
    def __init__(self) -> None:
        pass

    def add_tag(self, xpath:str, tag: str, index:int=-1) -> str:
        xpath_parts = xpath.split('/')
        if index < 0 or index >= len(xpath_parts) - 1:
            index = len(xpath_parts) - 1
            xpath_parts.insert(index, tag)
            print('Warning: The specified index is out of range. The tag was added to the end of the XPath.')
        else:
            xpath_parts.insert(index, tag)
        new_xpath = '/'.join(xpath_parts)
        return new_xpath

    def remove_tag(self, xpath:str, index:int=-1) -> str:
        parts = xpath.split('/')
        if index >= len(parts):
            index = -1
            print("The index is greater than the number of parts. Removing the last part instead.")
        if index < 0:
            index = len(parts) + index
        parts[index] = parts[index][:-1]
        return '/'.join(parts)

    def add_last(self, xpath:str, index:int=-1) -> str:
        parts = xpath.split('/')
        if index >= len(parts):
            index = -1
            print("Warning: Index value exceeds xpath parts. Applying to last part instead.")
        parts[index] = parts[index] + '[last()]'
        return '/'.join(parts)

    def remove_last(self, xpath:str, index:int=-1) -> str:
        parts = xpath.split('/')
        if index >= len(parts):
            index = -1
            print("Warning: Index value exceeds xpath parts. Removing 'last()' from the last part instead.")
        parts[index] = parts[index].replace('[last()]', '')
        return '/'.join(parts)

    def add_position(self, xpath:str, operator:str, value:int, index:int=-1) -> str:
        xpath_parts = xpath.split("/")
        if index < 0:
            index += len(xpath_parts)
        if index < len(xpath_parts):
            last_part = xpath_parts[index]
            if "position()" in last_part:
                last_part = re.sub(r'\[position\(\)[^\]]*\]', '', last_part)
            position_expr = f"[position() {operator} {value}]"
            new_last_part = last_part + position_expr
            xpath_parts[index] = new_last_part
            return "/".join(xpath_parts)
        else:
            print("Warning: The specified index is greater than the maximum index in the given XPath. The attribute was added to the last part.")
            last_part = xpath_parts[-1]
            if "position()" in last_part:
                last_part = re.sub(r'\[position\(\)[^\]]*\]', '', last_part)
            position_expr = f"[position() {operator} {value}]"
            new_last_part = last_part + position_expr
            xpath_parts[-1] = new_last_part
            return "/".join(xpath_parts)

    def remove_position(self, xpath:str, index:int=-1) -> str:
        xpath_parts = xpath.split("/")
        last_part = xpath_parts[-1]
        position_exprs = re.findall(r'\[position\(\)\s*=\s*\d+\]', last_part)
        if len(position_exprs) >= index:
            position_expr = position_exprs[-index]
            new_last_part = re.sub(position_expr, '', last_part)
            xpath_parts[-1] = new_last_part
            new_xpath = "/".join(xpath_parts)
            return new_xpath
        else:
            new_last_part = re.sub(r'\[position\(\)\s*=\s*\d+\]', '', last_part)
            new_xpath = xpath.replace(last_part, new_last_part)
            print(f"Warning: The specified index is greater than the number of position expressions in the given XPath. The last position expression was removed from the XPath.")
            return new_xpath

    def add_text(self, xpath:str, text:str, index:int=-1) -> str:
        parts = xpath.split('/')
        if index >= len(parts):
            print("Index is greater than or equal to the number of parts in the XPath. Appending the text to the last part of the XPath.")
            parts[-1] += f"[text()='{text}']"
        else:
            parts[index] += f"[text()='{text}']"
        return '/'.join(parts)

    def remove_text(self, xpath:str, index:int=-1) -> str:
        xpath_parts = xpath.split('/')
        xpath_parts = [part for part in xpath_parts if part != '']
        num_text_expressions = 0
        for i in range(len(xpath_parts)):
            if 'text()=' in xpath_parts[i]:
                num_text_expressions += 1
                if num_text_expressions == index:
                    xpath_parts[i] = xpath_parts[i].split("text()=")[0]
                    return '/'.join(xpath_parts)

        if index > num_text_expressions:
            print("Index is greater than the number of text() expressions in the XPath. Removing the last text() expression.")
            for i in range(len(xpath_parts)-1, -1, -1):
                if 'text()=' in xpath_parts[i]:
                    xpath_parts[i] = xpath_parts[i].split("text()=")[0]
                    return '/'.join(xpath_parts)

    def add_num(self, xpath:str, num:int=1) -> str:
        parts = xpath.split('/')
        if num <= len(parts):
            parts[num - 1] = f"{parts[num - 1]}[{num}]"
        else:
            parts[-1] = f"{parts[-1]}[{num}]"
            print(f"Warning: index value exceeds xpath parts length. Appending [{num}] to the last part of the xpath.")
        return '/'.join(parts)

    def remove_num(self, xpath:str, index:int) -> str:
        parts = xpath.split('/')
        if index < len(parts):
            last_part = parts[index]
            if '[' in last_part and last_part.endswith(']'):
                last_part = last_part[:last_part.index('[')]
                parts[index] = last_part
                return '/'.join(parts)
        else:
            last_part = parts[-1]
            if '[' in last_part and last_part.endswith(']'):
                last_part = last_part[:last_part.index('[')]
                parts[-1] = last_part
                print("Warning: index value exceeds xpath parts length. Removing the specified index from the last part of the xpath.")
                return '/'.join(parts)
        return xpath

    def add_specify(self, xpath:str, tag:str) -> str:
        return xpath.replace('*', tag)

    def remove_specify(self, xpath:str) -> str:
        tags = ['a', 'abbr', 'acronym', 'address', 'applet', 'area', 'article', 'aside', 'audio', 'b', 'base', 'basefont', 'bdi', 'bdo', 'bgsound', 'big', 'blink', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'command', 'content', 'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'dir', 'div', 'dl', 'dt', 'element', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'font', 'footer', 'form', 'frame', 'frameset', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hgroup', 'hr', 'html', 'i', 'iframe', 'image', 'img', 'input', 'ins', 'isindex', 'kbd', 'keygen', 'label', 'legend', 'li', 'link', 'listing', 'main', 'map', 'mark', 'marquee', 'math', 'menu', 'menuitem', 'meta', 'meter', 'nav', 'nobr', 'noframes', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'picture', 'plaintext', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section', 'select', 'shadow', 'small', 'source', 'spacer', 'span', 'strike', 'strong', 'style', 'sub', 'summary', 'sup', 'svg', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'tt', 'u', 'ul', 'var', 'video', 'wbr', 'xmp']
        for tag in tags:
            if f'/{tag}' in xpath:
                return xpath.replace(f'/{tag}', '/*')
        return xpath

    def add_following_sibling(self, xpath:str, tag:str, index:int=-1) -> str:
        parts = xpath.split('/')
        if index < len(parts):
            parts[index] += f"/following-sibling::{tag}"
        else:
            parts[-1] += f"/following-sibling::{tag}"
            print("Warning: index value exceeds xpath parts length. Appending following-sibling::{} to the last part of the xpath.".format(tag))
        return '/'.join(parts)

    def remove_following_sibling(self, xpath:str, index:int=-1) -> str:
        parts = xpath.split('/')
        if index < len(parts):
            part = parts[index]
            if part.startswith('following-sibling::'):
                del parts[index]
            else:
                for i in range(index + 1, len(parts)):
                    if parts[i].startswith('following-sibling::'):
                        del parts[i]
                        break
        else:
            last_part = parts[-1]
            if last_part.startswith('following-sibling::'):
                parts[-2] = parts[-2].rstrip('/')
                del parts[-1]
            else:
                last_part = last_part.rstrip('/')
                last_part_parts = last_part.split('[')
                if last_part_parts[-1].startswith('following-sibling::'):
                    last_part = last_part[:last_part.rindex('[')]
                parts[-1] = last_part

                print("Warning: index value exceeds xpath parts length. Removing following-sibling:: from the last part of the xpath.")

        return '/'.join(parts)

    def add_preceding_sibling(self, xpath:str, index:int, tag:str) -> str:
        parts = xpath.split('/')
        if index < len(parts):
            parts[index] += f"/preceding-sibling::{tag}"
        else:
            parts[-1] += f"/preceding-sibling::{tag}"
            print(f"Warning: index value exceeds xpath parts length. Appending preceding-sibling::{tag} to the last part of the xpath.")
        return '/'.join(parts)

    def remove_preceding_sibling(self, xpath:str, index:int=-1) -> str:
        parts = xpath.split('/')
        if index < len(parts):
            part = parts[index]
            if part.startswith('preceding-sibling::'):
                del parts[index]
            else:
                for i in reversed(range(0, index)):
                    if parts[i].startswith('preceding-sibling::'):
                        del parts[i]
                        break
        else:
            last_part = parts[-1]
            if last_part.startswith('preceding-sibling::'):
                parts[-2] = parts[-2].rstrip('/')
                del parts[-1]
            else:
                last_part = last_part.rstrip('/')
                last_part_parts = last_part.split('[')
                if last_part_parts[-1].startswith('preceding-sibling::'):
                    last_part = last_part[:last_part.rindex('[')]
                parts[-1] = last_part

                print("Warning: index value exceeds xpath parts length. Removing preceding-sibling:: from the last part of the xpath.")

        return '/'.join(parts)

    def add_parent(self, xpath:str, tag:str) -> str:
        return xpath + f"/parent::{tag}"

    def remove_parent(self, xpath:str) -> str: 
        split_xpath = xpath.split('/')
        for i in range(len(split_xpath)):
            if split_xpath[i].startswith('parent::'):
                split_xpath = split_xpath[:i] + split_xpath[i+1:]
                break
        return '/'.join(split_xpath)

    def change_equals_to_contains(self, xpath:str) -> str:
        if '@class=' in xpath:
            start_idx = xpath.index('"') + 1
            end_idx = xpath.index('"', start_idx)
            class_val = xpath[start_idx:end_idx]
            new_xpath = xpath.replace(f'@class="{class_val}"', f'contains(@class, "{class_val}")')
            return new_xpath
        else:
            return xpath

    def change_contains_to_equals(self, xpath:str) -> str:
        xpath_list = xpath.split('/')
        for i, element in enumerate(xpath_list):
            if 'contains(' in element:
                class_name = element.split(",")[1].strip(")")
                new_element = f"*[@class='{class_name}']"
                xpath_list[i] = new_element
        return '/'.join(xpath_list)

    def add_attrib_equals(self, xpath:str, attribute:str, value:str, index:int=1) -> str:
        tree = etree.fromstring("<root>" + xpath + "</root>")
        xpath_parts = xpath.split("/")
        if index < len(xpath_parts):
            xpath_parts[index] = xpath_parts[index] + f"[@{attribute}='{value}']"
            new_xpath = "/".join(xpath_parts)
        else:
            last_part = xpath_parts[-1] + f"[@{attribute}='{value}']"
            new_xpath = "/".join(xpath_parts[:-1]) + "/" + last_part
            print("Warning: The specified index is greater than the maximum index in the given XPath. The attribute was added to the last part.")
        return new_xpath
    
    def add_attrib_contains(self, xpath:str, attribute:str, value:str, index:int=1) -> str:
        tree = etree.fromstring("<root>" + xpath + "</root>")
        xpath_parts = xpath.split("/")
        if index < len(xpath_parts):
            xpath_parts[index] = xpath_parts[index] + f"[contains(@{attribute}, '{value}')]"
            new_xpath = "/".join(xpath_parts)
        else:
            last_part = xpath_parts[-1] + f"[contains(@{attribute}, '{value}')]"
            new_xpath = "/".join(xpath_parts[:-1]) + "/" + last_part
            print("Warning: The specified index is greater than the maximum index in the given XPath. The attribute was added to the last part.")
        return new_xpath
   
    def change_attrib_value(self, xpath:str, attribute:str, value:str, index:int=1) -> str:
        tree = etree.fromstring("<root>" + xpath + "</root>")
        for element in tree.xpath(".//*[@*]"):
            attributes = list(element.attrib)
            if attribute in attributes:
                count = 0
                for att in attributes:
                    if att == attribute:
                        count += 1
                        if count == index:
                            element.attrib[att] = value
                            break
                else:
                    last_attribute = attributes[-1]
                    last_attribute_value = element.attrib[last_attribute]
                    element.attrib[attribute] = value
                    print(f"Warning: {xpath} does not have {attribute}{index} attribute. Changed {last_attribute} value: {last_attribute_value} to {attribute}: {value}")
        return etree.tostring(tree, encoding=str)[6:-7]

    def change_attrib_name(self, xpath:str, attribute:str, value:str, index:int=1) -> str:
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(xpath, parser)

        attribute_list = root.xpath(f"//@{attribute}")
        count = 0
        last_attribute = ""
        last_attribute_value = ""
        for i in range(len(attribute_list)):
            if index is None or count == index:
                if count == 0:
                    element = attribute_list[i].getparent()
                element.attrib[attribute] = value
                print(f"{attribute}{index} attribute in {xpath} changed to {attribute}{count}: {value}")
                return etree.tostring(root).decode()
            last_attribute = attribute_list[i]
            last_attribute_value = element.attrib[last_attribute]
            count += 1

        element.attrib[last_attribute] = value
        print(f"Warning: {xpath} does not have {attribute}{index} attribute. Changed {last_attribute} value: {last_attribute_value} to {attribute + str(count)}: {value}")
        return etree.tostring(root).decode()

    def add_ceiling(self, xpath:str, value:int, index:int=-1) -> str:
        parts = xpath.split('/')
        if index < 0:
            index += len(parts)
        if index < len(parts):
            parts[index] = f"ceiling({parts[index]}, {value})"
            return '/'.join(parts)
        else:
            print("Error: The index value exceeds the number of XPath parts.")
            return xpath

    def remove_ceiling(self, xpath:str, index:int=-1) -> str:
        parts = xpath.split('/')
        if index < 0:
            index += len(parts)
        if index < len(parts):
            part = parts[index]
            if part.startswith('ceiling(') and part.endswith(')'):
                parts[index] = part.split('(', 1)[1].rsplit(',', 1)[0]
                return '/'.join(parts)
            print("Error: ceiling() function not found at the specified index.")
        else:
            print("Error: The index value exceeds the number of XPath parts.")
        return xpath
    
    def add_count(self, xpath:str, value:int, index:int=-1) -> str:
        parts = xpath.split('/')
        if index < 0:
            index += len(parts)
        if index < len(parts):
            parts[index] = f"count({parts[index]}, {value})"
            return '/'.join(parts)
        else:
            print("Error: The index value exceeds the number of XPath parts.")
            return xpath

    def remove_count(self, xpath:str, index:int=-1) -> str:
        parts = xpath.split('/')
        if index < 0:
            index += len(parts)
        if index < len(parts):
            part = parts[index]
            if part.startswith('count(') and part.endswith(')'):
                parts[index] = part.split('(', 1)[1].rsplit(',', 1)[0]
                return '/'.join(parts)
            print("Error: count() function not found at the specified index.")
        else:
            print("Error: The index value exceeds the number of XPath parts.")
        return xpath
