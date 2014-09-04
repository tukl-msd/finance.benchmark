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
            "/user[auth_user]/{auth_user.id}/:field",
            "/benchmark_set[benchmark_set]",
            "/benchmark_set[benchmark_set]/:field",
            "/benchmark_set/{benchmark_set.name.startswith}",
            "/benchmark_set/{benchmark_set.name}/:field",
            "/job[job]",
            "/job/{job.id}/:field",
            "/market_parameters/{market_parameters.id}",
            "/option_parameters/{option_parameters.id}",
            "/option_parameters/{option_parameters.id}/:field",
            "/option_price/{option_price.id}/:field",
            "/results[numeric_results]",
            "/results[numeric_results]/{numeric_results.id}",
            "/scheduler_worker[scheduler_worker]",
            "/scheduler_worker[scheduler_worker]/:field",
            "/scheduler_worker/{scheduler_worker.id}/:field",
            "/scheduler_worker/{scheduler_worker.status}",
            "/scheduler_worker/{scheduler_worker.status}/:field",
            "/scheduler_worker/{scheduler_worker.worker_name.startswith}",
            "/scheduler_worker/{scheduler_worker.worker_name}/:field",
            "/simulation/{simulation.job_id}"
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

        "Create list of simulations from one job"
        job_sim_list = []
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
            task_id = scheduler.queue_task('new_sim',pvars=dict(mkt_param=market_parameters, opt_param=option_parameters, alg_param=payload_alg_param, sim_id=new_sim_param),group_name='cpu')
            db.commit()

            monitoring = scheduler.queue_task('send_simulation_id',pvars={'task':int(task_id.id),'sim_id':new_sim_param},group_name='cpu')
            job_sim_list.append(int(monitoring.id))
            db.commit()

        send_mail_confirmation = scheduler.queue_task('send_mail',pvars={'task_set':job_sim_list,'job_id':new_job},group_name='cpu')

    return dict(simulation_form=simulation_form,test_var=lala,toobar=response.toolbar())

def results():
    job_id = ''
    simulations =''
    search_str =''
    job_results =[]
    results_form=SQLFORM.factory(Field('Job_ID', requires=[IS_IN_DB(db, db.job.id),IS_NOT_EMPTY()]))
    if results_form.process().accepted:
        job_id = results_form.vars.Job_ID

        " Get all simulations related to Job_ID"
        search_str = 'http://localhost:8000/benchmarktool/default/api/simulation/'+str(job_id)+'.json'
        simulations = json.loads(requests.get(search_str).text);
        simulations = simulations['content']

        for simulation in simulations:
            " Get results from simulation"
            search_str = 'http://localhost:8000/benchmarktool/default/api/results/'+str(simulation['result_id'])+'.json'
            sim_result = json.loads(requests.get(search_str).text);
            sim_result = sim_result['content'][0]

            " Get worker_name "
            search_str = 'http://localhost:8000/benchmarktool/default/api/scheduler_worker/'+str(simulation['compute_server'])+'/worker_name.json'
            working_node = json.loads(requests.get(search_str).text);
            working_node = working_node['content'][0]['worker_name']
            " Create a list with graph data "
            job_results.append({'compute_server':working_node,'energy':sim_result['energy'],'runtime_value':sim_result['runtime_value'],'price':sim_result['price'],'precision':sim_result['precision_value']})

    elif results_form.errors:
        response.flash = T('This job ID doesn\'t exist. Please check it again!')
    return dict(job_id=job_id,results_form=results_form, job_results=job_results)

def plot_graph():
    worker = []
    energy = []
    runtime = []
    price = []
    precision = []

    for result in request.vars.job_results:
        worker.append(result['compute_server']+' - Price:'+str(result['price'])+' - Precision:'+str(result['precision']))
        energy.append(result['energy'])
        runtime.append(result['runtime_value'])
    """
    response.headers['Content-Type']='image/svg+xml'
    bar_chart = pygal.Bar(style=CleanStyle) # Then create a bar graph object
    bar_chart.title = 'Comparative simulation results'
    bar_chart.x_labels = worker
    bar_chart.add('Energy Consumption', energy)
    bar_chart.add('Run Time', runtime)
    """
    """


    response.headers['Content-Type']='image/svg+xml'
    bar_chart = pygal.Bar()
    bar_chart.title = 'Comparative simulation results'
    bar_chart.x_labels = map(str, range(2002, 2013))
    bar_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    bar_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    bar_hart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    bar_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    bar_chart.render()
    """
    "return bar_chart.render()"
    mail.send('nogueira@rhrk.uni-kl.de','ID do resultado',str(worker))

    return dict()
