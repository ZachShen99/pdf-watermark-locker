PDF Batch Processing Tool User Manual
Welcome to the PDF Batch Processing Tool! This Python-based desktop application enables you to efficiently add watermarks, convert PDFs to images (to prevent text selection and copying), and apply password protection to your PDF files.

1. Setting Up the Environment
To use this tool, you must first set up the Python environment and install the required libraries. Follow these steps carefully.
1.1 Installing Python
Windows

Download Python: Visit python.org/downloads and download the latest stable version (Python 3.8 or higher recommended). Select the Windows installer (64-bit).
Run the Installer: Double-click the downloaded .exe file to start the installation.
Important: On the first installation screen, check "Add Python.exe to PATH" to enable running Python from the command line.
Choose Install Now or Customize installation (to select a custom path).
Wait for the installation to complete.

macOS

Download Python: Visit python.org/downloads and download the latest stable version (Python 3.8 or higher recommended). Select the macOS 64-bit universal2 installer or macOS 64-bit Intel installer.
Run the Installer: Double-click the downloaded .pkg file and follow the prompts. Python typically configures PATH automatically.
Verify Installation: Open the Terminal app, type python3 --version, and press Enter. A displayed version number confirms successful installation.

1.2 Installing Required Python Libraries
For both Windows and macOS, follow these steps:

Open a Command-Line Tool:
Windows: Search for "cmd" or "PowerShell".
macOS: Open the Terminal app.


Run the following command to install required libraries:pip install Pillow PyMuPDF tkinterdnd2

On macOS, if pip doesn’t work, use:pip3 install Pillow PyMuPDF tkinterdnd2



1.3 Installing QPDF (Required for Password Protection)
The password protection feature requires QPDF, an external command-line tool. Install it and add it to your system’s PATH.
Windows

Visit qpdf.readthedocs.io and download the Windows package (e.g., qpdf-*-mingw64.zip).
Extract the package to a folder (e.g., C:\Program Files\qpdf).
Add QPDF to PATH:
Right-click This PC or My Computer, select Properties.
Click Advanced system settings > Environment Variables.
Under System Variables, find and select the Path variable, then click Edit.
Click New and add the path to the QPDF bin folder (e.g., C:\Program Files\qpdf-xx.x.x\bin, where xx.x.x is the version number).
Click OK to close all windows.


Verify Installation: Open a new command-line window, type qpdf --version, and press Enter. A displayed version number confirms success.

macOS

Install Homebrew (if not installed): In Terminal, run:/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Follow the prompts, entering your password if required.
Install QPDF: Run:brew install qpdf


Verify Installation: Type qpdf --version in Terminal and press Enter. A displayed version number confirms success.


2. Preparing Program Files

Ensure you have the following files:
pdf_processor_app.py (main application file)
pdf_logic.py (core processing logic)


Place both files in the same folder.


3. Launching the Program
3.1 Via Command Line (Recommended)

Open a command-line tool:
Windows: Command Prompt or PowerShell.
macOS: Terminal.


Navigate to the folder containing pdf_processor_app.py using the cd command:
Example (Windows): cd C:\Users\YourUser\Documents\PDFTool
Example (macOS): cd /Users/YourUser/Documents/PDFTool


Run the program:python pdf_processor_app.py

On macOS, if python doesn’t work, use:python3 pdf_processor_app.py



3.2 Via File Explorer (If Python is Configured)

Locate pdf_processor_app.py in your file explorer.
Double-click the file. If Python is correctly configured, the application window will open.


4. Interface and Features
The program interface is divided into key sections:
4.1 PDF File Selection

Select or Drag-and-Drop PDF Files: Click Browse PDF to select a PDF file or drag and drop it into the input field.

4.2 Operation Tabs

Watermark Settings: Add image or text watermarks.

Watermark Type: Choose Image Watermark or Text Watermark.
Image Watermark: Select or drag a watermark image (supports .jpg, .png, etc.).
Text Watermark: Enter the desired watermark text.
Font Selection: Click Browse Font to choose a .ttf or .otf font file. Leave blank for the default font.


Tiling Settings:
Rows (1–100): Set the number of vertical watermark tiles.
Columns (1–100): Set the number of horizontal watermark tiles.
Watermark Size (1–100%): Adjust the watermark size relative to its tile cell.


General Settings:
Rotation Angle (0–360°): Set the watermark’s rotation.
Opacity (0.0–1.0): Adjust transparency (0.0 = fully transparent, 1.0 = fully opaque).




Image Conversion: Convert PDF pages to images, preventing text selection or copying.

Enable Image Conversion: Check Convert PDF to Image (Text Unselectable).
Image Quality: Select Low, Medium, or High (affects file size and clarity).
Invert Colors: Check to reverse page colors (e.g., black background to white). Requires image conversion to be enabled.


Password Settings: Add password protection to the output PDF.

Open Password (User Password): Set a password to open the PDF.
Edit Password (Owner Password): Set a password for modifying permissions (e.g., printing, copying).
Important: If an open password is set, an edit password _



must also be set. Setting only an open password is not allowed.
4.3 Start Processing Button

Click Start Processing PDF to execute the selected operations.

4.4 Status Label

Displays processing progress and results.


5. Usage Workflow

Select PDF File: Click Browse PDF or drag and drop a PDF into the input field.
Configure Operations: Select and configure options in the Watermark Settings, Image Conversion, and Password Settings tabs. You can use one or combine multiple operations (e.g., watermark, then convert to image, then encrypt).
Start Processing: Click Start Processing PDF to begin.
Wait for Completion: The status label shows progress. Upon completion, a prompt appears, and the processed PDF is saved in the same directory as the original, with suffixes like _watermarked, _image_processed, or _protected.


6. Important Notes

Original File Safety: The tool creates new PDF files without modifying the original.
File Paths: Ensure paths for PDF files, watermark images, and custom fonts are valid.
Processing Time: Large or multi-page PDFs may take time to process.
QPDF Errors: If QPDF-related errors occur, verify that QPDF is installed and added to PATH.
Image Conversion: Converted PDFs become images, making text unselectable, uncopyable, and unsearchable.
Password Rules: If setting an open password, an edit password must also be set.


We hope this manual helps you effectively use the PDF Batch Processing Tool! If you have further questions, feel free to ask.
