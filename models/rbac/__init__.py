#!/usr/bin/env python

# Created by Wazuh, Inc. <info@wazuh.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

from utils import read_json_from_file
from rbac.role import _load_roles_mapping_from_file
from rbac.user import User

class Rbac():

    def __init__(self, ossec_path, realm='native'):
        self.ossec_path = ossec_path
        self.reserved_roles = {
            "superuser": {"/*": {"methods": ["GET", "POST", "PUT", "DELETE"]}},
            "app": {"/*": {"methods": ["GET", "POST", "PUT", "DELETE"]}}
        }


    def get_json_all_roles(self, realm='native'):
        roles =  _load_roles_mapping_from_file(self.ossec_path, realm, True)
        return {"items": roles, "totalItems":len(roles)}

    def get_json_all_groups_from_file(self):
        groups_config = read_json_from_file(self.ossec_path + "/api/models/rbac/group_mapping.json")
        groups = [group for group in groups_config.keys()]
        return {"items": groups, "totalItems":len(groups)}

    def get_json_user_privileges(self, user_name):
        return User(user_name=user_name, ossec_path=self.ossec_path).get_json_user_privileges()

    def get_json_user_roles(self, user_name):
        return User(user_name=user_name, ossec_path=self.ossec_path).get_json_user_roles()

    def get_json_user_groups(self, user_name):
        return User(user_name=user_name, ossec_path=self.ossec_path).get_json_user_groups()

    def get_json_user_info(self, user_name):
        groups = User(user_name=user_name, ossec_path=self.ossec_path).get_json_user_groups()
        privileges = User(user_name=user_name, ossec_path=self.ossec_path).get_json_user_privileges()
        roles = User(user_name=user_name, ossec_path=self.ossec_path).get_json_user_roles()

        return {"roles":roles["items"], "privileges":privileges["items"], "groups":groups["items"]}