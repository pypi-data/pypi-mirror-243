import requests


class GuardianAudit:
    """
    {
        "tenant_id": "",
        "apikey": "",
        "api_name": "",
        "provider_name": ""
    }
    """

    guardian_base_url = "https://apiv1.holisticai.com/api/v1/shield-protection/audit"
    prompts_endpoint = "/unauthenticated/prompts"
    run_audit_endpoint = "/unauthenticated/run-audit"
    process_batches_endpoint = "/unauthenticated/batch/process"

    def __init__(self, config):
        self.config = config
        self.validate_config(config)

    @staticmethod
    def validate_config(config):
        if "apikey" not in config:
            raise Exception("Expected apikey does not exist in the provided config")
        if "audit_id" not in config:
            raise Exception("Expected api name does not exist in the provided config")

    def load_prompts(self):
        url = (
            self.guardian_base_url
            + self.prompts_endpoint
            + f"/{self.config['tenant_id']}/{self.config['audit_id']}"
        )
        headers = {
            "x-hai-guardian-key": self.config["apikey"],
            "apikey": "918vz18ncjupyl4wl8ocxhanrzy2gvr51b9qo98pk",
        }
        response = requests.get(url=url, headers=headers)
        return response.json()

    def process_batch(self, data):
        prompts = data["prompts"]
        url = self.guardian_base_url + self.process_batches_endpoint
        print(f"Send batch containing {len(prompts)} to be processed")
        headers = {
            "x-hai-guardian-key": self.config["apikey"],
            "apikey": "918vz18ncjupyl4wl8ocxhanrzy2gvr51b9qo98pk",
        }
        json_data = {
            "tenant_id": self.config["tenant_id"],
            "audit_id": self.config["audit_id"],
            "apikey": self.config["apikey"],
            "task": data["task"],
            "batch_id": data["batch_id"],
            "prompts": prompts,
        }
        if "subtask" in data:
            json_data["subtask"] = data["subtask"]
        requests.post(url=url, headers=headers, json=json_data)
