import json

class save_req:
    all_requests = []
    def create_req(self,model="dataelement",name="Test1",app="aristotle_mdr"):
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
        self.all_requests.append(payload)

    def save_req_file(self):
        with open('data.json', 'w') as outfile:
            outfile.write(json.dumps(self.all_requests, sort_keys = True, indent = 4, ensure_ascii = False))