import fitz # PyMuPDF
from PIL import Image, ImageDraw, ImageFont, ImageOps # Pillow 图像处理库
import io # 用于处理字节流
import os # 用于文件路径操作
import subprocess # 用于执行外部命令（QPDF）
import math # 用于数学计算
import uuid # 用于生成唯一标识符，确保临时文件名的唯一性

# --- PDF 反色处理函数 (使用 Pillow) ---
# 注意：此函数在我们的应用中已被 process_pdf_to_image 内部调用，
# 通常不会直接从GUI层调用。保留它作为模块内部辅助函数。
def invert_pdf_colors_via_pillow(input_pdf_path, output_pdf_path, status_callback=None):
    """
    将PDF文档的颜色反转，并保存为新的PDF文件。
    此过程会将PDF页面转换为图像，因此输出的PDF将不再包含可选文本。
    Args:
        input_pdf_path (str): 输入PDF文件的路径。
        output_pdf_path (str): 输出反色PDF文件的路径。
        status_callback (callable, optional): 一个回调函数，用于更新处理进度。
                                              接受一个字符串参数 (当前状态信息)。
    """
    try:
        doc = fitz.open(input_pdf_path)
    except Exception as e:
        raise ValueError(f"无法打开PDF文件进行图片处理：{e}")

    new_pdf = fitz.open()

    original_outline = doc.get_toc()

    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(200/72, 200/72)) # 使用200 DPI作为基础渲染
        
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        
        inverted_img = ImageOps.invert(img.convert('RGB'))
        
        img_byte_arr = io.BytesIO()
        inverted_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0) # 将文件指针移到开头

        new_page = new_pdf.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(page.rect, stream=img_byte_arr.getvalue())

        if status_callback:
            status_callback(f"正在反转颜色... 页面 {i+1}/{len(doc)}")

    if original_outline:
        try:
            new_pdf.set_toc(original_outline)
        except Exception as e:
            print(f"警告: 未能在新PDF中设置书签: {e}")

    new_pdf.save(output_pdf_path, garbage=4, deflate=True, clean=True)
    new_pdf.close()
    doc.close()
    return output_pdf_path

