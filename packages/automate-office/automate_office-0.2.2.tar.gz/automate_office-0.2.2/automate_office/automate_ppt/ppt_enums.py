from pptx.enum.text import PP_ALIGN


DEFAULT_PARAGRAPH_SPACING = 8


PARAGRAPH_ALIGN = {
    "居中": PP_ALIGN.CENTER,
    "左对齐": PP_ALIGN.LEFT,
    "右对齐": PP_ALIGN.RIGHT,
    # 均匀分布
    "均匀": PP_ALIGN.DISTRIBUTE,
    
    # 每行都在边距处开始和结束，并调整了单词之间的间距, 这样一来，该行就填满了段落的宽度。
    "填满": PP_ALIGN.JUSTIFY,
    # 在单词之间使用少量空格
    '填满2': PP_ALIGN.JUSTIFY_LOW,
    "THAI_DISTRIBUTE": PP_ALIGN.THAI_DISTRIBUTE
}


