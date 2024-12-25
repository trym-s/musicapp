def get_playlists_with_song_counts():
    """Kullanıcıların playlistlerini, şarkı sayılarını ve playlist ID'sini getirir."""
    return """
    SELECT p.playlist_id AS playlist_id, 
           u.username AS user_name, 
           p.name AS playlist_name, 
           COUNT(ps.song_id) AS song_count
    FROM musicapp.playlist p
    JOIN musicapp."user" u ON p.user_id = u.user_id
    LEFT JOIN musicapp.playlist_song ps ON p.playlist_id = ps.playlist_id
    GROUP BY p.playlist_id, u.username, p.name
    ORDER BY p.playlist_id ASC;
    """

def get_user_favorites_query(username):
    """Belirli bir kullanıcının favorilerini getirir."""
    return (
        """
        SELECT f.favorite_type, 
               CASE 
                   WHEN f.favorite_type = 'artist' THEN a.name
                   WHEN f.favorite_type = 'album' THEN al.title
                   WHEN f.favorite_type = 'song' THEN s.title
               END AS favorite_name
        FROM musicapp.user_favorite f
        LEFT JOIN musicapp.artist a ON f.favorite_type = 'artist' AND f.favorite_id = a.artist_id
        LEFT JOIN musicapp.album al ON f.favorite_type = 'album' AND f.favorite_id = al.album_id
        LEFT JOIN musicapp.song s ON f.favorite_type = 'song' AND f.favorite_id = s.song_id
        JOIN musicapp."user" u ON f.user_id = u.user_id
        WHERE u.username = %s
        ORDER BY f.favorite_id ASC;
        """,
        (username,),
    )


def get_playlist_name():
    """Belirli bir playlist'in adını getirir."""
    return """
    SELECT name
    FROM musicapp.playlist
    WHERE playlist_id = %s;
    """
def add_song_to_playlist():
    """Bir şarkıyı belirli bir playlist'e ekler."""
    return """
    INSERT INTO musicapp.playlist_song (playlist_id, song_id)
    VALUES (%s, %s);
    """
def get_all_playlists():
    """Tüm playlist'leri ve ID'lerini getirir."""
    return """
    SELECT playlist_id, name
    FROM musicapp.playlist
    ORDER BY playlist_id ASC;
    """
def get_all_usernames():
    """Tüm kullanıcı adlarını getirir."""
    return """
    SELECT username 
    FROM musicapp."user"
    ORDER BY username;
    """

def get_song_reviews():
    return """
    SELECT r.review_text, r.rating, u.username, r.created_at
    FROM musicapp.song_review r
    JOIN musicapp."user" u ON r.user_id = u.user_id
    WHERE r.song_id = %s
    ORDER BY r.review_id ASC;
    """

def get_songs_in_playlist():
    """Bir playlist içindeki şarkıları getirir."""
    return """
    SELECT s.title AS song_title, 
           a.name AS artist_name, 
           s.duration AS duration
    FROM musicapp.playlist_song ps
    JOIN musicapp.song s ON ps.song_id = s.song_id
    JOIN musicapp.artist a ON s.artist_id = a.artist_id
    WHERE ps.playlist_id = %s
    ORDER BY s.song_id ASC;
    """


def add_song_review():
    return """
    INSERT INTO musicapp.song_review (user_id, song_id, review_text, rating)
    VALUES (%s, %s, %s, %s);
    """

def get_most_listened_genre():
    """En çok dinlenen türü getirir."""
    return """
    SELECT g.name AS genre_name, COUNT(lh.song_id) AS listen_count
    FROM musicapp.listening_history lh
    JOIN musicapp.song s ON lh.song_id = s.song_id
    JOIN musicapp.song_genre sg ON s.song_id = sg.song_id
    JOIN musicapp.genre g ON sg.genre_id = g.genre_id
    GROUP BY g.name
    ORDER BY listen_count DESC;
    """

def get_top_rated_songs_query():
    """En yüksek puanlı şarkıları getirir."""
    return """
    SELECT s.title AS song_title, a.name AS artist_name, s.rating AS song_rating
    FROM musicapp.song s
    JOIN musicapp.artist a ON s.artist_id = a.artist_id
    WHERE s.rating >= 4.5
    ORDER BY s.rating DESC, s.title;
    """

def get_all_artists_query():
    """Tüm sanatçıları getirir."""
    return """
    SELECT artist_id, name 
    FROM musicapp.artist 
    ORDER BY artist_id ASC;
    """

def get_albums_by_artist_query(artist_id):
    """Belirli bir sanatçıya ait albümleri getirir."""
    return """
    SELECT album_id, title 
    FROM musicapp.album 
    WHERE artist_id = %s
    ORDER BY album_id ASC;
    """, (artist_id,)

