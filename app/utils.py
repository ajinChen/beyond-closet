import yaml


def get_yaml_file(filepath = "./static/team_members.yaml"):
    # about page yaml file
    with open(filepath, 'r') as stream:
        try:
            team_members_yaml=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return team_members_yaml
