from localjsondb.jsonDB import ValidatedSchemaFactory, BaseJsonDbORM, DoFactory


class _MyProjectsettingsProp:
    projectname: str
    pjdir: str = ""
    value: dict = {}


class _MyProjectSettingsSchema(_MyProjectsettingsProp, ValidatedSchemaFactory):
    pass


class MyProjectSettingsDo(_MyProjectsettingsProp, DoFactory):
    pass


class MyProjectSettingsOrm(BaseJsonDbORM):
    dbpath = "./mydb/system"
    schema = _MyProjectSettingsSchema

    def __init__(self, _dbname):
        self.dbname = _dbname
        super().__init__()


MyProjectSettings = MyProjectSettingsOrm("myprojectSettings")


def getPjdirByPjnm(_projectname):
    myProjectSettingsDo = MyProjectSettingsDo()
    myProjectSettingsDo.projectname = _projectname
    for a in MyProjectSettings.jsondb.getByQuery(myProjectSettingsDo.to_query_dict()):
        return a["pjdir"]

    return {}


def getValueByPjnm(_projectname):
    myProjectSettingsDo = MyProjectSettingsDo()
    myProjectSettingsDo.projectname = _projectname
    for a in MyProjectSettings.jsondb.getByQuery(myProjectSettingsDo.to_query_dict()):
        return a["value"]

    return {}


def getAllProject():
    out = []
    for a in MyProjectSettings.jsondb.getAll():
        out.append(a["projectname"])

    if len(out) == 0:
        return [""]

    return out


def upsertPjdirAndValueByPjnm(_projectname, _pjdir, _value):
    myProjectSettingsDo = MyProjectSettingsDo()
    myProjectSettingsDo.projectname = _projectname
    myProjectSettingsDo.pjdir = _pjdir
    myProjectSettingsDo.value = _value

    MyProjectSettings.upsertByprimaryKey(myProjectSettingsDo)


def deletePjSettingsByKey(_projectname):
    myProjectSettingsDo = MyProjectSettingsDo()
    myProjectSettingsDo.projectname = _projectname
    MyProjectSettings.delete(myProjectSettingsDo)
