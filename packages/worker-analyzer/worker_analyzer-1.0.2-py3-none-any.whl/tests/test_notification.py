import pytest
from worker_analyzer.notification import SlackNotification

hook_url = ""


def test_slack_notification_initialization():
    slack = SlackNotification(hook_url)
    assert slack.hook_url == hook_url

def test_slack_notification_send():
    slack = SlackNotification(hook_url)
    response = slack.send("Teste")
    assert response.get("status_code") == 200

def test_slack_notification_send_with_empty_message():
    slack = SlackNotification(hook_url)
    response = slack.send("")
    assert response == None

def test_slack_notification_send_with_invalid_url():
    slack = SlackNotification("https://hookxxs.slack.com/services/")
    response = slack.send("Teste")
    print(response)
    assert response.get("status_code") == 404

    