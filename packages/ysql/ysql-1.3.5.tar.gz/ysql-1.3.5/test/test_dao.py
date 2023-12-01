# -*- coding:utf-8 -*-
from dataclasses import asdict
import pytest

from test.model import Student, DaoStudent, Score

students = [
    Student(name=f'李华{i}', age=i, phone=123456789,
            weight=50.0, height=100.0 + i, address=f'hit{i}',
            student_id=i)
    for i in range(1, 100)
]


@pytest.mark.order(1)
def test_dao_create_table(init_db):
    """创建表"""
    db = init_db
    for dao in db.dao_list:
        dao.create_table()
    db.commit()


@pytest.mark.order(2)
def test_insert(init_db):
    """插入数据"""
    db = init_db
    for student in students:
        record_id = db.dao_student.insert(entity=student)
        db.commit()

        result = db.dao_student.select_student_by_id(record_id)
        result = result[0]
        assert result._asdict() == asdict(students[result.student_id - 1])


def test_select_all(init_db):
    """查询全部"""
    db = init_db
    results = db.dao_student.select_all()

    for result in results:
        assert result._asdict() == asdict(students[result.student_id - 1])


def test_select_all_with_substitute(init_db):
    """使用表名替代符"""
    db = init_db
    results = db.dao_student.select_all_with_substitute()

    for result in results:
        assert result._asdict() == asdict(students[result.student_id - 1])


def test_select_student_by_id(init_db):
    """具体查询"""
    db = init_db
    select_id = 50
    result = db.dao_student.select_student_by_id(student_id=select_id)
    assert result[0]._asdict() == asdict(students[select_id - 1])


def test_generate_sql(init_db):
    """使用单独传入sql的模式"""
    db = init_db
    select_id = 50
    result = db.dao_student.select_student_by_generate_sql_and_id(student_id=select_id,
                                                                  sql_statement=DaoStudent.generate_sql('some args'))
    assert result[0]._asdict() == asdict(students[select_id - 1])


def test_update_name(init_db):
    """更新"""
    db = init_db
    select_id = 50
    new_name = '好家伙'
    db.dao_student.update_name_by_id(name=new_name, student_id=select_id)
    db.commit()
    result = db.dao_student.select_student_by_id(select_id)
    assert result[0].name == new_name


def test_update_name_with_substitute(init_db):
    """使用替代符更新"""
    db = init_db
    select_id = 50
    new_name = '好家伙'
    db.dao_student.update_name_by_id_with_substitute(name=new_name, student_id=select_id)
    db.commit()
    result = db.dao_student.select_student_by_id(select_id)
    assert result[0].name == new_name


def test_update_name_with_double_substitute(init_db):
    """使用替代符更新"""
    db = init_db
    select_id = 50
    new_name = '好家伙'
    with pytest.raises(TypeError) as error:
        db.dao_student.update_name_by_id_with_double_substitute(name=new_name, student_id=select_id)
        db.commit()
        result = db.dao_student.select_student_by_id(select_id)

    assert "sql语句中表名代替符'__'只允许有1个，但存在2个" in str(error.value)


def test_foreign_key_cascade(init_db):
    db = init_db
    db.execute("PRAGMA foreign_keys = ON;")
    select_id = 50
    score = Score(150.0, student_id=select_id)
    db.dao_score.insert(score)
    db.dao_student.delete_student_by_id(student_id=select_id)
    db.commit()

    result = db.dao_score.get_score(select_id)
    assert len(result) == 0


if __name__ == '__main__':
    pytest.main(["-v", __file__])
