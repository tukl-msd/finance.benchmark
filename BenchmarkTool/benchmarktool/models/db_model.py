# coding: utf8
import json
import requests
import time

from gluon.scheduler import Scheduler
#Use migrate = True when you want to create all the tables
#scheduler = Scheduler(db)
scheduler = Scheduler(db, migrate=False)

# table definition
db.define_table('algorithm_parameters',
                Field('start_level','integer'),
                Field('multilevel_constant','integer'),
                Field('number_of_paths_on_first_level','integer'),
                Field('epsilon','double'),
                Field('price_precision','double'),
                Field('reference_price','double'))

db.define_table('barrier',
                Field('name','string'),
                format='%(name)s')

db.define_table('market_parameters',
                 Field('correlation', 'double'),
                 Field('long_run_variance', 'double'),
                 Field('speed_of_revertion', 'double'),
                 Field('volatility_of_volatility', 'double'),
                 Field('spot_price', 'double'),
                 Field('spot_volatility', 'double'),
                 Field('riskless_interest_rate', 'double'))

db.define_table('option_price',
                 Field('name', 'string'),
                 format='%(name)s')

db.define_table('numeric_results',
                 Field('energy', 'double'),
                 Field('runtime_value', 'double'),
                 Field('price', 'double'),
                 Field('precision_value', 'double'))

db.define_table('option_parameters',
                 Field('option_type', db.option_price, widget=SQLFORM.widgets.options.widget),
                 Field('strike_price', 'double'),
                 Field('time_to_maturity', 'double'),
                 Field('lbarrier_type', db.barrier, widget=SQLFORM.widgets.options.widget),
                 Field('lbarrier_value', 'double'),
                 Field('ubarrier_type', db.barrier, widget=SQLFORM.widgets.options.widget),
                 Field('ubarrier_value', 'double'))

db.define_table('job',
                 Field('username', db.auth_user),
                 Field('market_parameters', db.market_parameters),
                 Field('option_parameters', db.option_parameters))

db.define_table('benchmark_set',
                Field('name','string',length=255,unique=True),
                Field('description','text'),
                Field('mkt_parameters',db.market_parameters),
                Field('opt_parameters',db.option_parameters),
                format='%(name)s')

db.define_table('simulation',
                Field('compute_server', db.scheduler_worker),
                Field('alg_parameters',db.algorithm_parameters),
                Field('job_id',db.job),
                Field('result_id',db.numeric_results))

# Field requirements definition
db.algorithm_parameters.start_level.requires = IS_EXPR('int(value)>0')
db.algorithm_parameters.multilevel_constant.requires = IS_EXPR('int(value)>0')
db.algorithm_parameters.number_of_paths_on_first_level.requires = IS_EXPR('int(value)>0')
db.algorithm_parameters.epsilon.requires = IS_EXPR('float(value)>0')
db.algorithm_parameters.price_precision.requires = IS_EXPR('float(value)>0')
db.algorithm_parameters.reference_price.requires = IS_EXPR('float(value)>0')

db.barrier.name.requires = IS_NOT_EMPTY()

db.market_parameters.correlation.requires = [IS_NOT_EMPTY(),IS_FLOAT_IN_RANGE(-1,1)]
db.market_parameters.long_run_variance.requires = [IS_NOT_EMPTY(),IS_FLOAT_IN_RANGE(-1,1)]
db.market_parameters.speed_of_revertion.requires = [IS_NOT_EMPTY(),IS_EXPR('float(value)>0')]
db.market_parameters.volatility_of_volatility.requires = [IS_NOT_EMPTY(),IS_EXPR('float(value)>0')]
db.market_parameters.spot_price.requires = [IS_NOT_EMPTY(),IS_EXPR('float(value)>0')]
db.market_parameters.spot_volatility.requires = [IS_NOT_EMPTY(),IS_EXPR('float(value)>0')]
db.market_parameters.riskless_interest_rate.requires = [IS_NOT_EMPTY(),IS_EXPR('float(value)>0')]

db.option_price.name.requires = [IS_NOT_IN_DB(db, db.option_price.name),IS_NOT_EMPTY()]