def get_songs_by_album_query(album_id):
    """Belirli bir albüme ait şarkıları getirir."""
    return """
    SELECT song_id, title, duration 
    FROM musicapp.song 
    WHERE album_id = %s
    ORDER BY song_id ASC;
    """, (album_id,)

def get_all_playlists():
    """Tüm kullanıcılar ve playlistleri gösteren sorgu."""
    return """
    SELECT 
        p.playlist_id AS playlist_id,       -- Playlist ID'yi ekledik
        u.username AS user_name,
        p.name AS playlist_name,
        COUNT(ps.song_id) AS song_count
    FROM 
        musicapp.playlist p
    JOIN 
        musicapp."user" u ON p.user_id = u.user_id
    LEFT JOIN 
        musicapp.playlist_song ps ON p.playlist_id = ps.playlist_id
    GROUP BY 
        p.playlist_id, u.username, p.name  -- Playlist ID'yi GROUP BY'a ekledik
    ORDER BY 
        u.username, p.name;
    """
def get_all_users():
    """Tüm kullanıcıların ID ve kullanıcı adlarını getirir."""
    return """
    SELECT user_id, username
    FROM musicapp."user"
    ORDER BY user_id;
    """

def update_playlist_name():
    """Bir playlist'in adını günceller."""
    return """
    UPDATE musicapp.playlist
    SET name = %s
    WHERE playlist_id = %s;
    """

def remove_from_favorites():
    """Kullanıcının favorilerinden bir öğeyi siler."""
    return """
    DELETE FROM musicapp.user_favorite
    WHERE user_id = %s AND favorite_type = %s AND favorite_id = %s;
    """
def update_username():
    """Kullanıcı adını güncelleyen sorgu."""
    return """
    UPDATE musicapp."user"
    SET username = %s
    WHERE user_id = %s;
    """
def get_all_users():
    """Tüm kullanıcıların ID ve kullanıcı adlarını getirir."""
    return """
    SELECT user_id, username
    FROM musicapp."user"
    ORDER BY user_id;
    """

def add_to_favorites():
    """Kullanıcı favorilerine sanatçı, albüm veya şarkı ekler."""
    return """
    INSERT INTO musicapp.user_favorite (user_id, favorite_type, favorite_id)
    VALUES (%s, %s, %s);
    """
def get_user_favorites(username):
    """Belirli bir kullanıcının favori sanatçılarını, albümlerini ve şarkılarını getirir."""
    return f"""
    SELECT 
        f.favorite_type,
        CASE 
            WHEN f.favorite_type = 'artist' THEN a.name
            WHEN f.favorite_type = 'album' THEN al.title
            WHEN f.favorite_type = 'song' THEN s.title
        END AS favorite_name
    FROM 
        musicapp.user_favorite f
    LEFT JOIN 
        musicapp.artist a ON f.favorite_type = 'artist' AND f.favorite_id = a.artist_id
    LEFT JOIN 
        musicapp.album al ON f.favorite_type = 'album' AND f.favorite_id = al.album_id
    LEFT JOIN 
        musicapp.song s ON f.favorite_type = 'song' AND f.favorite_id = s.song_id
    JOIN 
        musicapp."user" u ON f.user_id = u.user_id
    WHERE 
        u.username = '{username}'
    ORDER BY 
        f.favorite_type;
    """
def add_to_favorites():
    """Kullanıcı favorilerine sanatçı, albüm veya şarkı ekler."""
    return """
    INSERT INTO musicapp.user_favorite (user_id, favorite_type, favorite_id)
    VALUES (%s, %s, %s);
    """
def get_top_rated_songs():
    """En yüksek puanlı şarkıları getirir."""
    return """
    SELECT 
        s.title AS song ASC_title,
        a.name AS artist_name,
        s.rating AS song_rating
    FROM 
        musicapp.song s
    JOIN 
        musicapp.artist a ON s.artist_id = a.artist_id
    WHERE 
        s.rating >= 4.5
    ORDER BY 
        s.rating DESC, s.title;
    """

def get_average_listening_time_per_user():
    """Kullanıcı başına ortalama dinleme süresini hesaplar ve sonucu tam sayıya çevirir."""
    return """
    SELECT u.username AS user_name, 
           CAST(AVG(lh.duration_listened) AS INT) AS avg_listening_time
    FROM musicapp.listening_history lh
    JOIN musicapp."user" u ON lh.user_id = u.user_id
    GROUP BY u.username
    ORDER BY avg_listening_time DESC;
    """
