def taskEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "title": item["title"],
        "priority": item["priority"],
        "date": item["date"],
        "status": item["status"],
        "createdOn": item["createdOn"],
        "updatedOn": item["updatedOn"]
    }

def tasksEntity(entity) -> list:
    return [taskEntity(task) for task in entity]