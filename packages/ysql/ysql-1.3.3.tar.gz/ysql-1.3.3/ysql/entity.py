# -*- coding: utf-8 -*-
from typing import Union, NamedTuple


def Entity(check_type: bool = False):
    """数据类dataclass的装饰器。

    在定义dataclass时，同时将约束条件和默认值赋予类属性。
    通过改造原生dataclass的init方法和getattribute方法，实现sql建表时约束条件的解析，以及正常使用被装饰dataclass时属性值的获取。

    Args:
        check_type(bool): 传入True -> 实例化dataclass时检查属性值和类型注释是否一致，不一致将触发类型错误。否则不检查。

    Example1:

        @Entity
        @dataclass
        class Student:  # 类名即表名，不区分大小写
            name: str  # 字段名以及字段类型
            score: float = 100

    Example2:

        @Entity(check_type=True)  # 启用类型检查
        @dataclass
        class Student:
            name: str  # 字段名以及字段类型
            score: float = 100.0
            # Example1中的score属性虽然注释为float，而实际默认值为int，但仍然可以正常工作（由于python和sqlite都是宽松的类型约束）。
            # 若使用check_type，将进行严格的检查，类型不一致的情况（如Example1）会抛出异常。

    !Note:
        在实用角度上@dataclass应该合并到@Entity内部，这样定义数据类时只需要使用一个装饰器，并且不需要初级使用者关心什么是dataclass，
        但经过测试发现，如果不显式的使用@dataclass装饰器，在实例化数据类时Pycharm将无法给出代码提示，这是不可忍受的。
        并且经过测试发现只有Pycharm2020及之前的版本可以正确给出代码提示，高于2020版存在代码提示的bug，详见:
        https://intellij-support.jetbrains.com/hc/en-us/community/posts/4421575751442-Code-Completion-doesn-t-work-for-class-functions-decorated-with-decorators-that-return-inner-functions

    """

    def decorator(cls):
        orig_getattribute = cls.__getattribute__
        orig_init = cls.__init__

        def getattribute(self, name):
            """重写被装饰dataclass的取值方法"""
            # 只有访问定义的属性时才进一步处理
            if name in set(attr_name for attr_name, attr_type in cls.__annotations__.items()):
                return _parse_attr_value(orig_getattribute(self, name))
            # 访问内部属性则返回原始值
            return orig_getattribute(self, name)

        def init_and_check_type(self, *args, **kwargs):
            """重写被装饰dataclass的初始化方法"""
            orig_init(self, *args, **kwargs)

            for attr_name, attr_type in cls.__annotations__.items():
                # 先检查类型注解是否是允许的数据类型
                if attr_type not in {int, str, float, bytes}:
                    raise TypeError(
                        f"定义'{cls.__name__}'类时，"
                        f"'{attr_name}'属性的类型应该属于: 'int'、'str'、'float'、'bytes'，"
                        f"但得到的是 '{attr_type.__name__}'")

                # 再检查属性值的类型与类型注解是否一致
                attr_value = getattribute(self, attr_name)
                # 不检查默认值为None的属性
                if attr_value is None:
                    continue
                elif not isinstance(attr_value, attr_type):
                    raise TypeError(
                        f"实例化'{cls.__name__}'类时,"
                        f"'{attr_name}'属性的类型应该是 '{attr_type.__name__}' ,"
                        f"但得到的是 '{type(attr_value).__name__}'")

        # 由于无参装饰器的特性，在无参使用该装饰器时，check_type的值被覆盖为cls，因此必须显式的与True进行判断
        if check_type == True:  # noqa
            cls.__init__ = init_and_check_type
        cls.__getattribute__ = getattribute
        return cls

    # 无参使用该装饰器时
    if callable(check_type):
        return decorator(cls=check_type)

    return decorator


class _InnerConstraint(NamedTuple):
    """内部维护的约束类，存储实际约束"""
    constraint: tuple


