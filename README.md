# Visitor Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey)

## About
A web-based Visitor Management System built with Flask during my internship at WCL. It allows organizations to register visitors, capture their details, and maintain a log — all through a simple browser interface.

## Problem it Solves
Manual visitor registers at offices are slow, hard to search, and easy to lose. This system digitizes the process — faster registration, searchable records, and photo capture.

## Features
- Visitor registration with name, contact info, and photo
- Real-time photo capture using OpenCV
- Visitor records stored in MySQL database
- Clean UI built with HTML/CSS

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Frontend | HTML, CSS |
| Database | MySQL |
| Image Capture | OpenCV |

## Screenshots
> *(Add screenshots here)*

## Installation

### Requirements
- Python 3.x
- MySQL Workbench installed and running

```bash
git clone https://github.com/souravi12/visitor_system.git
cd visitor_system
pip install -r requirements.txt
```

Configure your MySQL credentials in `app.py`, then:

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

## Developer
Built by Souravi — internship project at WCL.
```

Also I'd recommend deleting `database.db` from your repo since you're using MySQL — it's just a confusing leftover file. Want help doing that?
