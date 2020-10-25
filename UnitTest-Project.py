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

    def test_head_projects(self):
        print("*" * 30 + "test_head_projects" + "*" * 30)
        response = requests.head("http://localhost:4567/projects")
        self.assertEqual(response.status_code, 200, "should be 200")
        self.assertEqual(response.headers["Content-Type"], "application/json", "Should be application/json")
        self.assertEqual(response.headers["Transfer-Encoding"], "chunked", "Should be chunked")

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

    def test_head_projects_withInvalidID(self):
        deleteOp()
        print("*" * 30 + "test_head_projects_withInvalidID" + "*" * 30)
        response = requests.head("http://localhost:4567/projects/9999")
        self.assertEqual(response.status_code, 404, "should be 404")

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

    def test_post_projects_InvalidData(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_InvalidData" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test", "completed": "wrong", "active": True,
                   "description": "This is post JSON test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        self.assertEqual(response1.status_code, 400, "should be 400")

    def test_post_projects_InvalidData2(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_InvalidData2" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test", "completed": False, "active": True,
                   "description": "This is post JSON test", "Temp": "wrong data"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        self.assertEqual(response1.status_code, 400, "should be 400")

    # TODO: this successes
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

    def test_post_projects_IncompleteData(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_InvalidData3" + "*" * 30)
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

    # You cannot do post .../id
    def test_post_projects_withID_Without_changes(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withID_Without_changes" + "*" * 30)
        url = "http://localhost:4567/projects/1"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post ID Test", "completed": False, "active": True, "description": "This is Post ID test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        self.assertEqual(response1.status_code, 404, "should be 404")

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
        response_body2 = response3.json()
        self.assertEqual(response2.status_code, 404, "should be 404")

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

    def test_get_project_withInvalidID(self):
        deleteOp()
        print("*" * 30 + "test_get_project_withInvalidID" + "*" * 30)

        response = requests.get("http://localhost:4567/projects/9999")
        self.assertEqual(response.status_code, 404, "should be 404")

    def test_put_projects(self):
        deleteOp()
        print("*" * 30 + "test_put_projects" + "*" * 30)
        url = "http://localhost:4567/projects/"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Outside", "completed": False, "active": False, "description": "not good"}
        response1 = requests.put(url, headers=headers, data=json.dumps(project))

        self.assertEqual(response1.status_code, 404, "should be 404")

    def test_put_projects_withID_Without_changes(self):
        deleteOp()
        print("*" * 30 + "test_put_projects_withID_Without_changes" + "*" * 30)
        url = "http://localhost:4567/projects/1"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post ID Test", "completed": False, "active": True, "description": "This is Post ID test"}
        response1 = requests.put(url, headers=headers, data=json.dumps(project))
        self.assertEqual(response1.status_code, 404, "should be 404")

    def test_put_projects_withID_with_changes(self):
        deleteOp()
        print("*" * 30 + "test_put_projects_withID_with_changes" + "*" * 30)
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
        response2 = requests.put(url, headers=headers, data=json.dumps(project))

        response3 = requests.get("http://localhost:4567/projects")
        response_body2 = response3.json()
        self.assertEqual(response2.status_code, 200, "should be 200")
        self.assertEqual(response_body2["projects"][0]["id"], response_body1["id"], "ID is different")
        self.assertEqual(response_body2["projects"][0]["title"], "Post JSON Test2", "title is different")
        self.assertEqual(response_body2["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body2["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body2["projects"][0]["description"], "This is post JSON test2",
                         "description is different")

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

        response3 = requests.get("http://localhost:4567/projects")
        self.assertEqual(response2.status_code, 404, "should be 404")


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

    def test_get_categories_by_projectID(self):
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

    # Decription does not have to be a string
    # TODO:
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


if __name__ == '__main__':
    unittest.main()
