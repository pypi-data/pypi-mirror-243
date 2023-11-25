# -*- coding: utf-8 -*-
from ysql import Constraint, _parse_constraints
from ysql.tool import log

# ====================================================================================================================
# 约定的表名代替符，在sql语句中凡是涉及本表表名的，均可采取此代替符，内部可自动替换。
TABLE_SUBSTITUTE = '__'
SQL_STATEMENT = 'sql_statement'


# ====================================================================================================================
# 装饰器方法
def Dao(entity):
    """对数据访问类使用的装饰器，用于绑定数据类和数据访问类

    Args:
        entity: 该数据访问类对应的数据类

    Example:

        @Entity
        @dataclass
        class Student:  # 定义一个数据类
            name: str
            score: float

        @Dao(Student)  # 通过Dao装饰器绑定对应的数据类
        class DaoStudent:  # 定义一个数据访问类
            ...

    """

    def decorator(cls):
        # 新增cursor属性
        setattr(cls, "cursor", None)
        # 新增entity属性
        setattr(cls, "entity", entity)
        # 新增更新游标方法
        setattr(cls, update_cursor.__name__, update_cursor)
        # 新增生成表方法
        setattr(cls, generate_sql_create_table.__name__, generate_sql_create_table)
        # 新增插入方法
        setattr(cls, "insert", insert)
        return cls

    return decorator


def Sql(static_sql_statement: str):
    """执行sql语句的装饰器，传入sql语句的同时会自动实现被装饰函数。

    Args:
        static_sql_statement: 简单固定的纯字符串sql语句。

    Example1:

        # 对于简单固定的sql语句可以直接传入Sql装饰器。
        # 此段代码无法直接运行，需要首先连接数据库并插入记录才可运行。

        @Entity
        @dataclass
        class Student:
            name: str
            score: float
            student_id: int = Constraint.auto_primary_key

        @Dao(Student)
        class DaoStudent:

            @Sql("select * from student where student_id=?;")
            def get_student(self, student_id):
                pass  # 此处并非以pass示意省略，而是Sql装饰器会自动实现该函数，因此实际使用时均只需要pass即可。

    Example2:

        # 复杂sql语句可能需要外部传参，此时应该通过隐藏的参数sql_statement来传递复杂sql语句。
        # 此段代码无法直接运行，需要首先连接数据库并插入记录才可运行。

        @Dao(Student)
        class DaoStudent:

            @staticmethod  # 借助静态方法装饰器，可以避免烦人且不需要的self参数的传递。也可以将该方法定义在其他任何位置。
            def generate_sql(*arg, **kwargs) -> str:
                print(*arg, **kwargs)
                return "select name from student where student_id=?;"

            @Sql("select * from student where student_id=?;")
            def get_student(self, student_id):
                pass

            @Sql  # 不再直接传递sql语句
            def get_student_name(self, student_id):
                pass

        dao = DaoStudent()
        result1 = dao.get_student(student_id=1)
        result2 = dao.get_student_name(student_id=1,
                                       sql_statement=Dao.generate_sql('some args'))  # 通过隐藏的sql_statement参数传递sql语句。

        # 将以列表形式返回查询结果，其中每条记录的数据格式都是具名元组（与数据类类似）
        # result1: [namedtuple('Record', 'name score student_id'), ...]  查询全部字段时，具名元组与定义的数据类完全一致。
        # result2: [namedtuple('Record', 'name'), ...]  # 查询部分字段时，仅以查询的字段生成相应的具名元组。

    !Note:
        设计思想始终是sql语句与数据传递分离。
        1.对于简单sql情况，通过Sql装饰器传递sql语句，被装饰器函数传递数据。
        2.对于复杂sql情况，为避免sql注入，请勿直接将数据与sql模板进行拼接，而是通过隐藏的参数sql_statement来传递复杂sql语句，被装饰器函数
          仍然负责传递数据。

    """

    def decorator(func):  # noqa

        def wrapper(self, *args, **kwargs):
            sql_statement = static_sql_statement

            if SQL_STATEMENT in kwargs and callable(static_sql_statement):
                # 取出这个特殊参数，并从参数字典中移除
                sql_statement = kwargs.pop(SQL_STATEMENT)

            if isinstance(sql_statement, str):
                ValueError(
                    f"传入的sql语句应该是 'str' 类型，但得到的是 {type(sql_statement).__name__}")

            sql_statement = __check_table_substitute(sql_statement=sql_statement, entity=self.entity)
            log.debug(f"转换后的sql:{sql_statement}")

            self.cursor.execute(sql_statement, __flatten_args_and_kwargs(args, kwargs))
            return self.cursor.fetchall()

        return wrapper

    if callable(static_sql_statement):
        return decorator(func=static_sql_statement)

    return decorator


