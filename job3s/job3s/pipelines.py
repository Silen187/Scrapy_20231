import mysql.connector
class SaveToMySQL_test_Pipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='103.56.158.31',
            port='3306',
            user='tuyendungUser',
            password='sinhvienBK',
            database='ThongTinTuyenDung'
        )
        
        # self.conn = mysql.connector.connect(
        #     host='127.0.0.1',
        #     port='3306',
        #     user='root',
        #     password='Camtruykich123',
        #     database='tuyendung_2'
        # )

        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        sql = """
            REPLACE INTO Stg_ThongTin(Web, Nganh, Link, TenCV, CongTy, TinhThanh, Luong, LoaiHinh, KinhNghiem, CapBac, HanNopCV, YeuCau, MoTa, PhucLoi, SoLuong) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cur.execute(sql, (item['Web'], item['Nganh'], item['Link'], item['TenCV'], item['CongTy'], item['TinhThanh'], item['Luong'], item['LoaiHinh'], item['KinhNghiem'], item['CapBac'], item['HanNopCV'], item['YeuCau'], item['MoTa'], item['PhucLoi'], item['SoLuong']))
        self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()