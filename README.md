# PDF Batch Processing Tool User Manual

Welcome to the PDF Batch Processing Tool! This is a Python-based desktop application designed to help you quickly and conveniently watermark PDF files, convert them to images (to prevent text selection and copying), and set password protection.

---

## 1. Environment Setup (Important!)

Since this is a Python program, users need to prepare the Python runtime environment and necessary libraries.

### 1.1. Install Python

### a) For Windows Users

1.  **Download Python Installer:** Visit the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/).
2.  In the "Windows" section, download the latest stable version of the **Python installer** (Python 3.8 or higher is recommended). Typically, choose "Windows installer (64-bit)".
3.  **Run the Installer:** Double-click the downloaded `.exe` file to start the installation.
4.  **Crucial Step:** On the first screen of the installation wizard, **make sure to check the "Add Python.exe to PATH" option**. This ensures you can run Python commands directly from the command line.
5.  Click "Install Now" or "Customize installation" (if you need to customize the installation path).
6.  Wait for the installation to complete.

### b) For Mac Users

1.  **Download Python Installer:** Visit the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/).
2.  In the "macOS" section, download the latest stable version of the **Python installer** (Python 3.8 or higher is recommended). Typically, choose "macOS 64-bit universal2 installer" or "macOS 64-bit Intel installer".
3.  **Run the Installer:** Double-click the downloaded `.pkg` file and follow the prompts to complete the installation. Python usually configures the PATH automatically.
4.  **Verify Installation:** Open the "**Terminal**" application, type `python3 --version`, and press Enter. If the Python version number is displayed, the installation was successful.

### 1.2. Install Required Python Libraries

For both Windows and Mac, the steps to install Python libraries are the same:

1.  **Open your Command Line Tool:**
    * **Windows:** Search for "cmd" or "PowerShell" and open it.
    * **Mac:** Open the "**Terminal**" application.
