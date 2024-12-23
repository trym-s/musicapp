from tabulate import tabulate
from artist_album_song import select_artist_album_song
from queries import *
from console_helpers import execute_query


def display_options():
    """Mevcut sorgu seçeneklerini ekrana yazdırır."""
    print("\nAvailable Queries:")
    print("1. List all playlists with song counts.")
    print("2. Show user favorites (Artists, Albums, Songs).")
    print("3. List top-rated songs.")
    print("4. Select Artist > Album > Songs.")
    print("5. Show most listened genre.")
    print("6. Show average listening time per user.")
    print("0. Exit.")

def process_option(option, connection):
    """Kullanıcının seçtiği sorguyu çalıştırır."""
    if option == 1:
        query = get_playlists_with_song_counts()
        results = execute_query(connection, query)
        print(tabulate(results, headers=["User", "Playlist", "Song Count"], tablefmt="psql"))
    elif option == 2:
        username = input("Enter username to view favorites: ")
        query = get_user_favorites_query(username)
        results = execute_query(connection, query)
        print(tabulate(results, headers=["Favorite Type", "Favorite Name"], tablefmt="psql"))
    elif option == 3:
        query = get_top_rated_songs_query()
        results = execute_query(connection, query)
        print(tabulate(results, headers=["Song Title", "Artist", "Rating"], tablefmt="psql"))
    elif option == 4:
        select_artist_album_song(connection)    
    elif option == 5:  # En çok dinlenen tür
        query = get_most_listened_genre()
        results = execute_query(connection, query)
        print(tabulate(results, headers = ["Genre", "Listen Count"], tablefmt="psql"))
    elif option == 6:  # Kullanıcı başına ortalama dinleme süresi
        query = get_average_listening_time_per_user()
        results = execute_query(connection, query)
        print(tabulate(results, headers = ["User", "Average Listening Time"], tablefmt="psql"))
    elif option == 0:
        print("Exiting...")
    else:
        print("Invalid option. Please try again.")
