import requests
import os
from urllib.parse import unquote
from typing import List, Optional, Any
import mimetypes
from typing import Optional, Dict

class Client:

    def __init__(self, api_key: str, base_url='https://api.vectify.ai'):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {'api_key': self.api_key}
        if self.heartbeat() == False:
            print("* Please note some services are unavailable at the moment.")
        print('here')


    def _request(self, method: str, endpoint: str, data: Optional[dict] = None):
        url = f"{self.base_url}{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers)
            elif method == "POST":
                response = requests.post(url, json=data, headers=self.headers)
            
            response.raise_for_status()  # This will raise an exception for HTTP error codes.
            return response.json()

        except requests.exceptions.HTTPError as e:
            # Log or print the HTTP error
            print(f"HTTP error occurred: {e}")

            # Try to extract and print the error details from the response
            try:
                error_details = response.json()
                print("Error details:", error_details)
            except ValueError:
                # If response is not in JSON format, print the raw response text
                print("Error response:", response.text)

            return {"error": "An error occurred during the request."}


    def heartbeat(self):
        return self._request("GET", "/heartbeat")

    def usage(self):
        return self._request("GET", "/usage")
    
    def list_models(self) -> List[str]:
        return self._request("GET", "/models")

    def list_retrieval_agents(self) -> List[str]:
        return self._request("GET", "/retrieve/agents")
    
    def list_chat_agents(self) -> List[str]:
        return self._request("GET", "/chat/agents")

    def list_sources(self) -> List[str]:
        return self._request("GET", "/sources")
    
    def list_embedding_models(self) -> List[str]:
        return self._request("GET", "/embedding_models")
    
    def list_files(self, source_name: str = 'default') -> List[str]:
        data = {
            'source_name': source_name
        }
        return self._request("POST", "/files", data)
    
        
    def get_source_info(self, source_name: str = 'default') -> Dict:
        data = {
            'source_name': source_name
        }
        return self._request("POST", "/sources/info", data)


    def add_source(self, source_name: str, embedding_model: Optional[str] = None, metadata_fields: Optional[Dict[str, str]] = None):
        data = {
            'source_name': source_name
        }
        optionals = {
            'embedding_model': embedding_model,
            'metadata_fields': metadata_fields
        }
        data.update({k: v for k, v in optionals.items() if v is not None})

        return self._request("POST", "/sources/add", data)

    
    def delete_source(self, source_name: str):
        data = {
            'source_name': source_name
        }
        response = self._request("POST", "/sources/delete", data)
        if (response == False):
            print(f"Failed to delete source '{source_name}'.")
            return False
        print(f"Source '{source_name}' was deleted.")
        return True


    def get_source_usage(self, source_name: str):
        data = {
            'source_name': source_name
        }
        return self._request("POST", "/sources/usage", data)


    def add_text(self, source_name: str, text: str, metadata: Optional[dict] = None):
        data = {
            'source_name': source_name,
            'text': text
        }
        if metadata is not None:
            data['metadata'] = metadata

        try:
            self._request("POST", "/text/add", data)
            print(f"Text provdied was uploaded to source '{source_name}'.")
            return True
        except Exception as e:
            print(f"Failed to upload text: {e}")
            return False


    def add_file(self, source_name: str, local_path: str, metadata: dict = None):
        file_name = os.path.basename(local_path)

        mime_type, encoding = mimetypes.guess_type(local_path)
        if mime_type is None:
            print (f"Possibly unknown file type: '{file_name}'.")
            # return False
        elif not ('text' in mime_type or 'pdf' in mime_type or 'word' in mime_type):
             print(f"Unsupported file type: '{file_name}'. Only text, PDF and Word files are supported.")
             return False
                
        data = {
            'source_name': source_name,
            'file_name': file_name
        }
        if metadata is not None:
            data['metadata'] = metadata

        presigned_url = self._request("POST", "/files/upload-url", data)

        path_splits = presigned_url.split('/')
        last_part = path_splits[-1].split('?')[0]
        file_name = unquote(last_part)
        data['file_name'] = file_name
        
        try:
            with open(local_path, 'rb') as file:
                files = {'file': file}
                response = requests.put(presigned_url, data=file)

            if response.status_code != 200:
                print(f"Failed to upload file. HTTP Status code: {response.status_code}")
                return False

            self._request("POST", "/files/upload-sync", data)
            print(f"File '{file_name}' was uploaded to source '{source_name}'.")
            return True
        except FileNotFoundError:
            print(f"The file {local_path} does not exist.")
            return False
        except IOError as e:
            print(f"An error occurred while reading the file: {e}")
            return False


    def delete_file(self, source_name: str, file_name: str):
        data = {
            'source_name': source_name,
            'file_name': file_name
        }

        response = self._request("POST", "/files/delete", data)
        if response == None:
            print(f"Failed to delete file: {response}")
            return False
        return response


    def download_file(self, source_name: str, file_name: str, local_path: str):

        data = {
            'source_name': source_name,
            'file_name': file_name
        }

        presigned_url = self._request("POST", "/files/download-url", data)
        if presigned_url == None:
            print(f"File '{file_name}' does not exist in source '{source_name}'.")
            return False
        
        response = requests.get(presigned_url)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f"File '{file_name}' from source '{source_name}' was downloaded to '{local_path}'.")
            return True
        else:
            print(f"Failed to download file. HTTP Status Code: {response.status_code}. Reason: {response.text}")
            return False
        

    def get_file_retrieval_status(self, source_name: str, file_name: str):
        data = {
            'source_name': source_name,
            'file_name': file_name
        }

        response = self._request("POST", "/files/retrieval-status", data)
        if response == None:
            print(f"File '{file_name}' does not exist in source '{source_name}'.")
            return False
        return response
    

    def get_file_chunks(self, source_name: str, file_name: str):
        data = {
            'source_name': source_name,
            'file_name': file_name
        }

        response = self._request("POST", "/files/chunks", data)
        if response == None:
            print(f"File '{file_name}' does not exist in source '{source_name}'.")
            return False
        return response


    def add_openai_key(self, key: str):
        data = {
            'key': key
        }
        return self._request("POST", "/openai-key", data)
    
    def remove_openai_key(self):
        data = {
            'key': None
        }
        return self._request("POST", "/openai-key", data) 


    def retrieve(self, query: str, top_k: int, sources: List[str], 
                 agent: str = None, metadata: str = None, where: dict = None, llm: str = None):
        data = {
            'query': query,
            'top_k': top_k,
            'sources': sources
        }
        optionals = {
            'agent': agent, 
            'metadata': metadata,
            'where': where,
            'llm': llm
        }
        data.update({k: v for k, v in optionals.items() if v is not None})

        return self._request("POST", "/retrieve", data)

