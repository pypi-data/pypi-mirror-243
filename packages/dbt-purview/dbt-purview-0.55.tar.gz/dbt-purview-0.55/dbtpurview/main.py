import click
import json
import requests
from airflow.hooks.base import BaseHook

@click.command()
@click.option('--env', default='databricks')
@click.option('--dwhcid', default='jaffle_shop_databricks_connection')
@click.option('--azpurview', default='azure_purview')
@click.option('--path', default='/tmp')
def dbtpurview(env,dwhcid,azpurview,path):

   azpurview_conn =  BaseHook.get_connection(str(azpurview))
   extras_dict_purview = json.loads(azpurview_conn.get_extra())
   tenantId = str(extras_dict_purview['azure__tenantId'])
   resource = str(extras_dict_purview['resource'])
   clientId = str(azpurview_conn.login)
   secret = str(azpurview_conn.password)

   if(env == "databricks"):
        conn = BaseHook.get_connection(str(dwhcid))
        host = str(conn.host)
        schema = str(conn.schema)
        database = str(conn.schema)
        type_name = "hive"

   if(env == "snowflake"):
         snowflake_conn = BaseHook.get_connection(str(dwhcid))
         e1xtras_dict = json.loads(snowflake_conn.get_extra())
         host = str(e1xtras_dict['account'])
         host = host + ".snowflakecomputing.com"
         database = str(e1xtras_dict['database'])
         schema = str(snowflake_conn.schema)
         type_name = "snowflake"

   file = open(path + "/manifest.json")
   data = json.load(file)
   child_map = data.get("parent_map", {})

   filtered_model_list = []
   for i in child_map:
        if(i.split(".")[0] != "test"):
               filtered_model_list.append(i)
   
   model_list = {}
   for i in filtered_model_list:
      if(i.split(".")[::-1][0] not in ['v1','v2','v3','v4','v5']):
         model_list[i] = i.split(".")[::-1][0]
      else:
         model_list[i] = i.split(".")[::-1][1]
   
   
   nodes = data.get("nodes", {})
   sources = data.get("sources", {})
   model_meterialized = {}
   for i in filtered_model_list:
      if(nodes.get(i) != None):
         if(nodes.get(i).get("config").get("materialized") != 'view'):
            model_meterialized[i] = 'table'
         else:
            model_meterialized[i] = nodes.get(i).get("config").get("materialized")

   qualified_model_name = {}
   for i in filtered_model_list:
      if(model_meterialized.get(i) != None):
         qualified_model_name[i] = prepare_qualified_name(env, database, schema, host, model_list.get(i),model_meterialized.get(i))
      else:
         qualified_model_name[i] = prepare_qualified_name(env, database, schema, host, model_list.get(i),"table")

   url = f"https://login.microsoftonline.com/{tenantId}/oauth2/token"
   reqeust = {
       "grant_type":"client_credentials",
       "client_id":clientId,
       "client_secret":secret,
       "resource":"https://purview.azure.net",
       "scope":f"{clientId}/.default"
   }
   response = post(url,reqeust)
   access_token = response.get("access_token")
   create_custom_assest_type(access_token,resource)
   model_guid = {}
   for i in filtered_model_list:
      if(model_meterialized.get(i) == "view"):
         url = f"https://{resource}/datamap/api/atlas/v2/entity/uniqueAttribute/type/{type_name}_view?attr:qualifiedName={qualified_model_name.get(i)}"
      else:
         url = f"https://{resource}/datamap/api/atlas/v2/entity/uniqueAttribute/type/{type_name}_table?attr:qualifiedName={qualified_model_name.get(i)}"
      header = {
          "Authorization": "Bearer "+access_token
      } 
      response = get(url,header)
      model_guid[i] = response.get("entity").get("guid")

   dbt_models = list_assets_as_dbt_models(access_token,resource)
   
   list_dbt_models  = []
   for model_name in filtered_model_list:
      if(model_name.split(".")[0] != "source"):
            list_dbt_models.append("dbt_"+model_name)

   for i in dbt_models.get("value"):
      model_name = i.get("displayText")
      print(model_name)
      if(model_name not in list_dbt_models):
         header = {
            "Authorization": "Bearer "+access_token,
            "Content-Type": "application/json"
         }
         print(list_dbt_models)
         print(i)
         requests.delete(f"https://{resource}/catalog/api/atlas/v2/entity/guid/${i.get('id')}",headers=header)

   for child in filtered_model_list:
      if(child.split(".")[0] != "source"):
         child_id = model_guid.get(child)
         parent_ids = []
         for parent in child_map.get(child):
            if(parent.split(".")[0] != "test"):
               parent_ids.append(model_guid.get(parent))
         
         input_string = []
         for i in parent_ids:
            input_string.append({
                              "guid": i
                           })
         data = {
                  "entity": {
                     "typeName":"dbt_models",
                     "attributes":{
                           "qualifiedName" : "dbt_"+child,
                           "name" : "dbt_"+child,
                           "inputs" : input_string,
                           "outputs" : [{
                              "guid":child_id
                           }],
                           "raw_query" : nodes.get(child).get("raw_code"),
                           "compile_query" : nodes.get(child).get("compiled_code"),
                           "tag" : nodes.get(child).get("tags"),
                           "description" : nodes.get(child).get("description"),
                           "meta" : nodes.get(child).get("config").get("meta") ,
                           "materialized" : nodes.get(child).get("config").get("materialized"),
                           "incremental_strategy": nodes.get(child).get("config").get("incremental_strategy"),
                           "full_refresh": nodes.get(child).get("config").get("full_refresh"),
                           "unique_key": nodes.get(child).get("config").get("unique_key"),
                           "on_schema_change": nodes.get(child).get("config").get("on_schema_change"),
                           "post-hook": nodes.get(child).get("config").get("post-hook"),
                           "pre-hook": nodes.get(child).get("config").get("pre-hook"),
                           "columns": json.dumps(nodes.get(child).get("columns")),
                           "version": nodes.get(child).get("latest_version"),
                           "contract": nodes.get(child).get("contract")
                     }, 
                     "status": "ACTIVE"
                  },
                  "referredEntities":{}
               }
         data_json = json.dumps(data)
         header = {
            "Authorization": "Bearer "+access_token,
            "Content-Type": "application/json"
         }
         response = post_with_header(f"https://{resource}/datamap/api/atlas/v2/entity",header,data_json)

   update_column_description(nodes,sources,filtered_model_list,model_meterialized,env,database,schema,host,type_name,resource,access_token)

   file.close()

