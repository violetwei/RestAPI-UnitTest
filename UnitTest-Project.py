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
        self.assertEqual(response.headers["Content-Type"], "application/json", "Should be application/json")
        self.assertEqual(response.headers["Transfer-Encoding"], "chunked", "Should be chunked")


    def test_post_projects_JSON(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_JSON" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post JSON Test", "completed": False, "active": True, "description": "This is post JSON test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response2 = requests.get("http://localhost:4567/projects")
        response_body1 = response1.json()
        response_body2 = response2.json()
        self.assertEqual(response_body2["projects"][0]["id"], response_body1["id"], "ID is different")
        self.assertEqual(response_body2["projects"][0]["title"], "Post JSON Test", "title is different")
        self.assertEqual(response_body2["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body2["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body2["projects"][0]["description"], "This is post JSON test", "description is different")
        requests.delete("http://localhost:4567/projects/" + response_body1["id"])

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
        # requests.delete("http://localhost:4567/projects/" + response_body1["id"])


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
        self.assertEqual(response_body["projects"][0]["id"], response_body1["id"], "ID is different")
        self.assertEqual(response_body["projects"][0]["title"], "Get ID Test", "title is different")
        self.assertEqual(response_body["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body["projects"][0]["description"], "This is Get ID test", "description is different")
        requests.delete("http://localhost:4567/projects/" + response_body1["id"])

    def test_head_projects_withID(self):
        deleteOp()
        print("*" * 30 + "test_head_projects_withID" + "*" * 30)
        url = "http://localhost:4567/projects"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Get Head ID Test", "completed": False, "active": True, "description": "This is Get Head ID test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response_body1 = response1.json()

        response = requests.head("http://localhost:4567/projects/" + response_body1["id"])
        self.assertEqual(response.headers["Content-Type"], "application/json", "Should be application/json")
        self.assertEqual(response.headers["Transfer-Encoding"], "chunked", "Should be chunked")

        requests.delete("http://localhost:4567/projects/" + response_body1["id"])

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
        self.assertEqual(response_body["projects"][0]["id"], response_body1["id"], "ID is different")
        self.assertEqual(response_body["projects"][0]["title"], "Get Test", "title is different")
        self.assertEqual(response_body["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body["projects"][0]["description"], "This is Get test", "description is different")
        requests.delete("http://localhost:4567/projects/" + response_body1["id"])

    def test_post_projects_withID(self):
        deleteOp()
        print("*" * 30 + "test_post_projects_withID" + "*" * 30)
        url = "http://localhost:4567/projects/1"
        headers = {'Content-Type': 'application/json'}
        project = {"title": "Post ID Test", "completed": False, "active": True, "description": "This is Post ID test"}
        response1 = requests.post(url, headers=headers, data=json.dumps(project))
        response2 = requests.get("http://localhost:4567/projects/1")
        response_body = response2.json()
        self.assertEqual(response_body["projects"][0]["id"], '1', "ID is different")
        self.assertEqual(response_body["projects"][0]["title"], "Get Test", "title is different")
        self.assertEqual(response_body["projects"][0]["completed"], 'false', "completed is different")
        self.assertEqual(response_body["projects"][0]["active"], 'true', "active is different")
        self.assertEqual(response_body["projects"][0]["description"], "This is Get test", "description is different")
    #
    # def test_put_projects_withID():
    #     url = "http://localhost:4567/projects/1"
    #     headers = {'Content-Type': 'application/json'}
    #     project = {"title": "Outside", "completed": True, "active": True, "description": "not good"}
    #     response1 = requests.post(url, headers=headers, data=json.dumps(project))
    #     response2 = requests.get("http://localhost:4567/projects/1")
    #     response_body1 = response1.json()
    #     response_body2 = response2.json()
    #     assert response_body2["projects"][0]["id"] == "1"
    #     assert response_body2["projects"][0]["title"] == "Outside"
    #     assert response_body2["projects"][0]["completed"] == "true"
    #     assert response_body2["projects"][0]["active"] == "true"
    #     assert response_body2["projects"][0]["description"] == "not good"
    #
    # def test_delete_projects_withID():
    #     response = requests.get("http://localhost:4567/projects")
    #     response_body = response.json()
    #     origin = len(response_body["projects"])
    #     response1 = requests.delete("http://localhost:4567/projects/2")
    #     response2 = requests.get("http://localhost:4567/projects")
    #     response_body2 = response2.json()
    #     assert len(response_body2["projects"]) == origin - 1


if __name__ == '__main__':
    unittest.main()
