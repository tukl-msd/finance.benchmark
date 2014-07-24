# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import json
import requests
from requests.auth import HTTPBasicAuth

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

### DO NOT FORGET: enable autentication!
@request.restful()
def api():
    response.view = 'generic.'+request.extension
    def GET(*args,**vars):
        patterns = [
            "/benchmark_set[benchmark_set]",
            "/benchmark_set[benchmark_set]/:field",
            "/benchmark_set/{benchmark_set.name.startswith}",
            "/benchmark_set/{benchmark_set.name}/:field",
            "/scheduler_worker[scheduler_worker]",
            "/scheduler_worker[scheduler_worker]/:field",
            "/scheduler_worker/{scheduler_worker.status}",
            "/scheduler_worker/{scheduler_worker.status}/:field",
            "/scheduler_worker/{scheduler_worker.worker_name.startswith}",
            "/scheduler_worker/{scheduler_worker.worker_name}/:field",
            "/results[numeric_results]"
            ]

        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            return dict(content=parser.response)
        else:
            raise HTTP(parser.status,parser.error)

    def POST(table_name,**vars):
        return db[table_name].validate_and_insert(**vars)

    def PUT(table_name,record_id,**vars):
        return db(db[table_name]._id==record_id).update(**vars)

    def DELETE(table_name,record_id):
        return db(db[table_name]._id==record_id).delete()
    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)

@auth.requires_login()
def add_simulation_from_benchmark():
    """
        Start new simulation from the benchmark list
    """
    " Get the names of all existing benchmarks "
    search_str = "http://localhost:8000/tcc/default/api/benchmark_set.json"
    benchmark_row = json.loads(requests.get(search_str).text);

    " Create a list with the benchmark names"
    benchmarks = [benchmark_row['content'][i]['name'] for i in range(len(benchmark_row['content']))]

    " Get the names of all active working nodes"
    search_str = "http://localhost:8000/tcc/default/api/scheduler_worker/active.json"
    working_nodes_row = json.loads(requests.get(search_str).text);

    " Create a list with all active working nodes names"
    working_nd = [(working_nodes_row['content'][i]['id'], working_nodes_row['content'][i]['worker_name']) for i in range(len(working_nodes_row['content']))]

    " Create a form to add new simulation based on pre-determined benchmarks "
    simulation_form = SQLFORM.factory(
                                      Field('benchmark_set', requires=IS_IN_SET(benchmarks, zero=T('-- Select benchmark set --'))),
                                      Field('start_level','integer',default=1, requires=IS_EXPR('int(value)>0')),
                                      Field('final_level','integer',default=16, requires=IS_EXPR('int(value)>0')),
                                      Field('reference_price','double',requires=IS_EXPR('float(value)>0')),
                                      Field('price_precision','double',requires=IS_EXPR('float(value)>0')),
                                      Field('available_resources', 'boolean', requires=IS_IN_SET(working_nd, multiple=True), widget=SQLFORM.widgets.checkboxes.widget))

    " Validate the input data from the form "
    if simulation_form.validate():

        " Get all the fields of benchmark_set table which id corresponds to the selected one from UI  "
        search_str = "http://application_host/default/api/benchmark_set/"+simulation_form.vars.benchmark_set+".json"
        sel_benchmark_row = json.loads(requests.get(search_str).text);

        " Generates the payload to insert a new job register to the database "
        payload = {'market_parameters': benchmark_row['content'][0]['mkt_param'] , 'option_parameters': benchmark_row['content'][0]['opt_param'], 'username': auth.user_id}
        new_job = requests.post("http://application_host/default/api/job.json", data=payload)

        " if it was successfuly added, then add new algorithm parameter register "
        if (new_job == 200):
            payload = {'price_precision': simulation_form.vars.price_precision, 'reference_price': simulation_form.vars.reference_price, 'start_level': simulation_form.vars.start_level, 'final_level': simulation_form.vars.final_level}
            new_alg_param = requests.post("http://application_host/default/api/algorithm_parameters.json", data=payload)
            if (new_job == 200):
                " if it was successfuly added, then assign all the simulations to the selected working nodes "
                for resource in range(len(simulation_form.vars.available_resources)):
                    payload = {'compute_server': resource, 'alg_param': new_alg_param.id, 'job_id': new_job.id}
                    new_sim_param = requests.post("http://application_host/default/api/algorithm_parameters.json", data=payload)
                    if (new_sim !=200):
                        "If there are any error, tell the user "
                        response.flash = T('The simulation could not begin!')
            else:
                response.flash = T('The parameters could not be added!')
        else:
            response.flash = T('The task could not be started!')
    elif simulation_form.errors:
            response.flash = T('Please check for errors on form!')
    else:
        response.flash = T('Please fill the form')
    return dict(simulation_form=simulation_form)
