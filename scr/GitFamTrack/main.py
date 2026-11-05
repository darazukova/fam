"""Точка входа FamTrack."""
from database.database import init_db
from ui.menus import main_menu

if __name__ == "__main__":
    init_db()
    main_menu()
