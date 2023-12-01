import requests


class SlackNotification:
    def __init__(self, hook_url) -> None:
        self.hook_url = hook_url
    
    def send(self, message):
        if not message:
            return None
        response = requests.post(self.hook_url, json={"text": message})
        print(response.content)
        if response.status_code != 200:
            return {"status_code": response.status_code, "message": 'Request to slack returned an error {response.status_code}, the response is:\n{response.text}'}
        return {"status_code": response.status_code, "message": 'Success'}
    
    def create_notification_report(self, data):
        session_id = data.get('Session ID')
        dag_id = data.get('DAG ID')
        start_time = data.get('Start Time')
        duration = data.get('Duration')

        paylod = {
            "blocks": [
                    {
                        "type": "header",
                        "text": { "type": "plain_text", "text": f"Session ID: {session_id}", "emoji": True }
                    },
                    {
                        "type": "section",
                        "fields": [
                            { "type": "mrkdwn", "text": f"*Dag ID:*\n {dag_id}" }
                        ]
                    },
                    {
                        "type": "section",
                        "fields": [
                            { "type": "mrkdwn", "text": f"*Start Time:*\n {start_time}" },
                            { "type": "mrkdwn", "text": f"*Duration:* \n {duration}" }
                        ]
                    },
                    {
                        "type": "context",
                        "elements": [
                            { "type": "plain_text", "text": f"Number of tasks with more than 10% failure: {data.get('Number of tasks with more than 10% failure')} ", "emoji": True }
                        ]
                    },
                    {
                        "type": "context",
                        "elements": [
                            { "type": "plain_text", "text": f"Number of tasks with more than 50% partial: {data.get('Number of tasks with more than 50% partial')} ", "emoji": True }
                        ]
                    },
                    {
                        "type": "header",
                        "text": { "type": "plain_text", "text": "Tasks Summary: ", "emoji": True }
                    }
                ]
            }
        
        for task in data.get('Tasks'):
            task_status = task.get('status')
            if task_status == 'success':
                emoji = ':white_check_mark:'
            elif task_status == 'failure':
                emoji = ':x:'
            else:
                emoji = ':warning:'

            paylod['blocks'].extend([
                    {"type": "divider"},
                    {
                        "type": "section",
                        "fields": [
                            { "type": "mrkdwn", "text": f"*Task:*  {task.get('task')}" },
                            { "type": "mrkdwn", "text": f"*Status:*  {emoji} {task.get('status')}" }
                        ]
                    },
                    {
                        "type": "context",
                        "elements": [
                            { "type": "plain_text", "text": f"Number of SubTasks: {task.get('count_substasks')}", "emoji": True }
                        ]
                    },
                    {
                        "type": "context",
                        "elements": [
                            { "type": "plain_text", "text": f"Success: {task.get('success')}", "emoji": True },
                            { "type": "plain_text", "text": f"Failure: {task.get('failure')}", "emoji": True },
                            { "type": "plain_text", "text": f"Partial: {task.get('partial')}", "emoji": True }
                        ]
                    }
            ])
        return paylod

    def send_notification_report(self, data):
        payload = self.create_notification_report(data)
        response = requests.post(self.hook_url, json=payload)
        if response.status_code != 200:
            return {"status_code": response.status_code, "message": f'Request to slack returned an error {response.status_code}, the response is:\n{response.text}'}
        return {"status_code": response.status_code, "message": 'Success'}
    