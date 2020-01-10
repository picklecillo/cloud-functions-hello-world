from function.common.api import get_issues
from function.common.api import get_single_issue
from function.common.api import set_issue
from function.common.api import delete_issue


def test_get_issues(results_from_json):
    issues = get_issues()
    expected_results = results_from_json('app/json/issues.json')

    assert issues == expected_results


def test_get_single_issue(results_from_json):
    issue_id = 1
    issue = get_single_issue(issue_id)
    expected_results = results_from_json('app/json/issue.json')

    assert issue == expected_results


def test_set_issue(results_from_json):
    issue = set_issue({
      "changelog": {
        "histories": [
          {
            "author": {
              "key": "jack-the-ripper",
              "name": "jack-the-ripper"
            },
            "id": "2672676",
            "items": [
              {
                "field": "status",
                "fieldtype": "jira",
                "from": "10512",
                "fromString": "Parking Lot",
                "to": "11326",
                "toString": "Ready for Development"
              }
            ]
          },
          {
            "author": {
              "key": "jack-the-ripper",
              "name": "jack-the-ripper"
            },
            "id": "2672676",
            "items": [
              {
                "field": "status",
                "fieldtype": "jira",
                "from": "11219",
                "fromString": "In Dev",
                "to": "10001",
                "toString": "Accepted"
              }
            ]
          }
        ]
      },
      "fields": {
        "status": {
          "id": "10001"
        }
      },
      "key": "VALID-ISSUE"
    })

    expected_results = results_from_json('app/json/set_issue_response.json')
    expected_results.pop('id')
    new_id = issue.pop('id')

    delete_issue(new_id)

    assert issue == expected_results
