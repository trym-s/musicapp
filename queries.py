def get_playlists_with_song_counts():
    """Kullanıcıların playlistlerini ve şarkı sayılarını getirir."""
    return """
    SELECT u.username AS user_name, p.name AS playlist_name, COUNT(ps.song_id) AS song_count
    FROM musicapp.playlist p
    JOIN musicapp."user" u ON p.user_id = u.user_id
    LEFT JOIN musicapp.playlist_song ps ON p.playlist_id = ps.playlist_id
    GROUP BY u.username, p.name
    ORDER BY u.username, p.name;
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
        ORDER BY f.favorite_type;
        """,
        (username,),
    )
def get_most_listened_genre():
    """En çok dinlenen türü getirir."""
    return """
    SELECT g.name AS genre_name, COUNT(lh.song_id) AS listen_count
    FROM musicapp.listening_history lh
    JOIN musicapp.song s ON lh.song_id = s.song_id
    JOIN musicapp.song_genre sg ON s.song_id = sg.song_id
    JOIN musicapp.genre g ON sg.genre_id = g.genre_id
    GROUP BY g.name
    ORDER BY listen_count DESC
    LIMIT 1;
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
    ORDER BY name;
    """

def get_albums_by_artist_query(artist_id):
    """Belirli bir sanatçıya ait albümleri getirir."""
    return """
    SELECT album_id, title 
    FROM musicapp.album 
    WHERE artist_id = %s
    ORDER BY release_date DESC;
    """, (artist_id,)

def get_songs_by_album_query(album_id):
    """Belirli bir albüme ait şarkıları getirir."""
    return """
    SELECT song_id, title, duration 
    FROM musicapp.song 
    WHERE album_id = %s
    ORDER BY title;
    """, (album_id,)

def get_all_playlists():
    """Tüm kullanıcılar ve playlistleri gösteren sorgu."""
    return """
    SELECT 
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
        u.username, p.name
    ORDER BY 
        u.username, p.name;
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

def get_top_rated_songs():
    """En yüksek puanlı şarkıları getirir."""
    return """
    SELECT 
        s.title AS song_title,
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
