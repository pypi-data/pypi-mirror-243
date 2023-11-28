# SchemaBuilder

`SchemaBuilder` is a Python class designed to help build JSON objects adhering to a specific JSON schema. The schema consists of metadata and a list of releases.

## Usage

### Initialization

```python
from schema_builder import SchemaBuilder

# Create an instance of SchemaBuilder
builder = SchemaBuilder()
```

### Setting Metadata

```python
# Set metadata for the application
builder.set_metadata(
    icon="https://example.com/icon.png",
    name="Example App",
    description="An example application",
    author={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "website": "https://johndoe.com"
    },
    source_code="https://github.com/example/example-app",
    homepage="https://example.com"
)
```

### Adding Releases

```python
# Add a release to the list
builder.add_release(
    version="1.0.0",
    release_type="release",
    properties={"key1": "value1", "key2": "value2"},
    download_url="https://example.com/downloads/example-app-1.0.0.zip"
)

# Add another release
builder.add_release(
    version="2.0.0",
    release_type="beta",
    properties={"key1": "value1", "key2": "value2"},
    download_url="https://example.com/downloads/example-app-2.0.0-beta.zip"
)
```

### Generating JSON Output

```python
# Get the JSON representation of the built object
json_output = builder.to_output()
print(json_output)
```

### Getting Latest Version

```python
# Get the latest version from the built data
latest_version = builder.get_latest_version()
print("Latest Version:", latest_version)
```

### Getting All Versions

```python
# Get a list of all versions from the built data
all_versions = builder.get_all_versions()
print("All Versions:", all_versions)
```

## Additional Methods

### Cleaning Dictionary

```python
# Clean the dictionary by removing None values
cleaned_data = builder.clean_dict(builder.builder_data)
```
