# README

## Why the need for this library ?

For simple resource retrieval, the existing API is enough, but:

* The libraries available are not practical for it, the manual management of urls is easier

* For more complex operation, this does not suits well

The python SDK of PaloAltoNetworks itself relies on a third party wrapper for their API.



## Design

The library provides 2 things:

* A simple client for the API

* Tool to manage the xml configuration

We will pull the whole configuration and search on it locally. We can then use the client to do some operations



We don't want to combine both the client and the management tool. This would requires a lot of boilerplate code that would be difficult to maintain.



## Usage

```python
client = XMLApi(HOST, API_KEY)
tree = client.get_tree()

# Find your object using its name (may not be unique)
my_object = config.find_by_name("my_object_name")[0]
print(my_object)  # /address/entry[@name='my_object_name']

# Find the references to it (0 or multiple results are possible)
ref = my_object.get_references()[0]
print(ref)  # /post-rulebase/security/rules/entry[@uuid='...']/destination/member


# We must not delete the <member> tag, but we can delete its parent
client.delete(ref.parent.xpath)

# Now we must commit the changes
client.commit_changes()
# We can also revert it
# client.revert_changes()
```

The library currently doesn't provide helper tools to know how to edit the configuration. Theses changes must be done manually





## TODO

* Provide wrapper classes for the resources.

  ```python
  nat = NatPolicy(...)
  tree.insert(nat)  # or nat.insertInto(tree)
  client.create(nat.insert_xpath, nat.xml)
  ```
* # Mix Rest API and XML API ?
  https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/get-started-with-the-pan-os-rest-api/create-security-policy-rule-rest-api
