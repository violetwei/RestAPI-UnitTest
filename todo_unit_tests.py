import requests
import json
import unittest
import xml.etree.ElementTree as ET

def deleteOp():
    response = requests.get("http://localhost:4567/todos")
    for body in response.json()['todos']:
        requests.delete("http://localhost:4567/todos/" + body['id'])

class TestTodos(unittest.TestCase):
    def test_check_content_type_equals_json(self):
        print("*" * 30 + " test_check_content_type_equals_json " + "*" * 30)
        response = requests.get("http://localhost:4567/projects")
        equalsJson = self.assertEqual(response.headers["Content-Type"], "application/json")
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
        self.assertEqual(post_response.status_code, 201)
        #print(post_response)
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
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response_body["todos"][0]["id"], post_response.json()["id"])
        self.assertEqual(get_response_body["todos"][0]["title"], "testget")
        self.assertEqual(get_response_body["todos"][0]["doneStatus"], "true")
        self.assertEqual(get_response_body["todos"][0]["description"], "unit test")
        print("Passed")


def main():
    unittest.main()

if __name__ == "__main__":
    main()