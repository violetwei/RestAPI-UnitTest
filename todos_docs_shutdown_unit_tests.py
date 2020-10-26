import requests
import json
import unittest
import xml.etree.ElementTree as ET

def deleteOp():
    response = requests.get("http://localhost:4567/todos")
    for body in response.json()['todos']:
        requests.delete("http://localhost:4567/todos/" + body['id'])

class TestTodosDocsShutdown(unittest.TestCase):
    def test_check_content_type_equals_json(self):
        print("*" * 30 + " test_check_content_type_equals_json " + "*" * 30)
        response = requests.get("http://localhost:4567/projects")
        self.assertEqual(response.headers["Content-Type"], "application/json")
        print("Passed")

    
    # Test: HEAD /todos
    def test_head_projects(self):
        print("*" * 30 + " test_head_projects " + "*" * 30)
        response = requests.head("http://localhost:4567/projects")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.headers["Transfer-Encoding"], "chunked")
        print("Passed")


    # Test: POST /todos    
    def test_post_todos_JSON(self):
        deleteOp()
        print("*" * 30 + " test_post_todos_JSON " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "iusmod tempor incidi", "doneStatus": False, "description": "Duis aute irure dolo"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        self.assertEqual(post_response.status_code, 201, "Created")
        #print(post_response)
        print("Passed")


    # Test: bad request post 
    def test_post_todos_with_InvalidData(self):
        deleteOp()
        print("*" * 30 + " test_post_todos_with_InvalidData " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Wrong Post test", "doneStatus": "False", "description": "bad request"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        self.assertEqual(post_response.status_code, 400, "bad request")
        print("Passed")


    # Test: GET /todos
    def test_get_todos_JSON(self):
        deleteOp()
        print("*" * 30 + " test_get_todos_JSON " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "testget", "doneStatus": True, "description": "unit test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        get_response = requests.get("http://localhost:4567/todos")
        get_response_body = get_response.json()
        self.assertEqual(get_response.status_code, 200, "OK")
        self.assertEqual(get_response_body["todos"][0]["id"], post_response.json()["id"])
        self.assertEqual(get_response_body["todos"][0]["title"], "testget")
        self.assertEqual(get_response_body["todos"][0]["doneStatus"], "true")
        self.assertEqual(get_response_body["todos"][0]["description"], "unit test")
        print("Passed")


    # Test: HEAD todos/:id
    def test_head_todos_withID(self):
        deleteOp()
        print("*" * 30 + " test_head_todos_withID " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Get Head ID Test", "doneStatus": False,
                   "description": "This is Get Head ID test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        response = requests.head("http://localhost:4567/todos/" + post_response_body["id"])
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.headers["Transfer-Encoding"], "chunked")
        print("Passed")


    # Test: HEAD todos/:id  - case of invalid id
    def test_head_todos_with_InvalidID(self):
        deleteOp()
        print("*" * 30 + " test_head_todos_with_InvalidID " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Get Head Invalid ID Test", "doneStatus": False,
                   "description": "This is Get Head Invalid ID test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        response = requests.head("http://localhost:4567/todos/" + post_response_body["id"] + "10")
        self.assertEqual(response.status_code, 404, "Not Found")
        print("Passed")


    # Test: GET /todos/:id
    def test_get_todos_withID(self):
        deleteOp()
        print("*" * 30 + " test_head_todos_withID " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Get with ID Test", "doneStatus": True,
                   "description": "This is Get with ID test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(project))
        post_response_body = post_response.json()
        get_response = requests.get("http://localhost:4567/todos/" + post_response_body["id"])
        get_response_body = get_response.json()
        self.assertEqual(get_response.status_code, 200, "OK")
        self.assertEqual(get_response_body["todos"][0]["id"], post_response.json()["id"])
        self.assertEqual(get_response_body["todos"][0]["title"], "Get with ID Test")
        self.assertEqual(get_response_body["todos"][0]["doneStatus"], "true")
        self.assertEqual(get_response_body["todos"][0]["description"], "This is Get with ID test")
        print("Passed")


    # Test: GET /todos/:id  -  case of invalid id
    def test_get_todos_with_InvalidID(self):
        deleteOp()
        print("*" * 30 + " test_head_todos_with_InvalidID " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Get with Invalid ID Test", "doneStatus": True,
                   "description": "This is Get with Invalid ID test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(project))
        post_response_body = post_response.json()
        get_response = requests.get("http://localhost:4567/todos/" + post_response_body["id"] + "10")
        self.assertEqual(get_response.status_code, 404, "Not Found")
        print("Passed")


    # Test: POST /todos/:id  
    def test_post_todos_withID(self):
        deleteOp()
        print("*" * 30 + " test_post_todos_withID " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Post test with ID", "doneStatus": False, "description": "initial post"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "Created")
        # amend a specific instances of todo using a id with a body containing the fields to amend
        amended_todo = {"title": "Amended Post test with ID", "doneStatus": True, "description": "amended post"}
        amended_post_response = requests.post("http://localhost:4567/todos/" + post_response_body["id"], headers=headers, data=json.dumps(amended_todo))
        self.assertEqual(amended_post_response.status_code, 200, "OK")
        print("Passed")


    # Test: POST /todos/:id   - case of invalid data
    def test_post_todos_withID_InvalidData(self):
        deleteOp()
        print("*" * 30 + " test_post_todos_withID_InvalidData " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Post test with ID", "doneStatus": False, "description": "initial post"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "Created")
        # amend a specific instances of todo using a id with a body containing the fields to amend
        amended_todo = {"title": "Invalid Amended Post test with ID", "doneStatus": "True", "description": "amended post"}
        amended_post_response = requests.post("http://localhost:4567/todos/" + post_response_body["id"], headers=headers, data=json.dumps(amended_todo))
        self.assertEqual(amended_post_response.status_code, 400, "Bad Request")
        print("Passed")

    
    # Test: POST /todos/:id - case of invalid id
    def test_post_todos_with_InvalidID(self):
        deleteOp()
        print("*" * 30 + " test_post_todos_with_InvalidID " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Post test with Invalid ID", "doneStatus": False, "description": "initial post"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "Created")
        # amend a specific instances of todo using a id with a body containing the fields to amend
        amended_todo = {"title": "Amended Post test with ID", "doneStatus": True, "description": "amended post"}
        amended_post_response = requests.post("http://localhost:4567/todos/" + post_response_body["id"] + "10", headers=headers, data=json.dumps(amended_todo))
        self.assertEqual(amended_post_response.status_code, 404, "Not Found")
        print("Passed")


    # Test: PUT /todos/:id
    def test_put_todos_withID(self):
        deleteOp()
        print("*" * 30 + " test_put_todos_withID " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Put test with ID", "doneStatus": False, "description": "initial post"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "Created")
        # amend a specific instances of todo using a id with a body containing the fields to amend using put
        amended_todo = {"title": "Amended Put test with ID", "doneStatus": True, "description": "put test"}
        amended_post_response = requests.put("http://localhost:4567/todos/" + post_response_body["id"], headers=headers, data=json.dumps(amended_todo))
        self.assertEqual(amended_post_response.status_code, 200, "OK")
        print("Passed")


    # Test: PUT /todos/:id   - case of invalid data
    def test_put_todos_withID_InvalidData(self):
        deleteOp()
        print("*" * 30 + " test_put_todos_withID_InvalidData " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Put test with ID", "doneStatus": False, "description": "initial post"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "Created")
        # amend a specific instances of todo using a id with a body containing the fields to amend using put
        amended_todo = {"title": "Invalid Amended Put test with ID", "doneStatus": "True", "description": "put test"}
        amended_post_response = requests.put("http://localhost:4567/todos/" + post_response_body["id"], headers=headers, data=json.dumps(amended_todo))
        self.assertEqual(amended_post_response.status_code, 400, "Bad Request")
        print("Passed")

    
    # Test: PUT /todos/:id  - case of invalid id
    def test_put_todos_with_InvalidID(self):
        deleteOp()
        print("*" * 30 + " test_put_todos_with_InvalidID " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Put test with Invalid ID", "doneStatus": False, "description": "initial post"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "Created")
        # amend a specific instances of todo using a id with a body containing the fields to amend using put
        amended_todo = {"title": "Amended Put test with ID", "doneStatus": True, "description": "put test"}
        amended_post_response = requests.put("http://localhost:4567/todos/" + post_response_body["id"] + "10", headers=headers, data=json.dumps(amended_todo))
        self.assertEqual(amended_post_response.status_code, 404, "Not Found")
        print("Passed")


    # Test: DELETE /todos/:id
    def test_delete_todos_withID(self):
        deleteOp()
        print("*" * 30 + " test_delete_todos_withID " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Delete test with ID", "doneStatus": False, "description": "delete post"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "Created")
        # delete a specific instances of todo using a id
        delete_response = requests.delete("http://localhost:4567/todos/" + post_response_body["id"])
        self.assertEqual(delete_response.status_code, 200, "OK")
        print("Passed")


    # Test: DELETE /todos/:id  - case of invalid id
    def test_delete_todos_with_InvalidID(self):
        deleteOp()
        print("*" * 30 + " test_delete_todos_with_InvalidID " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Delete test with Invalid ID", "doneStatus": False, "description": "delete post"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "Created")
        # delete a specific instances of todo using a id
        delete_response = requests.delete("http://localhost:4567/todos/" + post_response_body["id"] + "10")
        self.assertEqual(delete_response.status_code, 404, "Not Found")
        print("Passed")

    
    # Test: HEAD /todos/:id/categories
    def test_head_todos_withID_categories(self):
        deleteOp()
        print("*" * 30 + " test_head_todos_withID_categories " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "HEAD test with ID & categories", "doneStatus": False, "description": "head test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        response = requests.head("http://localhost:4567/todos/" + post_response_body["id"] + "/categories")
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.headers["Transfer-Encoding"], "chunked")
        print("Passed")


    # Test: HEAD /todos/:id/categories - case of invalid id
    def test_head_todos_with_InvalidID_categories(self):
        deleteOp()
        print("*" * 30 + " test_head_todos_with_InvalidID_categories " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "HEAD test with Invalid ID & categories", "doneStatus": False, "description": "head test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        response = requests.head("http://localhost:4567/todos/" + post_response_body["id"] + "100" + "/categories")
        self.assertEqual(response.status_code, 404, "Not Found")
        #self.assertEqual(response.headers["Content-Type"], "application/json")
        #self.assertEqual(response.headers["Transfer-Encoding"], "chunked")
        print("Passed")

    
    # Test: POST /todos/:id/categories
    def test_post_todos_withID_categories(self):
        deleteOp()
        print("*" * 30 + " test_post_todos_withID_categories " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Post test with ID & categories", "doneStatus": False, "description": "post test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        category_items = {"title": "category x", "description": "post test"}
        category_post_response = requests.post("http://localhost:4567/todos/" + post_response_body["id"] + "/categories", headers=headers, data=json.dumps(category_items))
        self.assertEqual(category_post_response.status_code, 201, "created")
        print("Passed")


    # Test: POST /todos/:id/categories - case of invalid category data
    def test_post_todos_withID_InvalidCategories(self):
        deleteOp()
        print("*" * 30 + " test_post_todos_withID_InvalidCategories " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Post test with ID & Invalid categories", "doneStatus": False, "description": "post test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        category_items = {"title_name": "category x", "description": "post test"}
        category_post_response = requests.post("http://localhost:4567/todos/" + post_response_body["id"] + "/categories", headers=headers, data=json.dumps(category_items))
        self.assertEqual(category_post_response.status_code, 400, "bad request")
        print("Passed")

    
    # Test: POST /todos/:id/categories - case of invalid id
    def test_post_todos_with_InvalidID_categories(self):
        deleteOp()
        print("*" * 30 + " test_post_todos_with_InvalidID_categories " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Post test with Invalid ID & categories", "doneStatus": False, "description": "post test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        category_items = {"title": "category x", "description": "post test"}
        category_post_response = requests.post("http://localhost:4567/todos/" + post_response_body["id"] + "100" + "/categories", headers=headers, data=json.dumps(category_items))
        self.assertEqual(category_post_response.status_code, 404, "Not found")
        print("Passed")


    # Test: GET /todos/:id/categories
    def test_get_todos_withID_categories(self):
        deleteOp()
        print("*" * 30 + " test_get_todos_withID_categories " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Get test with ID & categories", "doneStatus": False, "description": "get test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        category_items = {"title": "category1", "description": "test"}
        category_post_response = requests.post("http://localhost:4567/todos/" + post_response_body["id"] + "/categories", headers=headers, data=json.dumps(category_items))
        self.assertEqual(category_post_response.status_code, 201, "created")

        get_response = requests.get("http://localhost:4567/todos/" + post_response_body["id"] + "/categories")
        get_response_body = get_response.json()
        self.assertEqual(get_response.status_code, 200, "OK")
        self.assertEqual(get_response_body["categories"][0]["id"], category_post_response.json()["id"])
        self.assertEqual(get_response_body["categories"][0]["title"], "category1")
        self.assertEqual(get_response_body["categories"][0]["description"], "test")
        #print(get_response_body)
        print("Passed")


    # Test: GET /todos/:id/categories  - case of invalid id
    def test_get_todos_with_InvlaidID_categories(self):
        deleteOp()
        print("*" * 30 + " test_get_todos_with_InvalidID_categories " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Get test with Invalid ID & categories", "doneStatus": False, "description": "get test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        category_items = {"title": "category1", "description": "test"}
        category_post_response = requests.post("http://localhost:4567/todos/" + post_response_body["id"] + "/categories", headers=headers, data=json.dumps(category_items))
        self.assertEqual(category_post_response.status_code, 201, "created")

        get_response = requests.get("http://localhost:4567/todos/" + post_response_body["id"] + "$700" + "/categories")
        self.assertEqual(get_response.status_code, 404, "Not found")
        print("Passed")

        
    # Test: Delete /todos/:id/categories/:id
    def test_delete_todos_id_categories_id(self):
        deleteOp()
        print("*" * 30 + " test_delete_todos_id_categories_id " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Delete test with ID & categoriesID", "doneStatus": False, "description": "delete test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        category_items = {"title": "category x", "description": "delete test"}
        category_post_response = requests.post("http://localhost:4567/todos/" + post_response_body["id"] + "/categories", 
            headers=headers, data=json.dumps(category_items))
        self.assertEqual(category_post_response.status_code, 201, "created")

        delete_response = requests.delete("http://localhost:4567/todos/" + post_response_body["id"] + "/categories/" 
            + category_post_response.json()["id"])
        self.assertEqual(delete_response.status_code, 200, "OK")
        print("Passed")


    # Test: Delete /todos/:id/categories/:id  - case of invalid id
    def test_delete_todos_InvalidId_categories_id(self):
        deleteOp()
        print("*" * 30 + " test_delete_todos_InvalidId_categories_id " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Delete test with Invlid ID & categoriesID", "doneStatus": False, "description": "delete test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        category_items = {"title": "category x", "description": "delete test"}
        category_post_response = requests.post("http://localhost:4567/todos/" + post_response_body["id"] + "/categories", 
            headers=headers, data=json.dumps(category_items))
        self.assertEqual(category_post_response.status_code, 201, "created")

        delete_response = requests.delete("http://localhost:4567/todos/" + post_response_body["id"] + " 80" 
            + "/categories/" + category_post_response.json()["id"] + "10")
        self.assertEqual(delete_response.status_code, 404, "not found")
        print("Passed")

    
    # Test: GET todos/:id/taskof
    def test_get_todos_id_tasksof(self):
        deleteOp()
        print("*" * 30 + " test_get_todos_id_tasksof " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Get test with ID & taskof", "doneStatus": False, "description": "get test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        get_response = requests.get("http://localhost:4567/todos/" + post_response_body["id"] + "/tasksof")
        #get_response_body = get_response.json()
        self.assertEqual(get_response.status_code, 200, "OK")
        print("Passed")


    # Test: GET todos/:id/taskof  - case of invalid id
    def test_get_todos_InvalidId_tasksof(self):
        deleteOp()
        print("*" * 30 + " test_get_todos_InvalidId_tasksof " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Get test with Invalid ID & taskof", "doneStatus": False, "description": "get test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        get_response = requests.get("http://localhost:4567/todos/" + post_response_body["id"] + "*30" + "/tasksof")
        #get_response_body = get_response.json()
        self.assertEqual(get_response.status_code, 404, "not found")
        print("Passed")


    # Test: HEAD todos/:id/taskof
    def test_head_todos_id_tasksof(self):
        deleteOp()
        print("*" * 30 + " test_head_todos_id_tasksof " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "HEAD test with ID & taskof", "doneStatus": False, "description": "HEAD test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        response = requests.head("http://localhost:4567/todos/" + post_response_body["id"] + "/tasksof")
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.headers["Transfer-Encoding"], "chunked")
        print("Passed")


    # Test: HEAD todos/:id/taskof  - case of invalid id
    def test_head_todos_InvalidId_tasksof(self):
        deleteOp()
        print("*" * 30 + " test_head_todos_InvalidId_tasksof " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "HEAD test with Invalid ID & taskof", "doneStatus": False, "description": "HEAD test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        response = requests.head("http://localhost:4567/todos/" + post_response_body["id"] + "89000" + "/tasksof")
        self.assertEqual(response.status_code, 404, "not found")
        #self.assertEqual(response.headers["Content-Type"], "application/json")
        #self.assertEqual(response.headers["Transfer-Encoding"], "chunked")
        print("Passed")

    
    # Test: POST todos/:id/taskof
    def test_post_todos_id_tasksof(self):
        deleteOp()
        print("*" * 30 + " test_post_todos_id_tasksof " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Post test with ID & taskof", "doneStatus": False, "description": "post test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        project = {"title": "Post Task Test", "completed": False, "active": True,
                   "description": "This is Post Task test"}
        post_url = "http://localhost:4567/todos/" + post_response_body["id"] + "/tasksof"
        post_response = requests.post(post_url, headers=headers, data=json.dumps(project))
        self.assertEqual(post_response.status_code, 201, "created")
        print("Passed")

    
    # Test: POST todos/:id/taskof  - case of Invalid Data
    def test_post_todos_id_tasksof_Invalid_Data(self):
        deleteOp()
        print("*" * 30 + " test_post_todos_id_tasksof_Invalid_Data " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Post test with ID & taskof with invalid data", "doneStatus": False, "description": "post test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        project = {"title": "Post Task Test", "completed": "False", "active": True,
                   "description": "This is Post Task test"}
        post_url = "http://localhost:4567/todos/" + post_response_body["id"] + "/tasksof"
        post_response = requests.post(post_url, headers=headers, data=json.dumps(project))
        self.assertEqual(post_response.status_code, 400, "Bad Request")
        print("Passed")


    # Test: POST todos/:id/taskof  - case of Invalid Data 2
    def test_post_todos_id_tasksof_Invalid_Data2(self):
        deleteOp()
        print("*" * 30 + " test_post_todos_id_tasksof_Invalid_Data2 " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Post test with ID & taskof with invalid data 2", "doneStatus": False, "description": "post test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        project = {"title": "Post Task Test", "isCompleted": False, "active": True,
                   "description": "This is Post Task test"}
        post_url = "http://localhost:4567/todos/" + post_response_body["id"] + "/tasksof"
        post_response = requests.post(post_url, headers=headers, data=json.dumps(project))
        self.assertEqual(post_response.status_code, 400, "Bad Request")
        print("Passed")


    # Test: POST todos/:id/taskof - case of invalid id
    def test_post_todos_InvalidId_tasksof(self):
        deleteOp()
        print("*" * 30 + " test_post_todos_InvalidId_tasksof " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Post test with Invalid ID & taskof", "doneStatus": False, "description": "post test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        project = {"title": "Invalid Post Task Test", "completed": False, "active": True,
                   "description": "This is Post Task test"}
        post_url = "http://localhost:4567/todos/" + post_response_body["id"] + "680000" + "/tasksof"
        post_response = requests.post(post_url, headers=headers, data=json.dumps(project))
        self.assertEqual(post_response.status_code, 404, "not found")
        print("Passed")


    # Test: DELETE todos/:id/taskof/:id
    def test_delete_todos_id_tasksof(self):
        deleteOp()
        print("*" * 30 + " test_delete_todos_id_tasksof " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Delete test with ID & taskof", "doneStatus": False, "description": "delete test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        project = {"title": "Delete Task Test", "completed": False, "active": True,
                   "description": "This is Delete Task test"}
        post_url = "http://localhost:4567/todos/" + post_response_body["id"] + "/tasksof"
        project_post_response = requests.post(post_url, headers=headers, data=json.dumps(project))
        project_post_response_body = project_post_response.json()
        self.assertEqual(project_post_response.status_code, 201, "created")

        delete_url = "http://localhost:4567/todos/" + post_response_body["id"] + "/tasksof/" + project_post_response_body["id"]
        delete_response = requests.delete(delete_url)
        self.assertEqual(delete_response.status_code, 200, "OK")
        print("Passed")


    # Test: DELETE todos/:id/taskof/:id  - case of invalid id
    def test_delete_todos_InvalidId_tasksof(self):
        deleteOp()
        print("*" * 30 + " test_delete_todos_InvalidId_tasksof " + "*" * 30)
        url = "http://localhost:4567/todos"
        headers = {'Content-Type': 'application/json'}
        todo = {"title": "Delete test with Invalid ID & taskof", "doneStatus": False, "description": "delete test"}
        post_response = requests.post(url, headers=headers, data=json.dumps(todo))
        post_response_body = post_response.json()
        self.assertEqual(post_response.status_code, 201, "created")

        project = {"title": "Invalid Delete Task Test", "completed": False, "active": True,
                   "description": "This is Delete Task test"}
        post_url = "http://localhost:4567/todos/" + post_response_body["id"] + "/tasksof"
        project_post_response = requests.post(post_url, headers=headers, data=json.dumps(project))
        project_post_response_body = project_post_response.json()
        self.assertEqual(project_post_response.status_code, 201, "created")

        delete_url = "http://localhost:4567/todos/" + post_response_body["id"] + "/tasksof/" + project_post_response_body["id"] + "6888"
        delete_response = requests.delete(delete_url)
        self.assertEqual(delete_response.status_code, 404, "Not found")
        print("Passed")
        
        
    # Test: /docs
    def test_docs(self):
        print("*" * 30 + " test_docs " + "*" * 30)
        get_url = "http://localhost:4567/docs"
        get_response = requests.get(get_url)
        self.assertEqual(get_response.status_code, 200, "OK")
        print("Passed")


    # Test: /shutdown
    def test_shutdown(self):
        print("*" * 30 + " test_shutdown " + "*" * 30)
        get_url = "http://localhost:4567/shutdown"
        get_response = requests.get(get_url)
        print(get_response)
        print("Passed")

def main():
    unittest.main()

if __name__ == "__main__":
    main()
