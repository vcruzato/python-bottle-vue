# -*- coding: utf-8 -*-

from pony.orm import *


__author__ = 'Vinicius Cruzato'
__python__ = "3.6.3"

# create the database object
db = Database()

# -------------------------------------------------
# ORM CLASSES
# -------------------------------------------------
class Customer(db.Entity):
    cstm_id = PrimaryKey(int, auto=True)
    cstm_name = Required(str, unique=True)
    type = Set('Type')


class Type(db.Entity):
    typ_id = PrimaryKey(int, auto=True)
    typ_cstm_id = Required(Customer)
    typ_name = Required(str)
    field = Set('Field')
    values = Set('FieldValue')


class Field(db.Entity):
    fld_id = PrimaryKey(int, auto=True)
    fld_typ_id = Required(Type)
    fld_name = Required(str)
    field_value = Optional('FieldValue')


class FieldValue(db.Entity):
    fdvl_id = PrimaryKey(int, auto=True)
    fdvl_fld_id = Required(Field)
    fdvl_value = Required(str)
    fdvl_typ_id = Required(Type)