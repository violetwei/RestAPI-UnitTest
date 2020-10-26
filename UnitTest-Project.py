import requests
import json
import unittest
import xml.etree.ElementTree as ET


def deleteOp():
    response = requests.get("http://localhost:4567/projects")
    for body in response.json()['projects']:
        requests.delete("http://localhost:4567/projects/" + body['id'])


class TestProject(unittest.TestCase):

    def test_check_content_type_equals_json(self):
        print("*" * 30 + "test_check_content_type_equals_json" + "*" * 30)
        response = requests.get("http://localhost:4567/projects")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Should be application/json")
        print("Test Passed")

    def test_head_projects(self):
        print("*" * 30 + "test_head_projects" + "*" * 30)
        response = requests.head("http://localhost:4567/projects")
        self.assertEqual(response.status_code, 200, "should be 200")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Should be application/json")
        self.assertEqual(response.headers["Transfer-Encoding"], "chunked", "Should be chunked")
        print("Test Passed")

    def test_head_projects_withID(self):
        deleteOp()
        print("*" * 30 + "test_head_projects_withID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Get Head ID Test", "completed": False, "active": True,
                   "description": "This is Get Head ID test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        response = requests.head("http://localhost:4567/projects/" + response_body1["id"])
        self.assertEqual(response.status_code, 200, "should be 200")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Should be application/json")
        self.assertEqual(response.headers["Transfer-Encoding"], "chunked", "Should be chunked")
        print("Test Passed")

    def test_head_projects_withInvalidID(self):
        deleteOp()
        print("*" * 30 + "test_head_projects_withInvalidID" + "*" * 30)
        response = requests.head("http://localhost:4567/projects/9999")
        self.assertEqual(response.status_code, 404, "should be 404")
        print("Test Passed")

    def test_post_projects_JSON(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_JSON" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test", "completed": False, "active": True,
                   "description": "This is post JSON test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response2 = requests.get("http://localhost:4567/projects")
        response_body1 = response1.json()
        response_body2 = response2.json()
        self.assertEqual(response1.status_code, 201, "should be 201")
        self.assertEqual(response_body2["projects"][0]["id"], response_body1["id"], "ID is different")
        self.assertEqual(response_body2["projects"][0]["title"], "Post JSON Test", "title is different")
        self.assertEqual(response_body2["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body2["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body2["projects"][0]["description"], "This is post JSON test",
                         "description is different")
        print("Test Passed")

    def test_post_projects_InvalidData(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_InvalidData" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test", "completed": "wrong", "active": True,
                   "description": "This is post JSON test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        self.assertEqual(response1.status_code, 400, "should be 400")
        print("Test Passed")

    def test_post_projects_InvalidData2(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_InvalidData2" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test", "completed": False, "active": True,
                   "description": "This is post JSON test", "Temp": "wrong data"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        self.assertEqual(response1.status_code, 400, "should be 400")
        print("Test Passed")

    # TODO: this successes, talk about this later
    def test_post_projects_InvalidData3(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_InvalidData3" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test", "completed": False, "active": True, "description": 1234}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response2 = requests.get("http://localhost:4567/projects")
        response_body1 = response1.json()
        response_body2 = response2.json()
        self.assertEqual(response1.status_code, 201, "should be 201")
        self.assertEqual(response_body2["projects"][0]["id"], response_body1["id"], "ID is different")
        self.assertEqual(response_body2["projects"][0]["title"], "Post JSON Test", "title is different")
        self.assertEqual(response_body2["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body2["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body2["projects"][0]["description"], "1234.0", "description is different")
        print("Test Passed")

    def test_post_projects_IncompleteData(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_IncompleteData" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test", "completed": False, "active": True}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response2 = requests.get("http://localhost:4567/projects")
        response_body1 = response1.json()
        response_body2 = response2.json()
        self.assertEqual(response1.status_code, 201, "should be 201")
        self.assertEqual(response_body2["projects"][0]["id"], response_body1["id"], "ID is different")
        self.assertEqual(response_body2["projects"][0]["title"], "Post JSON Test", "title is different")
        self.assertEqual(response_body2["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body2["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body2["projects"][0]["description"], '', "active is different")
        print("Test Passed")

    def test_post_projects_withID_Without_changes(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withID_Without_changes" + "*" * 30)
        url = "http://localhost:4567/projects/1"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post ID Test", "completed": False, "active": True, "description": "This is Post ID test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        self.assertEqual(response1.status_code, 404, "should be 404")
        print("Test Passed")

    def test_post_projects_withID_with_changes(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_JSON" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test", "completed": False, "active": True,
                   "description": "This is post JSON test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        url = "http://localhost:4567/projects/" + response_body1["id"]
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test2", "completed": False, "active": True,
                   "description": "This is post JSON test2"}
        response2 = requests.post(url, headers=headers, data=json.dumps(project))
        response3 = requests.get("http://localhost:4567/projects")
        response_body2 = response3.json()
        self.assertEqual(response2.status_code, 200, "should be 200")
        self.assertEqual(response_body2["projects"][0]["id"], response_body1["id"], "ID is different")
        self.assertEqual(response_body2["projects"][0]["title"], "Post JSON Test2", "title is different")
        self.assertEqual(response_body2["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body2["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body2["projects"][0]["description"], "This is post JSON test2",
                         "description is different")
        print("Test Passed")

    def test_post_projects_withInvalid_ID(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withInvalid_ID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test", "completed": False, "active": True,
                   "description": "This is post JSON test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))

        response_body1 = response1.json()
        num = int(response_body1["id"]) + 1
        url = "http://localhost:4567/projects/" + str(num)
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test2", "completed": False, "active": True,
                   "description": "This is post JSON test2"}
        response2 = requests.post(url, headers=headers, data=json.dumps(project))

        response3 = requests.get("http://localhost:4567/projects")
        self.assertEqual(response2.status_code, 404, "should be 404")
        print("Test Passed")


    # TODO: Figure out xml part
    # def test_post_projects_XML(self):
    #     print("*" * 30 + "test_post_projects_XML" + "*" * 30)
    #     url = "http://localhost:4567/projects"
    #     headers = {'Content-Type': 'application/xml'}
    #     data = ET.Element('project')
    #     item0 = ET.SubElement(data, 'active')
    #     item1 = ET.SubElement(data, 'description')
    #     item3 = ET.SubElement(data, 'completed')
    #     item4 = ET.SubElement(data, 'title')
    #     item0.text = 'true'
    #     item1.text = 'This is post test'
    #     item3.text = 'true'
    #     item4.text = 'Post Test'
    #     response1 = requests.post(url, headers=headers, data=data)
    #     response2 = requests.get("http://localhost:4567/projects")
    #     response_body1 = response1.json()
    #     print(response_body1)
    #     response_body2 = response2.json()
    # self.assertEqual(response_body2["projects"][0]["id"], response_body1["id"], "ID is different")
    # self.assertEqual(response_body2["projects"][0]["title"], "Post Test", "title is different")
    # self.assertEqual(response_body2["projects"][0]["completed"], False, "completed is different")
    # self.assertEqual(response_body2["projects"][0]["active"], True, "active is different")
    # self.assertEqual(response_body2["projects"][0]["description"], "This is post test", "description is different")

    def test_get_projects_withID(self):
        deleteOp()
        print("*" * 30 + "test_get_projects_withID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Get ID Test", "completed": False, "active": True, "description": "This is Get ID test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        response = requests.get("http://localhost:4567/projects/" + response_body1["id"])
        response_body = response.json()
        self.assertEqual(response.status_code, 200, "should be 200")
        self.assertEqual(response_body["projects"][0]["id"], response_body1["id"], "ID is different")
        self.assertEqual(response_body["projects"][0]["title"], "Get ID Test", "title is different")
        self.assertEqual(response_body["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body["projects"][0]["description"], "This is Get ID test", "description is different")
        print("Test Passed")

    def test_get_projects(self):
        deleteOp()
        print("*" * 30 + "test_get_projects" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Get Test", "completed": False, "active": True, "description": "This is Get test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        response = requests.get("http://localhost:4567/projects")
        response_body = response.json()
        self.assertEqual(response.status_code, 200, "should be 200")
        self.assertEqual(response_body["projects"][0]["id"], response_body1["id"], "ID is different")
        self.assertEqual(response_body["projects"][0]["title"], "Get Test", "title is different")
        self.assertEqual(response_body["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body["projects"][0]["description"], "This is Get test", "description is different")
        print("Test Passed")


    def test_get_project_withInvalidID(self):
        deleteOp()
        print("*" * 30 + "test_get_project_withInvalidID" + "*" * 30)
        response = requests.get("http://localhost:4567/projects/9999")
        self.assertEqual(response.status_code, 404, "should be 404")
        print("Test Passed")

    def test_put_projects(self):
        deleteOp()
        print("*" * 30 + "test_put_projects" + "*" * 30)
        url = "http://localhost:4567/projects/"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Outside", "completed": False, "active": False, "description": "not good"}
        response1 = requests.put(url, headers=headers, data=json.dumps(project))
        self.assertEqual(response1.status_code, 404, "should be 404")
        print("Test Passed")

    def test_put_projects_withID_Without_changes(self):
        deleteOp()
        print("*" * 30 + "test_put_projects_withID_Without_changes" + "*" * 30)
        url = "http://localhost:4567/projects/1"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post ID Test", "completed": False, "active": True, "description": "This is Post ID test"}
        response1 = requests.put(url, headers=headers, data=json.dumps(project))
        self.assertEqual(response1.status_code, 404, "should be 404")
        print("Test Passed")

    def test_put_projects_withID_with_changes(self):
        deleteOp()
        print("*" * 30 + "test_put_projects_withID_with_changes" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Put JSON Test", "completed": False, "active": True,
                   "description": "This is Put JSON test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        url = "http://localhost:4567/projects/" + response_body1["id"]
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Put JSON Test2", "completed": False, "active": True,
                   "description": "This is Put JSON test2"}
        response2 = requests.put(url, headers=headers, data=json.dumps(project))
        response3 = requests.get("http://localhost:4567/projects")
        response_body2 = response3.json()
        self.assertEqual(response2.status_code, 200, "should be 200")
        self.assertEqual(response_body2["projects"][0]["id"], response_body1["id"], "ID is different")
        self.assertEqual(response_body2["projects"][0]["title"], "Put JSON Test2", "title is different")
        self.assertEqual(response_body2["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body2["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body2["projects"][0]["description"], "This is Put JSON test2",
                         "description is different")
        print("Test Passed")

    # TODO: mising boolean empty is false, a bug, talk about it tomorrow
    def test_put_projects_withID_with_changes_incompletedata(self):
        deleteOp()
        print("*" * 30 + "test_put_projects_withID_with_changes_incompletedata" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Put JSON Test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        url = "http://localhost:4567/projects/" + response_body1["id"]
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Put JSON Test2", "active": True,
                   "description": "This is Put JSON test2"}
        response2 = requests.put(url, headers=headers, data=json.dumps(project))
        response3 = requests.get("http://localhost:4567/projects")
        response_body2 = response3.json()
        self.assertEqual(response2.status_code, 200, "should be 200")
        self.assertEqual(response_body2["projects"][0]["id"], response_body1["id"], "ID is different")
        self.assertEqual(response_body2["projects"][0]["title"], "Put JSON Test2", "title is different")
        self.assertEqual(response_body2["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body2["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body2["projects"][0]["description"], "This is Put JSON test2",
                         "description is different")
        print("Test Passed")

    def test_put_projects_withID_with_changes_invaliddata(self):
        deleteOp()
        print("*" * 30 + "test_put_projects_withID_with_changes_invaliddata" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Put JSON Test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        url = "http://localhost:4567/projects/" + response_body1["id"]
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Put JSON Test2", "completed": "False", "active": True,
                   "description": "This is Put JSON test2"}
        response2 = requests.put(url, headers=headers, data=json.dumps(project))
        response3 = requests.get("http://localhost:4567/projects")
        response_body2 = response3.json()
        self.assertEqual(response2.status_code, 400, "should be 400")
        print("Test Passed")

    # TODO: Again, don't have to be a string
    def test_put_projects_withID_with_changes_invaliddata2(self):
        deleteOp()
        print("*" * 30 + "test_put_projects_withID_with_changes_invaliddata2" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Put JSON Test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        url = "http://localhost:4567/projects/" + response_body1["id"]
        headers = {'Content-Type': 'application/json'}
        project = {"title": 123456.456123, "completed": False, "active": True,
                   "description": "123.4545"}
        response2 = requests.put(url, headers=headers, data=json.dumps(project))
        response3 = requests.get("http://localhost:4567/projects")
        response_body2 = response3.json()
        self.assertEqual(response2.status_code, 200, "should be 200")
        self.assertEqual(response_body2["projects"][0]["id"], response_body1["id"], "ID is different")
        self.assertEqual(response_body2["projects"][0]["title"], "123456.456123", "title is different")
        self.assertEqual(response_body2["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body2["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body2["projects"][0]["description"], "123.4545",
                         "description is different")
        print("Test Passed")

    def test_put_projects_withInvalidID(self):
        deleteOp()
        print("*" * 30 + "test_put_projects_withInvalidID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test", "completed": False, "active": True,
                   "description": "This is post JSON test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        num = int(response_body1["id"]) + 1
        url = "http://localhost:4567/projects/" + str(num)
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test2", "completed": False, "active": True,
                   "description": "This is post JSON test2"}
        response2 = requests.put(url, headers=headers, data=json.dumps(project))
        self.assertEqual(response2.status_code, 404, "should be 404")
        print("Test Passed")

    def test_delete_projects(self):
        deleteOp()
        print("*" * 30 + "test_delete_projects" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Delete Test", "completed": False, "active": True, "description": "This is Delete test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        delete = requests.delete("http://localhost:4567/projects/")
        self.assertEqual(delete.status_code, 404, "should be 404")
        print("Test Passed")

    def test_delete_projects_withID(self):
        deleteOp()
        print("*" * 30 + "test_delete_projects_withID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Delete Test", "completed": False, "active": True, "description": "This is Delete test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        delete = requests.delete("http://localhost:4567/projects/" + response_body1["id"])
        response2 = requests.get("http://localhost:4567/projects")
        response_body2 = response2.json()
        self.assertEqual(delete.status_code, 200, "should be 200")
        self.assertEqual(len(response_body2["projects"]), 0, "should be 0")
        print("Test Passed")

    def test_delete_projects_withInvalidID(self):
        deleteOp()
        print("*" * 30 + "test_delete_projects_withInvalidID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Delete Test", "completed": False, "active": True, "description": "This is Delete test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        num = int(response_body1["id"]) + 1
        delete = requests.delete("http://localhost:4567/projects/" + str(num))
        self.assertEqual(delete.status_code, 404, "should be 404")
        print("Test Passed")







    def test_post_projects_withID_categories(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withID_categories" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        url = "http://localhost:4567/projects/" + response_body1["id"] + "/categories"
        headers = {'Content-Type': 'application/json'}
        category = {
            "title": "Category test",
            "description": "This is category test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        response2 = requests.get(url)
        response_body2 = response2.json()
        self.assertEqual(response1.status_code, 201, "should be 201")
        self.assertEqual(response_body2["categories"][0]["id"], response1.json()["id"], "ID is different")
        self.assertEqual(response_body2["categories"][0]["title"], "Category test", "Title is different")
        self.assertEqual(response_body2["categories"][0]["description"], "This is category test",
                         "description is different")
        print("Test Passed")

    def test_post_projects_withInvalidID_categories(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withInvalidID_categories" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        num = int(response_body1["id"]) + 1
        url = "http://localhost:4567/projects/" + str(num) + "/categories"
        headers = {'Content-Type': 'application/json'}
        category = {
            "title": "Category test",
            "description": "This is category test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        self.assertEqual(response1.status_code, 404, "should be 404")
        print("Test Passed")

    def test_post_projects_withID_categories_InvalidData(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withID_categories_InvalidData" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        url = "http://localhost:4567/projects/" + response_body1["id"] + "/categories"
        headers = {'Content-Type': 'application/json'}
        category = {
            "title": "Category test",
            "description": "This is category test",
            "invalid": "fkldsjklsj"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        self.assertEqual(response1.status_code, 400, "should be 400")
        print("Test Passed")

    # Decription does not have to be a string
    # TODO: Again, float to string
    def test_post_projects_withID_categories_InvalidData2(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withID_categories_InvalidData2" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        url = "http://localhost:4567/projects/" + response_body1["id"] + "/categories"
        headers = {'Content-Type': 'application/json'}
        category = {
            "title": "Category test",
            "description": 2134,
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        response2 = requests.get(url)
        response_body2 = response2.json()
        self.assertEqual(response1.status_code, 201, "should be 201")
        self.assertEqual(response_body2["categories"][0]["id"], response1.json()["id"], "ID is different")
        self.assertEqual(response_body2["categories"][0]["title"], "Category test", "Title is different")
        self.assertEqual(response_body2["categories"][0]["description"], "2134.0", "description is different")
        print("Test Passed")

    def test_post_projects_withID_categories_IncompleteData(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withID_categories_IncompleteData" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()

        url = "http://localhost:4567/projects/" + response_body1["id"] + "/categories"
        headers = {'Content-Type': 'application/json'}
        category = {
            "title": "Category test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        response2 = requests.get(url)
        response_body2 = response2.json()
        self.assertEqual(response1.status_code, 201, "should be 201")
        self.assertEqual(response_body2["categories"][0]["id"], response1.json()["id"], "ID is different")
        self.assertEqual(response_body2["categories"][0]["title"], "Category test", "Title is different")
        print("Test Passed")

    def test_get_projects_withID_categories(self):
        deleteOp()
        print("*" * 30 + "test_get_projects_withID_categories" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()

        url = "http://localhost:4567/projects/" + response_body1["id"] + "/categories"
        headers = {'Content-Type': 'application/json'}
        category = {
            "title": "Category test",
            "description": "This is category test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        response = requests.get(url)
        response_body = response.json()
        self.assertEqual(response.status_code, 200, "should be 200")
        self.assertEqual(response_body["categories"][0]["id"], response1.json()["id"], "ID is different")
        self.assertEqual(response_body["categories"][0]["title"], "Category test", "title is different")
        self.assertEqual(response_body["categories"][0]["description"], "This is category test",
                         "description is different")
        print("Test Passed")

    def test_get_projects_withInvalidID_categories(self):
        deleteOp()
        print("*" * 30 + "test_get_projects_withInvalidID_categories" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        num = int(response_body1["id"]) + 1
        url = "http://localhost:4567/projects/" + str(num) + "/categories"
        headers = {'Content-Type': 'application/json'}
        category = {
            "title": "Category test",
            "description": "This is category test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        response = requests.get(url)
        response_body = response.json()
        self.assertEqual(response.status_code, 200, "should be 200")
        self.assertEqual(len(response_body["categories"]), 0, "should be 0")
        print("Test Passed")

    def test_get_projects_withID_categoriesID(self):
        deleteOp()
        print("*" * 30 + "test_get_projects_withID_categoriesID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()

        url = "http://localhost:4567/projects/" + response_body1["id"] + "/categories"
        headers = {'Content-Type': 'application/json'}
        category = {
            "title": "Category test",
            "description": "This is category test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        url = url + "/" + response1.json()["id"]
        response = requests.get(url)
        self.assertEqual(response.status_code, 404, "should be 404")
        print("Test Passed")

    def test_head_projects_withID_categories(self):
        print("*" * 30 + "test_head_projects_withID_categories" + "*" * 30)
        deleteOp()
        print("*" * 30 + "test_get_projects_withID_categoriesID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()

        url = "http://localhost:4567/projects/" + response_body1["id"] + "/categories"
        response1 = requests.head(url)
        self.assertEqual(response1.status_code, 200, "should be 200")
        self.assertEqual(response1.headers["Content-Type"], "application/json", "Should be application/json")
        self.assertEqual(response1.headers["Transfer-Encoding"], "chunked", "Should be chunked")
        print("Test Passed")


    def test_head_projects_withInvalidID_categories(self):
        deleteOp()
        print("*" * 30 + "test_head_projects_withInvalidID_categories" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        num = int(response_body1["id"]) + 1
        url = "http://localhost:4567/projects/" + str(num) + "/categories"
        response1 = requests.head(url)
        self.assertEqual(response1.status_code, 200, "should be 200")
        self.assertEqual(response1.headers["Content-Type"], "application/json", "Should be application/json")
        self.assertEqual(response1.headers["Transfer-Encoding"], "chunked", "Should be chunked")
        print("Test Passed")

    def test_delete_projects_withInvalidID_categories(self):
        deleteOp()
        print("*" * 30 + "test_delete_projects_withID_categories" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        num = int(response_body1["id"]) + 1
        url = "http://localhost:4567/projects/" + str(num) + "/categories"
        delete = requests.delete(url)
        self.assertEqual(delete.status_code, 405, "should be 405")
        print("Test Passed")

    def test_delete_projects_withID_categories(self):
        deleteOp()
        print("*" * 30 + "test_delete_projects_withID_categories" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        num = int(response_body1["id"])
        url = "http://localhost:4567/projects/" + str(num) + "/categories"
        delete = requests.delete(url)
        self.assertEqual(delete.status_code, 405, "should be 405")
        print("Test Passed")

    def test_delete_projects_withID_categoriesID(self):
        deleteOp()
        print("*" * 30 + "test_delete_projects_withID_categoriesID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()

        url = "http://localhost:4567/projects/" + response_body1["id"] + "/categories"
        headers = {'Content-Type': 'application/json'}
        category = {
            "title": "Category test",
            "description": "This is category test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        url2 = url + "/" + response1.json()["id"]
        delete = requests.delete(url2)
        response2 = requests.get(url)
        response_body2 = response2.json()
        self.assertEqual(delete.status_code, 200, "should be 200")
        self.assertEqual(len(response_body2["categories"]), 0, "should be 0")
        print("Test Passed")

    def test_delete_projects_withID_categoriesInvalidID(self):
        deleteOp()
        print("*" * 30 + "test_delete_projects_withID_categoriesInvalidID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()

        url = "http://localhost:4567/projects/" + response_body1["id"] + "/categories"
        headers = {'Content-Type': 'application/json'}
        category = {
            "title": "Category test",
            "description": "This is category test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        url2 = url + "/" + str(int(response1.json()["id"])+1)
        delete = requests.delete(url2)
        response2 = requests.get(url)
        response_body2 = response2.json()
        self.assertEqual(delete.status_code, 404, "should be 404")
        print("Test Passed")










    def test_post_projects_withID_tasks(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withID_tasks" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Task Test", "completed": False, "active": True,
                   "description": "This is Post Task test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        url = "http://localhost:4567/projects/" + response_body1["id"] + "/tasks"
        headers = {'Content-Type': 'application/json'}
        task = {
            "title": "Task Test",
            "doneStatus": True,
            "description": "This is task test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(task))
        response2 = requests.get(url)
        response_body2 = response2.json()
        self.assertEqual(response1.status_code, 201, "should be 201")
        self.assertEqual(response_body2["todos"][0]['tasksof'][0]["id"], response1.json()['tasksof'][0]["id"], "ID is different")
        self.assertEqual(response_body2["todos"][0]["title"], "Task Test", "Title is different")
        self.assertEqual(response_body2["todos"][0]["doneStatus"], "true", "doneStatus is different")
        self.assertEqual(response_body2["todos"][0]["description"], "This is task test",
                         "description is different")
        print("Test Passed")

    def test_post_projects_withInvalidID_tasks(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withInvalidID_tasks" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Task Test", "completed": False, "active": True,
                   "description": "This is Post Task test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        num = int(response_body1["id"]) + 1
        url = "http://localhost:4567/projects/" + str(num) + "/tasks"
        headers = {'Content-Type': 'application/json'}
        task = {
            "title": "Task Test",
            "doneStatus": True,
            "description": "This is a task test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(task))
        self.assertEqual(response1.status_code, 404, "should be 404")
        print("Test Passed")

    def test_post_projects_withID_tasks_InvalidData(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withID_tasks_InvalidData" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Task Test", "completed": False, "active": True,
                   "description": "This is Post Task test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        url = "http://localhost:4567/projects/" + response_body1["id"] + "/tasks"
        headers = {'Content-Type': 'application/json'}
        task = {
            "title": "Task Test",
            "doneStatus": True,
            "description": "This is a task test",
            "invalid": "fjksdfkdsjkfds"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(task))
        self.assertEqual(response1.status_code, 400, "should be 400")
        print("Test Passed")

    # Decription does not have to be a string
    # TODO: Again, float to string
    def test_post_projects_withID_tasks_InvalidData2(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withID_tasks_InvalidData2" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Task Test", "completed": False, "active": True,
                   "description": "This is Post Task test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        url = "http://localhost:4567/projects/" + response_body1["id"] + "/tasks"
        headers = {'Content-Type': 'application/json'}
        task = {
            "title": 123456,
            "doneStatus": True,
            "description": "This is a task test",
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(task))
        response2 = requests.get(url)
        response_body2 = response2.json()
        self.assertEqual(response1.status_code, 201, "should be 201")

        self.assertEqual(response_body2["todos"][0]['tasksof'][0]['id'], response1.json()['tasksof'][0]["id"], "ID is different")
        self.assertEqual(response_body2["todos"][0]["title"], "123456.0", "Title is different")
        self.assertEqual(response_body2["todos"][0]["doneStatus"], "true", "Title is different")
        self.assertEqual(response_body2["todos"][0]["description"], "This is a task test", "description is different")
        print("Test Passed")

        # TODO:400? I guess yes, title is mandatory
    def test_post_projects_withID_tasks_IncompleteData(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withID_tasks_IncompleteData" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Tasks Test", "completed": False, "active": True,
                   "description": "This is Post Tasks test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()

        url = "http://localhost:4567/projects/" + response_body1["id"] + "/tasks"
        headers = {'Content-Type': 'application/json'}
        category = {
            "doneStatus": True,
            "description": "This is a task test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(category))
        response2 = requests.get(url)
        response_body2 = response2.json()
        self.assertEqual(response1.status_code, 400, "should be 400")
        print("Test Passed")

    def test_get_projects_withID_tasks(self):
        deleteOp()
        print("*" * 30 + "test_get_projects_withID_tasks" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Tasks Test", "completed": False, "active": True,
                   "description": "This is Post Tasks test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()

        url = "http://localhost:4567/projects/" + response_body1["id"] + "/tasks"
        headers = {'Content-Type': 'application/json'}
        task = {
            "title": "Task Test",
            "doneStatus": True,
            "description": "This is a task test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(task))
        response = requests.get(url)
        response_body = response.json()
        self.assertEqual(response.status_code, 200, "should be 200")
        self.assertEqual(response_body["todos"][0]['tasksof'][0]['id'], response1.json()['tasksof'][0]["id"], "ID is different")
        self.assertEqual(response_body["todos"][0]["title"], "Task Test", "Title is different")
        self.assertEqual(response_body["todos"][0]["doneStatus"], "true", "Title is different")
        self.assertEqual(response_body["todos"][0]["description"], "This is a task test", "description is different")
        print("Test Passed")

    def test_get_projects_withInvalidID_tasks(self):
        deleteOp()
        print("*" * 30 + "test_get_projects_withInvalidID_tasks" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Tasks Test", "completed": False, "active": True,
                   "description": "This is Post Tasks test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        num = int(response_body1["id"]) + 1
        url = "http://localhost:4567/projects/" + str(num) + "/tasks"
        headers = {'Content-Type': 'application/json'}
        task = {
            "title": "Task Test",
            "doneStatus": True,
            "description": "This is a task test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(task))
        response = requests.get(url)
        response_body = response.json()
        self.assertEqual(response.status_code, 200, "should be 200")
        self.assertEqual(len(response_body["todos"]), 0, "should be 0")
        print("Test Passed")

    def test_get_projects_withID_tasksID(self):
        deleteOp()
        print("*" * 30 + "test_get_projects_withID_tasksID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()

        url = "http://localhost:4567/projects/" + response_body1["id"] + "/tasks"
        headers = {'Content-Type': 'application/json'}
        task = {
            "title": "Task Test",
            "doneStatus": True,
            "description": "This is a task test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(task))
        url = url + "/" + response1.json()['tasksof'][0]["id"]
        response = requests.get(url)
        self.assertEqual(response.status_code, 404, "should be 404")
        print("Test Passed")

    def test_head_projects_withID_tasks(self):
        print("*" * 30 + "test_head_projects_withID_tasks" + "*" * 30)
        deleteOp()
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Tasks Test", "completed": False, "active": True,
                   "description": "This is Post Tasks test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()

        url = "http://localhost:4567/projects/" + response_body1["id"] + "/tasks"
        response1 = requests.head(url)
        self.assertEqual(response1.status_code, 200, "should be 200")
        self.assertEqual(response1.headers["Content-Type"], "application/json", "Should be application/json")
        self.assertEqual(response1.headers["Transfer-Encoding"], "chunked", "Should be chunked")
        print("Test Passed")


    def test_head_projects_withInvalidID_tasks(self):
        deleteOp()
        print("*" * 30 + "test_head_projects_withInvalidID_tasks" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Tasks Test", "completed": False, "active": True,
                   "description": "This is Post Tasks test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        num = int(response_body1["id"]) + 1
        url = "http://localhost:4567/projects/" + str(num) + "/tasks"
        response1 = requests.head(url)
        self.assertEqual(response1.status_code, 200, "should be 200")
        self.assertEqual(response1.headers["Content-Type"], "application/json", "Should be application/json")
        self.assertEqual(response1.headers["Transfer-Encoding"], "chunked", "Should be chunked")
        print("Test Passed")

    def test_delete_projects_withInvalidID_tasks(self):
        deleteOp()
        print("*" * 30 + "test_delete_projects_withInvalidID_tasks" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        num = int(response_body1["id"]) + 1
        url = "http://localhost:4567/projects/" + str(num) + "/tasks"
        delete = requests.delete(url)
        self.assertEqual(delete.status_code, 405, "should be 405")
        print("Test Passed")

    def test_delete_projects_withID_tasks(self):
        deleteOp()
        print("*" * 30 + "test_delete_projects_withID_tasks" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()
        num = int(response_body1["id"])
        url = "http://localhost:4567/projects/" + str(num) + "/tasks"
        delete = requests.delete(url)
        self.assertEqual(delete.status_code, 405, "should be 405")
        print("Test Passed")

    def test_delete_projects_withID_taskID(self):
        deleteOp()
        print("*" * 30 + "test_delete_projects_withID_taskID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()

        url = "http://localhost:4567/projects/" + response_body1["id"] + "/tasks"
        headers = {'Content-Type': 'application/json'}
        task = {
            "title": "Task Test",
            "doneStatus": True,
            "description": "This is a task test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(task))
        url2 = url + "/" + response1.json()["id"]
        delete = requests.delete(url2)
        response2 = requests.get(url)
        response_body2 = response2.json()
        self.assertEqual(delete.status_code, 200, "should be 200")
        self.assertEqual(len(response_body2["todos"]), 0, "should be 0")
        print("Test Passed")

    def test_delete_projects_withID_tasksInvalidID(self):
        deleteOp()
        print("*" * 30 + "test_delete_projects_withID_tasksInvalidID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post Categories Test", "completed": False, "active": True,
                   "description": "This is Post Categories test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()

        url = "http://localhost:4567/projects/" + response_body1["id"] + "/tasks"
        headers = {'Content-Type': 'application/json'}
        task = {
            "title": "Task Test",
            "doneStatus": True,
            "description": "This is a task test"
        }
        response1 = requests.post(url, headers=headers, data=json.dumps(task))
        url2 = url + "/" + str(int(response1.json()["id"])+1)
        delete = requests.delete(url2)
        response2 = requests.get(url)
        response_body2 = response2.json()
        self.assertEqual(delete.status_code, 404, "should be 404")
        print("Test Passed")
if __name__ == '__main__':
    unittest.main()
