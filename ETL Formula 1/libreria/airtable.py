import requests
import pandas as pd
import numpy as np

# OOP approach to Airtable functionality - import class
class AirtableConnector:
    def __init__(self, TOKEN: str, BASE_ID: str):
        self.airtable_base_url = "https://api.airtable.com/v0"
        self.TOKEN = TOKEN
        self.BASE_ID = BASE_ID
        self.headers = {
            "Authorization" : f"Bearer {self.TOKEN}",
            "Content-Type"  : "application/json"
        }


    def setup(self, 
                df: pd.DataFrame,
                table_name: str,
                columns: list[str], 
                dtypes: list[str], 
                options: list[str]):
        
        response_table = self.create_table(table_name, columns, dtypes, options)

        TABLE_ID = response_table.json().get('id')

        if not TABLE_ID:
            print(response_table.json())

        df = df.replace(np.nan, None) 

        responses_uploads = self.load_from_df(df, TABLE_ID) # could use table_name

        print("All uploads successful:")
        print(all([response.status_code == 200 for response in responses_uploads]))  
        
        return response_table, responses_uploads


    def _generate_schema(self, columns: list[str], dtypes: list[str], options: list[str]):
        if len(columns) != len(dtypes):
            raise ValueError('Los argumentos "columns" y "dtypes" necesitan ser del mismo tamaño')

        fields = zip(columns, dtypes, options)
        schema = [{ 
                    "name": column,
                    "type": dtype,
                    "options": option,
                } if option 

                else {
                    "name": column,
                    "type": dtype
                }
                for column, dtype, option in fields 
            ]
        
        return schema


    def create_text_table(self, table_name: str, columns: list[str], description="") -> requests.Response:
        # URL
        endpoint = f"{self.airtable_base_url}/meta/bases/{self.BASE_ID}/tables"
        
        dtypes = ['singleLineText']*len(columns)
        options = [{}]*len(columns)

        schema = self._generate_schema(columns, dtypes, options)
        print(schema)

        # Put schema, description and table name into data
        data = {
            "description": description,
            "fields": schema,
            "name": table_name,
        }
        response = requests.post(url = endpoint, json = data, headers = self.headers)
        
        error = response.json().get('error')
        if error:
            print("-"*25)
            print("data")
            print(data)
            print("-"*25)
            print("ERROR")
            print(error)
            raise ValueError(f'{error["type"]}: {error["message"]}')

        return response
    

    def create_table(self, table_name: str, columns: list[str], dtypes: list[str], options: list[str], description="") -> requests.Response:
        # URL
        endpoint = f"{self.airtable_base_url}/meta/bases/{self.BASE_ID}/tables"
        
        schema = self._generate_schema(columns, dtypes, options)
        print(schema)
        # Put schema, description and table name into data
        data = {
            "description": description,
            "fields": schema,
            "name": table_name,
        }
        response = requests.post(url = endpoint, json = data, headers = self.headers)
        
        error = response.json().get('error')
        if error:
            print("-"*25)
            print("data")
            print(data)
            print("-"*25)
            print("ERROR")
            print(error)
            raise ValueError(f'{error["type"]}: {error["message"]}')

        return response
    

    def load_from_df(self, df: pd.DataFrame, TABLE_ID: str):
        # URL
        endpoint = f"{self.airtable_base_url}/{self.BASE_ID}/{TABLE_ID}"
        
        # Store response objects
        responses = []

        # Add 10 rows at a time
        for i in range(0, df.shape[0], 10):

            try:
                records = [{"fields" : df.iloc[i+j, :].to_dict()} for j in range(10)]
            except IndexError:
                records = [{"fields" : df.iloc[i+j, :].to_dict()} for j in range(df.shape[0]%10)]
            finally:
                datos_subir = {"records" : records,
                            "typecast" : True}
                print("-"*25)
                print("DATOS")
                print(datos_subir)
            response = requests.post(url = endpoint, json = datos_subir, headers = self.headers)

            responses.append(response)

            print(f"response: {response.status_code}")

            print(f"endpoint: {response.url}")

            print("-"*120)

            print(response.json())

            print("-"*120)

        return responses
    

    def _get_table(self, TABLE_ID: str):

        responses = []

        params = {"offset" : None}

        # URL
        endpoint = f"{self.airtable_base_url}/{self.BASE_ID}/{TABLE_ID}"

        while params.get("offset") != None or not responses:
            
            response = requests.get(url = endpoint, headers = self.headers, params = params)
            
            print(response.url)
            
            print(f"response: {response.status_code}")
            
            params["offset"] = response.json().get("offset")
            
            responses.append(response)
            
        return responses


    def to_df(self, TABLE_ID: str):
        responses = self._get_table(TABLE_ID)
        airtable_df = pd.DataFrame()
        for response in responses:
            records = response.json().get('records')
            data = [record.get('fields') for record in records]
            df = pd.DataFrame(data)
            airtable_df = pd.concat([airtable_df, df])
        return airtable_df


# Functional approach - helper functions can also be imported - less functionality
def format_airtable_schema(names, dtypes):

    if len(names) != len(dtypes):
        raise ValueError('Los dos argumentos necesitan ser del mismo tamaño')

    fields = zip(names, dtypes)
    schema = [{"name": name,
               "type": dtype}
               for name, dtype in fields
               ]

    return schema


def airtable_create(TOKEN, BASE_ID, table_name, schema, description):
    # URL
    airtable_base_url = "https://api.airtable.com/v0"
    endpoint = f"{airtable_base_url}/meta/bases/{BASE_ID}/tables"

    # Headers
    headers = {"Authorization" : f"Bearer {TOKEN}",
            "Content-Type"  : "application/json"}
    
    # Put schema, description and table name into data
    data = {
        "description": description,
        "fields": schema,
        "name": table_name,
    }

    response = requests.post(url = endpoint, json = data, headers = headers)

    return response
    

def airtable_load(df, TOKEN, BASE_ID, TABLE_ID):
    # URL
    airtable_base_url = "https://api.airtable.com/v0"
    endpoint = f"{airtable_base_url}/{BASE_ID}/{TABLE_ID}"
    
    # Headers
    headers = {"Authorization" : f"Bearer {TOKEN}",
            "Content-Type"  : "application/json"}
    
    # Store response objects
    responses = []

    # Add 10 rows at a time
    for i in range(0, df.shape[0], 10):

        try:
            records = [{"fields" : df.iloc[i+j, :].to_dict()} for j in range(10)]
        except IndexError:
            records = [{"fields" : df.iloc[i+j, :].to_dict()} for j in range(df.shape[0]%10)]
        finally:
            datos_subir = {"records" : records,
                        "typecast" : True}
            
        response = requests.post(url = endpoint, json = datos_subir, headers = headers)

        print(f"response: {response.status_code}")

        print(f"endpoint: {response.url}")

        print("-"*120)

        print(response.json())

        print("-"*120)

        responses.append(response)

    return responses