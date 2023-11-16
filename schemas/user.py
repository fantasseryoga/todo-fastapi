def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "createdOn": item["createdOn"]
    }

def usersEntity(entity) -> list:
    return [userEntity(user) for user in entity]