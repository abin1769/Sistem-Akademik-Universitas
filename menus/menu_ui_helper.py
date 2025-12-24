"""
menus/menu_ui_helper.py
Helper class untuk UI dan input validation.
Menangani display dan input yang berulang di menu-menu.
"""


class MenuInputError(Exception):
    """Custom exception untuk input validation"""
    pass


class MenuInputValidator:
    """Helper untuk validasi input dari user"""
    
    @staticmethod
    def get_integer(prompt, min_val=None, max_val=None):
        """
        Get integer input dengan validasi.
        
        Args:
            prompt: Prompt yang ditampilkan
            min_val: Nilai minimum (optional)
            max_val: Nilai maksimum (optional)
        
        Returns:
            Integer yang valid
        """
        while True:
            try:
                value = int(input(prompt))
                if min_val is not None and value < min_val:
                    print(f"Masukkan angka minimal {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Masukkan angka maksimal {max_val}")
                    continue
                return value
            except ValueError:
                print("Input harus berupa angka")
    
    @staticmethod
    def get_string(prompt, min_length=1, max_length=None, allow_empty=False):
        """
        Get string input dengan validasi.
        
        Args:
            prompt: Prompt yang ditampilkan
            min_length: Panjang minimum
            max_length: Panjang maksimum
            allow_empty: Bolehkah input kosong
        
        Returns:
            String yang valid
        """
        while True:
            value = input(prompt).strip()
            if not value and not allow_empty:
                print(f"Input tidak boleh kosong")
                continue
            if len(value) < min_length:
                print(f"Minimal {min_length} karakter")
                continue
            if max_length and len(value) > max_length:
                print(f"Maksimal {max_length} karakter")
                continue
            return value
    
    @staticmethod
    def confirm_action(prompt="Lanjutkan? (y/n): "):
        """
        Get yes/no confirmation.
        
        Returns:
            True jika user pilih 'y' atau 'yes'
        """
        while True:
            choice = input(prompt).lower().strip()
            if choice in ('y', 'yes', 'iya'):
                return True
            elif choice in ('n', 'no', 'tidak'):
                return False
            else:
                print("Pilih 'y' atau 'n'")
    
    @staticmethod
    def get_choice_from_list(items, prompt="Pilih: "):
        """
        Get user choice dari list items.
        
        Args:
            items: List of items to choose from
            prompt: Prompt message
        
        Returns:
            Selected item dan index (tuple)
        """
        for i, item in enumerate(items, 1):
            print(f"{i}. {item}")
        
        choice = MenuInputValidator.get_integer(
            prompt,
            min_val=1,
            max_val=len(items)
        )
        return items[choice - 1], choice - 1


class MenuDisplay:
    """Helper untuk menampilkan output/display konsisten"""
    
    @staticmethod
    def header(title):
        """Tampilkan header dengan border"""
        print("\n" + "=" * 60)
        print(f"  {title.center(56)}")
        print("=" * 60)
    
    @staticmethod
    def subheader(title):
        """Tampilkan sub-header"""
        print(f"\n--- {title} ---")
    
    @staticmethod
    def success(message):
        """Tampilkan pesan sukses"""
        print(f"[OK] {message}")
    
    @staticmethod
    def error(message):
        """Tampilkan pesan error"""
        print(f"[ERROR] {message}")
    
    @staticmethod
    def info(message):
        """Tampilkan pesan informasi"""
        print(f"[INFO] {message}")
    
    @staticmethod
    def warning(message):
        """Tampilkan pesan warning"""
        print(f"[WARNING] {message}")
    
    @staticmethod
    def table_header(columns, col_widths=None):
        """Tampilkan table header"""
        if col_widths is None:
            col_widths = [20] * len(columns)
        
        header_line = " | ".join(col.ljust(width) for col, width in zip(columns, col_widths))
        print(header_line)
        print("-" * len(header_line))
    
    @staticmethod
    def table_row(values, col_widths=None):
        """Tampilkan table row"""
        if col_widths is None:
            col_widths = [20] * len(values)
        
        row_line = " | ".join(str(val).ljust(width) for val, width in zip(values, col_widths))
        print(row_line)
    
    @staticmethod
    def separator():
        """Tampilkan garis pemisah"""
        print("-" * 60)
    
    @staticmethod
    def pause(message="Tekan Enter untuk lanjut..."):
        """Pause dan tunggu user tekan enter"""
        input(f"\n{message}")


class MenuUI:
    """Combined helper untuk menu operations"""
    
    @staticmethod
    def show_list(items, title="Daftar Item", item_format=None):
        """
        Display list of items dengan numbered format.
        
        Args:
            items: List of items
            title: Title untuk list
            item_format: Function untuk format setiap item (optional)
        """
        MenuDisplay.subheader(title)
        
        if not items:
            print("(Kosong)")
            return
        
        for i, item in enumerate(items, 1):
            if item_format:
                print(f"{i}. {item_format(item)}")
            else:
                print(f"{i}. {item}")
    
    @staticmethod
    def show_data_table(data, columns, col_widths=None, title="Data"):
        """
        Display data dalam format table.
        
        Args:
            data: List of dictionaries or objects
            columns: List of column names/keys
            col_widths: Column widths (optional)
            title: Table title
        """
        MenuDisplay.subheader(title)
        
        if not data:
            print("(Kosong)")
            return
        
        MenuDisplay.table_header(columns, col_widths)
        
        for row in data:
            if isinstance(row, dict):
                values = [str(row.get(col, '-')) for col in columns]
            else:
                values = [str(getattr(row, col, '-')) for col in columns]
            MenuDisplay.table_row(values, col_widths)
    
    @staticmethod
    def get_multiple_choice(items, title="Pilih item", allow_multiple=False):
        """
        Get user choice(s) dari list.
        
        Args:
            items: List of items
            title: Selection title
            allow_multiple: Bolehkah pilih lebih dari 1
        
        Returns:
            Selected item(s)
        """
        MenuUI.show_list(items, title)
        
        if allow_multiple:
            print(f"\nMasukkan nomor pilihan (pisahkan dengan koma, contoh: 1,2,3)")
            choices_str = MenuInputValidator.get_string("Pilihan: ")
            try:
                indices = [int(c.strip()) - 1 for c in choices_str.split(',')]
                selected = [items[i] for i in indices if 0 <= i < len(items)]
                if not selected:
                    raise MenuInputError("Pilihan tidak valid")
                return selected
            except (ValueError, IndexError):
                raise MenuInputError("Format pilihan tidak valid")
        else:
            item, idx = MenuInputValidator.get_choice_from_list(items, "Pilihan: ")
            return item