## PDF 图片化处理函数 (`process_pdf_to_image`)
def process_pdf_to_image(input_pdf_path, output_pdf_path, invert_colors=False, status_callback=None, quality="中"):
    """
    将PDF转换为基于图片的PDF，可选反色，并保留书签。
    新增了品质选项，会影响图片渲染的DPI。
    """
    try:
        doc = fitz.open(input_pdf_path)
    except Exception as e:
        raise ValueError(f"无法打开PDF文件进行图片处理：{e}")

    original_toc = doc.get_toc()

    temp_image_paths = []
    output_doc = fitz.open() # 创建一个新的空PDF文档用于输出

    # 根据品质选择设置DPI
    dpi = 200 # 默认中等品质 DPI

    if quality == "极低":
        dpi = 50
    elif quality == "低":
        dpi = 100
    elif quality == "高":
        dpi = 300
    elif quality == "极高":
        dpi = 400
    # "中" 保持默认 200 DPI

    for page_num in range(doc.page_count):
        if status_callback:
            status_callback(f"正在将页面 {page_num + 1}/{doc.page_count} 转换为图片 ({quality}品质)...")
        page = doc.load_page(page_num) # 使用 load_page 更安全和推荐

        # 将页面渲染为指定DPI的像素图
        matrix = fitz.Matrix(dpi / 72, dpi / 72) # 将默认 72 DPI 缩放到目标 DPI
        pix = page.get_pixmap(matrix=matrix)

        # --- 关键修正：使用 pix.tobytes() 方法获取图像数据 ---
        # 明确指定为 PNG 格式的字节流，PyMuPDF 会正确处理
        img_byte_data = pix.tobytes("png") 
        # 使用 io.BytesIO 将字节流包装成文件对象，Pillow 可以直接读取
        img_pil = Image.open(io.BytesIO(img_byte_data))
        # --- 修正结束 ---

        # 确保图片是RGB模式，Pillow处理可能需要
        if img_pil.mode != 'RGB':
            img_pil = img_pil.convert('RGB')

        if invert_colors:
            if status_callback:
                status_callback(f"正在反转页面 {page_num + 1}/{doc.page_count} 的颜色...")
            # 使用Pillow反转颜色
            img_pil = ImageOps.invert(img_pil) # ImageOps.invert 适用于RGB图像

        # 将图片保存到临时文件
        # 使用PNG保证无损，并添加UUID确保唯一性，避免多进程/多线程时的冲突

        unique_id_part = uuid.uuid4().hex 
        # Method 2 (Alternative if Method 1 still fails due to strange environment): 
        # unique_id_part = str(uuid.uuid4()).replace('-', '') # Directly convert to string and remove hyphens
        
        temp_img_path = f"temp_page_{page_num}_{unique_id_part}.png"
        # --- 修正结束 ---

        # temp_img_path = f"temp_page_{page_num}_{str(uuid.uuid4().hex())}.png"
        img_pil.save(temp_img_path)
        temp_image_paths.append(temp_img_path)

        # 将图片插入到新的PDF文档中
        img_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
        img_rect = img_page.rect
        img_page.insert_image(img_rect, filename=temp_img_path)

    doc.close() # 关闭输入PDF

    try:
        # 将书签写入新的PDF文档
        if original_toc: # 仅当存在原始书签时才设置TOC
            output_doc.set_toc(original_toc)

        # 保存输出PDF，进行垃圾回收和压缩
        output_doc.save(output_pdf_path, garbage=3, deflate=True)
        output_doc.close()
    except Exception as e:
        raise RuntimeError(f"保存图片化PDF失败：{e}")
    finally:
        # 清理临时图片文件
        for temp_path in temp_image_paths:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError as e:
                    print(f"警告: 无法删除临时文件 {temp_path}: {e}")
        if status_callback:
            status_callback("图片处理完成。")

