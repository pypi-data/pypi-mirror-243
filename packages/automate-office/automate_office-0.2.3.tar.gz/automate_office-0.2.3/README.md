# PPT
### 空slide
1. 创建空PPT, 支持inches和cm
    ```python
    from automate_office.automate_ppt.MyPPTCreator import PPTCreator
    my_ppt = PPTCreator(size_params={"unit_type": "inches", "width": 10, "height": 5.625})
    ```
2. 存储PPT，默认存储在Downloads目录下
    ```python
    my_ppt.save_pptx(filename=None, save_path=None)
    ```

3. 创建slide
    ```python
    my_slide = my_ppt.create_slide(slide_idx=6)
    ``` 

4. 创建文本框
    ```python
    my_ppt.add_textbox(
        self, 
        cur_slide: slide.Slide, 
        # left top width height, 相对于长宽的比例，0-1之间
        rel_coordinate=(0, 0, 1, 1), 
        paragraph_infos=None
    )
    ``` 
    - paragraph_infos: 下面是一个例子
    ```python
    paragraph_infos = [
        {
            "对齐": "居中",
            "文字": [
                ["段落1第1部分文字", "微软雅黑", 12, False, False, (0, 255, 0)],
                ["段落1第2部分文字", "微软雅黑", 12, False, False, (0, 0, 255)],
                ...
            ],
            "段落间距": 8
        },
        {
            "对齐": "左对齐",
            "文字": [
                ["段落2第1部分文字", "微软雅黑", 12, False, False, (0, 255, 0)],
                ["段落2第2部分文字", "微软雅黑", 12, False, False, (0, 0, 255)],
                ...
            ],
            "段落间距": 8
        },
    ]
    ```

5. 创建矩形
    ```python
    my_ppt.add_rectangle_shape
    ```
6. 创建图片
    ```python
    my_ppt.add_picture
    ```
7. 创建柱状图
    ```python
    my_ppt.add_bar_chart
    ```
8. 创建折线图
    ```python
    my_ppt.add_line_chart
    ```
9. 创建饼图
    ```python
    my_ppt.add_pie_chart
    ```
10. 创建表格
    ```python
    my_ppt.add_table
    ```
11. 修改已有PPT的文字
    ```python
    from automate_office.automate_ppt.modify_ppt import set_textframe
    set_textframe(text_frame, paragraph_infos=None, vertical_anchor = MSO_ANCHOR.MIDDLE)
    ```
