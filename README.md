# PDF 批量处理工具 使用说明书

欢迎使用 PDF 批量处理工具！这是一个基于 Python 的桌面应用程序，旨在帮助您方便快捷地为 PDF 文件添加水印、将其图片化（以便防止文本选中和复制），以及设置密码保护。

---

## 一、运行环境准备 (重要！)

由于这是一个 Python 程序，用户需要先准备好 Python 运行环境和相关的库。

### 1. 安装 Python

### a) Windows 电脑

1.  **下载 Python 安装包：** 访问 Python 官方网站：[https://www.python.org/downloads/](https://www.python.org/downloads/)。
2.  在 "Windows" 部分，下载最新稳定版本的 **Python 安装器**（推荐 Python 3.8 或更高版本）。通常选择 "Windows installer (64-bit)"。
3.  **运行安装器：** 双击下载的 `.exe` 文件开始安装。
4.  **重要步骤：** 在安装界面的第一个屏幕，**务必勾选 “Add Python.exe to PATH” 选项**。这能确保您可以在命令行中直接运行 Python 命令。
5.  点击 "Install Now" 或 "Customize installation" (如果您需要自定义安装路径)。
6.  等待安装完成。

### b) Mac 电脑

1.  **下载 Python 安装包：** 访问 Python 官方网站：[https://www.python.org/downloads/](https://www.python.org/downloads/)。
2.  在 "macOS" 部分，下载最新稳定版本的 **Python 安装器**（推荐 Python 3.8 或更高版本）。通常选择 "macOS 64-bit universal2 installer" 或 "macOS 64-bit Intel installer"。
3.  **运行安装器：** 双击下载的 `.pkg` 文件，按照提示完成安装。Python 通常会自动配置 PATH。
4.  **验证安装：** 打开“**终端**” (Terminal) 应用程序，输入 `python3 --version` 并按回车。如果显示了 Python 版本号，则表示安装成功。

### 2. 安装所需 Python 库

无论是 Windows 还是 Mac，安装 Python 库的步骤都是相同的：

1.  **打开命令行工具：**
    * **Windows：** 搜索 "cmd" 或 "PowerShell" 并打开。
    * **Mac：** 打开 "**终端**" (Terminal) 应用程序。
2.  在命令行中运行以下命令，安装程序所需的 Python 库：
    ```bash
    pip install Pillow PyMuPDF tkinterdnd2
    ```
    （在 Mac 上，如果 `pip` 命令无效，可能需要使用 `pip3`：`pip3 install Pillow PyMuPDF tkinterdnd2`）

### 3. 关于 QPDF (额外工具，用于密码保护)

本工具的**密码保护功能**依赖一个名为 **QPDF** 的外部命令行工具。

**如果您需要使用密码保护功能，请务必安装 QPDF 并将其添加到系统环境变量 (PATH) 中。**

* **QPDF 官方下载地址：** [https://qpdf.readthedocs.io/en/stable/download.html](https://qpdf.readthedocs.io/en/stable/download.html)

### a) Windows 电脑 (安装 QPDF)

1.  访问 QPDF 官方下载页面，下载适用于 Windows 的压缩包（例如 `qpdf-*-mingw64.zip`）。
2.  将下载的压缩包解压到您希望存放软件的位置（例如 `C:\Program Files\qpdf`）。
3.  **添加 QPDF 到 PATH：**
    * 右键点击“**此电脑**”或“**我的电脑**”图标，选择“**属性**”。
    * 点击“**高级系统设置**”。
    * 点击“**环境变量**”按钮。
    * 在“**系统变量**”下找到名为 `Path` 的变量，选中它，然后点击“**编辑**”。
    * 点击“**新建**”，然后粘贴您解压的 QPDF 文件夹中 `bin` 目录的完整路径（例如 `C:\Program Files\qpdf-xx.x.x\bin`，`xx.x.x` 是版本号）。
    * 一路点击“**确定**”关闭所有窗口。
4.  **验证安装：** 打开一个新的命令行窗口，输入 `qpdf --version` 并按回车。如果显示了 QPDF 的版本信息，则表示安装成功。

### b) Mac 电脑 (安装 QPDF)

Mac 用户通常可以使用 Homebrew 包管理器来安装 QPDF，这非常方便。

1.  **安装 Homebrew (如果尚未安装)：** 打开“**终端**” (Terminal)，运行以下命令：
    ```bash
    /bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"
    ```
    按照提示完成安装，可能需要输入您的电脑密码。
2.  **安装 QPDF：** 在终端中运行以下命令：
    ```bash
    brew install qpdf
    ```
3.  **验证安装：** 在终端中输入 `qpdf --version` 并按回车。如果显示了 QPDF 的版本信息，则表示安装成功。

---

## 二、程序文件准备

1.  请确保您已获得以下两个程序文件：
    * `pdf_processor_app.py` (主程序文件)
    * `pdf_logic.py` (核心处理逻辑文件)
2.  将这两个文件**放在同一个文件夹**中。

---

## 三、如何启动程序

### 1. 通过命令行启动 (推荐)

1.  **打开命令行工具** (Windows: Command Prompt/PowerShell; Mac: Terminal)。
2.  使用 `cd` 命令**导航**到存放 `pdf_processor_app.py` 的文件夹目录。
    * 例如 (Windows)：`cd C:\Users\YourUser\Documents\PDF工具`
    * 例如 (Mac)：`cd /Users/YourUser/Documents/PDF工具`
3.  运行以下命令启动程序：
    ```bash
    python pdf_processor_app.py
    ```
    （在 Mac 上，如果 `python` 命令无效，可能需要使用 `python3`：`python3 pdf_processor_app.py`）

### 2. 通过文件管理器直接启动 (如果 Python 配置正确)

1.  在文件管理器中，找到 `pdf_processor_app.py` 文件。
2.  **双击**该文件。如果您的 Python 环境配置正确，程序窗口应该会直接弹出。

---

## 四、界面与功能说明

程序界面分为几个主要区域：

### 1. PDF 文件选择区域

* **“选择或拖放 PDF 文件:”**：点击 **“浏览 PDF”** 按钮选择您要处理的 PDF 文件，或者直接将 PDF 文件拖放到旁边的输入框中。

### 2. 操作标签页

* **水印设置**：为 PDF 添加图片水印或文字水印。
    * **水印类型**：选择 **“图片水印”** 或 **“文字水印”**。
    * **图片水印设置**：选择或拖放水印图片文件（支持 `.jpg`, `.png` 等）。
    * **文字水印设置**：输入您想作为水印的文字。
        * **字体选择**：可以点击 **“浏览字体”** 选择您电脑上的 `.ttf` 或 `.otf` 字体文件，留空则使用默认字体。
    * **平铺设置**：
        * **行数 (1-100)**：设置水印在页面上垂直平铺的行数。
        * **列数 (1-100)**：设置水印在页面上水平平铺的列数。
        * **水印大小 (1-100%)**：设置每个水印相对于其平铺单元格大小的百分比。
    * **通用设置**：
        * **旋转角度 (0-360)**：设置水印的旋转角度。
        * **不透明度 (0.0-1.0)**：设置水印的透明度，0.0 为完全透明，1.0 为完全不透明。

* **图片化处理**：将 PDF 的每一页转换为图片，从而使 PDF 文本不可选中、不可复制。
    * **“将PDF图片化 (文本不可选)”**：勾选此项启用图片化处理。
    * **图片品质**：选择输出图片的品质（低、中、高），会影响文件大小和清晰度。
    * **“应用反色”**：勾选此项会在图片化后将页面颜色反转（例如，黑底白字变为白底黑字）。**此功能必须在勾选“将PDF图片化”后才能启用。**

* **密码设置**：为输出的 PDF 文件添加密码保护。
    * **打开密码 (用户密码)**：设置打开 PDF 文件所需的密码。
    * **编辑密码 (所有者密码)**：设置用于修改 PDF 权限（如打印、复制内容）的密码。
    * **重要提示**：为确保 PDF 安全，**如果您设置了“打开密码”，则必须同时设置“编辑密码”**。只设置打开密码而不设置编辑密码是不允许的。

### 3. “开始处理 PDF” 按钮

* 点击此按钮开始执行您在上面选定的所有操作。

### 4. 状态标签

* 显示当前处理进度和结果信息。

---

## 五、使用流程

1.  **选择 PDF 文件**：点击“浏览 PDF”或拖放您的 PDF 文件到指定框中。
2.  **选择操作**：根据您的需求，在“水印设置”、“图片化处理”和“密码设置”这三个标签页中勾选相应的选项并填写参数。
    * 您可以单独选择一个操作，也可以组合选择多个操作（例如：先添加水印，再图片化，最后加密）。
3.  **点击“开始处理 PDF”**：程序将按顺序执行所选操作。
4.  **等待完成**：处理过程中，状态标签会显示进度。完成后，会弹出提示框，处理后的 PDF 文件会保存在原始 PDF 文件所在的目录，并以 `_watermarked`、`_image_processed`、`_protected` 等后缀命名。

---

## 六、注意事项

* **原始文件安全**：本工具会生成新的 PDF 文件，不会直接修改您的原始 PDF 文件，请放心使用。
* **文件路径**：请确保您选择的 PDF 文件、水印图片文件以及自定义字体文件的路径是有效的。
* **处理时间**：处理大型或多页的 PDF 文件可能需要一些时间，请耐心等待。
* **QPDF 错误**：如果出现与 QPDF 相关的错误，请检查 QPDF 是否已正确安装并添加到系统 PATH。
* **图片化与文本**：一旦 PDF 被图片化，其中的文本将变为图像，无法再被选中、复制或搜索。
* **密码组合**：请务必遵循密码设置的规则，即如果设置了打开密码，则必须同时设置编辑密码。

---

希望这份详细的说明书能帮助您顺利使用 PDF 批量处理工具！您在使用过程中还有其他疑问吗？