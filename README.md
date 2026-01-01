# Shrimp Data Entry Project
#### Video Demo:  https://youtu.be/cSiOcsirqk4
#### Description:
A Python/Kivy-based data-entry application for recording and managing shrimp sample data.
The app provides multiple screens for entering general information, performing calculations,
viewing history and summaries, and accessing contact/about pages. Data is stored locally
using `db.py`. The application is launched from `main.py`, UI screens are implemented in
the `screen_*.py` modules, and `persian_helper.py` offers Persian localization support.
Included assets (fonts and images) are in the `assets/` folder. Use `buildozer.spec` to
package the app for Android if you want a mobile build.

- **Github repository (I will update): https://github.com/alerezaaa/shrimp_data_entry_project**

**The main project started with a recommendation from an organization in Iran**, and the plan was to create an interactive application
Which online database, including SQL and a great webpage for administrators. But unfortunately, the organization postponed their agreement
And as far as I had to submit my project, I decided to change it a little bit to submit my project and then I can wait for them to decide.

The only place that I didn't use Python to program was smartphones, so I accepted the project and I couldn't handle the whole project based on my knowledge, especially from your course,
And the only dark area for me was a smart phone programming, which I decided to use Kivy. That was a great experience for me and thank you for giving this experience.

##### workflow
1. Start on the main menu (General Info / Navigation).
2. Enter daily data on the Calculation screen (e.g., feed amount and stock info).
3. Review a Summary screen that shows a clean 2-column table (“Field | Value”).
4. Tap “Save” to store the latest calculation as a new row in a local SQLite database.
5. Use History to read back previously saved rows (and later filter/search them).

##### Features

- **Persian-first UI** (RTL-friendly labels, fonts, and shaped text)
- **Multi-screen navigation** using `ScreenManager`
- **Live calculations** on the Calculation screen and a structured Summary view
- **Local persistence** using SQLite (no network required)
- **Android-friendly storage** by keeping the database inside the app’s writable sandbox (`App.user_data_dir`)

##### Project layout

A typical repository layout for this project looks like this:

- `src/`
  - `main.py` — App entry point (builds the ScreenManager, initializes shared state, sets DB path)
  - `db.py` — SQLite helpers (create tables, insert rows, fetch rows for history)
  - `persian_helper.py` — Persian text shaping helpers (arabic reshaper + bidi), plus shared utilities
  - `screen_general_info.py` — Main menu / general info screen (navigation hub)
  - `screen_calculation.py` — Data entry + calculation logic (produces one “record” dict)
  - `screen_summary.py` — Summary table UI + “Save” action (writes record to SQLite)
  - `screen_history.py` — History list UI (reads rows from SQLite and displays them)
  - `screen_about_us.py` — Static “About us” screen
  - `screen_contact_us.py` — Static “Contact us” screen
- `assets/`
  - `fonts/` — Vazir font files used to avoid missing-glyph “boxes”
  - `images/` — App logo and icons used by the menu/buttons


##### How to run (desktop)

(Under Development)

1. Create a virtual environment
2. Install dependencies from `requirements.txt`
3. Run the app entry point, for example:
```bash
python src/main.py
```



#### Github repository (I will update): https://github.com/alerezaaa/shrimp_data_entry_project
**Github Action to build APK file** also included in my repository
