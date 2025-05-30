from localjsondb.jsonDB import ValidatedSchemaFactory, BaseJsonDbORM, DoFactory


class _MyStreamlitProp:
    formname: str
    keyname: str
    value: dict = {}


class _MyStreamlitSchema(_MyStreamlitProp, ValidatedSchemaFactory):
    pass


class MyStreamlitDo(_MyStreamlitProp, DoFactory):
    pass


class MyStreamlitOrm(BaseJsonDbORM):
    dbpath = "./mydb/system"
    schema = _MyStreamlitSchema

    def __init__(self, _dbname):
        self.dbname = _dbname
        super().__init__()


MyStremalit = MyStreamlitOrm("myStreamlit")


def getValueByFormnameAndKeyName(_formname, _keyname, _value):
    myStreamlitDo = MyStreamlitDo()
    myStreamlitDo.formname = _formname
    myStreamlitDo.keyname = _keyname
    for a in MyStremalit.jsondb.getByQuery(myStreamlitDo.to_query_dict()):
        data = MyStreamlitDo().from_json_dict(a)
        return data.value[_value]

    return {}


def getValueListByFormnameAndKeyName(_formname, _keyname):
    myStreamlitDo = MyStreamlitDo()
    myStreamlitDo.formname = _formname
    myStreamlitDo.keyname = _keyname
    for a in MyStremalit.jsondb.getByQuery(myStreamlitDo.to_query_dict()):
        return a["value"].keys()
    return []


def upsertValueByFormnameAndKeyName(_formname, _keyname, _value):
    myStreamlitDo_systemrole = MyStreamlitDo()
    myStreamlitDo_systemrole.formname = _formname
    myStreamlitDo_systemrole.keyname = _keyname
    myStreamlitDo_systemrole.value = _value

    MyStremalit.upsertByprimaryKey(myStreamlitDo_systemrole)
