import psycopg2 as pg
from querrysectors import equity_markets, get_instrument_list

class SectorQuerry:
    def __init__(self,dbname='infront', user='ihs3', password='ihs3', host = '10.234.10.30'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host

    def create_connection(self):
        try:
            self.conn = pg.connect("dbname='" + self.dbname + "' user='" + self.user + "' password='" + self.password +
                                  "' host='" + self.host + "'")
            print("IHS connection: Success")
        except:
            print("Unable to connect to the database")

    def send_querry(self,querry_string):
        cursor = self.conn.cursor()
        cursor.execute(querry_string)
        out = cursor.fetchall()
        return out


#with default
b = SectorQuerry()
b.create_connection()
c = b.send_querry(get_instrument_list('se'))

instrument_post = []
for t in c:
    d = {'feed': t[0],'ticker': t[1]}
    instrument_post.append(d)
