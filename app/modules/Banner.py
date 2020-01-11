from app.utils.DB import DB


class Banner():
    @staticmethod
    def getAll():
        """
        获取新闻信息
        :return: {"indexBannner":,"indexNotice":}
        """
        bannner = []
        notice = []
        for eachBanner in DB.c.publicInfo["indexBanner"].find({}, {"_id": 0}):
            bannner.append(eachBanner)
        for eachNotice in DB.c.publicInfo["indexNotice"].find({}, {"_id": 0}):
            notice.append(eachNotice)
        return {"indexBanner": bannner, "indexNotice": notice}
