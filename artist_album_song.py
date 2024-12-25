from tabulate import tabulate
from queries import *
from console_helpers import execute_query, print_results  # Genel sorgu çalıştırma fonksiyonu
def select_artist_album_song(connection):
    """Sanatçı seçme, albüm seçme, şarkı listeleme ve ek işlemler."""
    # 1. Sanatçıları Listele
    artist_query = get_all_artists_query()
    artists = execute_query(connection, artist_query)

    if not artists:
        print("No artists found.")
        return

    print("\nAvailable Artists:")
    print(tabulate(artists, headers=["ID", "Artist Name"], tablefmt="psql"))
    
    try:
        artist_id = int(input("Enter the ID of the artist: "))
    except ValueError:
        print("Invalid input. Please enter a valid artist ID.")
        return

    # 2. Sanatçının Albümlerini Listele
    album_query = get_albums_by_artist_query(artist_id)
    albums = execute_query(connection, album_query)
    
    if not albums:
        print("No albums found for this artist.")
        return

    print("\nAvailable Albums:")
    print(tabulate(albums, headers=["ID", "Album Title"], tablefmt="psql"))
    
    try:
        album_id = int(input("Enter the ID of the album: "))
    except ValueError:
        print("Invalid input. Please enter a valid album ID.")
        return

    # 3. Albüme Ait Şarkıları Listele
    song_query = get_songs_by_album_query(album_id)
    songs = execute_query(connection, song_query)
    
    if not songs:
        print("No songs found for this album.")
        return

    print("\nSongs in Selected Album:")
    print(tabulate(songs, headers=["ID", "Song Title", "Duration (sec)"], tablefmt="psql"))

    # 4. Şarkılar için Menü
    while True:
        print("\nWhat would you like to do?")
        print("1. Add a song review")
        print("2. View song reviews")
        print("3. Add song to a playlist")  # Yeni seçenek
        print("0. Go back to main menu")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a valid choice.")
            continue

        if choice == 1:  # Add a Song Review
            try:
                song_id = int(input("Enter the song ID to review: "))
                user_id = int(input("Enter your user ID: "))
                review_text = input("Enter your review: ")
                rating = int(input("Enter your rating (1-5): "))
                query = add_song_review()
                execute_query(connection, (query, (user_id, song_id, review_text, rating)))
                print("Review added successfully!")
            except Exception as e:
                print("Error adding review:", e)

        elif choice == 2:  # View Song Reviews
            try:
                song_id = int(input("Enter the song ID to view reviews: "))
                query = get_song_reviews()
                results = execute_query(connection, (query, (song_id,)))
                print_results(results, ["Review", "Rating", "User", "Created At"])
            except Exception as e:
                print("Error retrieving reviews:", e)

        elif choice == 3:  # Add Song to Playlist
            try:
                song_id = int(input("Enter the song ID to add to a playlist: "))

                # Playlist'leri Listele
                query = get_all_playlists()
                playlists = execute_query(connection, query)
                if not playlists:
                    print("No playlists found. Please create a playlist first.")
                    continue

                print("\nAvailable Playlists:")
                print(tabulate(playlists, headers=["Playlist ID", "User Name", "Playlist Name", "Song Count"], tablefmt="psql"))
                # Kullanıcı Playlist'i Seçsin
                playlist_id = int(input("Enter the ID of the playlist to add the song to: "))
                query = add_song_to_playlist()
                execute_query(connection, (query, (playlist_id, song_id)))
                print("Song added to playlist successfully!")
            except Exception as e:
                print("Error adding song to playlist:", e)

        elif choice == 0:  # Return to Main Menu
            break

        else:
            print("Invalid choice. Please try again.")
