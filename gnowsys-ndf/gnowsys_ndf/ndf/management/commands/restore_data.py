from gnowsys_ndf.ndf.models  import *
import os
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from bson.json_util import dumps,loads,object_hook
import json
class Command(BaseCommand):
    help = "setup the initial database"
    def handle(self,*args,**options):
		file_names = ['GSystemType.json','factorydata','metatype.json','AttributeType.json','RelationType.json']
		for i in file_names:	
			PROJECT_ROOT = os.path.abspath(os.path.dirname(os.pardir))
			refcatpath = os.path.join(PROJECT_ROOT + '/GRef.cat./' + i)
			path_val = os.path.exists(refcatpath)
			if path_val:
				with open(refcatpath, 'r') as json_file:
					json_data = json_file.read()
				json_documents_list = json.loads(json_data)
				
			# Process data in proper format
			
			
			# process data based on the structure type			
			parsed_json_document = []
			for j,json_data in enumerate(json_documents_list):
				converted_data = node_collection.from_json(json.dumps(json_data))
				if i ==  'GSystemType.json':
					node = node_collection.collection.GSystemType()
				elif i == 'factorydata.json':
					if json_data['_type'] == 'Group':
						node = node_collection.collection.Group()
					else:					
						node = node_collection.collection.GSystem()
				elif i == 'metatype.json':
					node = node_collection.collection.MetaType()
				elif i == 'RelationType.json': 
					node = node_collection.collection.RelationType()
				elif i == 'AttributeType.json':
					node = node_collection.collection.AttributeType()
				if converted_data['name'] not in ['NUSSD Course','QuizItem']:
					for key, values in converted_data.items():
						if values and type(values) == list:
							oid_ObjectId_list = []
							oid_list_str = values.__str__()
							if '$oid' in oid_list_str:
								for oid_dict in values:
									oid_ObjectId = ObjectId(oid_dict['$oid'])
									oid_ObjectId_list.append(oid_ObjectId)

								node[key] = oid_ObjectId_list
							
						else:
							if key != "_type":
								node[key] = values
					node.save()
					
						












#temprorily blocked code
'''


    def handle(self, *args, **options):


        path  = os.path.abspath(os.path.dirname(os.pardir))
        path = os.path.join(path,'home/')
        print path
        file_path_exists =  os.path.exists(path)
        
        filenamelist = []
        for dir_, _, files in os.walk(path):
            for filename in files:
                filepath =  os.path.join(dir_, filename)
                filenamelist.append(filepath)
        for i in filenamelist:      
           data = get_json_file(i)
           final_data = check_data(data) 



def get_json_file(filepath):

    history_manager = HistoryManager()
    rcs = RCS()
    version_no = '1.13'
    path = '55b0da90f87f070bb518c33e.json'
    rcs.checkout((filepath,version_no))
    with open(path, 'r') as version_file:
            json_data = version_file.read()
    #print json_data
    json_dict = json.loads(json_data)
    json_data = json.dumps(json_dict)
    # Converts the json-formatted data into python-specific format
    doc_obj =  loads(json_data)
    doc_obj =  dumps(doc_obj)
    doc_obj = node_collection.from_json(doc_obj)
    print doc_obj
    rcs.checkin((filepath,version_no))
    #parse the data for perfect json node creation
    return doc_obj  
'''
    

def check_data(data):
    ''' method to check if all the system types relations and pre dependencies
        are present in the system before pushing them to the current system 
    '''
    temp_node = node_collection.collection.Group()
    temp_dict = {}
    ''' dictionary creation '''
    '''
    for key, values in data.items():
        temp_dict[key] = values

    temp_node.update(temp_dict)
    '''
    #temp_node.save()	
	
