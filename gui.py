import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from app_logic import add_word
from database import get_sets, get_cards, delete_set


class FlashcardsApp:
    def __init__(self, root, conn):
        self.conn = conn
        self.root = root
        self.current_cards = []
        self.card_index = 0

        # Style
        self.style = Style(theme='superhero')

        # Configure root window
        self.root.title("Flashcards App")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        self.root.bind("<Configure>", self.on_resize)

        # Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs
        self.create_set_tab()
        self.saved_set_tab()
        self.learn_mode_tab()

        # Populate combobox
        self.populate_sets_combobox()

    def on_resize(self, event):
        """Adjust font size dynamically based on window size."""
        new_width = self.root.winfo_width()
        font_size = max(10, int(new_width / 80))  # Adjust font size dynamically
        self.word_label.config(font=("Helvetica", font_size))
        self.definition_label.config(font=("Helvetica", font_size // 1.5))

    def create_set_tab(self):
        """Create a tab for adding new flashcards."""
        self.set_name_var = tk.StringVar()
        self.word_var = tk.StringVar()
        self.definition_var = tk.StringVar()

        frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(frame, text="Create Set")

        # Center labels horizontally and keep entry fields filling the width
        ttk.Label(frame, text="Set Name:", anchor="center").pack(fill="x", padx=10, pady=5)
        ttk.Entry(frame, textvariable=self.set_name_var, justify="center").pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Word:", anchor="center").pack(fill="x", padx=10, pady=5)
        ttk.Entry(frame, textvariable=self.word_var, justify="center").pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Definition:", anchor="center").pack(fill="x", padx=10, pady=5)
        ttk.Entry(frame, textvariable=self.definition_var, justify="center").pack(fill="x", padx=10, pady=10)

        ttk.Button(frame, text="Add Word", command=self.add_word).pack(pady=20, padx=10, fill="x")

    def add_word(self):
        set_name = self.set_name_var.get()
        word = self.word_var.get()
        definition = self.definition_var.get()
        if set_name and word and definition:
            add_word(self.conn, set_name, word, definition)
            self.populate_sets_combobox()
            messagebox.showinfo("Success", f'Word "{word}" added to set "{set_name}".')
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def saved_set_tab(self):
        """Create a tab to view and manage saved sets."""
        frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(frame, text="Saved Set")

        # Create a frame to hold the combobox and buttons
        combobox_frame = ttk.Frame(frame)
        combobox_frame.pack(fill="x", padx=10, pady=10)

        # Create the combobox with the same width as buttons
        self.sets_combobox = ttk.Combobox(combobox_frame, state="readonly", justify="center")
        self.sets_combobox.pack(side="top", padx=10, pady=5, fill="x")

        # Create a frame for the buttons and move them further down
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=130)  # Increased pady to move buttons down

        # Buttons with consistent width
        ttk.Button(button_frame, text="Choose", command=self.select_set).pack(pady=5, padx=10, fill="x")
        ttk.Button(button_frame, text="Delete", command=self.delete_selected_set).pack(pady=5, padx=10, fill="x")

    def learn_mode_tab(self):
        """Create a tab for learning flashcards with improved design."""
        frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(frame, text="Learn Mode")

        # Word Label - Make it stand out with a background and larger font
        self.word_label = ttk.Label(frame, text="", font=("Helvetica", 36, 'bold'), anchor="center", relief="solid", padding=20, background="#4A90E2", foreground="white")
        self.word_label.pack(fill="x", padx=20, pady=30)

        # Definition Label - Slightly smaller font with some padding and background color
        self.definition_label = ttk.Label(frame, text="", font=("Helvetica", 18), anchor="center", relief="solid", padding=20, background="#4A90E2", foreground="black")
        self.definition_label.pack(fill="x", padx=20, pady=20)

        # Create a frame for the buttons with a little more padding and consistent button size
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=40)

        # Buttons with consistent width and custom styling
        self.create_button(button_frame, "Reveal", self.reveal_card)
        self.create_button(button_frame, "Previous", self.prev_card)
        self.create_button(button_frame, "Next", self.next_card)

    def create_button(self, parent_frame, text, command):
        """Helper function to create styled buttons with consistent design."""
        button = ttk.Button(parent_frame, text=text, command=command, style="TButton")
        button.pack(side="left", padx=20, pady=10, expand=True)
        button.config(width=12)  # Consistent button width for all buttons
        return button

    def populate_sets_combobox(self):
        sets = get_sets(self.conn)
        self.sets_combobox["values"] = tuple(sets.keys())

    def select_set(self):
        set_name = self.sets_combobox.get()
        if set_name:
            set_id = get_sets(self.conn)[set_name]
            self.current_cards = get_cards(self.conn, set_id)
            self.card_index = 0
            self.show_card()
        else:
            messagebox.showwarning("Selection Error", "Please select a set.")

    def delete_selected_set(self):
        set_name = self.sets_combobox.get()
        if set_name:
            result = messagebox.askyesno("Confirm", f'Delete the set "{set_name}"?')
            if result:
                set_id = get_sets(self.conn)[set_name]
                delete_set(self.conn, set_id)
                self.populate_sets_combobox()
                messagebox.showinfo("Success", f'Set "{set_name}" deleted.')
        else:
            messagebox.showwarning("Selection Error", "Please select a set to delete.")

    def show_card(self):
        if self.current_cards:
            word, _ = self.current_cards[self.card_index]
            self.word_label.config(text=word)
            self.definition_label.config(text="")
        else:
            self.word_label.config(text="No cards available.")
            self.definition_label.config(text="")

    def reveal_card(self):
        if self.current_cards:
            _, definition = self.current_cards[self.card_index]
            self.definition_label.config(text=definition)

    def next_card(self):
        if self.current_cards and self.card_index < len(self.current_cards) - 1:
            self.card_index += 1
            self.show_card()

    def prev_card(self):
        if self.current_cards and self.card_index > 0:
            self.card_index -= 1
            self.show_card()
