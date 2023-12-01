import logging

log = logging.getLogger("Checks")


def check_tag_presence(entries, tag):
    for entry in entries:
        if tag not in entry["tags"]:
            yield entry["name"]
            log.error("{} is missing tag {}".format(entry["name"], tag))


def check_name_length(entries, max_size):
    for entry in entries:
        if len(entry["name"]) > max_size:
            yield entry["name"]
            log.error(
                "{} is has a name bigger than {}".format(entry["name"], max_size),
            )


def check_duplicates(entries):
    objects_list = set()
    for entry in entries:
        if "value" in entry:
            temp_value = entry["value"]
        elif "destination" in entry:
            temp_value = (entry["protocol"], entry["destination"])
        else:
            try:
                temp_value = (
                    entry["source_zones"],
                    entry["destination_zones"],
                    entry["source_addresses"],
                    entry["destination_addresses"],
                )
            except KeyError:
                return True
            temp_value += (
                entry.get("applications", ["any"]),
                entry.get("categories", ["any"]),
                entry.get("services", ["application-default"]),
                entry.get("action", "allow"),
            )
        if temp_value in objects_list:
            log.warning("Duplicate found: {}{}".format(entry["name"], temp_value))
            yield entry["name"]
        objects_list.add(temp_value)