def Insert(func):  # noqa
    """执行插入功能的装饰器，会自动生成插入sql语句，以及自动实现被装饰函数。

    Returns:
        自动返回刚插入记录的自增主键（如果使用自增主键）。

    Example:

        # 此段代码无法直接运行，需要首先连接数据库才可运行。

        @Entity
        @dataclass
        class Student:
            name: str
            score: float
            student_id: int = Constraint.auto_primary_key

        @Dao(Student)
        class DaoStudent:

            @Insert  # 无需传递任何参数或者sql语句。
            def insert(self, entity):  # entity是必须的固定参数。
                pass  # 此处并非以pass示意省略，而是Insert装饰器会自动实现该函数，因此实际使用时均只需要pass即可。

        dao = DaoStudent()
        bob = Student(name='Bob', score=95.5)
        dao.insert(entity=bob)  # 将整条记录以数据类的形式插入数据库，避免了同时使用多个参数的麻烦。

    !Note:
        由于插入部分的结构完全固定，因此对数据访问类使用Dao装饰器后，会自动内置insert(entity)方法，无需额外定义（建议），可直接调用，但缺点是无法获取代码提示。

    """

    def wrapper(self, entity):
        """entity参数是传入的数据类实例（对象），而self.entity是定义的数据类（类）"""

        # 获取entity类的属性名和类型
        fields = [field_name for field_name, _ in self.entity.__annotations__.items()]

        # 过滤掉有自增主键约束的属性
        fields = [field_name for field_name in fields
                  if Constraint.auto_primary_key[0]
                  not in _parse_constraints(attr_value=getattr(self.entity, field_name, None))]

        sql_statement = f"insert into {self.entity.__name__} " \
                        f"({', '.join(field_name for field_name in fields)}) " \
                        f"values ({', '.join('?' for _ in fields)});"
        log.debug(f"生成的插入sql:{sql_statement}")

        if not isinstance(entity, self.entity):
            raise TypeError(
                f"insert方法传入参数的类型和绑定的Entity不一致，"
                f"应传入 {self.entity.__name__} 实例，但得到的是 {type(entity).__name__}")

        values = [getattr(entity, field_name) for field_name in fields]
        self.cursor.execute(sql_statement, values)

        return self.cursor.lastrowid

    return wrapper


# ====================================================================================================================
# 被装饰数据访问类新增的方法
@Insert
def insert(self, entity):  # noqa
    """默认内置的insert方法，无需额外实现，可以直接调用。

    Args:
        entity: 数据类的实例

    Returns:
        自动返回刚插入记录的自增主键（如果使用自增主键）。

    Example:

        # 此段代码无法直接运行，需要首先连接数据库才可运行。

        @Entity
        @dataclass
        class Student:
            name: str
            score: float
            student_id: int = Constraint.auto_primary_key

        @Dao(Student)
        class DaoStudent:
            pass

        dao = DaoStudent()
        bob = Student(name='Bob', score=95.5)
        student_id = dao.insert(entity=bob)  # 返回刚插入记录的自增主键

    """
    pass


