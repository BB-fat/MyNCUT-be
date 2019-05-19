import cx_Oracle


class SchoolLife():
    def __init__(self,userid):
        self.userid=userid
        con=cx_Oracle.connect("C##MYNUCT","c8SYjM05x7U","")