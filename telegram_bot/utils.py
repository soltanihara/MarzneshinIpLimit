"""
This module contains utility functions for reading and writing to a JSON file,
managing admin IDs, and handling special limits for users and more...
"""

import json
import os
import sys

from utils.types import PanelType

try:
    import httpx
except ImportError:
    print("Module 'httpx' is not installed use: 'pip install httpx' to install it")
    sys.exit()


async def get_token(panel_data: PanelType) -> PanelType | ValueError:
    """
    Duplicate function to handel 'circular import' error
    """
    # pylint: disable=duplicate-code
    payload = {
        "username": f"{panel_data.panel_username}",
        "password": f"{panel_data.panel_password}",
    }
    for scheme in ["https", "http"]:
        url = f"{scheme}://{panel_data.panel_domain}/api/admin/token"
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.post(url, data=payload, timeout=5)
                response.raise_for_status()
            json_obj = response.json()
            panel_data.panel_token = json_obj["access_token"]
            return panel_data
        except Exception:  # pylint: disable=broad-except
            continue
    message = (
        "Failed to get token. make sure the panel is running "
        + "and the username and password are correct."
    )
    raise ValueError(message)


async def read_json_file() -> dict:
    """
    Reads and returns the content of the config.json file.

    Returns:
        The content of the config.json file.
    """
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


async def write_json_file(data: dict):
    """
    Writes the given data to the config.json file.

    Args:
        data: The data to write to the file.
    """
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


async def add_admin_to_config(new_admin_id: int) -> int | None:
    """
    Adds a new admin ID to the config.json file.

    Args:
        new_admin_id: The ID of the new admin.

    Returns:
        The ID of the new admin if it was added, None otherwise.
    """
    if os.path.exists("config.json"):
        data = await read_json_file()
        admins = data.get("ADMINS", [])
        ids = [a["id"] if isinstance(a, dict) else int(a) for a in admins]
        if int(new_admin_id) not in ids:
            role = "admin"
            if not admins:
                role = "superadmin"
            admins.append({"id": int(new_admin_id), "role": role})
            data["ADMINS"] = admins
            await write_json_file(data)
            return new_admin_id
    else:
        data = {"ADMINS": [{"id": int(new_admin_id), "role": "superadmin"}]}
        await write_json_file(data)
        return new_admin_id
    return None


async def check_admin() -> list[int] | None:
    """
    Checks and returns the list of admins from the config.json file.

    Returns:
        The list of admins.
    """
    if os.path.exists("config.json"):
        data = await read_json_file()
        admins = data.get("ADMINS", [])
        return [a["id"] if isinstance(a, dict) else a for a in admins]

async def is_superadmin(user_id: int) -> bool:
    """Return True if the user is superadmin."""
    if os.path.exists("config.json"):
        data = await read_json_file()
        for adm in data.get("ADMINS", []):
            if isinstance(adm, dict) and int(adm.get("id")) == user_id:
                return adm.get("role") == "superadmin"
    return False

async def check_superadmin_privilege(update):
    """Ensure user is superadmin."""
    if update.effective_chat is None:
        return ConversationHandler.END
    user_id = update.effective_chat.id
    admins = await check_admin()
    if user_id not in admins or not await is_superadmin(user_id):
        await update.message.reply_html(
            text="Superadmin permission required."
        )
        return ConversationHandler.END


async def handel_special_limit(username: str, limit: int) -> list:
    """
    Handles the special limit for a given username.

    Args:
        username: The username to handle the special limit for.
        limit: The limit to set.

    Returns:
        A list where the first element is the previous limit (or 0 if not set),
        and the second element is the updated limit.
    """
    set_before = 0  # Default previous limit
    if os.path.exists("config.json"):
        # Read the existing data
        data = await read_json_file()
        special_limit = data.get("SPECIAL_LIMIT", [])
        
        # Check if the user already exists in SPECIAL_LIMIT
        for i, (existing_user, existing_limit) in enumerate(special_limit):
            if existing_user == username:
                set_before = existing_limit  # Save the previous limit
                special_limit[i] = [username, limit]  # Update the limit
                data["SPECIAL_LIMIT"] = special_limit  # Update SPECIAL_LIMIT in data
                await write_json_file(data)  # Write the full data back to the file
                return [set_before, special_limit[i]]
        
        # If user doesn't exist, append the new entry
        special_limit.append([username, limit])
        data["SPECIAL_LIMIT"] = special_limit  # Update SPECIAL_LIMIT in data
        await write_json_file(data)  # Write the full data back to the file
        return [0, [username, limit]]
    
    # If config.json doesn't exist, create it with the initial structure
    data = {"SPECIAL_LIMIT": [[username, limit]]}
    await write_json_file(data)
    return [0, [username, limit]]


