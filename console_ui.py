from tabulate import tabulate
from artist_album_song import select_artist_album_song
from queries import *
from console_helpers import * 


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
        try:    
            print_results(results, ["Playlist ID", "User", "Playlist", "Song Count"])
            playlist_id = int(input("\nEnter the ID of the playlist to view its songs (or 0 to go back): "))
            if playlist_id == 0:
                return

            # Playlist adını al
            query = get_playlist_name()
            playlist_name_result = execute_query(connection, (query, (playlist_id,)))
            if not playlist_name_result:
                print("Playlist not found.")
                return
            playlist_name = playlist_name_result[0][0]
        
        # Seçilen playlist içindeki şarkıları listele
            query = get_songs_in_playlist()
            songs = execute_query(connection, (query, (playlist_id,)))
            if not songs:
                print("No songs found in this playlist.")
            else:
                print(f"\nSongs in Selected Playlist: {playlist_name}")
                print_results(songs, ["Song Title", "Artist Name", "Duration (sec)"])
        except Exception as e:
            print("Error retrieving playlist songs:", e)

    elif option == 2:
        try:
            # Kullanıcı adlarını listele
            query = get_all_usernames()
            usernames = execute_query(connection, query)
            if not usernames:
                print("No users found.")
                return
        
            print("\nAvailable Usernames:")
            for username in usernames:
                print(f"- {username[0]}")  # Username'leri listele
        
            # Kullanıcı adı seçimi
            selected_username = input("\nEnter username to view favorites: ")
            query = get_user_favorites_query(selected_username)
            results = execute_query(connection, query)
        
            if not results:
                print(f"No favorites found for user '{selected_username}'.")
            else:
                print_results(results, ["Favorite Type", "Favorite Name"])
        except Exception as e:
            print(f"Error fetching user favorites: {e}")

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
