from database.DB_connect import DBConnect
from model.connessione import Conessione
from model.rifugio import Rifugio


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def read_all_rifugi(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = {}
        query = """SELECT distinct r.id as id, r.nome as nome, r.localita as localita
                           FROM rifugio r, connessione c 
                           WHERE (r.id = c.id_rifugio1 or r.id = c.id_rifugio2) and c.anno <= %s"""
        cursor.execute(query, (year,))
        for row in cursor:
            result[row['id']] = (Rifugio(**row))
        conn.close()
        cursor.close()
        return result

    @staticmethod
    def read_all_conessioni(year: int):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """SELECT id, least(id_rifugio1,id_rifugio2) as id1, greatest(id_rifugio1,id_rifugio2) as id2, distanza, difficolta
                        FROM connessione
                        WHERE anno <= %s
                        group by id1,id2"""
        cursor.execute(query, (year,))
        for row in cursor:
            result.append(Conessione(row['id'], row['id1'], row['id2'], row['distanza'], row['difficolta']))
        conn.close()
        cursor.close()
        return result