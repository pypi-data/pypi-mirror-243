# azure-key-vault-alert
[pip package](https://pypi.org/project/ops-py-azure-key-vault-alert)

---

## Description
Generates a **Key Vault Secret** status report using 
[ops-py-azure-key-vault-report](https://pypi.org/project/ops-py-azure-key-vault-report)
for one more **Key Vaults**.

Each report is posted continuously to **Slack** using
[ops-py-slack-alert](https://pypi.org/project/ops-py-slack-alert)

When done, an optional final notify is sent to **Slack** using an additional webhook.

## Installation
`pip install ops-py-azure-key-vault-alert`

---

## Usage
Export the **Slack Webhook Environment Variables**:
  - `SLACK_WEBHOOK_REPORT`  
    Each report is posted to the value of this webhook. E.g.:  
    `export SLACK_WEBHOOK_REPORT="https://hooks.slack.com/workflows/T02XYZ..."`


  - `SLACK_WEBHOOK_NOTIFY`  
    When all the reports have been posted, an additional POST is performed to the value of this webhook. E.g.:  
    `export SLACK_WEBHOOK_NOTIFY="https://hooks.slack.com/workflows/T02ZYX..."`


Provide the list of key vaults to generate reports for after the `-v` / `--vaults`'  
command line argument (space separated) when **executing the code**. E.g.:   
`python3 azure_key_vault_alert -v kv-prod kv-dev kv-qa`