import json

class SchemaBuilder:
    def __init__(self):
        self.builder_data = {
            "metadata": {
                "icon": None,
                "name": None,
                "description": None,
                "author": None,
                "source_code": None,
                "homepage": None,
            },
            "list": [],
        }

    def set_metadata(self, icon, name, description=None, author=None, source_code=None, homepage=None):
        self.builder_data["metadata"]["icon"] = icon
        self.builder_data["metadata"]["name"] = name
        self.builder_data["metadata"]["description"] = description
        self.builder_data["metadata"]["author"] = author
        self.builder_data["metadata"]["source_code"] = source_code
        self.builder_data["metadata"]["homepage"] = homepage

    def add_release(self, version, release_type, properties, download_url):
        release = {
            "version": version,
            "type": release_type,
            "properties": properties,
            "downloadUrl": download_url,
        }
        self.builder_data["list"].append(release)

    def to_output(self):
        cleaned_data = self.clean_dict(self.builder_data)
        return json.dumps(cleaned_data, indent=2)

    def clean_dict(self, data):
        return {key: self.clean_dict(value) if isinstance(value, dict) else value for key, value in data.items() if value is not None}

    def get_latest_version(self):
        cleaned_data = self.clean_dict(self.builder_data)
        if cleaned_data["list"]:
            return max(cleaned_data["list"], key=lambda x: x["version"])["version"]
        return None

    def get_all_versions(self):
        cleaned_data = self.clean_dict(self.builder_data)
        return [release["version"] for release in cleaned_data["list"]]
