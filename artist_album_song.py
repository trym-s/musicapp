from tabulate import tabulate
from queries import (
    get_all_artists_query,
    get_albums_by_artist_query,
    get_songs_by_album_query,
)
from console_helpers import execute_query  # Genel sorgu çalıştırma fonksiyonu

def select_artist_album_song(connection):
    """Sanatçı seçme, albüm seçme ve şarkı listeleme işlemleri."""
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
