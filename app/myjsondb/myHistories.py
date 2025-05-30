import os
# from old.myjsondb.myHistory import MyHistoryOrm, MyHistoryDo
from localjsondb.jsonDB import ValidatedSchemaFactory, BaseJsonDbORM, DoFactory


class _MyHistoryProp:
    gptmodel: str
    input: str
    contentList: list = []


class _MyHistorySchema(_MyHistoryProp, ValidatedSchemaFactory):
    pass


class MyHistoryDo(_MyHistoryProp, DoFactory):
    pass


class MyHistoryOrm(BaseJsonDbORM):
    dbpath = "./mydb/tran"
    schema = _MyHistorySchema

    def __init__(self, _dbname):
        self.dbname = _dbname
        super().__init__()


def deleteile(file_path):
    try:
        # ファイルの存在確認
        if os.path.exists(file_path):
            # ファイルを削除
            os.remove(file_path)
            print(f"{file_path} を削除しました。")
        else:
            print(f"{file_path} が存在しません。")
    except OSError as e:
        print(f"エラー: {file_path} を削除できませんでした。エラー: {e}")


class MyHistoryOrms:
    dbpath = "./mydb/tran"
    db = {}
    
    def __init__(self):
        if not os.path.exists(self.dbpath):
            os.makedirs(self.dbpath)
        for a in self.GetDatabaseList():
            self.db[a] = MyHistoryOrm(a)
        # self.db["myHistory"] = MyHistoryOrm("myHistory")

    def CreateDatabase(self, _projectname):
        self.db[_projectname] = MyHistoryOrm(_projectname)
    
    def GetDatabase(self, _projectname):
        try:
            return self.db[_projectname]
        except Exception as e:
            print(e)
            return ""

    def GetDatabaseList(self):
        # ディレクトリ内のファイル名一覧を取得
        file_list = os.listdir(self.dbpath)

        # .jsonファイルのみをフィルタリングし、拡張子を除く
        json_files_without_extension = [os.path.splitext(file)[0] for file in file_list if file.endswith('.json')]

        return json_files_without_extension

    def DropDatabase(self, _projectname):
        # 削除するファイルのパス
        json_file_path = os.path.join(self.dbpath, _projectname + ".json")
        lock_file_path = os.path.join(self.dbpath, _projectname + ".json.lock")
        deleteile(json_file_path)
        deleteile(lock_file_path)


MyHistories = MyHistoryOrms()


def createProject(_projectname):
    MyHistories.CreateDatabase(_projectname)


def dropProject(_projectname):
    MyHistories.DropDatabase(_projectname)


def getProjectList():
    return MyHistories.GetDatabaseList()


def getValOfPjByKey(gptmodel, input, _projectname):
    MyHistory = MyHistories.GetDatabase(_projectname)
    myHistoryDo = MyHistoryDo()
    myHistoryDo.gptmodel = gptmodel
    myHistoryDo.input = input
    for a in MyHistory.jsondb.getByQuery(myHistoryDo.to_query_dict()):
        return a["contentList"]

    return []


def getAllHistoryOfPj(_projectname):
    MyHistory = MyHistories.GetDatabase(_projectname)
    if "" != MyHistory:
        out = []
        for a in MyHistory.jsondb.getAll():
            out.append({
                "gptmodel": a["gptmodel"],
                "input": a["input"],
                "registration_date": a["registration_date"]
            }
            )

        return out
    else:
        return []


def upsertValToPjByKey(_gptmodel, input, contentList, _projectname):
    MyHistory = MyHistories.GetDatabase(_projectname)
    myHistoryDo_systemrole = MyHistoryDo()
    myHistoryDo_systemrole.gptmodel = _gptmodel
    myHistoryDo_systemrole.input = input
    myHistoryDo_systemrole.contentList = contentList

    MyHistory.upsertByprimaryKey(myHistoryDo_systemrole)


def deletePjByKey(_gptmodel, _input, _registration_date, _projectname):
    MyHistory = MyHistories.GetDatabase(_projectname)
    myHistoryDo_systemrole = MyHistoryDo()
    myHistoryDo_systemrole.gptmodel = _gptmodel
    myHistoryDo_systemrole.input = _input
    myHistoryDo_systemrole.registration_date = _registration_date
    MyHistory.delete(myHistoryDo_systemrole)