class _Constant:
    """内部维护常用的sql约束字符串，并不直接对外开放。"""
    PRIMARY_KEY = _InnerConstraint(constraint=("PRIMARY KEY",))
    AUTO_PRIMARY_KEY = _InnerConstraint(constraint=("PRIMARY KEY AUTOINCREMENT",))
    NOT_NULL = _InnerConstraint(constraint=("NOT NULL",))
    UNIQUE = _InnerConstraint(constraint=("UNIQUE",))

    NO_ACTION = 'NO ACTION'
    RESTRICT = 'RESTRICT'
    CASCADE = 'CASCADE'
    SET_NULL = 'SET NULL'
    SET_DEFAULT = 'SET DEFAULT'

    ENABLED_TYPES = (int, str, float, bytes, type(None))
    ENABLED_UNION = Union[ENABLED_TYPES]


class Constraint:
    """以类的形式对外开放的各种字段约束。

    Example:

        @Entity
        @dataclass
        class Student:
            name: str  # 可以不使用约束
            score: float = 100  # 可以只赋予默认值
            address: str = 'HIT', Constraint.not_null  # 同时使用默认值和约束，需要以逗号分隔开
            student_id: int = Constraint.auto_primary_key, Constraint.not_null  # 同时使用多条约束，需要以逗号分隔开

    !Note:
        建议导入Constraint类时使用别名，可以有效简化存在大量约束的使用场景。

        Example:

            from ysql import Constraint as cs

            @Entity
            @dataclass
            class Student:
                name: str
                score: float = 100
                address: str = 'HIT', cs.not_null
                student_id: int = cs.auto_primary_key, cs.not_null

    """

    # =================================================================================================================
    # 1.可直接使用的约束常量
    primary_key = _Constant.PRIMARY_KEY  # 主键
    auto_primary_key = _Constant.AUTO_PRIMARY_KEY  # 自增主键
    not_null = _Constant.NOT_NULL  # 非空
    unique = _Constant.UNIQUE  # 唯一

    # 针对外键的约束
    no_action = _Constant.NO_ACTION
    cascade = _Constant.CASCADE
    set_null = _Constant.SET_NULL
    restrict = _Constant.RESTRICT
    set_default = _Constant.SET_DEFAULT

    # =================================================================================================================
    # 2.需要外部传值的约束
    @staticmethod
    def default(default_value: _Constant.ENABLED_UNION):
        """默认值约束

        Args:
            default_value: 该字段在sql中的默认值，与定义数据类时使用默认值作用类似。

        Example:

            @Entity
            @dataclass
            class Student:
                name: str
                score1: float = 100
                score2: float = Constraint.default(100)  # score1和score2的作用类似
                student_id: int = Constraint.auto_primary_key

        """
        if isinstance(default_value, _Constant.ENABLED_TYPES):
            return _InnerConstraint(constraint=(f'DEFAULT {default_value}',))  # noqa
        raise TypeError(
            f"dataclass属性默认值允许的数据类型: 'int', 'str', 'float', 'bytes',"
            f"但得到的是 '{type(default_value).__name__}'"
        )

    @staticmethod
    def check(check_condition: str):
        """条件约束

        Args:
            check_condition: 具体条件

        Example:

            @Entity
            @dataclass
            class Student:
                name: str
                score: float = Constraint.check('score > 60')  # 需要填写字段的字符形式名称
                student_id: int = Constraint.auto_primary_key

        """
        if type(check_condition) == str:
            return _InnerConstraint(constraint=(f'CHECK({check_condition})',))  # noqa
        raise TypeError(
            f"对dataclass属性使用条件约束时，允许的数据类型: 'str',"
            f"但得到的是 '{type(check_condition).__name__}'")

    @staticmethod
    def foreign_key(entity, field, delete_link=None, update_link=None):
        """外键约束

        Args:
            entity: 外键所在的数据类（父表）
            field: 外键对应的数据类属性
            delete_link: 级联删除方式
            update_link: 级联更新方式

        Example:

            @Entity
            @dataclass
            class Student:  # 父表
                name: str = Constraint.not_null
                student_id: int = Constraint.auto_primary_key

            @Entity
            @dataclass
            class Score:  # 子表
                score: float
                score_id: int = Constraint.auto_primary_key
                # 对student_id字段设置外键关联
                student_id: int = Constraint.foreign_key(entity=Student,
                                                         field='student_id',
                                                         delete_link=Constraint.cascade,
                                                         update_link=Constraint.cascade)

        """
        return _InnerConstraint(constraint=((entity.__name__, field, delete_link, update_link),))  # noqa

    @staticmethod
    def comment(comment: str):
        """字段注释

        Args:
            comment: 具体注释。注意，在sqlite中只能通过DDL(Data Definition Language)查看。

        Example:

            @Entity
                @dataclass
                class Student:
                    name: str = Constraint.comment('学生姓名')
                    student_id: int = Constraint.auto_primary_key, Constraint.comment('学生id')

        """
        if type(comment) == str:
            # 目前仅支持sqlite的注释格式
            return _InnerConstraint(constraint=(f'-- {comment}\n',))  # noqa
        raise TypeError(
            f"对dataclass属性使用sql注释时，允许的数据类型: 'str',"
            f"但得到的是 '{type(comment).__name__}'")


