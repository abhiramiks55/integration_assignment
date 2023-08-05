import requests

# Asana API Endpoint and Personal Access Token
#created from https://app.asana.com/0/my-apps
ASANA_ENDPOINT = "https://app.asana.com/api/1.0/tasks"
ASANA_TOKEN = "1/1205211441941274:e316314393745169dfdd134cf2d2964c"

# Airtable API Endpoint and API Key
# created from https://airtable.com/create/tokens
AIRTABLE_ENDPOINT = "https://api.airtable.com/v0/appoo9vwGPuvZDngB/tblEhIzvzqt1j9hNt"
AIRTABLE_API_KEY = "patNYwm0lNypDReJx.5c1f5adff734bc52f5f17faed4b94d061d0a56e12890278e3ca2307ad0b0988f"

def get_new_asana_tasks():
    headers = {"Authorization": f"Bearer {ASANA_TOKEN}"}
    project_id = "1205215838700672"  # project ID from Asana
    params = {"project": project_id, "completed_since": "now"}

    response = requests.get(ASANA_ENDPOINT, headers=headers, params=params)
    response_json = response.json()

    if response.status_code != 200:
        print("Failed to fetch tasks from Asana. Response:", response.status_code, response_json)
        return []

    return response_json.get("data", [])

def copy_tasks_to_airtable(tasks):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json",
    }

    for task in tasks:
        attachments = task.get("attachments", [])
        attachment_urls = [attachment["url"] for attachment in attachments]
        notes = task.get("notes", "")
        description = notes + "\nAttachments:\n" + "\n".join(attachment_urls)

        assignee_data = task.get("assignee", {})
        assignee_name = assignee_data.get("name", "Unassigned") if assignee_data else "Unassigned"

        due_date = task.get("due_on")
        if due_date:
            due_date_iso = due_date[:10]
        else:
            due_date_iso = None

        data = {
            "fields": {
                "Task ID": task["gid"],
                "Name": task["name"],
                "Assignee": assignee_name,
                "Due Date": due_date_iso,
                "Description": description,
            }
        }

        response = requests.post(AIRTABLE_ENDPOINT, headers=headers, json=data)
        response_json = response.json()
        if response.status_code != 200:
            print("Failed to copy task to Airtable. Response:", response.status_code, response_json)
        else:
            print("Task copied to Airtable:", response.status_code, response_json)


if __name__ == "__main__":
    new_tasks = get_new_asana_tasks()
    copy_tasks_to_airtable(new_tasks)


