# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


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

def admin():
    return dict()



"""
Administrative forms
"""
def add_algorithm():
    """
    form to add new algorithms on database.
    """
    alg_form=SQLFORM.factory(Field('name', requires=IS_NOT_IN_DB(db,db.algorithm.name)),
                             Field('description'),
                             table_name='algorithm')
    if alg_form.accepts(request,session):
        session.algorithm_id = db.algorithm.insert(**db.algorithm._filter_fields(alg_form.vars))
        redirect(URL('add_algorithm_parameters'))
    elif alg_form.errors:
        response.flash = T('Please check for errors on form!')
    else:
        response.flash = T('Please fill the form')
    return dict(alg_form=alg_form)

def add_algorithm_parameters():
    """
    form to add new algorithms paramethers
    """

    " Display existing parameters of the algorithm "
    alg_param = db(db.algorithm_parameters.algorithm==session.algorithm_id).select(db.algorithm_parameters.name,
                                                                                   db.algorithm_parameters.description,
                                                                                   orderby=db.algorithm_parameters.name)
    alg_param_headers={'algorithm_parameters.name':T('Parameters Name'),'algorithm_parameters.description':T('Description')}

    " Form to add new paramters to the algorithm "
    alg_param_form=SQLFORM.factory(Field('name'),
                             Field('description'),
                             table_name='algorithm_parameters')
    alg_param_form.add_button('Back', URL('admin.html'))

    " Form processing actions "
    if alg_param_form.accepts(request.vars, session):
        alg_param_form.vars.algorithm = session.algorithm_id
        db.algorithm_parameters.insert(**db.algorithm_parameters._filter_fields(alg_param_form.vars))
        redirect(URL('add_algorithm_parameters'))
    elif alg_param_form.errors:
        response.flash = T('Please check for errors on form!')
    else:
        response.flash = T('Please fill the form')

    return dict(alg_param_form=alg_param_form, alg_param=alg_param, alg_param_headers=alg_param_headers)

def add_option_price():
    """
    form to add new option price
    """
    " Display existing option pricers "
    opt_price = db().select(db.option_price.id,
                          db.option_price.name,
                          orderby=db.option_price.name)
    opt_price_header={'option_price.id':T('Unique Identifier'),'option_price.name':T('Option Name')}


    "Form to add new option pricer"
    opt_price_form = SQLFORM.factory(Field('name'),
                                     table_name= 'option_price')

    "Form processing actions"
    if opt_price_form.accepts(request.vars, session):
        db.option_price.insert(**db.option_price._filter_fields(opt_price_form.vars))
        redirect(URL('add_option_price'))
    elif opt_price_form.errors:
        response.flash = T('Please check for errors on form!')
    else:
         response.flash = T('Please fill the form')

    opt_price_form.add_button(T('Back'), URL('admin.html'))


    return dict(opt_price=opt_price, opt_price_form=opt_price_form, opt_price_header=opt_price_header)

def set_market_parameters():
    """
    Exposes form to set Market Parameters
    """
    "If there is an Market Parameter ID stored in this session (session.mkt_param_id),    "
    "then show update form, otherwise, add a new register to the market_parameters' table."
    mkt_form=SQLFORM(db.market_parameters,db.market_parameters(session.mkt_param_id),showid=False)

    if mkt_form.accepts(request, session):
        response.flash = 'form accepted'

        "Stores Market Parameter ID in the session"
        session.mkt_param_id=mkt_form.vars.id

        "If the function receive 'benchmark' as argument, returns to benchmark set admin page"
        if request.args(0)=='benchmark_set':
            redirect(URL('benchmark_set'))

    elif mkt_form.errors:
        response.flash = T('Form has errors')
    else:
        response.flash = T('Please fill the form')
    return dict(mkt_form=mkt_form)

def set_option_parameters():
    """
    Exposes form to set Option Parameters
    """
    "If there is an Option Parameter ID stored in this session (session.opt_param_id),    "
    "then show update form, otherwise, add a new register to the option_parameters' table."
    opt_form=SQLFORM(db.option_parameters,db.option_parameters(session.opt_param_id),labels={'option_type':T('Option Type'),'strike_price':T('Strike Price'), 'time_to_maturity':T('Time to Maturity'), 'lower_barrier':T('Lower Barrier'),'lbarrier_type':T('Lower Barrier Type'),'lbarrier_value':T('Lower Barrier Value'), 'upper_barrier':T('Upper Barrier'), 'ubarrier_type':T('Upper Barrier Type'), 'ubarrier_value':T('Upper Barrier Value')}, showid=False)
    """lb= (request.vars.lower_barrier==False) and """
    if opt_form.accepts(request, session):
        response.flash = T('Form accepted')

        "Stores Market Parameter ID in the session"
        session.opt_param_id=opt_form.vars.id

        "If the function receive 'benchmark' as argument, returns to benchmark set admin page"
        if request.args(0)=='benchmark_set':
            redirect(URL('benchmark_set'))

    elif opt_form.errors:
        response.flash = T('Form has errors')
    else:
        response.flash = T('please fill the form')
    return dict(opt_form=opt_form)

