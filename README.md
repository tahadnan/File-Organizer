# 🗂️ File Organizer
<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

</div>

A powerful CLI application that helps you organize your messy directories by automatically categorizing and moving files based on their extensions. Say goodbye to cluttered folders! 🚀

## ✨ Features

- 📁 Automatically organizes files into appropriate categories
- 🎨 Support for common file types (documents, images, videos, audio, etc.)
- ⚙️ Customizable file extension mappings
- 🔄 Progress tracking with rich console output
- 🎯 Simple and intuitive command-line interface

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/tahadnan/File-Organizer.git
cd File-Organizer
```

2. Install required dependencies:
```bash
pip install -r requiremts.txt
```

## 💡 Usage

Basic usage to organize a directory:
```bash
python main.py /path/to/directory
```

### Command Line Arguments

- `dirname`: The directory to be organized (required)
- `-c, --custom-mapping`: Path to a JSON file with custom extension mappings
- `-o, --overwrite`: Overwrite default mappings with custom ones completely
- `-v, --verbose`: Display detailed progress instead of a progress bar

### Examples

1. Organize current directory with default settings:
```bash
python <script_path> .
```

2. Organize with custom mappings:
```bash
python main.py /Downloads -c custom_mappings.json
```

3. Use verbose output:
```bash
python main.py /Documents -v
```

## 📝 Custom Mappings

You can create your own extension mappings using a JSON file. Here's an example structure:

```json
{
    "work": [".doc", ".docx", ".pdf"],
    "images": [".png", ".jpg", ".gif"],
    "custom_category": [".xyz", ".abc"]
}
```

## 📂 Default Categories

The organizer comes with the following default categories:

- 📄 Documents (`.pdf`, `.doc`, `.docx`, `.txt`, etc.)
- 🖼️ Images (`.jpg`, `.png`, `.gif`, etc.)
- 🎥 Videos (`.mp4`, `.avi`, `.mkv`, etc.)
- 🎵 Audio (`.mp3`, `.wav`, `.flac`, etc.)
- 📦 Archives (`.zip`, `.rar`, `.7z`, etc.)
- 💻 Code (`.py`, `.java`, `.cpp`, etc.)
- ⚙️ Executables (`.exe`, `.msi`, `.app`, etc.)
- 🗄️ Databases (`.db`, `.sqlite`, etc.)

## ⚠️ Important Notes

- The program will create directories for each category as needed
- Files with unsupported extensions will be skipped
- Existing files in destination folders won't be overwritten
- Use the `-v` flag to see detailed progress and any potential errors

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Submit a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Inspired by the need for a clean and organized file system

---

Made with ❤️ by [Taha Adnan](https://github.com/tahadnan)
