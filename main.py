import tkinter as tk
from ttkbootstrap import Style
from gui import FlashcardsApp
from database import create_tables
import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('flashcards.db')
    create_tables(conn)  # Ensure tables are created

    # Create the main GUI window
    root = tk.Tk()
    root.title('Language Learning Flashcards')
    root.geometry('500x400')

    # Initialize the application
    app = FlashcardsApp(root, conn)

    root.mainloop()

if __name__ == "__main__":
    main()
