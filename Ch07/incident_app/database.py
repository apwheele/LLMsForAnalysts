import duckdb
import os

DB_PATH = 'incidents.db'

def get_db_connection():
    return duckdb.connect(DB_PATH)

def init_db():
    conn = get_db_connection()
    # Create incident table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS incident (
            incidentid VARCHAR PRIMARY KEY,
            date DATE,
            address VARCHAR,
            firearmtype VARCHAR,
            offenders VARCHAR,
            victims VARCHAR,
            narrative VARCHAR
        )
    ''')
    
    # Create images table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS images (
            incidentid VARCHAR,
            image_path VARCHAR,
            FOREIGN KEY (incidentid) REFERENCES incident(incidentid)
        )
    ''')
    conn.close()

def add_incident(incident_data, image_paths):
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO incident (incidentid, date, address, firearmtype, offenders, victims, narrative)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            incident_data['incidentid'],
            incident_data['date'],
            incident_data['address'],
            incident_data.get('firearmtype'),
            incident_data.get('offenders'),
            incident_data.get('victims'),
            incident_data['narrative']
        ))
        
        for path in image_paths:
            conn.execute('INSERT INTO images (incidentid, image_path) VALUES (?, ?)', (incident_data['incidentid'], path))
            
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def search_incidents(keyword):
    conn = get_db_connection()
    # Simple keyword search across all fields using ILIKE and OR
    query = '''
        SELECT * FROM incident 
        WHERE incidentid ILIKE ? 
        OR address ILIKE ? 
        OR firearmtype ILIKE ? 
        OR offenders ILIKE ? 
        OR victims ILIKE ? 
        OR narrative ILIKE ?
    '''
    like_pattern = f'%{keyword}%'
    results = conn.execute(query, [like_pattern] * 6).fetchall()
    
    # Convert results to a list of dicts for easier template handling
    columns = [desc[0] for desc in conn.description]
    incidents = [dict(zip(columns, row)) for row in results]
    conn.close()
    return incidents

def get_incident(incidentid):
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM incident WHERE incidentid = ?', (incidentid,)).fetchone()
    if result:
        columns = [desc[0] for desc in conn.description]
        incident = dict(zip(columns, result))
        
        images = conn.execute('SELECT image_path FROM images WHERE incidentid = ?', (incidentid,)).fetchall()
        incident['images'] = [row[0] for row in images]
        conn.close()
        return incident
    conn.close()
    return None

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
