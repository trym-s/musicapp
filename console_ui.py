from tkinter import *
from tkinter import ttk, messagebox

class UI:
    def __init__(self, root, query_manager, database):
        self.root = root
        self.query_manager = query_manager
        self.database = database  # Veritabanı bağlantısı referansı

        # Ana pencere başlığı
        self.root.title("Music App")
        
        # Arayüz bileşenlerini oluştur
        self.create_widgets()

        # Pencere kapatma eventi
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Kullanıcı Adı Girişi
        username_frame = ttk.LabelFrame(self.root, text="Kullanıcı Adı")
        username_frame.pack(fill="x", padx=10, pady=5)

        self.username_entry = ttk.Entry(username_frame)
        self.username_entry.pack(fill="x", padx=5, pady=5)

        # Sorgu Butonları ve Sonuç Alanı
        query_frame = ttk.LabelFrame(self.root, text="Sorgular")
        query_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Butonlar
        ttk.Button(query_frame, text="Playlist ve Şarkı Sayısı", command=self.show_playlists).pack(fill="x", padx=5, pady=5)
        ttk.Button(query_frame, text="Kullanıcı Favorileri", command=self.show_user_favorites).pack(fill="x", padx=5, pady=5)
        ttk.Button(query_frame, text="En Çok Dinlenen Tür", command=self.show_most_listened_genre).pack(fill="x", padx=5, pady=5)
        ttk.Button(query_frame, text="En Yüksek Puanlı Şarkılar", command=self.show_top_rated_songs).pack(fill="x", padx=5, pady=5)
        ttk.Button(query_frame, text="Tüm Sanatçılar", command=self.show_all_artists).pack(fill="x", padx=5, pady=5)

        # Sonuç Listesi
        self.result_listbox = Listbox(query_frame, height=15)
        self.result_listbox.pack(fill="both", expand=True, padx=5, pady=5)

    def show_playlists(self):
        try:
            query = self.query_manager.get_playlists_with_song_counts()
            results = self.database.fetch_all(query)
            self.populate_results([f"{row['user_name']} - {row['playlist_name']} ({row['song_count']} şarkı)" for row in results])
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

    def show_user_favorites(self):
        username = self.username_entry.get()
        if not username:
            messagebox.showerror("Hata", "Lütfen bir kullanıcı adı girin.")
            return

        try:
            query, params = self.query_manager.get_user_favorites_query(username)
            results = self.database.fetch_all(query, params)
            self.populate_results([f"{row['favorite_type']}: {row['favorite_name']}" for row in results])
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

    def show_most_listened_genre(self):
        try:
            query = self.query_manager.get_most_listened_genre()
            results = self.database.fetch_all(query)
            self.populate_results([f"{row['genre_name']} ({row['listen_count']} dinlenme)" for row in results])
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

    def show_top_rated_songs(self):
        try:
            query = self.query_manager.get_top_rated_songs_query()
            results = self.database.fetch_all(query)
            self.populate_results([f"{row['song_title']} - {row['artist_name']} ({row['song_rating']})" for row in results])
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

    def show_all_artists(self):
        try:
            query = self.query_manager.get_all_artists_query()
            results = self.database.fetch_all(query)
            self.populate_results([f"{row['artist_id']}: {row['name']}" for row in results])
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

    def populate_results(self, results):
        self.result_listbox.delete(0, END)
        for result in results:
            self.result_listbox.insert(END, result)

    def on_closing(self):
        """Pencere kapatma eventi."""
        if messagebox.askokcancel("Çıkış", "Uygulamadan çıkmak istediğinize emin misiniz?"):
            # Veritabanı bağlantısını kapat
            self.database.close()
            self.root.destroy()  # Tkinter ana döngüsünü sonlandır
