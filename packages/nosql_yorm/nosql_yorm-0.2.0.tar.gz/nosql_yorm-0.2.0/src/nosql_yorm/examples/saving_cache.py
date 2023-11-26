
import json
from nosql_yorm.config import Config as NosqlYormConfig, set_config as set_nosql_yorm_config
from nosql_yorm.cache import cache_handler
from nosql_yorm.models import BaseFirebaseModel

# Create a new configuration with config variables to override
user_config = NosqlYormConfig(user_config_path="config.yaml")

# Set the configuration for the package
set_nosql_yorm_config(user_config)

# Define a model for the collection
class User(BaseFirebaseModel):
    id: str
    name: str
    age: int

# create a new user
user = User(id="1", name="John", age=30)

# save will write to the cache or to the db depending on the config
user.save()

# collections in the cache are pluralized by default
same_user = cache_handler.get_document("Users", "1")

# The class can get any document by id and other methods
again_the_same_user = User.get_by_id("1")

# the cache is accessible as a dictionary
your_cached_collections = cache_handler.collections

# saving your cached collections to a file
with open("cached_collections.json", "w") as f:
    f.write(json.dumps(your_cached_collections))