## 添加水印函数 (`add_watermark`)
def add_watermark(input_pdf, output_pdf, watermark_type='image',
                  watermark_source=None,
                  rows=5, cols=4, opacity_level=0.15,
                  rotation_angle=0,
                  watermark_size_percent=0.8,
                  custom_font_path=None):
    """
    为PDF文档添加水印（图片或文本），并保存为新的PDF文件。
    水印可以平铺，并支持透明度、旋转和大小调整。
    """
    try:
        doc = fitz.open(input_pdf)
    except Exception as e:
        raise ValueError(f"无法打开PDF文件：{e}")

    image_data = None
    original_watermark_img = None

    if watermark_type == 'image':
        watermark_img_path = watermark_source
        if not os.path.exists(watermark_img_path):
            raise FileNotFoundError(f"水印图片未找到: {watermark_img_path}")

        try:
            original_watermark_img = Image.open(watermark_img_path)
            if original_watermark_img.mode != 'RGBA':
                original_watermark_img = original_watermark_img.convert('RGBA')

        except Exception as e:
            raise RuntimeError(f"处理水印图片失败: {e}")

    elif watermark_type == 'text':
        watermark_text = watermark_source
        if not watermark_text:
            raise ValueError("文本水印内容不能为空。")

        try:
            font = None
            if custom_font_path and os.path.exists(custom_font_path):
                try:
                    font = ImageFont.truetype(custom_font_path, 72)
                except IOError:
                    print(f"警告: 无法加载自定义字体 '{custom_font_path}'，将使用Pillow默认字体。")
                    font = ImageFont.load_default()
                except Exception as e:
                    print(f"警告: 加载自定义字体时发生未知错误 '{custom_font_path}': {e}，将使用Pillow默认字体。")
                    font = ImageFont.load_default()
            else:
                font = ImageFont.load_default()
                print("警告: 未选择自定义字体或字体文件无效，使用Pillow默认字体。")
            
            bbox = font.getbbox(watermark_text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            diagonal = int(math.sqrt(text_width**2 + text_height**2))
            canvas_size = diagonal + 50 

            if canvas_size <= 0:
                canvas_size = 1

            text_image = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(text_image)

            draw_x = (canvas_size - text_width) / 2 - bbox[0]
            draw_y = (canvas_size - text_height) / 2 - bbox[1]

            draw.text((draw_x, draw_y), watermark_text, font=font, fill=(0, 0, 0, 255))

            original_watermark_img = text_image

        except Exception as e:
            raise RuntimeError(f"生成文本水印失败: {e}")

    else:
        raise ValueError("不支持的水印类型。")

    if original_watermark_img:
        if rotation_angle != 0:
            original_watermark_img = original_watermark_img.rotate(rotation_angle, expand=True, fillcolor=(0,0,0,0))

        datas = original_watermark_img.getdata()
        new_datas = []
        for item in datas:
            if len(item) == 4:
                if item[3] > 0:
                    new_datas.append((item[0], item[1], item[2], int(item[3] * opacity_level)))
                else:
                    new_datas.append(item)
            else:
                new_datas.append((item[0], item[1], item[2], int(255 * opacity_level)))
        original_watermark_img.putdata(new_datas)

        img_byte_arr = io.BytesIO()
        original_watermark_img.save(img_byte_arr, format='PNG')
        image_data = img_byte_arr.getvalue()

        img_actual_width = original_watermark_img.width
        img_actual_height = original_watermark_img.height
    else:
        return

    for page in doc:
        page_rect = page.rect
        page_width = page_rect.width
        page_height = page_rect.height

        cell_width = page_width / cols
        cell_height = page_height / rows

        if img_actual_height == 0:
            ratio_watermark = 1
        else:
            ratio_watermark = img_actual_width / img_actual_height

        if cell_height == 0:
            ratio_cell = 1
        else:
            ratio_cell = cell_width / cell_height

        if ratio_watermark > ratio_cell:
            max_fit_width = cell_width
            max_fit_height = cell_width / ratio_watermark
        else:
            max_fit_height = cell_height
            max_fit_width = cell_height * ratio_watermark

        final_img_width = max_fit_width * watermark_size_percent
        final_img_height = max_fit_height * watermark_size_percent

        if final_img_width <= 0 or final_img_height <= 0:
            print(f"警告: 水印计算尺寸过小，跳过页面 {page.number + 1} 的水印添加。")
            continue

        for row in range(rows):
            for col in range(cols):
                x0 = col * cell_width + (cell_width - final_img_width) / 2
                y0 = row * cell_height + (cell_height - final_img_height) / 2
                x1 = x0 + final_img_width
                y1 = y0 + final_img_height

                rect = fitz.Rect(x0, y0, x1, y1)
                page.insert_image(rect, stream=image_data, keep_proportion=True)

    doc.save(output_pdf, garbage=4, deflate=True, clean=True)
    doc.close()

## 使用 QPDF 保护 PDF 的函数 (`protect_pdf_with_qpdf`)
def protect_pdf_with_qpdf(input_pdf, output_pdf, open_password, owner_password):
    """
    使用 QPDF 工具为PDF添加密码和权限限制。
    需要系统安装 QPDF。
    """
    cmd = [
        'qpdf',
        '--encrypt', open_password, owner_password, '256', # 256位加密
        '--print=none',      # 禁止打印
        '--modify=none',     # 禁止修改（包括注释、表单填写等）
        '--extract=n',       # 禁止复制/提取文本和图像
        '--', input_pdf, output_pdf
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"QPDF 执行失败: {e.stderr}\n命令: {' '.join(cmd)}")
    except FileNotFoundError:
        raise FileNotFoundError("QPDF 命令未找到。请确保 QPDF 已安装并添加到系统 PATH 中。")
    except Exception as e:
        raise RuntimeError(f"QPDF 执行期间发生意外错误：{e}")