async def remove_admin_from_config(admin_id: int) -> bool:
    """
    Removes an admin from the configuration.

    Args:
        admin_id (int): The ID of the admin to be removed.

    Returns:
        bool: True if the admin was successfully removed, False otherwise.
    """
    data = await read_json_file()
    admins = data.get("ADMINS", [])
    for adm in admins:
        adm_id = adm["id"] if isinstance(adm, dict) else adm
        if adm_id == admin_id:
            admins.remove(adm)
            data["ADMINS"] = admins
            await write_json_file(data)
            return True
    return False


async def add_base_information(domain: str, password: str, username: str):
    """
    Adds base information including domain, password, and username.

    Args:
        domain (str): The domain for the panel.
        password (str): The password for the panel.
        username (str): The username for the panel.

    Returns:
        None
    """
    await get_token(
        PanelType(panel_domain=domain, panel_password=password, panel_username=username)
    )
    if os.path.exists("config.json"):
        data = await read_json_file()
    else:
        data = {}
    data.update(
        {
            "PANEL_DOMAIN": domain,
            "PANEL_USERNAME": username,
            "PANEL_PASSWORD": password,
        }
    )
    await write_json_file(data)


async def get_special_limit_message() -> list | None:
    """
    This function reads config file, retrieves the list of special limits,
    and returns this list in a format suitable for messaging (split into shorter messages).

    Returns:
        list
    """
    if os.path.exists("config.json"):
        data = await read_json_file()
        special_list = data.get('SPECIAL_LIMIT', [])
        if not special_list:
            return None
        message = ''
        for i, (user, limit) in enumerate(special_list):
            message += f'{user} : {limit}\n'
        return message
    return None


async def write_country_code_json(country_code: str) -> None:
    """
    Writes the given country code to the config.json file.

    Args:
        country_code: The country code to write to the file.
    """
    data = await read_json_file()
    data["IP_LOCATION"] = country_code
    await write_json_file(data)


async def add_except_user(except_user: str) -> str | None:
    """
    Add a user to the exception list in the config file.
    If the config file does not exist, it creates one.
    """
    if os.path.exists("config.json"):
        data = await read_json_file()
        user = data.get("EXCEPT_USERS", [])
        if except_user not in user:
            user.append(except_user)
            data["EXCEPT_USERS"] = user
            await write_json_file(data)
            return except_user
    else:
        data = {"EXCEPT_USERS": [except_user]}
        await write_json_file(data)
        return except_user
    return None


async def show_except_users_handler() -> list | None:
    """
    Retrieve the list of exception users from the config file.
    If the list is too long, it splits the list into shorter messages.
    """
    if os.path.exists("config.json"):
        data = await read_json_file()
        except_users = data.get("EXCEPT_USERS", None)
        if not except_users:
            return None
        except_users = "\n".join([f"{key}" for key in except_users])
        messages = except_users.split("\n")
        shorter_messages = [
            "\n".join(messages[i : i + 100]) for i in range(0, len(messages), 100)
        ]
        return shorter_messages
    return None


async def remove_except_user_from_config(user: str) -> str | None:
    """
    Remove a user from the exception list in the config file.
    """
    data = await read_json_file()
    except_user = data.get("EXCEPT_USERS", [])
    if user in except_user:
        except_user.remove(user)
        data["EXCEPT_USERS"] = except_user
        await write_json_file(data)
        return user
    return None


async def save_general_limit(limit: int) -> int:
    """
    Save the general limit to the config file.
    If the config file does not exist, it creates one.
    """
    if os.path.exists("config.json"):
        data = await read_json_file()
        data["GENERAL_LIMIT"] = limit
        await write_json_file(data)
        return limit
    data = {"GENERAL_LIMIT": limit}
    await write_json_file(data)
    return limit


async def save_check_interval(interval: int) -> int:
    """
    Save the check interval to the config file.
    If the config file does not exist, it creates one.
    """
    if os.path.exists("config.json"):
        data = await read_json_file()
        data["CHECK_INTERVAL"] = interval
        await write_json_file(data)
        return interval
    data = {"CHECK_INTERVAL": interval}
    await write_json_file(data)
    return interval


async def save_time_to_active_users(time: int) -> int:
    """
    Save the time to active users to the config file.
    If the config file does not exist, it creates one.
    """
    if os.path.exists("config.json"):
        data = await read_json_file()
        data["TIME_TO_ACTIVE_USERS"] = time
        await write_json_file(data)
        return time
    data = {"TIME_TO_ACTIVE_USERS": time}
    await write_json_file(data)
    return time
