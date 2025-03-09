from flask import Flask, jsonify 
from flask_restful import Resource, Api 
from Deposits import Deposits
from Statements import Statements
from flask_cors import CORS

import json
import logging
import os

logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s' 
)

logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

log = logging.getLogger()

dir = os.getcwd()

deposit_dir = os.path.join(dir, 'data', 'deposit','real')
statement_dir = os.path.join(dir, 'data', 'statement','real')

deposits = Deposits(deposit_dir=deposit_dir)
statements = Statements(statement_dir=statement_dir)

app = Flask(__name__) 
api = Api(app) 

CORS(app, resources={r'/*': {'origins': '*'}})

class Welcome(Resource): 
  
    def get(self): 
  
        return jsonify({'message': 'backend online'})
	
class Deposits(Resource): 

	def get(self, broker : str): 
		log.info(f"Deposits for {broker}")
		d = deposits.all_for(broker)
		result = d.to_json(orient='records')
		log.info(f'Found {len(d)} deposits for broker {broker}')
		return result

class Statements(Resource): 

	def get(self, broker : str): 
		log.info(f"Statements for {broker}")
		s = statements.all_for(broker)
		result = s.to_json(orient='records')
		log.info(f'Found {len(s)} statements for broker {broker}')
		return result

class Overview(Resource): 

	def get(self, broker : str): 
		log.info(f"Overview for {broker}")

		(depos_src_value, depos_src_currency, sum_deposits, currency_deposits) = deposits.sum_for(broker)
		latest_statement = statements.latest_for(broker)
		latest_value = latest_statement["value"]
		profit = (latest_value - sum_deposits)/sum_deposits

		result = []
		
		result.append({"currency": currency_deposits, "value_deposits": sum_deposits, "value_latest": latest_value, "profit": profit})

		return json.dumps(result)


class Broker(Resource): 

	def get(self, broker : str): 
		log.info(f"Data for {broker}")
		s = statements.all_for(broker)
		d = deposits.all_for(broker)


		s = s.to_dict(orient='records')
		d = d.to_dict(orient='records')

		log.info(f'Found {len(s)} statements for broker {broker}')
		log.info(f'Found {len(d)} deposits for broker {broker}')

		data = {"statements": s, "deposits": d}

		return json.dumps(data)
	

api.add_resource(Deposits, '/<string:broker>/deposits') 
api.add_resource(Statements, '/<string:broker>/statements') 
api.add_resource(Overview, '/<string:broker>/overview') 
api.add_resource(Broker, '/<string:broker>') 


api.add_resource(Welcome, '/') 



if __name__ == '__main__': 

	app.run(debug = True) 
