import tkinter as tk
from tkinter import messagebox, ttk
import pickle
from datetime import datetime
from Quanlythuvien import *

sample_books = [
    Book(book_id="B001", title="Cho tôi xin một vé đi tuổi thơ", author="Nguyễn Nhật Ánh", publish_year="2008", category="Văn học thiếu nhi", status=BookStatus.AVAILABLE, rating=5),
    Book(book_id="B002", title="Mắt biếc", author="Nguyễn Nhật Ánh", publish_year="1990", category="Tiểu thuyết", status=BookStatus.BORROWED, rating=4),
    Book(book_id="B003", title="Nhà giả kim", author="Paulo Coelho", publish_year="1988", category="Tiểu thuyết", status=BookStatus.AVAILABLE, rating=4),
    Book(book_id="B004", title="Dế mèn phiêu lưu ký", author="Tô Hoài", publish_year="1941", category="Văn học thiếu nhi", status=BookStatus.AVAILABLE, rating=5),
    Book(book_id="B005", title="Số đỏ", author="Vũ Trọng Phụng", publish_year="1936", category="Tiểu thuyết", status=BookStatus.LOST, rating=3),
    Book(book_id="B006", title="Tắt đèn", author="Ngô Tất Tố", publish_year="1937", category="Tiểu thuyết", status=BookStatus.AVAILABLE, rating=4),
    Book(book_id="B007", title="Harry Potter và Hòn đá Phù thủy", author="J.K. Rowling", publish_year="1997", category="Tiểu thuyết giả tưởng", status=BookStatus.BORROWED, rating=5),
    Book(book_id="B008", title="1984", author="George Orwell", publish_year="1949", category="Tiểu thuyết dystopia", status=BookStatus.AVAILABLE, rating=4),
    Book(book_id="B009", title="Tội ác và hình phạt", author="Fyodor Dostoevsky", publish_year="1866", category="Tiểu thuyết", status=BookStatus.AVAILABLE, rating=5),
    Book(book_id="B010", title="Cây cam ngọt của tôi", author="José Mauro de Vasconcelos", publish_year="1968", category="Tiểu thuyết", status=BookStatus.BORROWED, rating=4),
]
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống Quản lý Thư viện")
        self.root.geometry("1000x600")
        self.book_list = BookManager.load_from_file()
        if not self.book_list.books:  # Nếu danh sách sách rỗng, thêm sách mẫu
            for book in sample_books:
                self.book_list.add_book(book)
            BookManager.save_to_file(self.book_list)
        self.users = UserManager.load_from_file()
        self.current_user = None

        # Khởi tạo admin mặc định nếu chưa có
        self._initialize_default_admin()
        self.setup_style()
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True)
        self.show_login_or_register()

    def _initialize_default_admin(self):
        if not any(user.role == "admin" for user in self.users):
            self.users.append(Admin("1", "admin", "admin123"))
            UserManager.save_to_file(self.users)

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
            ttk.Label(form_frame, text="Chưa có tài khoản nào. Vui lòng đăng ký.", foreground="red").pack(pady=10)

        ttk.Label(form_frame, text="Tên đăng nhập:").pack(pady=5)
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.pack()

        ttk.Label(form_frame, text="Mật khẩu:").pack(pady=5)
        self.password_entry = ttk.Entry(form_frame, show="*", width=30)
        self.password_entry.pack()

        ttk.Button(form_frame, text="Đăng nhập", command=self.login).pack(pady=10)
        ttk.Button(form_frame, text="Đăng ký", command=self.register).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        for user in self.users:
            if user.login(username, password):
                self.current_user = user
                self.show_main_interface()
                messagebox.showinfo("Thành công", f"Đăng nhập thành công! Chào mừng {user.username}.")
                return
        messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Lỗi", "Không được để trống tên đăng nhập hoặc mật khẩu")
            return
        if any(user.username == username for user in self.users):
            messagebox.showwarning("Lỗi", "Tên đăng nhập đã tồn tại")
            return
        if not InputValidator.validate_username(username):
            messagebox.showwarning("Lỗi", "Tên đăng nhập phải từ 4-20 ký tự, chỉ chứa chữ cái, số và dấu gạch dưới")
            return
        if len(password) < 6:
            messagebox.showwarning("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự")
            return

        user_id = str(max(int(u.user_id) for u in self.users) + 1) if self.users else "1"
        new_user = NormalUser(user_id, username, password)
        self.users.append(new_user)
        UserManager.save_to_file(self.users)
        messagebox.showinfo("Thành công", "Đăng ký thành công")

    def show_main_interface(self):
        self.clear_frame(self.main_frame)
        self.root.geometry("1000x600")

        self.menu_frame = tk.Frame(self.main_frame, width=250, bg="#f0f0f0")
        self.menu_frame.pack(side="left", fill="y")

        self.display_frame = tk.Frame(self.main_frame, bg="white")
        self.display_frame.pack(side="right", fill="both", expand=True)

        ttk.Label(self.menu_frame, text=f"Xin chào, {self.current_user.username}", background="#f0f0f0").pack(pady=10)

        if isinstance(self.current_user, Admin):
            ttk.Button(self.menu_frame, text="Thêm sách", command=self.show_add_book).pack(pady=5, fill="x", padx=10)
            ttk.Button(self.menu_frame, text="Chỉnh sửa sách", command=self.show_edit_book).pack(pady=5, fill="x", padx=10)
            ttk.Button(self.menu_frame, text="Xóa sách", command=self.show_delete_book).pack(pady=5, fill="x", padx=10)
            ttk.Button(self.menu_frame, text="Tìm kiếm sách", command=self.show_search_book).pack(pady=5, fill="x", padx=10)
            ttk.Button(self.menu_frame, text="Lọc theo thể loại", command=self.show_filter_by_category).pack(pady=5, fill="x", padx=10)
            ttk.Button(self.menu_frame, text="Lọc theo trạng thái", command=self.show_filter_by_status).pack(pady=5, fill="x", padx=10)
            ttk.Button(self.menu_frame, text="Lọc theo ngày thêm", command=self.show_filter_by_date).pack(pady=5, fill="x", padx=10)
        else:
            ttk.Button(self.menu_frame, text="Tìm kiếm sách", command=self.show_search_book).pack(pady=5, fill="x", padx=10)
            ttk.Button(self.menu_frame, text="Lưu sách yêu thích", command=self.show_save_book).pack(pady=5, fill="x", padx=10)
            ttk.Button(self.menu_frame, text="Xem sách yêu thích", command=self.show_saved_books).pack(pady=5, fill="x", padx=10)
            ttk.Button(self.menu_frame, text="Xóa sách yêu thích", command=self.show_remove_saved_book).pack(pady=5, fill="x", padx=10)

        ttk.Button(self.menu_frame, text="Xem tất cả sách", command=self.show_all_books).pack(pady=5, fill="x", padx=10)
        ttk.Button(self.menu_frame, text="Đăng xuất", command=self.logout).pack(pady=20, fill="x", padx=10)

        self.show_all_books()

    def show_add_book(self):
        self.clear_frame(self.display_frame)

        form_frame = tk.Frame(self.display_frame, bg="white")
        form_frame.place(relx=0.5, rely=0.05, anchor="n")

        ttk.Label(form_frame, text="Mã sách:").pack(pady=5)
        book_id_entry = ttk.Entry(form_frame, width=40)
        book_id_entry.pack()

        ttk.Label(form_frame, text="Tên sách:").pack(pady=5)
        title_entry = ttk.Entry(form_frame, width=40)
        title_entry.pack()

        ttk.Label(form_frame, text="Tác giả:").pack(pady=5)
        author_entry = ttk.Entry(form_frame, width=40)
        author_entry.pack()

        ttk.Label(form_frame, text="Năm xuất bản (YYYY):").pack(pady=5)
        year_entry = ttk.Entry(form_frame, width=40)
        year_entry.pack()

        ttk.Label(form_frame, text="Thể loại (Enter để bỏ qua):").pack(pady=5)
        category_entry = ttk.Entry(form_frame, width=40)
        category_entry.pack()

        ttk.Label(form_frame, text="Trạng thái:").pack(pady=5)
        status_var = tk.StringVar(value=BookStatus.AVAILABLE.value)
        status_combobox = ttk.Combobox(
            form_frame,
            textvariable=status_var,
            values=[status.value for status in BookStatus],
            state="readonly",
            width=37
        )
        status_combobox.pack()

        ttk.Label(form_frame, text="Đánh giá (chọn số sao):").pack(pady=5)
        rating_frame = tk.Frame(form_frame, bg="white")
        rating_frame.pack(pady=5)
        self.rating_value = tk.IntVar(value=0)
        self.star_buttons = []
        for i in range(1, 6):
            btn = tk.Button(
                rating_frame,
                text="⭐",
                font=("Arial", 12),
                bg="white",
                fg="grey",
                bd=0,
                command=lambda x=i: self.set_rating(x)
            )
            btn.pack(side="left", padx=2)
            self.star_buttons.append(btn)
        self.update_star_buttons()

        def submit():
            book_id = book_id_entry.get()
            title = title_entry.get()
            author = author_entry.get()
            year = year_entry.get()
            category = category_entry.get() or None
            status_value = status_var.get()
            rating = str(self.rating_value.get())

            if not book_id or not title or not author or not year:
                messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ thông tin bắt buộc")
                return
            if any(book.book_id == book_id for book in self.book_list.books):
                messagebox.showwarning("Lỗi", "Mã sách đã tồn tại")
                return
            if not InputValidator.validate_author(author):
                messagebox.showwarning("Lỗi", "Tên tác giả không hợp lệ")
                return
            if not InputValidator.validate_year(year):
                messagebox.showwarning("Lỗi", "Năm xuất bản không hợp lệ (phải là YYYY, từ 1000 đến hiện tại)")
                return
            if not InputValidator.validate_rating(rating):
                messagebox.showwarning("Lỗi", "Đánh giá phải từ 0-5")
                return

            status = BookStatus.AVAILABLE
            if status_value == BookStatus.BORROWED.value:
                status = BookStatus.BORROWED
            elif status_value == BookStatus.LOST.value:
                status = BookStatus.LOST

            new_book = Book(book_id, title, author, year, category, status, self.rating_value.get())
            self.current_user.add_book(self.book_list, new_book)
            BookManager.save_to_file(self.book_list)
            messagebox.showinfo("Thành công", "Đã thêm sách")
            self.show_all_books()

        ttk.Button(form_frame, text="Thêm sách", command=submit).pack(pady=15)

    def set_rating(self, value):
        self.rating_value.set(value)
        self.update_star_buttons()

    def update_star_buttons(self):
        for i, btn in enumerate(self.star_buttons):
            if i < self.rating_value.get():
                btn.config(fg="gold")
            else:
                btn.config(fg="grey")

    def show_edit_book(self):
        self.clear_frame(self.display_frame)

        ttk.Label(self.display_frame, text="Nhập mã sách cần chỉnh sửa:").pack(pady=10)
        book_id_entry = ttk.Entry(self.display_frame, width=40)
        book_id_entry.pack(pady=5)

        def search():
            book_id = book_id_entry.get()
            book = self.book_list.find_book_by_id(book_id)
            if not book:
                messagebox.showwarning("Lỗi", "Không tìm thấy sách")
                return

            self.clear_frame(self.display_frame)
            form_frame = tk.Frame(self.display_frame, bg="white")
            form_frame.place(relx=0.5, rely=0.05, anchor="n")

            ttk.Label(form_frame, text=f"Chỉnh sửa sách: {book.title}").pack(pady=5)

            ttk.Label(form_frame, text=f"Tên sách (hiện tại: {book.title}):").pack(pady=5)
            title_entry = ttk.Entry(form_frame, width=40)
            title_entry.pack()

            ttk.Label(form_frame, text=f"Tác giả (hiện tại: {book.author}):").pack(pady=5)
            author_entry = ttk.Entry(form_frame, width=40)
            author_entry.pack()

            ttk.Label(form_frame, text=f"Năm xuất bản (hiện tại: {book.publish_year}):").pack(pady=5)
            year_entry = ttk.Entry(form_frame, width=40)
            year_entry.pack()

            ttk.Label(form_frame, text=f"Thể loại (hiện tại: {book.category if book.category else 'N/A'}):").pack(pady=5)
            category_entry = ttk.Entry(form_frame, width=40)
            category_entry.pack()

            ttk.Label(form_frame, text=f"Trạng thái mới:").pack(pady=5)
            status_var = tk.StringVar(value=book.status.value)
            status_combobox = ttk.Combobox(
                form_frame,
                textvariable=status_var,
                values=[status.value for status in BookStatus],
                state="readonly",
                width=37
            )
            status_combobox.pack()

            ttk.Label(form_frame, text="Đánh giá mới (chọn số sao):").pack(pady=5)
            rating_frame = tk.Frame(form_frame, bg="white")
            rating_frame.pack(pady=5)
            self.rating_value = tk.IntVar(value=book.rating)
            self.star_buttons = []
            for i in range(1, 6):
                btn = tk.Button(
                    rating_frame,
                    text="⭐",
                    font=("Arial", 12),
                    bg="white",
                    fg="grey",
                    bd=0,
                    command=lambda x=i: self.set_rating(x)
                )
                btn.pack(side="left", padx=2)
                self.star_buttons.append(btn)
            self.update_star_buttons()

            def submit():
                updates = {}
                if title_entry.get():
                    updates['title'] = title_entry.get()
                if author_entry.get():
                    if not InputValidator.validate_author(author_entry.get()):
                        messagebox.showwarning("Lỗi", "Tên tác giả không hợp lệ")
                        return
                    updates['author'] = author_entry.get()
                if year_entry.get():
                    if not InputValidator.validate_year(year_entry.get()):
                        messagebox.showwarning("Lỗi", "Năm xuất bản không hợp lệ")
                        return
                    updates['publish_year'] = year_entry.get()
                if category_entry.get():
                    updates['category'] = None if category_entry.get().lower() == 'none' else category_entry.get()
                status_value = status_var.get()
                if status_value:
                    if status_value == BookStatus.AVAILABLE.value:
                        updates['status'] = BookStatus.AVAILABLE
                    elif status_value == BookStatus.BORROWED.value:
                        updates['status'] = BookStatus.BORROWED
                    elif status_value == BookStatus.LOST.value:
                        updates['status'] = BookStatus.LOST
                updates['rating'] = self.rating_value.get()

                if updates:
                    self.current_user.edit_book(self.book_list, book_id, **updates)
                    BookManager.save_to_file(self.book_list)
                    messagebox.showinfo("Thành công", "Cập nhật sách thành công")
                    self.show_all_books()
                else:
                    messagebox.showinfo("Thông báo", "Không có thay đổi nào được thực hiện")

            ttk.Button(form_frame, text="Cập nhật", command=submit).pack(pady=15)
        ttk.Button(self.display_frame, text="Tìm sách", command=search).pack(pady=10)

    def show_delete_book(self):
        self.clear_frame(self.display_frame)
        ttk.Label(self.display_frame, text="Nhập mã sách muốn xóa:").pack(pady=10)
        book_id_entry = ttk.Entry(self.display_frame, width=40)
        book_id_entry.pack(pady=5)
        def delete_book():
            book_id = book_id_entry.get()
            self.current_user.delete_book(self.book_list, book_id)
            try:
                BookManager.save_to_file(self.book_list)
                messagebox.showinfo("Thành công", "Đã xóa sách")
                self.show_all_books()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu tệp: {str(e)}")

        ttk.Button(self.display_frame, text="Xóa", command=delete_book, style="TButton").pack(pady=10)

    def show_search_book(self):
        self.clear_frame(self.display_frame)

        ttk.Label(self.display_frame, text="Nhập từ khóa tìm kiếm (tên, tác giả, thể loại):").pack(pady=10)
        keyword_entry = ttk.Entry(self.display_frame, width=50)
        keyword_entry.pack(pady=5)

        def search():
            keyword = keyword_entry.get()
            found_books = self.book_list.search_books(keyword)
            if found_books:
                messagebox.showinfo("Kết quả", f"Tìm thấy {len(found_books)} sách")
                self.show_books(found_books)
            else:
                messagebox.showwarning("Kết quả", "Không tìm thấy sách phù hợp")
        ttk.Button(self.display_frame, text="Tìm", command=search).pack(pady=10)

    def show_filter_by_category(self):
        self.clear_frame(self.display_frame)

        ttk.Label(self.display_frame, text="Nhập thể loại cần lọc:").pack(pady=10)
        category_entry = ttk.Entry(self.display_frame, width=40)
        category_entry.pack(pady=5)

        def filter():
            category = category_entry.get()
            found_books = self.book_list.filter_by_category(category)
            if found_books:
                messagebox.showinfo("Kết quả", f"Tìm thấy {len(found_books)} sách thuộc thể loại '{category}'")
                self.show_books(found_books)
            else:
                messagebox.showwarning("Kết quả", f"Không có sách nào thuộc thể loại '{category}'")
        ttk.Button(self.display_frame, text="Lọc", command=filter).pack(pady=10)

    def show_filter_by_status(self):
        self.clear_frame(self.display_frame)

        ttk.Label(self.display_frame, text="Chọn trạng thái:").pack(pady=10)
        status_var = tk.StringVar(value=BookStatus.AVAILABLE.value)
        status_combobox = ttk.Combobox(
            self.display_frame,
            textvariable=status_var,
            values=[status.value for status in BookStatus],
            state="readonly",
            width=37
        )
        status_combobox.pack(pady=5)

        def filter():
            status_value = status_var.get()
            status = BookStatus.AVAILABLE
            if status_value == BookStatus.BORROWED.value:
                status = BookStatus.BORROWED
            elif status_value == BookStatus.LOST.value:
                status = BookStatus.LOST
            found_books = self.book_list.filter_by_status(status)
            if found_books:
                messagebox.showinfo("Kết quả", f"Tìm thấy {len(found_books)} sách có trạng thái '{status.value}'")
                self.show_books(found_books)
            else:
                messagebox.showwarning("Kết quả", f"Không có sách nào có trạng thái '{status.value}'")

        ttk.Button(self.display_frame, text="Lọc", command=filter).pack(pady=10)

    def show_filter_by_date(self):
        self.clear_frame(self.display_frame)

        ttk.Label(self.display_frame, text="Ngày bắt đầu (YYYY-MM-DD):").pack(pady=5)
        start_date_entry = ttk.Entry(self.display_frame, width=40)
        start_date_entry.pack(pady=5)

        ttk.Label(self.display_frame, text="Ngày kết thúc (YYYY-MM-DD):").pack(pady=5)
        end_date_entry = ttk.Entry(self.display_frame, width=40)
        end_date_entry.pack(pady=5)

        def filter():
            try:
                start_date = datetime.strptime(start_date_entry.get(), "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_entry.get(), "%Y-%m-%d").date()
                found_books = self.book_list.filter_by_date(start_date, end_date)
                if found_books:
                    messagebox.showinfo("Kết quả", f"Tìm thấy {len(found_books)} sách được thêm từ {start_date} đến {end_date}")
                    self.show_books(found_books)
                else:
                    messagebox.showwarning("Kết quả", f"Không có sách nào được thêm từ {start_date} đến {end_date}")
            except ValueError:
                messagebox.showwarning("Lỗi", "Định dạng ngày không hợp lệ! Sử dụng YYYY-MM-DD")

        ttk.Button(self.display_frame, text="Lọc", command=filter).pack(pady=10)

    def show_save_book(self):
        self.clear_frame(self.display_frame)

        ttk.Label(self.display_frame, text="Nhập mã sách muốn lưu vào danh sách yêu thích:").pack(pady=10)
        book_id_entry = ttk.Entry(self.display_frame, width=40)
        book_id_entry.pack(pady=5)

        def save():
            book_id = book_id_entry.get()
            book = self.book_list.find_book_by_id(book_id)
            if book:
                self.current_user.save_book(book)
                UserManager.save_to_file(self.users)
                messagebox.showinfo("Thành công", f"Đã lưu sách '{book.title}' vào danh sách yêu thích")
            else:
                messagebox.showwarning("Lỗi", "Không tìm thấy sách")

        ttk.Button(self.display_frame, text="Lưu", command=save).pack(pady=10)

    def show_saved_books(self):
        self.clear_frame(self.display_frame)

        if not self.current_user.saved_books:
            messagebox.showinfo("Thông báo", "Danh sách yêu thích trống")
            return

        ttk.Label(self.display_frame, text="Sách yêu thích", font=("Arial", 14, "bold")).pack(pady=10)
        self.show_books(self.current_user.saved_books)

    def show_remove_saved_book(self):
        self.clear_frame(self.display_frame)

        ttk.Label(self.display_frame, text="Nhập mã sách muốn xóa khỏi danh sách yêu thích:").pack(pady=10)
        book_id_entry = ttk.Entry(self.display_frame, width=40)
        book_id_entry.pack(pady=5)

        def remove():
            book_id = book_id_entry.get()
            self.current_user.remove_saved_book(book_id)
            UserManager.save_to_file(self.users)
            messagebox.showinfo("Thành công", f"Đã xóa sách '{book_id}' khỏi danh sách yêu thích")

        ttk.Button(self.display_frame, text="Xóa", command=remove).pack(pady=10)

    def show_books(self, books):
        self.clear_frame(self.display_frame)

        if not books:
            ttk.Label(self.display_frame, text="Không có sách để hiển thị.", font=("Arial", 12), foreground="red").pack(pady=20)
            return

        frame_table = tk.Frame(self.display_frame)
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "title", "author", "year", "category", "status", "rating", "added_date")
        tree = ttk.Treeview(frame_table, columns=columns, show="headings")
        tree.heading("id", text="Mã sách")
        tree.heading("title", text="Tên sách")
        tree.heading("author", text="Tác giả")
        tree.heading("year", text="Năm XB")
        tree.heading("category", text="Thể loại")
        tree.heading("status", text="Trạng thái")
        tree.heading("rating", text="Đánh giá")
        tree.heading("added_date", text="Ngày thêm")

        tree.column("id", width=100, anchor="center")
        tree.column("title", width=250, anchor="w")
        tree.column("author", width=200, anchor="w")
        tree.column("year", width=80, anchor="center")
        tree.column("category", width=150, anchor="w")
        tree.column("status", width=100, anchor="center")
        tree.column("rating", width=80, anchor="center")
        tree.column("added_date", width=100, anchor="center")

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

        for book in books:
            tree.insert("", "end", values=(
                book.book_id,
                book.title,
                book.author,
                book.publish_year,
                book.category or "N/A",
                book.status.value,
                "★" * book.rating,
                book.added_date
            ))

        if not isinstance(self.current_user, Admin):
            save_btn = ttk.Button(self.display_frame, text="Lưu vào danh sách yêu thích", command=lambda: self.save_selected_book(tree))
            save_btn.pack(pady=10)

    def show_all_books(self):
        self.clear_frame(self.display_frame)

        # Tải lại dữ liệu từ books.pkl
        self.book_list = BookManager.load_from_file()

        if not self.book_list.books:
            ttk.Label(self.display_frame, text="Thư viện chưa có sách nào.", font=("Arial", 12), foreground="red").pack(pady=20)
            return

        ttk.Label(self.display_frame, text="Danh sách tất cả sách", font=("Arial", 14, "bold")).pack(pady=10)
        self.show_books(self.book_list.books)

    def save_selected_book(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một sách từ danh sách")
            return

        book_id = tree.item(selected_item, "values")[0]
        book = self.book_list.find_book_by_id(book_id)
        if book:
            self.current_user.save_book(book)
            UserManager.save_to_file(self.users)
            messagebox.showinfo("Thành công", f"Đã lưu sách '{book.title}' vào danh sách yêu thích")
        else:
            messagebox.showwarning("Lỗi", "Không tìm thấy sách")

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