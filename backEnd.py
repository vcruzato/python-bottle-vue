# -*- coding: utf-8 -*-

from bottle import run, app, template, post, get, put, delete, static_file, request, json_dumps
from pony.orm import Database, PrimaryKey, Set, Required, db_session, Optional, select
from pony.orm.core import TransactionIntegrityError, CacheIndexError
from os import path

__author__ = 'Vinicius Cruzato'
__python__ = "3.6.3"

# create the database object
db = Database()


# -------------------------------------------------
# HOME PATHS MAPPING USED BY THE WEB SERVER
# -------------------------------------------------
@get('/<filename:re:.*\.js>')
def javascript(filename):
    js_response = static_file(filename, root='./static/js')
    js_response.headers['Content-Type'] = 'application/json'
    js_response.headers['Cache-Control'] = 'no-cache'
    return js_response


@get('/<filename:re:.*\.css>')
def stylesheet(filename):
    return static_file(filename, root='./static/css')


@get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='./static/img')


@get('/<filename:re:.*\.(eot|ttf|woff|woff2|svg)>')
def fonts(filename):
    return static_file(filename, root='./static')


# -------------------------------------------------
# HTML PAGES
# -------------------------------------------------
@get('/')
def index():
    if path.exists('views/index.html'):

        return template('index.html')
    else:
        return template('error.html', error="ERROR: 404: Not Found")


# -------------------------------------------------
# API to see model result
# -------------------------------------------------
@get('/getModelResult')
@db_session
def get_model_result():
    customer_id = request.query.get('customer')
    if customer_id:
        query = select(
            (
                f.fld_name, v.fdvl_value)
                for c in Customer
                for t in Type
                for f in Field
                for v in FieldValue
                if c.cstm_id == customer_id
                and f.fld_typ_id == v.fdvl_typ_id
                and c == t.typ_cstm_id
                and t == f.fld_typ_id
                and f == v.fdvl_fld_id
            )
        return query.to_json()


# -------------------------------------------------
# customer model urls
# -------------------------------------------------
@get('/getCustomer')
@db_session
def get_customer():
    customer_list = []
    for customer in Customer.select():
        customer_list.append({'customer_id': customer.cstm_id, "customer_name": customer.cstm_name})
    return json_dumps({'getCustomer': customer_list})


@post('/addCustomer')
def add_customer():
    customer = request.json.get('customer')
    if customer:
        try:
            with db_session:
                Customer(cstm_name=customer)
                return json_dumps({'status': True})
        except TransactionIntegrityError as e_addCustomer:
            return json_dumps({'status': False, 'error': str(e_addCustomer)})
        except CacheIndexError as e_CacheIndexError:
            return json_dumps({'status': False, 'error': str(e_CacheIndexError)})
        except BaseException as e_BaseException:
            return json_dumps({'status': False, 'error': str(e_BaseException)})
    else:
        return json_dumps({'status': False, 'error': 'Unexpected error'})


@get('/getType')
@db_session
def get_type():
    typ_list = []
    customer = request.query.get('customer')
    if customer:
        customer_id = Customer.get(cstm_id=customer)
        for typ in Type.select(lambda f: f.typ_cstm_id == customer_id):
            typ_list.append({'typ_id': typ.typ_id, "typ_name": typ.typ_name})
        return json_dumps({'getType': typ_list})


@post('/addType')
def add_type():
    customer_id = request.json.get('customer')
    typ = request.json.get('type')
    if customer_id and typ:
        try:
            with db_session:
                customer = Customer.get(cstm_id=customer_id)
                if customer:
                    Type(typ_name=typ, typ_cstm_id=customer)
                    return json_dumps({'status': True})
        except TransactionIntegrityError as e_addCustomer:
            return json_dumps({'status': False, 'error': str(e_addCustomer)})
        except CacheIndexError as e_CacheIndexError:
            return json_dumps({'status': False, 'error': str(e_CacheIndexError)})
        except BaseException as e_BaseException:
            return json_dumps({'status': False, 'error': str(e_BaseException)})
    else:
        return json_dumps({'status': False})


@get('/getField')
@db_session
def get_field():
    field_list = []
    customer = request.query.get('customer')
    typ_id = request.query.get('type')
    if customer:
        customer_id = Customer.get(cstm_id=customer)
        if customer_id:
            typ = Type.get(typ_id=typ_id, typ_cstm_id=customer_id)
            if typ:
                for fld in Field.select(lambda f: f.fld_typ_id == typ):
                    field_list.append({'fld_id': fld.fld_id, "fld_name": fld.fld_name})
        return json_dumps({'getType': field_list})


@post('/addField')
def add_field():
    customer_id = request.json.get('customer')
    typ_id = request.json.get('type')
    field = request.json.get('field')
    if customer_id and typ_id and field:
        try:
            with db_session:
                customer = Customer.get(cstm_id=customer_id)
                if customer:
                    typ_id = Type.get(typ_id=typ_id)
                    if typ_id:
                        Field(fld_name=field, fld_typ_id=typ_id)
                        return json_dumps({'status': True})
        except TransactionIntegrityError as e_addCustomer:
            return json_dumps({'status': False, 'error': str(e_addCustomer)})
        except CacheIndexError as e_CacheIndexError:
            return json_dumps({'status': False, 'error': str(e_CacheIndexError)})
        except BaseException as e_BaseException:
            return json_dumps({'status': False, 'error': str(e_BaseException)})
    else:
        return json_dumps({'status': False})


@get('/getValue')
@db_session
def get_value():
    value_list = []
    typ_id = request.query.get('type')
    typ_id = Type.get(typ_id=typ_id)
    if typ_id:
        for field_value in FieldValue.select(lambda f: f.fdvl_typ_id == typ_id):
            value_list.append({'fdvl_id': field_value.fdvl_id, 'fdvl_value': field_value.fdvl_value})
    return json_dumps({'getType': value_list})


@post('/addValue')
def add_value():
    customer_id = request.json.get('customer')
    typ_id = request.json.get('type')
    field_id = request.json.get('field')
    field_value = request.json.get('value')
    if customer_id and typ_id and field_id and field_value:
        try:
            with db_session:
                customer = Customer.get(cstm_id=customer_id)
                if customer:
                    typ = Type.get(typ_id=typ_id, typ_cstm_id=customer)
                    if typ:
                        fld_id = Field.get(fld_id=field_id, fld_typ_id=typ)
                        if fld_id:
                            FieldValue(fdvl_value=field_value, fdvl_fld_id=fld_id, fdvl_typ_id=typ)
                        return json_dumps({'status': True})
        except TransactionIntegrityError as e_addCustomer:
            return json_dumps({'status': False, 'error': str(e_addCustomer)})
        except CacheIndexError as e_CacheIndexError:
            return json_dumps({'status': False, 'error': str(e_CacheIndexError)})
        except BaseException as e_BaseException:
            return json_dumps({'status': False, 'error': str(e_BaseException)})
    else:
        return json_dumps({'status': False})


@put('/names/<name>')
def __update():
    pass


@delete('/names/<name>')
def __delete_handler():
    pass


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


if __name__ == '__main__':

    # It is used for attaching declared entities to a specific database

    db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
    # db.bind(provider='sqlite', filename=':memory:')

    # The parameter create_tables=True indicates that, if the tables do not already exist,
    # then they will be created using the CREATE TABLE command.
    db.generate_mapping(create_tables=True)

    run(app(), host='0.0.0.0', port=4545)
