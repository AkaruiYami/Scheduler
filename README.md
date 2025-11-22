[![License: MIT](https://cdn.prod.website-files.com/5e0f1144930a8bc8aace526c/65dd9eb5aaca434fac4f1c34_License-MIT-blue.svg)](/LICENSE)
![GitHub last commit](https://img.shields.io/github/last-commit/AkaruiYami/Scheduler)

# Scheduler - Desktop Timetable Manager

A lightweight desktop application for managing weekly timetables and schedules. Built with PySimpleGUI, it provides a visual grid interface for organizing your weekly activities.

## ✨ Features

- **Visual Timetable Grid** - Weekday-based layout (Mon-Fri) with hourly time slots
- **Color-Coded Entries** - Each schedule item gets a unique color for easy identification
- **Multiple Timetable Support** - Create and save multiple schedule profiles
- **Right-Click Editing** - Quick edit or delete any existing entry
- **Screenshot Export** - Save your timetable as PNG images
- **Persistent Storage** - All timetables are saved locally and persist between sessions

## 🚀 Quick Start

### Installation

1. **Clone or download this repository**
2. **Install the required dependency:**
   ```bash
   pip install PySimpleGUI
   ```
3. **Run the application:**
   ```bash
   python main.py
   ```

### First Use

When you first open the application:
- You'll see an empty weekly grid (Mon-Fri, 7 AM - 6 PM)
- The dropdown menu will show "(New Timetable)" as your only option

## 📁 Project Structure

```
Scheduler/
├── main.py              # Main application entry point
├── layout.py            # UI layout definitions
├── ccolors.py           # Color management for schedule entries
├── models/              # Data models
│   ├── __init__.py
│   ├── timetable.py     # Timetable data structure
│   └── content.py       # Schedule entry content model
├── data/                # Saved timetables storage
├── screenshots/         # Screenshot exports
└── notes.txt            # Development notes
```

## ⚙️ Technical Details

**Default Schedule:**
- **Days:** Monday through Friday
- **Hours:** 7:00 AM to 6:00 PM
- **Time intervals:** 60 minutes
- **Time format:** 12-hour (e.g., "07:00AM", "01:00PM")

**Data Storage:**
- Timetables saved as pickle files (`.pkl`) in `data/` directory
- File naming: `TABLE_[your_name].pkl`
- Screenshots saved as PNG in `screenshots/` directory

**Dependencies:**
- **PySimpleGUI** - GUI framework
- **Python Standard Library** - pickle, datetime, os, sys

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome. Check the `notes.txt` file for current development priorities.

## 📄 License

This project is open source. Feel free to use and modify as needed.

---

**Made with PySimpleGUI** - A simple, cross-platform GUI framework for Python.

> [!Important]
> As I made aware of, PySimpleGUI is no longer offering hobbyist license. Check [PySimpleGUI Notice](https://pysimplegui.com/#notice)