2.  Run the following command in the command line to install the Python libraries required by the program:
    ```bash
    pip install Pillow PyMuPDF tkinterdnd2
    ```
    (On Mac, if the `pip` command doesn't work, you might need to use `pip3`: `pip3 install Pillow PyMuPDF tkinterdnd2`)

### 1.3. About QPDF (External Tool for Password Protection)

This tool's **password protection feature** relies on an external command-line tool called **QPDF**.

**If you need to use the password protection feature, you must install QPDF and add it to your system's environment variables (PATH).**

* **Official QPDF Download Link:** [https://qpdf.readthedocs.io/en/stable/download.html](https://qpdf.readthedocs.io/en/stable/download.html)

### a) For Windows Users (Installing QPDF)

1.  Visit the official QPDF download page and download the archive suitable for Windows (e.g., `qpdf-*-mingw64.zip`).
2.  Extract the downloaded archive to your preferred software location (e.g., `C:\Program Files\qpdf`).
3.  **Add QPDF to PATH:**
    * Right-click the "**This PC**" or "**My Computer**" icon, then select "**Properties**".
    * Click "**Advanced system settings**".
    * Click the "**Environment Variables...**" button.
    * Under "System variables", find the variable named `Path`, select it, and click "**Edit...**".
    * Click "**New**", then paste the full path to the `bin` directory within your extracted QPDF folder (e.g., `C:\Program Files\qpdf-xx.x.x\bin`, where `xx.x.x` is the version number).
    * Click "**OK**" all the way to close all windows.
4.  **Verify Installation:** Open a **new** command line window, type `qpdf --version`, and press Enter. If QPDF version information is displayed, the installation was successful.

### b) For Mac Users (Installing QPDF)

Mac users can typically install QPDF using the Homebrew package manager, which is very convenient.

1.  **Install Homebrew (if not already installed):** Open "**Terminal**" and run the following command:
    ```bash
    /bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"
    ```
    Follow the prompts to complete the installation; you might need to enter your computer's password.
2.  **Install QPDF:** In the Terminal, run the following command:
    ```bash
    brew install qpdf
    ```
3.  **Verify Installation:** In the Terminal, type `qpdf --version` and press Enter. If QPDF version information is displayed, the installation was successful.

---

## 2. Program File Preparation

1.  Please ensure you have obtained the following two program files:
    * `pdf_processor_app.py` (Main program file)
    * `pdf_logic.py` (Core processing logic file)
2.  Place both files **in the same folder**.

---

## 3. How to Launch the Program

### 3.1. Launch via Command Line (Recommended)

1.  **Open your command line tool** (Windows: Command Prompt/PowerShell; Mac: Terminal).
2.  Use the `cd` command to **navigate** to the folder containing `pdf_processor_app.py`.
    * Example (Windows): `cd C:\Users\YourUser\Documents\PDF_Tool`
    * Example (Mac): `cd /Users/YourUser/Documents/PDF_Tool`
3.  Run the following command to launch the program:
    ```bash
    python pdf_processor_app.py
    ```
    (On Mac, if the `python` command doesn't work, you might need to use `python3`: `python3 pdf_processor_app.py`)

### 3.2. Launch Directly from File Explorer (If Python is Configured Correctly)

1.  In your file explorer, locate the `pdf_processor_app.py` file.
2.  **Double-click** the file. If your Python environment is configured correctly, the program window should pop up directly.

---

## 4. Interface and Functionality Description

The program interface is divided into several main areas:

### 4.1. PDF File Selection Area

* **"Select or Drag & Drop PDF File:"**: Click the **"Browse PDF"** button to select the PDF file you want to process, or directly drag and drop the PDF file into the adjacent input box.

### 4.2. Operation Tabs

* **Watermark Settings**: Add image watermarks or text watermarks to your PDF.
    * **Watermark Type**: Choose **"Image Watermark"** or **"Text Watermark"**.
    * **Image Watermark Settings**: Select or drag & drop an image file for the watermark (supports `.jpg`, `.png`, etc.).
    * **Text Watermark Settings**: Enter the text you want to use as a watermark.
        * **Font Selection**: You can click **"Browse Font"** to select a `.ttf` or `.otf` font file from your computer; leave blank to use the default font.
    * **Tiling Settings**:
        * **Rows (1-100)**: Set the number of rows for vertical tiling of watermarks on the page.
        * **Columns (1-100)**: Set the number of columns for horizontal tiling of watermarks on the page.
        * **Watermark Size (1-100%)**: Set the percentage of each watermark relative to its tiling cell size.
    * **General Settings**:
        * **Rotation Angle (0-360)**: Set the rotation angle for the watermark.
        * **Opacity (0.0-1.0)**: Set the transparency of the watermark, where 0.0 is completely transparent and 1.0 is completely opaque.

* **Image Conversion Processing**: Convert each page of the PDF into an image, making PDF text unselectable and uncopyable.
    * **"Convert PDF to Image (Text Unselectable)"**: Check this option to enable image conversion.
    * **Image Quality**: Select the output image quality (Low, Medium, High), which will affect file size and clarity.
    * **"Apply Invert Colors"**: Check this option to invert page colors after image conversion (e.g., black text on white background becomes white text on black background). **This feature can only be enabled if "Convert PDF to Image" is checked.**

* **Password Settings**: Add password protection to the output PDF file.
    * **Open Password (User Password)**: Set the password required to open the PDF file.
    * **Edit Password (Owner Password)**: Set the password used to modify PDF permissions (e.g., printing, copying content).
    * **Important Note**: To ensure PDF security, **if you set an "Open Password", you must also set an "Edit Password"**. Setting only an Open Password without an Edit Password is not allowed.

### 4.3. "Start PDF Processing" Button

* Click this button to start performing all selected operations.

### 4.4. Status Label

* Displays current processing progress and result information.

---

## 5. Usage Workflow

1.  **Select PDF File**: Click "Browse PDF" or drag and drop your PDF file into the designated box.
2.  **Select Operations**: Based on your needs, check the corresponding options and fill in the parameters in the "Watermark Settings", "Image Conversion Processing", and "Password Settings" tabs.
    * You can select a single operation or combine multiple operations (e.g., add a watermark, then convert to image, then encrypt).
3.  **Click "Start PDF Processing"**: The program will execute the selected operations in order.
4.  **Wait for Completion**: During processing, the status label will display the progress. Upon completion, a prompt box will appear, and the processed PDF file will be saved in the same directory as the original PDF file, named with suffixes like `_watermarked`, `_image_processed`, `_protected`, etc.

---

## 6. Important Notes

* **Original File Safety**: This tool generates new PDF files and does not directly modify your original PDF files, so please use it with confidence.
* **File Paths**: Please ensure that the paths to your selected PDF file, watermark image file, and custom font file are valid.
* **Processing Time**: Processing large or multi-page PDF files may take some time; please be patient.
* **QPDF Errors**: If you encounter errors related to QPDF, please check if QPDF is correctly installed and added to your system's PATH.
* **Image Conversion and Text**: Once a PDF is converted to an image, the text within it becomes part of the image and can no longer be selected, copied, or searched.
* **Password Combination**: Please strictly follow the password setting rules: if you set an open password, you must also set an edit password.

---

We hope this detailed user manual helps you use the PDF Batch Processing Tool smoothly! Do you have any other questions during use?
