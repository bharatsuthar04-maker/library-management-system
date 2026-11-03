import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date, timedelta

# DATABASE CONNECTION
conn = sqlite3.connect("library.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    quantity INTEGER,
    available INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS members(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS issued(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    member_id INTEGER,
    issue_date TEXT,
    due_date TEXT,
    status TEXT
)
""")

conn.commit()

# MAIN WINDOW SETUP
root = tk.Tk()
root.title("Library Management System")
root.geometry("1100x700")
root.configure(bg="#f4f6f9")

# MODERN STYLING CONFIGURATION
style = ttk.Style()
style.theme_use("clam")  # Removes outdated Windows 3D borders

# Color Palette
BG_COLOR = "#f4f6f9"
CARD_BG = "#ffffff"
PRIMARY = "#4361ee"
PRIMARY_HOVER = "#3a53cc"
DANGER = "#ef233c"
DANGER_HOVER = "#d90429"
SUCCESS = "#2a9d8f"
SUCCESS_HOVER = "#21867a"
TEXT_MAIN = "#2b2d42"
NAV_BG = "#ffffff"

# Global Styles
style.configure("TFrame", background=BG_COLOR)
style.configure("Card.TFrame", background=CARD_BG)
style.configure("TLabel", background=BG_COLOR, foreground=TEXT_MAIN, font=("Segoe UI", 11))
style.configure("Card.TLabel", background=CARD_BG, foreground=TEXT_MAIN, font=("Segoe UI", 11))
style.configure("Title.TLabel", background=BG_COLOR, foreground=TEXT_MAIN, font=("Segoe UI", 22, "bold"))
style.configure("CardTitle.TLabel", background=CARD_BG, foreground=TEXT_MAIN, font=("Segoe UI", 16, "bold"))
style.configure("Value.TLabel", background=CARD_BG, foreground=PRIMARY, font=("Segoe UI", 24, "bold"))

# Entry Styling
style.configure("TEntry", fieldbackground=CARD_BG, font=("Segoe UI", 11), padding=5)
style.configure("TCombobox", fieldbackground=CARD_BG, font=("Segoe UI", 11), padding=5)

# Button Styling
style.configure("Primary.TButton", background=PRIMARY, foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=8)
style.map("Primary.TButton", background=[("active", PRIMARY_HOVER)])

style.configure("Danger.TButton", background=DANGER, foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=8)
style.map("Danger.TButton", background=[("active", DANGER_HOVER)])

style.configure("Success.TButton", background=SUCCESS, foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=8)
style.map("Success.TButton", background=[("active", SUCCESS_HOVER)])

style.configure("Nav.TButton", background=NAV_BG, foreground=TEXT_MAIN, font=("Segoe UI", 11, "bold"), borderwidth=0, padding=10)
style.map("Nav.TButton", background=[("active", "#e9ecef")])

# Treeview (Data Table) Styling
style.configure("Treeview", font=("Segoe UI", 10), rowheight=35, bordercolor="#e9ecef", borderwidth=0)
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#f8f9fa", foreground=TEXT_MAIN, padding=5)
style.map("Treeview", background=[("selected", PRIMARY)], foreground=[("selected", "white")])


def init_login_screen():
    global username, password
    
    for widget in root.winfo_children():
        widget.destroy()
        
    # Centered Login Card
    login_container = tk.Frame(root, bg=BG_COLOR)
    login_container.place(relx=0.5, rely=0.5, anchor="center")

    login_card = ttk.Frame(login_container, style="Card.TFrame", padding=(40, 40))
    login_card.pack(fill="both", expand=True)

    ttk.Label(login_card, text="Welcome Back", style="CardTitle.TLabel").pack(pady=(0, 5))
    ttk.Label(login_card, text="Sign in to continue to Library System", style="Card.TLabel", foreground="#6c757d").pack(pady=(0, 25))

    ttk.Label(login_card, text="Username", style="Card.TLabel").pack(anchor="w")
    username = ttk.Entry(login_card, width=35)
    username.pack(pady=(5, 15), ipady=3)

    ttk.Label(login_card, text="Password", style="Card.TLabel").pack(anchor="w")
    password = ttk.Entry(login_card, show="•", width=35)
    password.pack(pady=(5, 25), ipady=3)

    ttk.Button(login_card, text="LOGIN", style="Primary.TButton", command=login).pack(fill="x", pady=(0, 10))

def login():
    if username.get() == "admin" and password.get() == "admin123":
        dashboard()
    else:
        messagebox.showerror("Error", "Invalid Login Details")

# MAIN DASHBOARD
def dashboard():
    for widget in root.winfo_children():
        widget.destroy()

    # Top Navigation Bar
    nav = tk.Frame(root, bg=NAV_BG, height=60)
    nav.pack(fill="x", side="top")
    nav.pack_propagate(False)
    
    tk.Label(nav, text=""Smart Library Management System"", font=("Segoe UI", 16, "bold"), bg=NAV_BG, fg=PRIMARY).pack(side="left", padx=20)

    # Main Content Area
    content = ttk.Frame(root, padding=25)
    content.pack(fill="both", expand=True)

    def clear():
        for w in content.winfo_children():
            w.destroy()

    def dashboard_home():
        clear()
        ttk.Label(content, text="Dashboard Overview", style="Title.TLabel").pack(anchor="w", pady=(0, 20))

        cur.execute("SELECT COUNT(*) FROM books")
        books = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM members")
        members = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM issued WHERE status='Issued'")
        issued = cur.fetchone()[0]

        # Dashboard Cards Container
        cards_frame = ttk.Frame(content)
        cards_frame.pack(fill="x", pady=10)

        for label, value in [
            ("Total Book Titles", books),
            ("Total Members", members),
            ("Active Issues", issued)
        ]:
            card = ttk.Frame(cards_frame, style="Card.TFrame", padding=20)
            card.pack(side="left", fill="both", expand=True, padx=(0, 15))
            ttk.Label(card, text=label, style="Card.TLabel", foreground="#6c757d").pack(anchor="w")
            ttk.Label(card, text=str(value), style="Value.TLabel").pack(anchor="w", pady=(10, 0))

    # BOOK MANAGEMENT
    def books_page():
        clear()
        ttk.Label(content, text="Book Management", style="Title.TLabel").pack(anchor="w", pady=(0, 20))

        form_card = ttk.Frame(content, style="Card.TFrame", padding=20)
        form_card.pack(fill="x", pady=(0, 20))

        ttk.Label(form_card, text="Book Title", style="Card.TLabel").grid(row=0, column=0, sticky="w", padx=5)
        title = ttk.Entry(form_card, width=30)
        title.grid(row=1, column=0, padx=5, pady=(5, 0), ipady=3)

        ttk.Label(form_card, text="Author", style="Card.TLabel").grid(row=0, column=1, sticky="w", padx=15)
        author = ttk.Entry(form_card, width=30)
        author.grid(row=1, column=1, padx=15, pady=(5, 0), ipady=3)

        ttk.Label(form_card, text="Quantity", style="Card.TLabel").grid(row=0, column=2, sticky="w", padx=5)
        quantity = ttk.Entry(form_card, width=15)
        quantity.grid(row=1, column=2, padx=5, pady=(5, 0), ipady=3)

        # Treeview Container for Border/Background styling
        table_frame = ttk.Frame(content)
        table_frame.pack(fill="both", expand=True)
        
        tree = ttk.Treeview(table_frame, columns=("ID", "Title", "Author", "Qty", "Avail"), show="headings")

        for col, width in zip(("ID", "Title", "Author", "Qty", "Avail"), (50, 250, 200, 80, 80)):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center" if col in ("ID", "Qty", "Avail") else "w")
        tree.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            cur.execute("SELECT * FROM books")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)

        def add_book():
            try:
                t = title.get().strip()
                a = author.get().strip()
                q = int(quantity.get())
                if not t or not a or q < 1:
                    raise ValueError
                cur.execute("INSERT INTO books(title,author,quantity,available) VALUES(?,?,?,?)", (t, a, q, q))
                conn.commit()
                title.delete(0, "end")
                author.delete(0, "end")
                quantity.delete(0, "end")
                refresh()
            except ValueError:
                messagebox.showerror("Error", "Enter valid book details")

        def delete_book():
            selected = tree.focus()
            if not selected:
                return messagebox.showwarning("Select", "Select a book first")
            book_id = tree.item(selected)["values"][0]
            cur.execute("SELECT COUNT(*) FROM issued WHERE book_id=? AND status='Issued'", (book_id,))
            if cur.fetchone()[0] > 0:
                return messagebox.showerror("Error", "Book is currently issued")
            cur.execute("DELETE FROM books WHERE id=?", (book_id,))
            conn.commit()
            refresh()

        ttk.Button(form_card, text="Add Book", command=add_book, style="Primary.TButton").grid(row=1, column=3, padx=(20, 10), pady=(5, 0))
        ttk.Button(form_card, text="Delete Selected", command=delete_book, style="Danger.TButton").grid(row=1, column=4, padx=5, pady=(5, 0))

        refresh()

    # MEMBER MANAGEMENT
    def members_page():
        clear()
        ttk.Label(content, text="Member Management", style="Title.TLabel").pack(anchor="w", pady=(0, 20))

        form_card = ttk.Frame(content, style="Card.TFrame", padding=20)
        form_card.pack(fill="x", pady=(0, 20))

        ttk.Label(form_card, text="Full Name", style="Card.TLabel").grid(row=0, column=0, sticky="w", padx=5)
        name = ttk.Entry(form_card, width=35)
        name.grid(row=1, column=0, padx=5, pady=(5, 0), ipady=3)

        ttk.Label(form_card, text="Phone Number", style="Card.TLabel").grid(row=0, column=1, sticky="w", padx=15)
        phone = ttk.Entry(form_card, width=25)
        phone.grid(row=1, column=1, padx=15, pady=(5, 0), ipady=3)

        table_frame = ttk.Frame(content)
        table_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Phone"), show="headings")
        for c, w in zip(("ID", "Name", "Phone"), (80, 300, 200)):
            tree.heading(c, text=c)
            tree.column(c, width=w, anchor="center" if c == "ID" else "w")
        tree.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            cur.execute("SELECT * FROM members")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)

        def add_member():
            n, p = name.get().strip(), phone.get().strip()
            if not n:
                return messagebox.showerror("Error", "Enter member name")
            cur.execute("INSERT INTO members(name,phone) VALUES(?,?)", (n, p))
            conn.commit()
            name.delete(0, "end")
            phone.delete(0, "end")
            refresh()

        def delete_member():
            selected = tree.focus()
            if not selected:
                return messagebox.showwarning("Select", "Select member first")
            mid = tree.item(selected)["values"][0]
            cur.execute("SELECT COUNT(*) FROM issued WHERE member_id=? AND status='Issued'", (mid,))
            if cur.fetchone()[0]:
                return messagebox.showerror("Error", "Member has an active book issue")
            cur.execute("DELETE FROM members WHERE id=?", (mid,))
            conn.commit()
            refresh()

        ttk.Button(form_card, text="Add Member", command=add_member, style="Primary.TButton").grid(row=1, column=2, padx=(20, 10), pady=(5, 0))
        ttk.Button(form_card, text="Delete Selected", command=delete_member, style="Danger.TButton").grid(row=1, column=3, padx=5, pady=(5, 0))
        refresh()

    # ISSUE AND RETURN
    def issue_page():
        clear()
        ttk.Label(content, text="Issue & Return", style="Title.TLabel").pack(anchor="w", pady=(0, 20))

        form_card = ttk.Frame(content, style="Card.TFrame", padding=20)
        form_card.pack(fill="x", pady=(0, 20))

        cur.execute("SELECT id,title FROM books WHERE available>0")
        books = {f"{b[0]} - {b[1]}": b[0] for b in cur.fetchall()}

        cur.execute("SELECT id,name FROM members")
        members = {f"{m[0]} - {m[1]}": m[0] for m in cur.fetchall()}

        ttk.Label(form_card, text="Select Book", style="Card.TLabel").grid(row=0, column=0, sticky="w", padx=5)
        book_box = ttk.Combobox(form_card, values=list(books.keys()), width=35, state="readonly")
        book_box.grid(row=1, column=0, padx=5, pady=(5, 0), ipady=3)

        ttk.Label(form_card, text="Select Member", style="Card.TLabel").grid(row=0, column=1, sticky="w", padx=15)
        member_box = ttk.Combobox(form_card, values=list(members.keys()), width=35, state="readonly")
        member_box.grid(row=1, column=1, padx=15, pady=(5, 0), ipady=3)

        table_frame = ttk.Frame(content)
        table_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(table_frame, columns=("ID", "Book ID", "Member ID", "Issue Date", "Due Date", "Status"), show="headings")
        for c in ("ID", "Book ID", "Member ID", "Issue Date", "Due Date", "Status"):
            tree.heading(c, text=c)
            tree.column(c, width=100, anchor="center")
        tree.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            cur.execute("SELECT * FROM issued ORDER BY id DESC")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)

        def issue_book():
            b, m = book_box.get(), member_box.get()
            if b not in books or m not in members:
                return messagebox.showwarning("Error", "Select book and member")
            
            today = date.today()
            due = today + timedelta(days=14)

            cur.execute("INSERT INTO issued(book_id,member_id,issue_date,due_date,status) VALUES(?,?,?,?,?)",
                        (books[b], members[m], today.isoformat(), due.isoformat(), "Issued"))
            cur.execute("UPDATE books SET available=available-1 WHERE id=?", (books[b],))
            conn.commit()
            
            book_box.set('')
            member_box.set('')
            refresh()
            
            # Re-fetch books dynamically after issue
            cur.execute("SELECT id,title FROM books WHERE available>0")
            new_books = {f"{bk[0]} - {bk[1]}": bk[0] for bk in cur.fetchall()}
            book_box['values'] = list(new_books.keys())

        def return_book():
            selected = tree.focus()
            if not selected:
                return messagebox.showwarning("Select", "Select issued record")
            values = tree.item(selected)["values"]
            if values[5] != "Issued":
                return messagebox.showinfo("Info", "Book already returned")

            cur.execute("UPDATE issued SET status='Returned' WHERE id=?", (values[0],))
            cur.execute("UPDATE books SET available=available+1 WHERE id=?", (values[1],))
            conn.commit()
            refresh()

        ttk.Button(form_card, text="Issue Book", command=issue_book, style="Primary.TButton").grid(row=1, column=2, padx=(20, 10), pady=(5, 0))
        ttk.Button(form_card, text="Return Selected", command=return_book, style="Success.TButton").grid(row=1, column=3, padx=5, pady=(5, 0))
        refresh()

    # NAVIGATION BUTTONS RENDERING
    nav_buttons_frame = tk.Frame(nav, bg=NAV_BG)
    nav_buttons_frame.pack(side="right", padx=10)

    for text, command in [
        ("Dashboard", dashboard_home),
        ("Books", books_page),
        ("Members", members_page),
        ("Issue / Return", issue_page)
    ]:
        ttk.Button(nav_buttons_frame, text=text, command=command, style="Nav.TButton").pack(side="left", padx=5)

    # Logout separate to keep style distinct
    tk.Button(nav_buttons_frame, text="Logout", command=init_login_screen, bg=DANGER, fg="white", font=("Segoe UI", 10, "bold"), borderwidth=0, padx=15, pady=6).pack(side="left", padx=(20, 5))

    dashboard_home()

# Start Application
init_login_screen()
root.mainloop()
conn.close()
