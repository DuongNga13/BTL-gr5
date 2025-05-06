import tkinter as tk
from tkinter import messagebox, ttk
import pickle
from Laptrinh import NguoiDung, QuanLySach, Sach, tai_nguoi_dung, luu_nguoi_dung

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Thu vien sach")
        self.root.geometry("800x500")
        self.users = tai_nguoi_dung()
        self.current_user = None
        self.quan_ly_sach = QuanLySach()

        self.setup_style()

        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        self.show_login_or_register()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 11))
        style.configure("TButton", font=("Arial", 11), padding=6)
        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))
        style.configure("Treeview", font=('Arial', 10), rowheight=25)

    def show_login_or_register(self):
        self.clear_frame(self.main_frame)

        form_frame = tk.Frame(self.main_frame, bg="white")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        if not self.users:
            ttk.Label(form_frame, text="Chua co tai khoan nao. Vui long dang ky.", foreground="red").pack(pady=10)

        ttk.Label(form_frame, text="Ten dang nhap:").pack(pady=5)
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.pack()

        ttk.Label(form_frame, text="Mat khau:").pack(pady=5)
        self.password_entry = ttk.Entry(form_frame, show="*", width=30)
        self.password_entry.pack()

        ttk.Button(form_frame, text="Dang nhap", command=self.login).pack(pady=10)
        ttk.Button(form_frame, text="Dang ky", command=self.register).pack()

    def login(self):
        ten = self.username_entry.get()
        mat_khau = self.password_entry.get()
        for u in self.users:
            if u.get_ten_dang_nhap() == ten and u.get_mat_khau() == mat_khau:
                self.current_user = u
                self.show_main_interface()
                return
        messagebox.showerror("Loi", "Sai thong tin dang nhap")

    def register(self):
        ten = self.username_entry.get()
        mat_khau = self.password_entry.get()

        if not ten or not mat_khau:
            messagebox.showwarning("Loi", "Khong duoc de trong")
            return

        if any(u.get_ten_dang_nhap() == ten for u in self.users):
            messagebox.showwarning("Loi", "Ten dang nhap da ton tai")
            return

        user = NguoiDung(ten, mat_khau, False)
        self.users.append(user)
        luu_nguoi_dung(self.users)
        messagebox.showinfo("Thanh cong", "Dang ky thanh cong")

    def show_main_interface(self):
        self.clear_frame(self.main_frame)
        self.root.geometry("1000x600")

        self.menu_frame = tk.Frame(self.main_frame, width=250, bg="#f0f0f0")
        self.menu_frame.pack(side="left", fill="y")

        self.display_frame = tk.Frame(self.main_frame, bg="white")
        self.display_frame.pack(side="right", fill="both", expand=True)

        ttk.Label(self.menu_frame, text=f"Xin chao, {self.current_user.get_ten_dang_nhap()}", background="#f0f0f0").pack(pady=10)

        if self.current_user.is_admin():
            ttk.Button(self.menu_frame, text="Them sach", command=self.show_add_book).pack(pady=5, fill="x", padx=10)

        ttk.Button(self.menu_frame, text="Xem tat ca sach", command=self.show_all_books).pack(pady=5, fill="x", padx=10)
        ttk.Button(self.menu_frame, text="Dang xuat", command=self.logout).pack(pady=20, fill="x", padx=10)

        self.show_all_books()

    def show_add_book(self):
        self.clear_frame(self.display_frame)

        form_frame = tk.Frame(self.display_frame, bg="white")
        form_frame.place(relx=0.5, rely=0.05)

        ttk.Label(form_frame, text="Ma sach:").pack(pady=5)
        ma_entry = ttk.Entry(form_frame, width=40)
        ma_entry.pack()

        ttk.Label(form_frame, text="Ten sach:").pack(pady=5)
        ten_entry = ttk.Entry(form_frame, width=40)
        ten_entry.pack()

        ttk.Label(form_frame, text="Tac gia:").pack(pady=5)
        tg_entry = ttk.Entry(form_frame, width=40)
        tg_entry.pack()

        ttk.Label(form_frame, text="Nam xuat ban:").pack(pady=5)
        nam_entry = ttk.Entry(form_frame, width=40)
        nam_entry.pack()

        def submit():
            ma = ma_entry.get()
            ten = ten_entry.get()
            tg = tg_entry.get()
            nam = nam_entry.get()

            if not ma or not ten or not tg or not nam:
                messagebox.showwarning("Loi", "Vui long dien day du thong tin")
                return

            sach = Sach(ma, ten, tg, nam)
            self.quan_ly_sach.them_sach(sach)
            messagebox.showinfo("Thanh cong", "Da them sach")
            self.show_all_books()

        ttk.Button(form_frame, text="Them sach", command=submit).pack(pady=15)

    def show_all_books(self):
        self.clear_frame(self.display_frame)

        ttk.Label(self.display_frame, text="Danh sach sach", font=("Arial", 14, "bold")).pack(pady=10)

        frame_table = tk.Frame(self.display_frame)
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("ma", "ten", "tg", "nam")
        tree = ttk.Treeview(frame_table, columns=columns, show="headings")
        tree.heading("ma", text="Ma sach")
        tree.heading("ten", text="Ten sach")
        tree.heading("tg", text="Tac gia")
        tree.heading("nam", text="Nam XB")

        tree.column("ma", width=100)
        tree.column("ten", width=250)
        tree.column("tg", width=200)
        tree.column("nam", width=100)

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

        for sach in self.quan_ly_sach.danh_sach_sach:
            tree.insert("", "end", values=(sach.get_ma_sach(), sach.get_ten_sach(), sach.get_tac_gia(), sach.get_nam_xuat_ban()))

    def logout(self):
        self.current_user = None
        self.root.geometry("800x500")
        self.show_login_or_register()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()