def execute_query(connection, query_with_params):
    """
    Verilen sorguyu çalıştırır ve sonuçları döndürür.

    Args:
        connection: PostgreSQL veritabanı bağlantı nesnesi.
        query_with_params: Çalıştırılacak SQL sorgusu ve varsa parametreleri. 
                           Sorgu sadece string olabilir ya da (query, params) formatında tuple.

    Returns:
        list: Sorgudan dönen sonuçlar.
    """
    try:
        # Query ve parametreleri ayıkla
        query, params = query_with_params if isinstance(query_with_params, tuple) else (query_with_params, None)
        
        # Sorguyu çalıştır
        cursor = connection.cursor()
        cursor.execute(query, params if params else ())
        
        # Sonuçları al ve cursor'u kapat
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        print("Error executing query:", e)
        return None


def print_results(results, headers):
    """
    Sorgu sonuçlarını güzel bir şekilde ekrana yazdırır.

    Args:
        results: Sorgudan dönen sonuçlar (list of tuples).
        headers: Kolon başlıkları (list of strings).
    """
    from tabulate import tabulate

    if not results:
        print("No results found.")
    else:
        print(tabulate(results, headers=headers, tablefmt="psql"))