def set_algorithm():
    """
    Form to set an algorithm for a simulation
    """
    "Retrieve Algorithm names"
    algorithm = db().select(db.algorithm.ALL, orderby=db.algorithm.name)
    algorithm_names=[OPTION(algorithm[i].name, _value=str(algorithm[i].id)) for i in range(len(algorithm))]
    algorithm_names.insert(0, OPTION('- Please select an algorithm -', _value=''))

    "Create a form to select algorithm"
    algorithm_form=FORM(TR(T("Select an algorithm:"),
          SELECT(_name='algorithm_select', *algorithm_names)),
          TR(INPUT(_type='submit')))

    "Select the algortithm already selected, otherwise select the first one"
    algorithm_form.vars.algorithm_select = session.algorithm_id

    if algorithm_form.accepts(request, session):
        "Stores algorithm.id in the session"
        session.algorithm_id=request.vars.algorithm_select
        if request.args(0)=='benchmark_set':
            redirect(URL('benchmark_set'))
    else:
        response.flash = T('Please, select an algorithm')

    return dict(algorithm_form=algorithm_form)

def set_algorithm_parameters():
    """
    Exposes form to set algorithm parameters
    """
    if not session.algorithm_id:
        redirect(URL('set_algorithm'))

    fields = []
    fields_name = []
    paramethers_id = []
    values=[]

    for algorithm_paramether in db(db.algorithm_parameters.algorithm==session.algorithm_id).select(orderby=db.algorithm_parameters.name):
        fields.append(Field(algorithm_paramether.name.replace(' ', '_')))
        fields_name.append(algorithm_paramether.name.replace(' ', '_'))
        paramethers_id.append(algorithm_paramether.id)

    algorithm_parameters_form = SQLFORM.factory(*fields)

    if algorithm_parameters_form.accepts(request, session):
        for num in range(len(paramethers_id)):
            values.append({'bench_id':session.benchmark_id, 'algorithm_parameters':paramethers_id[num], 'aparameters_value':request.vars[fields_name[num]]})

        db.bench_alg_parameters.bulk_insert(values)
        if request.args(0)=='benchmark_set':
            redirect(URL('benchmark_set'))
    else:
        response.flash = T('Please, select an algorithm')

    return dict(algorithm_parameters_form=algorithm_parameters_form)


def benchmark_set():
    """
    Exposes form to administrate a set of benchmark
    """
    algorithm=''
    algorithm_parameters=''
    request.args=['benchmark_set']

    if (session.mkt_param_id and session.opt_param_id):
        if not session.benchmark_id:
            session.benchmark_id=db.benchmark_set.insert(mkt_parameters=session.mkt_param_id, opt_parameters=session.opt_param_id)

    " Market Parameters "
    mkt_param=A(T('Market Parameters'),_href=URL('set_market_parameters',args=request.args))

    " Option Parameters "
    opt_param=A(T('Option Parameters'),_href=URL('set_option_parameters',args=request.args))

    if session.benchmark_id:
        """Decide algorithm"""
        algorithm=A(T('Algorithm'),_href=URL('set_algorithm',args=request.args))

        """ fill up algorithm parameters for this benchmark"""
        algorithm_parameters=A(T('Algorithm Parameters'),_href=URL('set_algorithm_parameters',args=request.args))

    return dict(mkt_param=mkt_param, opt_param=opt_param, algorithm=algorithm, algorithm_parameters=algorithm_parameters)

"""
Simulation forms
"""
def form_new_sim():
    form_new_job=SQLFORM.factory(db.scheduler_task)
    if form_new_job.accepts(request,session):
        db.scheduler_task.insert(**db.scheduler_task._filter_fields(form_new_job.vars))
    elif form_new_job.errors:
        response.flash = T('Please check for errors on form!')
    else:
        response.flash = T('Please fill the form')
    return dict(form_new_job=form_new_job)
