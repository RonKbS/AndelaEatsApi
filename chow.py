#!/usr/bin/env python
'''
AndelaEats Chow CLI Tool
* Usage: python chow.py
*
* Command Line Arguments
* 	make:model name eg. python chow.py make:model user [--with_repo [_controller] ]
*	make:repo name eg. python chow.py make:repo user
*	make:blueprint name eg. python chow.py make:blueprint vendors [--url_prefix=vendors]
*	make:controller name eg. python chow.py make:controller user
'''

import sys, os

def create_model(name):
	name_clean = ''.join(list(map(lambda x: x.capitalize(), name.split('_'))))
	model_stub = '''from .base_model import BaseModel, db

class {model_name}(BaseModel):
	__tablename__ = '{table_name}'
	'''.format(model_name=name_clean, table_name=name)
	
	model_file_path = 'app/models/{}.py'.format(name)
	write_file(model_file_path, model_stub)
	return name_clean, model_file_path

def create_repo(name):
	pass

def create_blueprint(name, url_prefix=None):
	if url_prefix is None:
		url_prefix = ''
	
	blueprint_stub = '''from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request

url_prefix = '{{}}/{url_prefix}'.format(BaseBlueprint.base_url_prefix)
{name}_blueprint = Blueprint('{name}', __name__, url_prefix=url_prefix)
	'''.format(name=name, url_prefix=url_prefix)
	blueprint_file_path = 'app/blueprints/{}_blueprint.py'.format(name)
	write_file(blueprint_file_path, blueprint_stub)
	return name, blueprint_file_path

def create_controller(name):
	name_clean = ''.join(list(map(lambda x: x.capitalize(), name.split('_'))))
	controller_stub = '''from app.controllers.base_controller import BaseController

class {name}Controller(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
	'''.format(name=name_clean)
	
	controller_file_path = 'app/controllers/{}_controller.py'.format(name)
	write_file(controller_file_path, controller_stub)
	return name_clean, controller_file_path

def write_file(file_path, file_content):
	with open(file_path, 'w', encoding='utf-8') as file_handle:
		file_handle.write(file_content)

if __name__ == '__main__':
	
	args = sys.argv
	command = args[1]
	
	if command == 'make:model' or command == 'make:models':
		name = args[2]
		extras = args[3].split('--with_')[1].split('_')
		m = create_model(name)
		print('Model: {} Location: {}'.format(m[0], m[1]))
		
		if 'controller' in extras:
			c = create_controller(name=name)
			print('Controller: {}Controller Location: {}'.format(c[0], c[1]))
			
		if 'repo' in extras:
			pass
		
	
	if command == 'make:repo' or command == 'make:repos':
		name = args[2]
		pass
	
	
	if command == 'make:blueprint' or command == 'make:blueprints':
		name = args[2]
		url_prefix = None
		
		if len(args) > 3:
			url_prefix = args[3].split('--url_prefix=')[1]
			
		b = create_blueprint(name, url_prefix)
		print('Blueprint: {} Location: {}'.format(b[0], b[1]))
	
	
	if command == 'make:controller' or command == 'make:controllers':
		name = args[2]
		c = create_controller(name=name)
		print('Controller: {}Controller Location: {}'.format(c[0], c[1]))
	