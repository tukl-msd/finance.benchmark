# coding: utf8
from gluon.scheduler import Scheduler
scheduler = Scheduler(db)

# table definition
db.define_table('algorithm_parameters',
                Field('start_level','integer'),
                Field('final_level','integer'),
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
db.algorithm_parameters.final_level.requires = IS_EXPR('int(value)>0')
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

db.simulation.compute_server.requires = [IS_IN_DB(db, db.scheduler_worker.id, '%(name)s'),IS_NOT_EMPTY()]
db.simulation.result_id.requires = [IS_IN_DB(db, db.numeric_results.id),IS_NOT_EMPTY()]
db.simulation.alg_parameters.requires = [IS_IN_DB(db,db.algorithm_parameters.id),IS_NOT_EMPTY()]

#scheduler tasks
def new_sim():
    import subprocess
    output = subprocess.check_output(['python3','/home/cpnogueira/Downloads/pyheston/heston_web2py.py'])
    results=output[1:-2].split(',')

    payload = {'energy':results[0],'runtime_value':results[1],'price':results[2],'precision_value':results[3]}
    r = json.loads(requests.post("http://localhost:8000/benchmarktool/default/api/numeric_results.json", data=payload).text)

    return results
