from flask import Flask, jsonify 
from flask_restful import Resource, Api 
from Deposits import Deposits
from Statements import Statements
from flask_cors import CORS

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
		d = deposits.all_for(broker)
		return d.to_json(orient='records')


class Statements(Resource): 

	def get(self, broker : str): 
		s = statements.all_for(broker)
		return s.to_json(orient='records')


api.add_resource(Deposits, '/deposits/<string:broker>') 
api.add_resource(Statements, '/statements/<string:broker>') 
api.add_resource(Welcome, '/') 



if __name__ == '__main__': 

	app.run(debug = True) 
