def create_table_tables() -> str:
    return """
    CREATE TABLE IF NOT EXISTS tables
    (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    number INTEGER NOT NULL,
    id_hall_type INTEGER NOT NULL,
    FOREIGN KEY (id_hall_type) REFERENCES hall_types(id))
    """
def create_table_hours() -> str:
    return """
    CREATE TABLE IF NOT EXISTS hours
    (hour INTEGER PRIMARY KEY NOT NULL)
    """
def create_table_hall_types() -> str:
    return """
    CREATE TABLE IF NOT EXISTS hall_types
    (id INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
    description TEXT NOT NULL)
    """
def create_table_reserve() -> str:
    return """
    CREATE TABLE IF NOT EXISTS reserve
    (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    id_table INTEGER NOT NULL,
    hour INTEGER NOT NULL,
    date TEXT NOT NULL,
    client TEXT,
    client_id INTEGER,
    reserved INTEGER DEFAULT 0 NOT NULL,
    FOREIGN KEY (id_table) REFERENCES tables(id))
    """
def create_table_admins() -> str:
    return """
    CREATE TABLE IF NOT EXISTS admins
    (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    client_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    active INTEGER DEFAULT 1 NOT NULL)
    """
def insert_reserve_by_date() -> str:
    return """
    INSERT INTO reserve (id_table, "hour", date, client, client_id, reserved)
    SELECT t.id ,h.[hour], ?, NULL, NULL, 0 
    FROM tables as t
    CROSS JOIN hours AS h
    """
def select_reserve_by_date() -> str:
    return """
    SELECT * FROM reserve
    WHERE date = ?
    """
def select_unreserved_hours_by_date() -> str:
    return """
    SELECT 
        DISTINCT r.[hour]  
    FROM reserve as r
    WHERE r.date = ?
        AND reserved = 0
        AND (r.date > DATE() or  (r.date = DATE() 
        AND r.[hour] > ?))    
        AND r.[hour] <= ((SELECT MAX([hour]) FROM hours)-?)
    ORDER BY r.[hour]
    """
def select_unreserved_tables_by_date_duration_hour() -> str:
    return """
    SELECT 
        distinct r.id_table, 
        ht.description, 
        t.[number]
    FROM reserve as r
    INNER JOIN tables as t ON t.id = r.id_table 
    INNER JOIN hall_types as ht on ht.id = t.id_hall_type 
    WHERE 
    r.date= ?
    AND r.reserved=0
    AND r.[hour] between ? and ?
    GROUP BY r.id_table, ht.description , t.[number]
    HAVING count(*)>= ?
    ORDER BY r.id_table
    """
def select_table_by_id() -> str:
    return """
    SELECT 
        ht.description,
        t.[number]  
    FROM tables as t
    INNER JOIN hall_types as ht ON ht.id =t.id_hall_type 
    WHERE t.id = ?
    """
def update_reserve_client_by_id_table_date_hour() -> str:
    return """
    UPDATE reserve
    SET client = ?, client_id = ?, reserved = ?
    WHERE id_table = ? AND date = ? AND hour = ?
    """
def select_admins_client_id() -> str:
    return """
    SELECT client_id
    FROM admins 
    WHERE active = 1
    """
def select_admins_username_by_client_id() -> str:
    return """
    SELECT username
    FROM admins 
    WHERE client_id = ?
    """