def update_cursor(self, cursor):
    """更新dao中的游标"""
    self.cursor = cursor


def generate_sql_create_table(self):
    """自动实现的建表语句"""
    table_name = self.entity.__name__.lower()
    # 获取字段名称和类型的字典
    fields = self.entity.__annotations__

    field_definitions = []
    foreign_key_constraints = []

    for field_name, field_type in fields.items():
        # 获取字段的SQL类型
        sql_type = __convert_to_sql_type(field_type)
        # 获取字段的约束条件
        constraints = _parse_constraints(attr_value=getattr(self.entity, field_name, None))

        foreign_key_constraint = [item for item in constraints
                                  if isinstance(item, tuple)]
        constraints = [item for item in constraints
                       if item not in foreign_key_constraint]
        # 有外键
        if len(foreign_key_constraint) == 1:
            foreign_key_constraint = __generate_sql_foreign_key(field_name=field_name,
                                                                constraint=foreign_key_constraint[0])
            foreign_key_constraints.append(foreign_key_constraint)

        elif len(foreign_key_constraint) > 1:
            raise TypeError(
                '一个属性只能指定一个外键')

        # 合并其他约束条件
        constraint = " ".join(constraints)

        # 拼接字段定义
        field_definition = f"{field_name} {sql_type} {constraint}"
        field_definitions.append(field_definition)
    # 将外键约束列表添加到字段定义列表的末尾
    field_definitions.extend(foreign_key_constraints)
    # 默认为严格的数据类型约束
    sql_create_table = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(field_definitions)});"
    log.debug(f"生成的 SQL 语句：{sql_create_table}")
    return sql_create_table


# ====================================================================================================================
# 模块内使用的方法
def __convert_to_sql_type(python_type):
    """转换python注释类型为sql类型"""
    if python_type in {int, bool}:
        return "INTEGER"
    elif python_type == str:
        return "TEXT"
    elif python_type == float:
        return "REAL"
    elif python_type == bytes:
        return "BLOB"

    raise ValueError(
        f"ysql不支持该python数据类型: {python_type}")  # noqa


def __generate_sql_foreign_key(constraint: tuple, field_name: str):
    """生成外键约束的sql语句"""
    log.debug(f'获得的外键约束：{constraint}')
    foreign_key_entity, foreign_key_name, foreign_key_delete_link, foreign_key_update_link = constraint

    if foreign_key_delete_link is None and foreign_key_update_link is None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name})"

    # 存在表关联的情况
    elif foreign_key_delete_link is not None and foreign_key_update_link is None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name}) ON DELETE {foreign_key_delete_link}"
    elif foreign_key_delete_link is None and foreign_key_update_link is not None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name}) ON UPDATE {foreign_key_update_link}"
    elif foreign_key_delete_link is not None and foreign_key_update_link is not None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name}) " \
               f"ON DELETE {foreign_key_delete_link} ON UPDATE {foreign_key_update_link} "


def __flatten_args_and_kwargs(*args):  # 不能传入**kwargs，这由调用条件决定了
    """一维展开不定参数，返回列表形式"""

    def flatten_args(arg):
        if isinstance(arg, (list, tuple)):
            # 如果是列表或元组，递归展开每个元素
            return [item for sublist in map(flatten_args, arg) for item in sublist]
        elif isinstance(arg, dict):
            # 如果是字典，取出所有值并递归展开
            return flatten_args(list(arg.values()))
        else:
            # 否则返回单个值
            return [arg]

    return tuple(flatten_args(args))


def __check_table_substitute(sql_statement: str, entity):
    """将表名代替符替换为真正的表名"""
    if sql_statement.count(TABLE_SUBSTITUTE) > 1:
        raise TypeError(
            f"sql语句中表名代替符'{TABLE_SUBSTITUTE}'只允许有1个，但存在{sql_statement.count(TABLE_SUBSTITUTE)}个")

    return sql_statement.replace(TABLE_SUBSTITUTE, entity.__name__.upper())
