import mysql.connector
from itemadapter import ItemAdapter

class CleanItem:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        value = adapter.get('MoTa')
        value = value.replace("\\r\\n", "")
        value = value.replace("<\\/span>", "")
        value = value.replace("<\\/strong>", "")
        value = value.replace("<\\/p>", "")
        value = value.replace("<\\/li>", "")
        value = value.replace("<\\/ul>", "")
        adapter['MoTa'] = value.strip()
        return item


class SaveToMySQL_test_Pipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='103.56.158.31',
            port='3306',
            user='tuyendungUser',
            password='sinhvienBK',
            database='ThongTinTuyenDung'
        )

        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        sql = """
            INSERT IGNORE INTO Stg_ThongTin_raw(Web, Nganh, Link, TenCV, CongTy, TinhThanh, Luong, LoaiHinh, KinhNghiem, CapBac, HanNopCV, YeuCau, MoTa, PhucLoi, SoLuong) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cur.execute(sql, (item['Web'], item['Nganh'], item['Link'], item['TenCV'], item['CongTy'], item['TinhThanh'], item['Luong'], item['LoaiHinh'], item['KinhNghiem'], item['CapBac'], item['HanNopCV'], item['YeuCau'], item['MoTa'], item['PhucLoi'], item['SoLuong']))
        self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
        
        
class DatabaseConnector:
    def __init__(self, host, user, port, password, database):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            port = self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def get_links_from_database(self):
        connection = self.connect()
        cursor = connection.cursor()

        query = "SELECT Link FROM Stg_ThongTin_raw WHERE Web =\'TopDev\'"
        cursor.execute(query)

        links = [row[0] for row in cursor.fetchall()]

        cursor.close()
        connection.close()

        return links