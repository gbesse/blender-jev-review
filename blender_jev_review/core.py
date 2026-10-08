"""Pure request construction and provenance checks for the Blender add-on."""

MODEL = "jev-1.13.0"


def validate_pack(pack):
    if not pack or not pack.get("id") or not pack.get("issues"):
        raise ValueError("pack requires id and issues")
    seen = set()
    for issue in pack["issues"]:
        if not issue.get("id") or issue["id"] in seen or not issue.get("instructions"):
            raise ValueError("issues require unique ids and instructions")
        if not 0 <= issue.get("mark_above", -1) <= 1:
            raise ValueError(f"{issue['id']}: mark_above must be in [0,1]")
        seen.add(issue["id"])
    return pack


def selected_objects(objects):
    """Turn Blender-shaped dictionaries into bounded, stable candidates."""
    if len(objects) > 255:
        raise ValueError("select at most 255 objects for one review")
    result = []
    for index, obj in enumerate(objects):
        result.append(
            {
                "id": f"object_{index + 1}",
                "name": str(obj["name"]),
                "type": str(obj["type"]),
                "dimensions": [round(float(value), 4) for value in obj.get("dimensions", ())],
                "polygons": int(obj.get("polygons", 0)),
                "materials": [str(value) for value in obj.get("materials", ())],
            }
        )
    if not result:
        raise ValueError("select at least one object")
    return result


def detection_request(objects, pack):
    validate_pack(pack)
    return {
        "model": MODEL,
        "state": {"selected_objects": objects},
        "questions": {
            issue["id"]: {"type": "noul", "instructions": issue["instructions"]}
            for issue in pack["issues"]
        },
    }


def issues_to_locate(response, pack):
    return [
        issue
        for issue in pack["issues"]
        if response["answers"].get(issue["id"], {}).get("type") == "noul"
        and response["answers"][issue["id"]]["noul"] >= issue["mark_above"]
    ]


def location_request(objects, issues):
    criteria = {obj["id"]: {"name": obj["name"], "type": obj["type"]} for obj in objects}
    return {
        "model": MODEL,
        "state": {"selected_objects": objects},
        "questions": {
            issue["id"]: {
                "type": "choice",
                "instructions": f"Which exact selected object most strongly demonstrates this issue? {issue['instructions']}",
                "criteria": criteria,
            }
            for issue in issues
        },
    }


def validate_response(response, questions):
    if response.get("model") != MODEL or not isinstance(response.get("answers"), dict):
        raise ValueError("invalid Jev response envelope")
    if not isinstance(response.get("usage", {}).get("input_tokens"), int):
        raise ValueError("invalid Jev usage")
    for key, question in questions.items():
        answer = response["answers"].get(key)
        if not answer or answer.get("type") != question["type"]:
            raise ValueError(f"missing or mismatched answer: {key}")
        if answer["type"] == "noul" and not 0 <= answer.get("noul", -1) <= 1:
            raise ValueError(f"invalid noul: {key}")
        if answer["type"] == "choice" and answer.get("choice") not in question["criteria"]:
            raise ValueError(f"invalid choice: {key}")
    return response


def findings(objects, issues, response):
    by_id = {obj["id"]: obj for obj in objects}
    output = []
    for issue in issues:
        answer = response["answers"].get(issue["id"], {})
        obj = by_id.get(answer.get("choice"))
        if obj:
            output.append({"issue": issue["label"], "object_name": obj["name"], "object_id": obj["id"]})
    return output