def _parse_constraints(attr_value) -> list[str]:
    """从属性原始值中解析出约束条件。
    Args:
        attr_value: 属性原始值(同时包含默认值和约束条件，但仅在定义数据类时有效，实例化后不再包含约束条件)，如Student.name

    Returns:
        list[约束1, 约束2, 约束3, ...]

    Example:

        @Entity
        @dataclass
        class Student:
            name: str = Constraint.comment('学生姓名')
            student_id: int = Constraint.auto_primary_key, Constraint.comment('学生id')

        print(parse_constraints(Student.name))  # output: ['-- 学生姓名\n']
        print(parse_constraints(Student.student_id))  # output: ['PRIMARY KEY AUTOINCREMENT', '-- 学生id\n']

    """
    if not isinstance(attr_value, tuple):
        return []

    if len(attr_value) == 1 and isinstance(attr_value, _InnerConstraint):
        return list(attr_value.constraint)

    elif len(attr_value) > 1:
        constraints = []

        for item in attr_value:
            if not isinstance(item, _InnerConstraint):
                continue

            if item in constraints:
                raise TypeError(
                    f"重复使用了约束条件: {item.constraint}")
            constraints.append(item.constraint[0])

        return constraints

    else:
        raise TypeError(
            f"属性值的数据结构不满足要求，无法解析出sql约束\n传入的值: {attr_value}")


def _parse_attr_value(attr_value) -> _Constant.ENABLED_UNION:
    """从属性原始值中过滤约束条件，解析出真正的属性值。

    Args:
        attr_value: 属性原始值(同时包含默认值和约束条件，但仅在定义数据类时有效，实例化后不再包含约束条件)，如Student.name

    Returns:
        真正的属性值

    Example:

        @Entity
        @dataclass
        class Student:
            name: str
            student_id: int = Constraint.auto_primary_key

        bob = Student(name='Bob')
        print(parse_attr_value(bob.name))  # output: 'Bob'
        print(parse_attr_value(bob.student_id))  # output: None

    !Note:
        如果对数据类的某个属性使用了约束，且未指定默认值，而在实例化时不传入该属性的值。这不会引发实例化错误，该属性会存在一个默认的None值。
        因此在实例化时请仔细检查是否对每个需要赋值的属性都完成了赋值，避免遗漏某个属性的赋值。

        Example:

            @Entity
            @dataclass
            class Student:
                name: str
                student_id: int = Constraint.auto_primary_key  # 不指定默认值

            bob = Student(name='Bob')  # 实例化时不对student_id传值
            print(bob.student_id)  # output: None

    """
    # 原始值满足类型要求，直接返回该值
    if isinstance(attr_value, _Constant.ENABLED_TYPES):
        return attr_value

    # 首先排除非元组情况
    if not isinstance(attr_value, tuple):
        raise TypeError(
            "数据类的属性值不满足要求，只允许1个基本类型默认值和Constraint类约束")

    constraints = [value for value in attr_value if isinstance(value, _InnerConstraint)]
    values = [value for value in attr_value if isinstance(value, _Constant.ENABLED_TYPES)]

    # 存在基本类型和约束之外的值
    if len(constraints) + len(values) != len(attr_value):
        TypeError(
            "数据类的属性值不满足要求，只允许1个基本类型默认值和Constraint类约束")
    # 存在一个真正属性值
    if len(values) == 1:
        return values[0]
    # 全是约束
    elif len(values) == 0:
        return None
    else:
        TypeError(
            "数据类的属性值不满足要求，只允许1个基本类型默认值和Constraint类约束")