def list_assets_as_dbt_models(access_token, resource):
   url = f"https://{resource}/catalog/api/search/query?api-version=2021-05-01-preview"
   data = {
            "offset": 0,
            "orderby": [
               "name"
            ],
            "taxonomySetting": {
               "assetTypes": [
                     "dbt_models"
               ],
               "facet": {
                     "count": 10,
                     "sort": {
                        "count": "desc"
                     }
               }
            }
         }
   data_json = json.dumps(data)
   header = {
      "Authorization": "Bearer "+access_token,
      "Content-Type": "application/json"
   }
   result = post_with_header(url, header, data_json)
   return result

def post(url,data):   
   response = requests.post(url, data=data)
   if response.status_code == 200:
      result = response.json() 
   else:
      raise Exception(f"API request failed with status code: {response.status_code}")
   
   return result

def post_with_header(url,headers,data):   
   response = requests.post(url, headers=headers, data=data)
   if response.status_code == 200:
      result = response.json()
   else:
      print(response.json())
      raise Exception(f"API request failed with status code: {response.status_code}")
   
   return result

def get(url,header):   
   response = requests.get(url,headers=header)
   if response.status_code == 200:
      result = response.json() 
   else:
      raise Exception(f"API request failed with status code: {response.status_code}")
   
   return result

