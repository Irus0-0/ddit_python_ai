import cx_Oracle

class DaoBook:
    def __init__(self):
        self.conn = cx_Oracle.connect("GROUB_TEST_SPACE", "java", "localhost:1521/xe", encoding="UTF-8")
        self.cur = self.conn.cursor()
        
    def __makeDictFactory__(self, cursor):
        
        columns = [desc[0] for desc in cursor.description]
        
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return data
        
    def select_input_data(self):
        sql = f"""
                SELECT 
                    ei.USER_ID 
                    , ei.DEPT_NO
                    , ei.JBGD_CD
                    , (EXTRACT(YEAR FROM sysdate) - EXTRACT(YEAR FROM ei.JNCMP_YMD)) + 1 AS year
                    , (EXTRACT(YEAR FROM sysdate) - EXTRACT(YEAR FROM u.BRTH_YMD)) + 1 AS OLD
                    , ab.BOOK_NO
                    , abl.book_nm
                    , abl.BOOK_TP
                FROM 
                    USERS u 
                INNER JOIN 
                    EMP_INFO ei 
                ON 
                    u.USER_ID = ei.USER_ID
                INNER JOIN 
                    AI_BOOK ab 
                ON 
                    ab.USER_ID = ei.USER_ID
                INNER JOIN 
                    AI_BOOK_LIST abl
                ON 
                    abl.BOOK_NO = ab.BOOK_NO 
        """
        self.cur.execute(sql)
        list = self.__makeDictFactory__(self.cur)

        return list
    
    def select_predict_data(self):
        sql = f"""
                SELECT 
                    ei.USER_ID 
                    , ei.DEPT_NO
                    , ei.JBGD_CD
                    , (EXTRACT(YEAR FROM sysdate) - EXTRACT(YEAR FROM ei.JNCMP_YMD)) + 1 AS year
                    , (EXTRACT(YEAR FROM sysdate) - EXTRACT(YEAR FROM u.BRTH_YMD)) + 1 AS OLD
                    , i.ITRST_CD 
                FROM 
                    USERS u 
                INNER JOIN 
                    EMP_INFO ei 
                ON 
                    u.USER_ID = ei.USER_ID
                INNER JOIN 
                    ITRST i 
                ON 
                    i.USER_ID = u.USER_ID 
                order by 1
        """
        self.cur.execute(sql)
        list = self.__makeDictFactory__(self.cur)
        #사용자아아디/ 부서번호/ 직급코드/ 나이/ 연차/ 흥미코드
        return list
    
    def select_own_book(self):
        sql = f"""
                SELECT 
                    ei.USER_ID 
                    , ab.BOOK_NO
                FROM 
                    EMP_INFO ei
                INNER JOIN 
                    AI_BOOK ab
                ON 
                    ei.USER_ID = ab.USER_ID 
                ORDER BY 1
        """
        self.cur.execute(sql)
        list = self.__makeDictFactory__(self.cur)
        #사용자아아디/ 부서번호/ 직급코드/ 나이/ 연차/ 흥미코드
        return list
    
    def insert_result(self, my_result):
        sql = f"""
            INSERT INTO
                AI_BK_RSLT (
                    BK_RSLT_NO
                    , USER_ID
                    , BOOK_NO1
                    , BOOK_NO2
                    , BOOK_NO3)
            VALUES(
                {my_result[0]}
                , '{my_result[1]}'
                , {my_result[2]}
                , {my_result[3]}
                , {my_result[4]}
            )
        """
        self.cur.execute(sql)
        self.conn.commit()
        
        return self.cur.rowcount
 
    def __del__(self):
        self.cur.close()
        self.conn.close()
        
if __name__ == '__main__':
    db = DaoBook()
    cnt = db.select_input_data()
    print(cnt[0])

# 1 4 7 8 11 14