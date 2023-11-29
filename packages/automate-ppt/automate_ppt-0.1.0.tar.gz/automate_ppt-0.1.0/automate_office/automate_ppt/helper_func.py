from pptx.util import Pt
from docx.oxml.ns import qn
from pptx.dml.color import RGBColor


def set_font(cur_font, cur_font_info):
    """设置字体
    Args:
        cur_font (_type_): pptx.text.text.font类型
        cur_font_info (_type_): tuple, 字体、字号、加粗、斜体、颜色
    """
    font_name, font_size, bold, italic, rgb = cur_font_info

    cur_font.name = font_name
    # 下面这坨是因为python-pptx包不怎么支持中文字体，不管咋设置都是宋体
    if cur_font._rPr.find(qn("a:ea")) is not None:
        cur_font._rPr.find(qn("a:ea")).set("typeface", font_name)
    else:
        element = cur_font._rPr.makeelement(qn("a:ea"))
        element.set("typeface", font_name)
        cur_font._rPr.append(element)
    
    cur_font.size = Pt(font_size)
    cur_font.bold = bold
    cur_font.italic = italic
    cur_font.color.rgb = RGBColor(*rgb)


def set_color(obj, color):
    """设置对象颜色

    Args:
        obj (_type_): series.format.line, series.marker.format, font等任意类型
        color (_type_): RGB 三元组tuple
    """
    obj.fill.solid()
    obj.fill.fore_color.rgb = RGBColor(*color)
