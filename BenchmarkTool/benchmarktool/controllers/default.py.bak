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

import pygal
from pygal.style import CleanStyle


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
            "/results[numeric_results]",
            "/job[job]",
            "/job/{job.id}/:field",
            "/market_parameters/{market_parameters.id}",
            "/option_parameters/{option_parameters.id}",
            "/option_parameters/{option_parameters.id}/:field",
            "/option_price/{option_price.id}/:field"
            ]

        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            return dict(content=parser.response)
        else:
            raise HTTP(parser.status,parser.error)

    def POST(table_name,**vars):
        return db[table_name].validate_and_insert(**vars).id

    def PUT(table_name,record_id,**vars):
        return db(db[table_name]._id==record_id).update(**vars)

    def DELETE(table_name,record_id):
        return db(db[table_name]._id==record_id).delete()
    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)

@auth.requires_login()
def add_simulation_from_benchmark():
    if not session.resources: session.resources = 0
    session.resources+=1
    lala = ""

    """
        Start new simulation from the benchmark list
    """
    " Get the names of all existing benchmarks "
    search_str = "http://localhost:8000/benchmarktool/default/api/benchmark_set.json"
    benchmark_row = json.loads(requests.get(search_str).text);

    " Create a list with the benchmark names"
    benchmarks = [benchmark_row['content'][i]['name'] for i in range(len(benchmark_row['content']))]

    " Get the names of all active working nodes"
    search_str = "http://localhost:8000/benchmarktool/default/api/scheduler_worker/active.json"
    working_nodes_row = json.loads(requests.get(search_str).text);

    " Create a list with all active working nodes names"
    working_nd = [(working_nodes_row['content'][i]['id'], working_nodes_row['content'][i]['worker_name']) for i in range(len(working_nodes_row['content']))]


    " Create a form to add new simulation based on pre-determined benchmarks "
    simulation_form=SQLFORM.factory(Field('benchmark_set', requires=IS_IN_SET(benchmarks, zero=T('-- Select benchmark set --'))),
                  Field('start_level','integer',default=1, requires=IS_EXPR('int(value)>0')),
                  Field('multilevel_constant','integer',default=4, requires=IS_EXPR('int(value)>0')),
                  Field('epsilon','double',default=0.02, requires=IS_EXPR('float(value)>0')),
                  Field('number_of_paths_on_first_level','integer',default=10000, requires=IS_EXPR('int(value)>0')),
                  Field('reference_price','double',requires=IS_EXPR('float(value)>0')),
                  Field('price_precision','double',requires=IS_EXPR('float(value)>0')),
                  Field('available_resources', 'list:working_nd', requires=IS_IN_SET(working_nd, multiple=True), widget=SQLFORM.widgets.checkboxes.widget))

    " Validate the input data from the form "
    if simulation_form.validate():
        " Get all the fields of benchmark_set table which id corresponds to the selected one from UI  "
        search_str = "http://localhost:8000/benchmarktool/default/api/benchmark_set/"+simulation_form.vars.benchmark_set+".json"
        sel_benchmark_row = json.loads(requests.get(search_str).text);

        market_parameters= sel_benchmark_row['content'][0]['mkt_parameters']

        option_parameters= sel_benchmark_row['content'][0]['opt_parameters']

        " Generates the payload to insert a new job register to the database "
        payload_job = {'market_parameters': market_parameters , 'option_parameters': option_parameters, 'username': auth.user_id}
        new_job =  json.loads(requests.post("http://localhost:8000/benchmarktool/default/api/job.json", data=payload_job).text);

        " Add algorithm parameters "
        payload_alg_param = {'price_precision': simulation_form.vars.price_precision, 'reference_price': simulation_form.vars.reference_price, 'start_level': simulation_form.vars.start_level, 'multilevel_constant': simulation_form.vars.multilevel_constant, 'epsilon':simulation_form.vars.epsilon,'number_of_paths_on_first_level':simulation_form.vars.number_of_paths_on_first_level }
        new_alg_param = json.loads(requests.post("http://localhost:8000/benchmarktool/default/api/algorithm_parameters.json", data=payload_alg_param).text);

        " Assign all the simulations to the selected working nodes "
        for resource in simulation_form.vars.available_resources:
            payload = {'compute_server': resource, 'alg_parameters': new_alg_param, 'job_id': new_job}
            new_sim_param = json.loads(requests.post("http://localhost:8000/benchmarktool/default/api/simulation.json", data=payload).text)

            " Get market parameter"
            search_str = "http://localhost:8000/benchmarktool/default/api/market_parameters/"+str(market_parameters)+".json"
            sel_mkt_param_row = json.loads(requests.get(search_str).text);
            market_parameters= sel_mkt_param_row['content'][0]
            market_parameters = {key: value for key, value in sel_mkt_param_row['content'][0].items() if key != 'id'}

            " Get option parameter"
            search_str = "http://localhost:8000/benchmarktool/default/api/option_parameters/"+str(option_parameters)+".json"
            sel_opt_param_row = json.loads(requests.get(search_str).text);
            option_parameters= {key: value for key, value in sel_opt_param_row['content'][0].items() if key != 'id'}

            " Get option name"
            search_str = 'http://localhost:8000/benchmarktool/default/api/option_price/'+str(option_parameters['option_type'])+'/name.json'
            option_name = json.loads(requests.get(search_str).text);
            option_name = option_name['content'][0]['name']

            " Update dictionary "
            option_parameters['option_type'] = option_name

            "Queuing all tasks"
            result_id = scheduler.queue_task('new_sim',pvars=dict(mkt_param=market_parameters, opt_param=option_parameters, alg_param=payload_alg_param, sim_id=new_sim_param),group_name='cpu')
            lala = result_id
            "result_id = scheduler.queue_task(new_sim,pvars=dict(mkt_param=json.load(StringIO(market_parameters)), opt_param=json.load(StringIO(option_parameters)), alg_param=payload_alg_param, sim_id=new_sim_param),group_name='cpu')"

            "mail.send('nogueira@rhrk.uni-kl.de','Task ID',str(result_id))"
    return dict(simulation_form=simulation_form,test_var=lala,toobar=response.toolbar())

def results():
    return dict()

def plot_pygal():
    response.headers['Content-Type']='image/svg+xml'
    bar_chart = pygal.Bar(style=CleanStyle) # Then create a bar graph object
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]) # Add some values
    return bar_chart.render()
