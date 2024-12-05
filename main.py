import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class FlashcardAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.root.geometry("400x300")
        
        self.flashcards = {}
        self.current_word = None

        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        # Full paths to icons
        add_icon_path = r"D:\Users\Neo Reynes\Downloads\add_icon.png.png"
        test_icon_path = r"D:\Users\Neo Reynes\Downloads\test_icon.png.png"
        view_icon_path = r"D:\Users\Neo Reynes\Downloads\view_icon.png.png"

        # Add button icons using full paths
        add_icon = self.load_icon(add_icon_path, 30, 30)
        test_icon = self.load_icon(test_icon_path, 30, 30)
        view_icon = self.load_icon(view_icon_path, 30, 30)

        # Create buttons with icons and text
        ttk.Button(self.button_frame, text="Add Flashcard", image=add_icon, compound=tk.LEFT, command=self.add_flashcard).grid(row=0, column=0, padx=10)
        ttk.Button(self.button_frame, text="Test Knowledge", image=test_icon, compound=tk.LEFT, command=self.test_knowledge).grid(row=0, column=1, padx=10)
        ttk.Button(self.button_frame, text="View Flashcards", image=view_icon, compound=tk.LEFT, command=self.view_flashcards).grid(row=0, column=2, padx=10)

        # Keep references to icons to prevent garbage collection
        self.icons = [add_icon, test_icon, view_icon]

    def load_icon(self, path, width, height):
        """Load and resize icon."""
        try:
            img = Image.open(path)
            img = img.resize((width, height), Image.ANTIALIAS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load icon: {path}\n{e}")
            return None

    def add_flashcard(self):
        messagebox.showinfo("Add Flashcard", "Add Flashcard function is under development.")

    def test_knowledge(self):
        messagebox.showinfo("Test Knowledge", "Test Knowledge function is under development.")

    def view_flashcards(self):
        messagebox.showinfo("View Flashcards", "View Flashcards function is under development.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardAppGUI(root)
    root.mainloop()