db.option_parameters.option_type.requires = [IS_IN_DB(db, db.option_price.id, '%(name)s'),IS_NOT_EMPTY()]
db.option_parameters.strike_price.requires = IS_NOT_EMPTY()
db.option_parameters.time_to_maturity.requires = IS_NOT_EMPTY()
db.option_parameters.lbarrier_type.requires = [IS_EMPTY_OR(IS_IN_DB(db, db.barrier.id, '%(name)s'))]
db.option_parameters.ubarrier_type.requires = [IS_EMPTY_OR(IS_IN_DB(db, db.barrier.id, '%(name)s'))]


db.job.username.requires = [IS_IN_DB(db, db.auth_user.id, '%(name)s'),IS_NOT_EMPTY()]
db.job.market_parameters.requires = [IS_IN_DB(db, db.market_parameters.id),IS_NOT_EMPTY()]
db.job.option_parameters.requires = [IS_IN_DB(db, db.option_parameters.id),IS_NOT_EMPTY()]

db.benchmark_set.mkt_parameters.requires = [IS_IN_DB(db, db.market_parameters.id),IS_NOT_EMPTY()]
db.benchmark_set.opt_parameters.requires = [IS_IN_DB(db, db.option_parameters.id),IS_NOT_EMPTY()]

db.simulation.result_id.requires = [IS_IN_DB(db, db.numeric_results.id),IS_NOT_EMPTY()]
db.simulation.alg_parameters.requires = [IS_IN_DB(db,db.algorithm_parameters.id),IS_NOT_EMPTY()]

#scheduler tasks
def new_sim(mkt_param, opt_param, alg_param, sim_id):
    import subprocess
    
    cmnd = "python3 "+BENCHMARK_SCRIPT+" -a \""+str(alg_param)+"\" -m \""+str(mkt_param)+"\" -o \""+str(opt_param)+"\""
    try:
        output = subprocess.check_output(cmnd,shell=True)
    except subprocess.CalledProcessError as e:
        r = e
    else:
        results=output[1:-2].split(',')

        energy = float(results[0])
        runtime_value = float(results[1])
        price = float(results[2])
        precision_value = float(results[3])

        " Insert result into database"
        payload = {'energy': energy , 'runtime_value': runtime_value ,'price': price ,'precision_value': precision_value}
        try:
            r = json.loads(requests.post(HOST_URL+APPLICATION+"default/api/numeric_results.json", data=payload).text)
        except ValueError, e:
            r = e
        else:
            db.commit()
    return (r)

def send_simulation_id(task,sim_id):
    num_result_id = None
    " Pooling loop "
    while 1:
        task_status = scheduler.task_status(task, output=True)
        if task_status.result:
            num_result_id = task_status.result
            break
        time.sleep(60)

    " Link result with the corresponding simulation "
    payload = {'result_id': num_result_id}
    
    try:
        update_sim = json.loads(requests.put(HOST_URL+APPLICATION+"default/api/simulation/"+str(sim_id)+".json", data=payload).text)
    except ValueError, e:
        pass
    else:
        db.commit()
    return (sim_id)

def send_mail(task_set,job_id):
    num_tasks = len(task_set)
	
    while num_tasks != 0:
        for task in task_set:
            task_status = scheduler.task_status(task, output=True)
            if task_status.result:
                num_tasks=num_tasks-1
        time.sleep(60)

    " Send mail to user "
    search_str = HOST_URL+'benchmarktool/default/api/job/'+str(job_id)+'/username.json'
    try:
        user_id = json.loads(requests.get(search_str).text);
    except ValueError, e:
        pass
    else:    
        user_id = user_id['content'][0]['username']
    
        search_str = HOST_URL+'benchmarktool/default/api/user/'+str(user_id)+'/email.json'
        try:
            email = json.loads(requests.get(search_str).text);
        except ValueError, e:
            pass
        else:
            email = email['content'][0]['email']
            send_mail_result=mail.send(email,'[BenchmarkTool] Your simulation is ready','You can check the results of your simulation on \"http://gwt.eit.uni-kl.de:8000/benchmarktool/default/results\" and search for Job ID number:'+str(job_id)+'.')
    return(send_mail_result)
