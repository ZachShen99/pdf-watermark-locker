import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import ImageFont, ImageTk # ImageFont 用于加载字体
import os
import sys

# 导入 tkinterdnd2 库以支持拖放功能
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    messagebox.showerror("错误", "未找到 tkinterdnd2 库。请先安装它: pip install tkinterdnd2")
    sys.exit(1)

# 尝试导入 pdf_logic 模块
try:
    import pdf_logic
except ImportError:
    messagebox.showerror("错误", "未找到 pdf_logic.py。请确保它与主程序在同一目录下。")
    sys.exit(1)

class PDFProcessorApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("PDF 批量处理工具")
        # 当窗口关闭时调用 on_closing 方法
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 初始化自定义字体路径变量
        self.custom_font_path = tk.StringVar(value="") # 用于保存用户选择的字体路径

        # 创建并布局UI组件
        self._create_widgets()
        # 设置拖放绑定
        self._setup_bindings()
        # 执行初始设置（如更新水印选项状态）
        self._initial_setup()

    def _create_widgets(self):
        # 主框架，设置内边距
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.pack(expand=True, fill="both")

        # --- PDF 文件选择区域 ---
        pdf_selection_frame = ttk.LabelFrame(main_frame, text="PDF 文件选择", padding="10 10 10 10")
        pdf_selection_frame.pack(pady=10, fill="x") # 垂直方向留白，水平方向填充

        tk.Label(pdf_selection_frame, text="选择或拖放 PDF 文件:").pack(side="left", padx=5, pady=5)
        self.pdf_entry = tk.Entry(pdf_selection_frame)
        self.pdf_entry.pack(side="left", expand=True, fill="x", padx=5, pady=5)
        tk.Button(pdf_selection_frame, text="浏览 PDF", command=self._select_pdf).pack(side="right", padx=5, pady=5)

        # --- 笔记本 (标签页) ---
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill="both", pady=10)

        # --- 标签页 1: 水印设置 ---
        watermark_tab = ttk.Frame(self.notebook, padding="10 10 10 10")
        self.notebook.add(watermark_tab, text="水印设置")

        self.watermark_type_var = tk.StringVar(value='image') # 水印类型变量，默认图片水印

        # 水印类型选择
        watermark_type_frame = ttk.LabelFrame(watermark_tab, text="水印类型", padding="5 5 5 5")
        watermark_type_frame.pack(pady=5, fill="x")
        tk.Label(watermark_type_frame, text="选择水印类型:").pack(side="left", padx=5)
        tk.Radiobutton(watermark_type_frame, text="图片水印", variable=self.watermark_type_var, value='image', command=self._update_watermark_options).pack(side="left", padx=10)
        tk.Radiobutton(watermark_type_frame, text="文字水印", variable=self.watermark_type_var, value='text', command=self._update_watermark_options).pack(side="left", padx=10)

        # 图片水印选项框
        self.img_frame = ttk.LabelFrame(watermark_tab, text="图片水印设置", padding="5 5 5 5")
        tk.Label(self.img_frame, text="选择或拖放水印图片:").pack(side="left", padx=5, pady=5)
        self.img_entry = tk.Entry(self.img_frame)
        self.img_entry.pack(side="left", expand=True, fill="x", padx=5, pady=5)
        tk.Button(self.img_frame, text="浏览图片", command=self._select_image).pack(side="right", padx=5, pady=5)

        # 文字水印选项框
        self.text_frame = ttk.LabelFrame(watermark_tab, text="文字水印设置", padding="5 5 5 5")
        tk.Label(self.text_frame, text="输入水印文字:").pack(side="left", padx=5, pady=5)
        self.text_entry = tk.Entry(self.text_frame)
        self.text_entry.pack(side="left", expand=True, fill="x", padx=5, pady=5)

        # --- 字体选择区域 ---
        self.font_selection_frame = ttk.LabelFrame(self.text_frame, text="字体选择", padding="5 5 5 5")
        self.font_selection_frame.pack(pady=5, fill="x") # columnspan=2 让它横跨两列

        tk.Label(self.font_selection_frame, text="已选字体路径:").pack(side="left", padx=5)
        # 字体路径输入框设为只读，并通过 textvariable 绑定变量
        self.font_path_entry = tk.Entry(self.font_selection_frame, textvariable=self.custom_font_path, state='readonly')
        self.font_path_entry.pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(self.font_selection_frame, text="浏览字体", command=self._select_font).pack(side="right", padx=5)
        tk.Label(self.font_selection_frame, text="（留空使用默认字体，支持 .ttf, .otf）", fg="gray", font=("Arial", 8)).pack(anchor='w', padx=5, pady=(0,5))
        # --- 字体选择区域结束 ---

        # 平铺设置 (行数, 列数, 水印大小百分比)
        tiled_options_frame = ttk.LabelFrame(watermark_tab, text="平铺设置", padding="5 5 5 5")
        tiled_options_frame.pack(pady=5, fill="x")

        tk.Label(tiled_options_frame, text="行数 (1-100):").pack(side="left", padx=5)
        self.rows_entry = tk.Entry(tiled_options_frame, width=5)
        self.rows_entry.insert(0, "5")
        self.rows_entry.pack(side="left", padx=5)

        tk.Label(tiled_options_frame, text="列数 (1-100):").pack(side="left", padx=5)
        self.cols_entry = tk.Entry(tiled_options_frame, width=5)
        self.cols_entry.insert(0, "4")
        self.cols_entry.pack(side="left", padx=5)

        tk.Label(tiled_options_frame, text="水印大小 (1-100%):").pack(side="left", padx=5)
        self.size_percent_entry = tk.Entry(tiled_options_frame, width=5)
        self.size_percent_entry.insert(0, "80")
        self.size_percent_entry.pack(side="left", padx=5)

        # 通用水印选项 (旋转, 不透明度)
        common_options_frame = ttk.LabelFrame(watermark_tab, text="通用设置", padding="5 5 5 5")
        common_options_frame.pack(pady=5, fill="x")

        tk.Label(common_options_frame, text="旋转角度 (0-360):").pack(side="left", padx=5)
        self.rotation_entry = tk.Entry(common_options_frame, width=7)
        self.rotation_entry.insert(0, "0")
        self.rotation_entry.pack(side="left", padx=5)

        tk.Label(common_options_frame, text="不透明度 (0.0-1.0):").pack(side="left", padx=5)
        self.opacity_entry = tk.Entry(common_options_frame, width=7)
        self.opacity_entry.insert(0, "0.15")
        self.opacity_entry.pack(side="left", padx=5)

        # --- 标签页 2: 图片化处理 ---
        image_processing_tab = ttk.Frame(self.notebook, padding="10 10 10 10")
        self.notebook.add(image_processing_tab, text="图片化处理")

        self.convert_to_image_var = tk.BooleanVar(value=False)
        # 绑定命令，当复选框状态改变时，更新相关选项的可用性
        tk.Checkbutton(image_processing_tab, text="将PDF图片化 (文本不可选)", variable=self.convert_to_image_var, command=self._toggle_image_options).pack(anchor='w', pady=(10, 0), padx=10)
        tk.Label(image_processing_tab, text="（勾选此项会将所有PDF页面转换为图片，可能导致文件变大）", fg="gray", font=("Arial", 9)).pack(anchor='w', padx=10, pady=(0,5))

        # --- 图片品质选择 ---
        self.image_quality_var = tk.StringVar(value="中") # 默认选中“中”
        quality_frame = ttk.LabelFrame(image_processing_tab, text="图片品质", padding="5 5 5 5")
        quality_frame.pack(pady=5, fill="x", padx=10)
        tk.Label(quality_frame, text="选择输出品质:").pack(side="left", padx=5)
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.image_quality_var,
                                            values=["极低","低", "中", "高", "极高"], state="disabled") # 初始禁用
        self.quality_combo.pack(side="left", padx=5)
        # --- 图片品质选择结束 ---

        self.invert_colors_var = tk.BooleanVar(value=False)
        self.invert_colors_var.set(False) # 确保初始状态为未选中
        # 初始禁用反色复选框
        self.invert_checkbutton = tk.Checkbutton(image_processing_tab, text="应用反色 (需勾选“将PDF图片化”)", variable=self.invert_colors_var, state="disabled")
        self.invert_checkbutton.pack(anchor='w', pady=5, padx=10)
        tk.Label(image_processing_tab, text="（仅当“将PDF图片化”勾选时生效）", fg="gray", font=("Arial", 9)).pack(anchor='w', padx=10, pady=(0,5))

        # --- 标签页 3: 密码设置 ---
        password_tab = ttk.Frame(self.notebook, padding="10 10 10 10")
        self.notebook.add(password_tab, text="密码设置")

        tk.Label(password_tab, text="打开密码 (用户密码):").pack(anchor='w', padx=10, pady=(5,0))
        self.open_pw_entry = tk.Entry(password_tab, width=40, show='*') # show='*' 隐藏密码输入
        self.open_pw_entry.pack(anchor='w', padx=10, pady=(0,5), fill="x")

        tk.Label(password_tab, text="编辑密码 (所有者密码):").pack(anchor='w', padx=10, pady=(5,0))
        self.edit_pw_entry = tk.Entry(password_tab, width=40, show='*')
        self.edit_pw_entry.pack(anchor='w', padx=10, pady=(0,5), fill="x")
        tk.Label(password_tab, text="(留空表示不设置密码。设置所有者密码可阻止打印、修改、文本提取)", fg="gray", font=("Arial", 9)).pack(anchor='w', padx=10, pady=(0,5))

        # 开始处理按钮
        tk.Button(main_frame, text="开始处理 PDF", command=self._start_conversion, bg="black", fg="white", height=2).pack(pady=15, fill="x")

        # 状态标签
        self.status_label = tk.Label(main_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W) # bd=1, relief=SUNKEN 添加边框和凹陷效果
        self.status_label.pack(pady=5, fill="x")

    def _setup_bindings(self):
        # 注册拖放目标并绑定拖放事件
        self.pdf_entry.drop_target_register(DND_FILES)
        self.pdf_entry.dnd_bind('<<Drop>>', self._drop_pdf)
        self.img_entry.drop_target_register(DND_FILES)
        self.img_entry.dnd_bind('<<Drop>>', self._drop_image)
        # 字体路径入口也支持拖放
        self.font_path_entry.drop_target_register(DND_FILES)
        self.font_path_entry.dnd_bind('<<Drop>>', self._drop_font)

    def _initial_setup(self):
        # 初始更新水印选项状态，确保只有当前选择的水印类型可见
        self._update_watermark_options()
        # 初始更新图片化选项状态，确保品质和反色选项默认禁用
        self._toggle_image_options()

    def _select_pdf(self):
        # 打开文件选择对话框，只允许选择PDF文件
        filepath = filedialog.askopenfilename(filetypes=[("PDF 文件", "*.pdf")])
        if filepath:
            self.pdf_entry.delete(0, tk.END) # 清空当前内容
            self.pdf_entry.insert(0, filepath) # 插入新路径

    def _select_image(self):
        # 打开文件选择对话框，只允许选择图片文件
        filepath = filedialog.askopenfilename(filetypes=[("图片文件", "*.jpg *.png *.jpeg *.gif *.bmp")])
        if filepath:
            self.img_entry.delete(0, tk.END)
            self.img_entry.insert(0, filepath)

    def _select_font(self):
        # 打开文件选择对话框，只允许选择字体文件
        filepath = filedialog.askopenfilename(filetypes=[("字体文件", "*.ttf *.otf *.TTF *.OTF")])
        if filepath:
            self.custom_font_path.set(filepath) # 使用StringVar更新

    # --- 拖放事件处理函数 ---
    def _drop_pdf(self, event):
        filepath = event.data
        # 处理拖放路径可能带有的 {}
        if filepath.startswith('{') and filepath.endswith('}'):
            filepath = filepath[1:-1]
        files = filepath.split()
        if files:
            if files[0].lower().endswith(".pdf"):
                self.pdf_entry.delete(0, tk.END)
                self.pdf_entry.insert(0, files[0])
            else:
                messagebox.showwarning("拖放错误", "请拖放一个 PDF 文件。")

    def _drop_image(self, event):
        filepath = event.data
        if filepath.startswith('{') and filepath.endswith('}'):
            filepath = filepath[1:-1]
        files = filepath.split()
        if files:
            if any(files[0].lower().endswith(ext) for ext in ['.jpg', '.png', '.jpeg', '.gif', '.bmp']):
                self.img_entry.delete(0, tk.END)
                self.img_entry.insert(0, files[0])
            else:
                messagebox.showwarning("拖放错误", "请拖放一个图片文件。")

    def _drop_font(self, event):
        filepath = event.data
        if filepath.startswith('{') and filepath.endswith('}'):
            filepath = filepath[1:-1]
        files = filepath.split()
        if files:
            if any(files[0].lower().endswith(ext) for ext in ['.ttf', '.otf', '.ttf', '.otf']): # 允许大小写
                self.custom_font_path.set(files[0])
            else:
                messagebox.showwarning("拖放错误", "请拖放一个字体文件（.ttf 或 .otf）。")

    # 根据水印类型切换显示不同的设置选项
    def _update_watermark_options(self):
        selected_type = self.watermark_type_var.get()
        if selected_type == 'image':
            self.img_frame.pack(pady=5, fill="x")
            self.text_frame.pack_forget() # 隐藏文字水印设置
        elif selected_type == 'text':
            self.img_frame.pack_forget() # 隐藏图片水印设置
            self.text_frame.pack(pady=5, fill="x")
            # 确保字体选择框在文字水印模式下显示
            self.font_selection_frame.pack(pady=5, fill="x", columnspan=2)

    # 根据“图片化”复选框的状态，启用/禁用相关选项
    def _toggle_image_options(self):
        if self.convert_to_image_var.get():
            self.quality_combo.config(state="readonly") # 启用品质选择下拉菜单
            self.invert_checkbutton.config(state="normal") # 启用反色复选框
        else:
            self.quality_combo.config(state="disabled") # 禁用品质选择下拉菜单
            self.invert_checkbutton.config(state="disabled") # 禁用反色复选框
            self.invert_colors_var.set(False) # 同时取消反色选项

    # --- 开始处理 PDF 的主逻辑 ---
    def _start_conversion(self):
        input_pdf = self.pdf_entry.get()

        # 检查输入PDF是否有效
        if not input_pdf or not os.path.exists(input_pdf):
            messagebox.showerror("错误", "请选择有效的 PDF 文件。")
            return

        base_name = os.path.splitext(os.path.basename(input_pdf))[0]
        output_pdf_suffix = "" # 用于构建输出文件名后缀

        # 获取各操作选项的状态
        convert_to_image = self.convert_to_image_var.get()
        apply_invert = self.invert_colors_var.get()
        image_quality = self.image_quality_var.get() # 获取选择的图片品质
        open_password = self.open_pw_entry.get()
        edit_password = self.edit_pw_entry.get()

        has_password_operation = bool(open_password or edit_password)
        watermark_type = self.watermark_type_var.get()
        has_watermark_operation = False
        custom_font_path_val = self.custom_font_path.get() # 获取自定义字体路径

        # 判断是否需要进行水印操作
        if watermark_type == 'image' and self.img_entry.get():
            has_watermark_operation = True
        elif watermark_type == 'text' and self.text_entry.get():
            has_watermark_operation = True

        # 初始化水印相关参数的默认值
        rotation_angle = 0
        opacity_level = 0.15
        rows = 5
        cols = 4
        watermark_size_percent = 0.8

        # 如果有水印操作，则获取水印相关参数
        if has_watermark_operation:
            try:
                rows = int(self.rows_entry.get())
                if not (1 <= rows <= 100):
                    raise ValueError("行数必须在 1 到 100 之间。")
            except ValueError:
                messagebox.showerror("错误", "行数请输入 1 到 100 之间的整数。")
                return

            try:
                cols = int(self.cols_entry.get())
                if not (1 <= cols <= 100):
                    raise ValueError("列数必须在 1 到 100 之间。")
            except ValueError:
                messagebox.showerror("错误", "列数请输入 1 到 100 之间的整数。")
                return

            try:
                watermark_size_percent = float(self.size_percent_entry.get()) / 100.0
                if not (0.01 <= watermark_size_percent <= 1.0): # 1% 到 100%
                    raise ValueError("水印大小百分比必须在 1 到 100 之间。")
            except ValueError:
                messagebox.showerror("错误", "水印大小请输入 1 到 100 之间的数字。")
                return

            try:
                rotation_angle = float(self.rotation_entry.get())
                if not (0 <= rotation_angle <= 360):
                    raise ValueError("旋转角度必须在 0 到 360 之间。")
            except ValueError:
                messagebox.showerror("错误", "旋转角度请输入有效数字 (0-360)。")
                return

            try:
                opacity_level = float(self.opacity_entry.get())
                if not (0.0 <= opacity_level <= 1.0):
                    raise ValueError("透明度必须在 0.0 到 1.0 之间。")
            except ValueError:
                messagebox.showerror("错误", "透明度请输入有效数字 (0.0-1.0)。")
                return

            if watermark_type == 'image':
                actual_watermark_source = self.img_entry.get()
                if not actual_watermark_source or not os.path.exists(actual_watermark_source):
                    messagebox.showerror("错误", "请选择有效的图片文件作为水印。")
                    return

            elif watermark_type == 'text':
                actual_watermark_source = self.text_entry.get()
                if not actual_watermark_source:
                    messagebox.showerror("错误", "文本水印内容不能为空。")
                    return
                # 检查自定义字体路径是否有效（如果用户选择了）
                if custom_font_path_val and not os.path.exists(custom_font_path_val):
                    messagebox.showerror("错误", "您选择的字体文件不存在。请检查路径或选择其他字体。")
                    return

        # 强制要求勾选“将PDF图片化”才能“应用反色”
        if apply_invert and not convert_to_image:
            messagebox.showerror("操作冲突", "您选择了“应用反色”，但未勾选“将PDF图片化”。\n\n"
                                 "反色处理必须基于图片化的PDF页面。请勾选“将PDF图片化”后再试。")
            self.status_label.config(text="操作已取消。")
            return

        # 密码组合验证逻辑：禁止只设置打开密码而不设置编辑密码的不安全组合
        if open_password and not edit_password:
            messagebox.showerror("操作受限",
                                 "安全警告：您只设置了打开密码，但没有设置编辑密码。\n\n"
                                 "为确保 PDF 安全（尤其在使用 256 位加密时），此操作组合被禁止。\n\n"
                                 "请同时设置一个编辑密码以继续，或取消此操作。")
            self.status_label.config(text="操作已取消。请设置编辑密码。")
            return

        # 构建输出文件名后缀
        if has_watermark_operation:
            output_pdf_suffix += "_watermarked"
        if convert_to_image:
            output_pdf_suffix += f"_image_processed_{image_quality}" # 添加品质信息
            if apply_invert:
                output_pdf_suffix += "_inverted"
        if has_password_operation:
            output_pdf_suffix += "_protected"

        final_output_pdf_name = f"{base_name}{output_pdf_suffix}.pdf"

        # 如果用户没有选择任何操作，则提示
        if not has_watermark_operation and not convert_to_image and not has_password_operation:
            messagebox.showwarning("操作警告", "请至少选择一项操作（添加水印、图片化处理或设置密码）。")
            return

        # 更新状态标签并刷新UI
        self.status_label.config(text="正在处理PDF，请稍等...")
        self.root.update() # 立即更新UI

        current_pdf_for_processing = input_pdf # 当前要处理的PDF路径
        temp_files_to_clean = [] # 记录生成的临时文件，以便最后清理

        try:
            # 确定临时文件保存目录
            temp_dir = os.path.dirname(input_pdf)
            if not temp_dir or not os.access(temp_dir, os.W_OK):
                temp_dir = os.getcwd() # 如果无法写入源目录，则使用当前工作目录

            # --- 步骤 1: 添加水印 ---
            if has_watermark_operation:
                self.status_label.config(text="正在添加水印...")
                self.root.update_idletasks() # 立即更新UI

                watermarked_output_path = os.path.join(temp_dir, f"{base_name}_temp_watermarked_{os.urandom(4).hex()}.pdf")
                pdf_logic.add_watermark(current_pdf_for_processing, watermarked_output_path,
                                    watermark_type=watermark_type,
                                    watermark_source=actual_watermark_source,
                                    rows=rows,
                                    cols=cols,
                                    opacity_level=opacity_level,
                                    rotation_angle=rotation_angle,
                                    watermark_size_percent=watermark_size_percent,
                                    custom_font_path=custom_font_path_val # 传递自定义字体路径
                                   )
                current_pdf_for_processing = watermarked_output_path
                # 如果前一步骤生成了临时文件，则加入待清理列表
                if current_pdf_for_processing != input_pdf:
                    temp_files_to_clean.append(watermarked_output_path)

            # --- 步骤 2: 图片化处理 (包括反色) ---
            if convert_to_image:
                self.status_label.config(text="正在将PDF转换为图片...")
                self.root.update_idletasks()

                image_processed_output_path = os.path.join(temp_dir, f"{base_name}_temp_image_processed_{os.urandom(4).hex()}.pdf")

                pdf_logic.process_pdf_to_image(current_pdf_for_processing, image_processed_output_path,
                                              invert_colors=apply_invert,
                                              status_callback=lambda text: self._update_status(text),
                                              quality=image_quality # 传递品质参数
                                              )
                # 清理前一步骤生成的临时文件（如果存在且不是原始输入文件）
                if current_pdf_for_processing != input_pdf and current_pdf_for_processing not in temp_files_to_clean:
                    temp_files_to_clean.append(current_pdf_for_processing)
                current_pdf_for_processing = image_processed_output_path
                # 将当前步骤的输出文件加入待清理列表
                if current_pdf_for_processing not in temp_files_to_clean:
                    temp_files_to_clean.append(image_processed_output_path)


            # --- 步骤 3: 添加密码保护 ---
            if has_password_operation:
                self.status_label.config(text="正在添加密码和权限...")
                self.root.update_idletasks()

                # 如果没有密码，应该在前端已阻止，这里作为最后的防线
                if not open_password and not edit_password:
                    raise ValueError("请至少设置一个打开密码或编辑密码。")

                pdf_logic.protect_pdf_with_qpdf(current_pdf_for_processing, final_output_pdf_name, open_password, edit_password)

                # 如果当前处理的PDF是临时文件，加入清理列表
                if current_pdf_for_processing != input_pdf and os.path.exists(current_pdf_for_processing):
                    if current_pdf_for_processing not in temp_files_to_clean:
                        temp_files_to_clean.append(current_pdf_for_processing)
            else:
                # 如果没有密码操作，但前面有其他操作生成了临时文件，则将临时文件重命名为最终文件名
                if current_pdf_for_processing != input_pdf:
                    # 避免同名文件重命名错误
                    if os.path.abspath(current_pdf_for_processing) != os.path.abspath(final_output_pdf_name):
                        try:
                            os.rename(current_pdf_for_processing, final_output_pdf_name)
                            # 如果成功重命名，则不需要删除这个文件了
                            if current_pdf_for_processing in temp_files_to_clean:
                                temp_files_to_clean.remove(current_pdf_for_processing)
                        except OSError as e:
                            messagebox.showerror("文件重命名错误", f"无法将临时文件重命名为最终文件：{e}\n\n文件可能已保存为临时名称：{current_pdf_for_processing}")
                            self.status_label.config(text="重命名失败，请手动查找输出文件。")
                            return

            # 所有处理成功完成
            messagebox.showinfo("处理成功", f"✅ PDF 已成功处理并保存为：\n{final_output_pdf_name}")
            self.status_label.config(text="") # 清空状态标签

        except FileNotFoundError as e:
            messagebox.showerror("处理失败", str(e) + "\n\n请确保 QPDF 已安装并添加到系统 PATH 中。")
            self.status_label.config(text="")
        except Exception as e:
            messagebox.showerror("处理失败", f"❌ 处理过程中发生错误：\n{str(e)}")
            self.status_label.config(text="")
        finally:
            # 清理所有临时文件
            for temp_file in temp_files_to_clean:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except OSError as e:
                        print(f"警告: 无法删除临时文件 {temp_file}: {e}")

    def _update_status(self, message):
        self.status_label.config(text=message)
        # 强制更新UI，确保状态信息实时显示
        self.root.update_idletasks()

    # 窗口关闭时的确认提示
    def on_closing(self):
        if messagebox.askokcancel("退出", "您确定要退出程序吗？"):
            self.root.destroy()

# 主程序入口
if __name__ == "__main__":
    root = TkinterDnD.Tk() # 使用 TkinterDnD.Tk() 替代 tk.Tk() 以支持拖放
    app = PDFProcessorApp(root)
    root.mainloop()