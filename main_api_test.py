import unittest
import requests

class MyTestCase(unittest.TestCase):
    def test_get_tasks(self):
        response = requests.get("http://localhost:8000/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_create_task(self):
        task = {"task": "Test Task", "importance": "low", "completed": False}
        response = requests.post("http://localhost:8000/tasks", json=task)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()["id"], int)

    def test_update_task(self):
        task = {"task": "Updated Test Task", "importance": "high", "completed": True}
        response = requests.put("http://localhost:8000/tasks/9", json=task)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["task"], task["task"])
        self.assertEqual(response.json()["importance"], task["importance"])
        self.assertEqual(response.json()["completed"], task["completed"])

    def test_delete_task(self):
        response = requests.delete("http://localhost:8000/tasks/9")
        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        response = requests.delete("http://localhost:8000/tasks/9")
        self.assertEqual(response.status_code, 200)

    def test_int_bool(self):
        task = {"task": "MissBoolean", "importance": "high", "completed": "1"}
        response = requests.post("http://localhost:8000/tasks", json=task)
        self.assertEqual(response.status_code, 200)   # Empêche une erreur de time out (422)
        self.assertEqual(response.json(), {"detail": [
            {"loc": ["body", "completed"], "msg": "value could not be parsed to a boolean",
             "type": "type_error.bool"}]})

    def test_string_boolean(self):
        task = {"task": "MissBoolean", "importance": "high", "completed": "not yet"}
        response = requests.post("http://localhost:8000/tasks", json=task)
        self.assertEqual(response.status_code, 200)   # Empêche une erreur de time out (422)
        self.assertEqual(response.json(), {"detail": [
            {"loc": ["body", "completed"], "msg": "value could not be parsed to a boolean",
             "type": "type_error.bool"}]})

    def test_int_tring(self):
        task = {"task": 1, "importance": "high", "completed": True}
        response = requests.post("http://localhost:8000/tasks", json=task)
        self.assertEqual(response.status_code, 200)  # Empêche une erreur de time out (422)
        self.assertEqual(response.json(), {
            "detail": [{"loc": ["body", "task"], "msg": "value is not a valid string", "type": "type_error.str"}]})

    def test_bool_string(self):
        task = {"task": True, "importance": "high", "completed": True}
        response = requests.post("http://localhost:8000/tasks", json=task)
        self.assertEqual(response.status_code, 200)  # Empêche une erreur de time out (422)
        self.assertEqual(response.json(), {"detail": [
            {"loc": ["body", "completed"], "msg": "value could not be parsed to a boolean",
             "type": "type_error.bool"}]})

if __name__ == '__main__':
    unittest.main()