def prepare_qualified_name(env, database, schema, host, model_name,type):
   if(env == "databricks"):
       qualified_name = schema+"."+model_name+"@"+host
       return qualified_name
   if(env == "snowflake"):
       qualified_name = "snowflake://"+host+"/databases/"+str.upper(database)+"/schemas/"+str.upper(schema)+"/"+type+"s/"+str.upper(model_name)
       return qualified_name
   
def prepare_column_qualified_name(column_name, env, database, schema, host, model_name,type):
   if(env == "databricks"):
       qualified_name = schema+"."+model_name+"."+column_name+"@"+host
       return qualified_name
   if(env == "snowflake"):
       qualified_name = "snowflake://"+host+"/databases/"+str.upper(database)+"/schemas/"+str.upper(schema)+"/"+type+"s/"+str.upper(model_name)+"/columns/"+str.upper(column_name)
       return qualified_name   
   
def create_custom_assest_type(access_token,resource):
   header = {
         "Authorization": "Bearer "+access_token
         }
   response = requests.get(f"https://{resource}/datamap/api/atlas/v2/types/entitydef/name/dbt_models",headers=header)
   if response.status_code == 404:
      url = f"https://{resource}/datamap/api/atlas/v2/types/typedefs"
      data = {
            "entityDefs": [
               {
                     "superTypes": [
                        "Process"
                     ],
                     "name": "dbt_models",
                     "attributeDefs": [
                        {
                           "name": "raw_query",
                           "typeName": "string",
                           "isOptional": "false",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "compile_query",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "description",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "tag",
                           "typeName": "string",
                           "isOptional": "false",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "meta",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "materialized",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "incremental_strategy",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "full_refresh",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "unique_key",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "on_schema_change",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "post-hook",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "pre-hook",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "contract",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "latest_version",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "columns",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "constraints",
                           "typeName": "string",
                           "isOptional": "true",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        }
                     ]
               }
            ]
         }
      data_json = json.dumps(data)
      header = {
            "Authorization": "Bearer "+access_token,
            "Content-Type": "application/json"
         }
      response = post_with_header(url,header,data_json)
   else:
      print(response.json())  

def update_column_description(nodes,sources,filtered_model_list,model_meterialized,env,database,schema,host,type_name,resource,access_token):
      model_column_mapping = {}
      for i in filtered_model_list:
         if(nodes.get(i) != None and len(nodes.get(i).get("columns")) != 0): 
            model_column_mapping[i] = nodes.get(i).get("columns")
         if(sources.get(i) != None and len(sources.get(i).get("columns")) != 0):
            model_column_mapping[i] = sources.get(i).get("columns")


      for outer_key, inner_dict in model_column_mapping.items():
         for inner_key, column_data in inner_dict.items():
            if(outer_key.split(".")[::-1][0] not in ['v1','v2','v3','v4','v5']):
               model_name = outer_key.split(".")[::-1][0]
            else:
               model_name = outer_key.split(".")[::-1][1]

            if(model_meterialized.get(outer_key) != None):
               column_qaulified_name = prepare_column_qualified_name(inner_key, env, database, schema, host, model_name,model_meterialized.get(outer_key))
            else:
               column_qaulified_name = prepare_column_qualified_name(inner_key, env, database, schema, host, model_name,"table")

            if(model_meterialized.get(outer_key) == "view"):
               url = f"https://{resource}/datamap/api/atlas/v2/entity/uniqueAttribute/type/{type_name}_view_column?attr:qualifiedName={column_qaulified_name}"
            else:
               url = f"https://{resource}/datamap/api/atlas/v2/entity/uniqueAttribute/type/{type_name}_column?attr:qualifiedName={column_qaulified_name}"
            header = {
               "Authorization": "Bearer "+access_token
            }  
            response = get(url,header)
            column_guid = response.get("entity").get("guid")
            header = {
               "Authorization": "Bearer "+access_token,
               "Content-Type": "application/json"
            }  
            requests.put(f"https://{resource}/datamap/api/atlas/v2/entity/guid/{column_guid}?name=description",headers=header,data=json.dumps(column_data.get("description")))

if __name__ == '__main__':
   dbtpurview()   
   
   

