# Static Site Generator

_Static Site Generator is a program written in Python that takes Markdown files, transforms them into HTML using a customizable template, and builds a complete single-page site without databases or server-side logic._

---

## Table of Contents

- [Features](#features)
- [Motivation / Purpose](#motivation--purpose)
- [What I Did / My Contributions](#what-i-did--my-contributions)
- [Installation & Usage](#installation--usage)
- [Screenshots / Examples](#screenshots--examples)
- [Technologies Used](#technologies-used)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

---

## Features

- Converts Markdown files into HTML
- Uses a customizable HTML template
- Automatically builds a complete single-page website
- Requires no database or server-side logic
- Outputs ready-to-use static HTML files

## Motivation / Purpose

This project was developed as part of my learning journey on [boot.dev](https://boot.dev), to practice and master Python programming.  
**My personal goal** _was to practice Object-Oriented Programming and improve my understanding of how real projects are structured. I focused on organizing code into clear, efficient, and well-structured components spread across different files. This hands-on experience really helped me grasp the concepts and enjoy the process of building maintainable code._

## What I Did / My Contributions

- Implemented core project functions following the course guidelines, applying OOP principles to process Markdown and generate HTML.  
- Developed methods to parse Markdown elements and convert them into HTML nodes.  
- Created functions to split input text into blocks and convert them into an HTML structure.  
- Set up file copying and output folder refreshing on each run.  
- Completed work under supervision; no independent enhancements added yet.

## Installation & Usage

1. Clone the repo:
   ```bash
   git clone https://github.com/TMalik26/Static-Site-Generator.git
   cd Static-Site-Generator
   ```
2. Make sure you have Python 3 installed.
3. Place your Markdown files in the content/ folder.
4. Place any images or static assets in the static/ folder.
5. Run the project:
   ```bash
  python main.py
  # or
  python3 main.py
   ```
6. To view the generated site, open the docs/ folder. You can simply open docs/index.html in your browser. Or, for a better experience, start a local server:
   ```bash
   cd docs
   python -m http.server 8000
   # or
   python3 -m http.server 8000
   ```
Then open http://localhost:8000 in your browser to browse the static site.

## Screenshots / Examples

_Add screenshots or examples of your project’s output here._

## Technologies Used

- Python 3.12.3
- Standard Python libraries: `sys`, `unittest`, `enum`, `re`, `textwrap`, `os`, `shutil`

## Acknowledgments

- [boot.dev](https://boot.dev) for the project base and guidance  
- [To identify basic Markdown syntax](https://www.markdownguide.org/cheat-sheet/)  
- [HTML elements reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements)  
- [Block-level content](https://developer.mozilla.org/en-US/docs/Glossary/Block-level_content)  
- [enum](https://docs.python.org/3/library/enum.html) — Support for enumerations  
- [unittest](https://docs.python.org/3/library/unittest.html) — Unit testing framework  
- [re](https://docs.python.org/3/library/re.html) — Regular expression operations  
- [pathlib](https://docs.python.org/3/library/pathlib.html) — Object-oriented filesystem paths  
- [sys](https://docs.python.org/3/library/sys.html) — System-specific parameters and functions  

## Contact

- [LinkedIn](https://www.linkedin.com/in/tetiana-malik-8bb32335a/)
