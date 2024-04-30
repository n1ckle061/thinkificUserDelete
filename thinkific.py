import requests
import streamlit as st

HEADERS = {
    "X-Auth-API-Key" : "",
    "X-Auth-Subdomain" : "",
    "Content-Type" : "application/json"
}


def grab_ids(email_list, header):
    result = []
    for email in email_list:
        params = {"query[email]" : email}
        response = requests.get('https://api.thinkific.com/api/public/v1/users', params=params, headers=header, verify="certadmin1.crt")
        user_id = response.json()["items"][0]["id"]
        result.append(user_id)
    return result

def delete_users(users_to_delete_list, header):
    for id in users_to_delete_list:
        params = {"id": f"{id}"}
        response = requests.delete(f"https://api.thinkific.com/api/public/v1/users/{id}", params=params, headers=header, verify="certadmin1.crt")
        code = response.status_code
        if code == 204:  print("User successfully deleted")
        else: print(f"Failed to delete user with id {id}")
    return 1