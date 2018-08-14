import json

class save_req:
    all_requests = []
    def create_req(self,model="dataelement",name="Test1",app="aristotle_mdr",other_field_data={}):
        payload = {
            "concept_type": {
                "app": app,
                "model": model
            },
            "fields": {
                "name": name,
                "definition": "Placeholder"
            }
        }
        for key, value in other_field_data.items():
            payload["fields"][key] = value
        return payload
        # self.all_requests.append(payload)

    def save_req_file(self,data):
        with open('data.json', 'w') as outfile:
            outfile.write(json.dumps(data, sort_keys = True, indent = 4, ensure_ascii = False))