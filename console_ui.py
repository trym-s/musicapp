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
    print("7. Update a username.")
    print("8. Favorites Management")
    print("9. Show user's top artists and listening times.")
    print("0. Exit.")


def process_option(option, connection):
    """Kullanıcının seçtiği sorguyu çalıştırır."""

    try:
        if option == 1:
            query = get_playlists_with_song_counts()
            results = execute_query(connection, query)
            print_results(results, ["Playlist ID", "User", "Playlist", "Song Count"])

            print("\nOptions:")
            print("1. View songs in a playlist")
            print("2. Rename playlist")
            print("0. Go back")

            sub_option = int(input("Choose an option: "))
            if sub_option == 1:  # View songs in a playlist
                playlist_id = int(input("\nEnter the ID of the playlist to view its songs (or 0 to go back): "))
                if playlist_id == 0:
                    return

                query = get_playlist_name()
                playlist_name_result = execute_query(connection, (query, (playlist_id,)))
                if not playlist_name_result:
                    print("Playlist not found.")
                    return
                playlist_name = playlist_name_result[0][0]

                query = get_songs_in_playlist()
                songs = execute_query(connection, (query, (playlist_id,)))
                if not songs:
                    print("No songs found in this playlist.")
                else:
                    print(f"\nSongs in Selected Playlist: {playlist_name}")
                    print_results(songs, ["Song Title", "Artist Name", "Duration (sec)"])

            elif sub_option == 2:  # Rename playlist
                playlist_id = int(input("\nEnter the ID of the playlist to rename: "))
                query = get_playlist_name()
                playlist_name_result = execute_query(connection, (query, (playlist_id,)))
                if not playlist_name_result:
                    print("Playlist not found.")
                    return

                current_name = playlist_name_result[0][0]
                print(f"Current playlist name: {current_name}")
                new_name = input("Enter the new name for the playlist: ")

                query = update_playlist_name()
                execute_query(connection, (query, (new_name, playlist_id)))
                print(f"Playlist renamed successfully to '{new_name}'!")

            elif sub_option == 0:
                return
            else:
                print("Invalid option. Please try again.")

        elif option == 2:
            query = get_all_usernames()
            usernames = execute_query(connection, query)
            print("\nAvailable Usernames:")
            for username in usernames:
                print(f"- {username[0]}")
            selected_username = input("\nEnter username to view favorites: ")
            query = get_user_favorites_query(selected_username)
            results = execute_query(connection, query)
            if not results:
                print(f"No favorites found for user '{selected_username}'.")
            else:
                print_results(results, ["Favorite Type", "Favorite Name"])

        elif option == 3:
            query = get_top_rated_songs_query()
            results = execute_query(connection, query)
            print(tabulate(results, headers=["Song Title", "Artist", "Rating"], tablefmt="psql"))

        elif option == 4:
            select_artist_album_song(connection)

        elif option == 5:
            query = get_most_listened_genre()
            results = execute_query(connection, query)
            print(tabulate(results, headers=["Genre", "Listen Count"], tablefmt="psql"))

        elif option == 6:
            query = get_average_listening_time_per_user()
            results = execute_query(connection, query)
            print(tabulate(results, headers=["User", "Average Listening Time"], tablefmt="psql"))

        elif option == 7:
            query = get_all_users()
            users = execute_query(connection, query)
            print("\nExisting Users:")
            for user_id, username in users:
                print(f"User ID: {user_id}, Username: {username}")
            user_id = int(input("\nEnter the user ID to update: "))
            new_username = input("Enter the new username: ")
            query = update_username()
            execute_query(connection, (query, (new_username, user_id)))
            print(f"Username updated successfully for User ID {user_id}!")

        elif option == 8:
            print("\nFavorite Management:")
            print("1. Add to Favorites")
            print("2. Remove from Favorites")
            print("0. Go Back")
            favorite_option = int(input("Choose an option: "))

            if favorite_option == 1:
                query = get_all_users()
                users = execute_query(connection, query)
                print("\nAvailable Users:")
                for user_id, username in users:
                    print(f"User ID: {user_id}, Username: {username}")
                user_id = int(input("\nEnter the User ID: "))
                query = get_all_artists_query()
                artists = execute_query(connection, query)
                print("\nAvailable Artists:")
                for artist_id, name in artists:
                    print(f"Artist ID: {artist_id}, Name: {name}")
                input_value = input("\nEnter 'fav [artist_id]' to favorite artist or just [artist_id] to list albums: ")
                if input_value.startswith("fav"):
                    artist_id = int(input_value.split()[1])
                    query = add_to_favorites()
                    execute_query(connection, (query, (user_id, "artist", artist_id)))
                    print("Artist added to favorites successfully!")
                else:
                    artist_id = int(input_value)
                    query, params = get_albums_by_artist_query(artist_id)
                    albums = execute_query(connection, (query, params))
                    print("\nAvailable Albums:")
                    for album_id, title in albums:
                        print(f"Album ID: {album_id}, Title: {title}")
                    input_value = input("\nEnter 'fav [album_id]' to favorite album or just [album_id] to list songs: ")
                    if input_value.startswith("fav"):
                        album_id = int(input_value.split()[1])
                        query = add_to_favorites()
                        execute_query(connection, (query, (user_id, "album", album_id)))
                        print("Album added to favorites successfully!")
                    else:
                        album_id = int(input_value)
                        query, params = get_songs_by_album_query(album_id)
                        songs = execute_query(connection, (query, params))
                        print("\nAvailable Songs:")
                        for song_id, title in songs:
                            print(f"Song ID: {song_id}, Title: {title}")
                        input_value = input("\nEnter 'fav [song_id]' to favorite song: ")
                        if input_value.startswith("fav"):
                            song_id = int(input_value.split()[1])
                            query = add_to_favorites()
                            execute_query(connection, (query, (user_id, "song", song_id)))
                            print("Song added to favorites successfully!")

            elif favorite_option == 2:
                query = get_all_users()
                users = execute_query(connection, query)
                print("\nAvailable Users:")
                for user_id, username in users:
                    print(f"User ID: {user_id}, Username: {username}")
                user_id = int(input("\nEnter the User ID: "))
                query, _ = get_user_favorites_query("placeholder")
                query = query.replace("u.username = %s", "f.user_id = %s")
                favorites = execute_query(connection, (query, (user_id,)))
                if not favorites:
                    print("No favorites found for this user.")
                    return
                print("\nUser Favorites:")
                for idx, favorite in enumerate(favorites, start=1):
                    print(f"{idx}. Type: {favorite[0]}, Name: {favorite[1]}")
                favorite_index = int(input("\nEnter the number of the favorite to remove: "))
                if favorite_index < 1 or favorite_index > len(favorites):
                    print("Invalid selection.")
                    return
                favorite_to_remove = favorites[favorite_index - 1]
                favorite_type = favorite_to_remove[0]
                favorite_name = favorite_to_remove[1]
                query = remove_from_favorites()
                execute_query(connection, (query, (user_id, favorite_type, favorite_name)))
                print(f"Favorite '{favorite_name}' removed successfully!")

        elif option == 0:
            print("Exiting...")
        
        else:
            print("Invalid option. Please try again.")

    except Exception as e:
        print(f"Error: {e}")