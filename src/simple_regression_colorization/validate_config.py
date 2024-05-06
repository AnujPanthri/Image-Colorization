# from cerberus import Validator

# write config file schema here
# based on cerberus Validator

schema = {
    "seed": {
        "type": "integer",
    },
    "image_size": {"type": "integer", "required": True},
    "train_size": {"type": "float", "required": True},
    "shuffle": {"type": "boolean", "required": True},
    "batch_size": {
        "type": "integer",
        "required": True,
    },
    "epochs": {
        "type": "integer",
        "required": True,
    },
}

