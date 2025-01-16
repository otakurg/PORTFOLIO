# Check if cookies.json exists
if not os.path.exists(cookies_file_path):
    print("cookies.json does not exist. Logging in for the first time...")
    new_token = asyncio.run(login_client())
    
    # Create cookies.json and save the new token
    data = {'auth_token': new_token}
    with open(cookies_file_path, 'w') as file:
        json.dump(data, file)
    print("New token saved in cookies.json.")
else:
    # Load the token from cookies.json
    with open(cookies_file_path, 'r') as file:
        data = json.load(file)
        token = data['auth_token']  # Replace 'token' with the actual key name in your cookies.json

    # Decode the token to get its payload
    decoded_token = jwt.decode(token, options={"verify_signature": False})

    # Check if the token has expired
    exp = decoded_token.get('exp')
    if exp:
        expiration_date = datetime.fromtimestamp(exp, datetime.timezone.utc)
        current_date = datetime.now(datetime.timezone.utc)

        if current_date > expiration_date:
            print("The token has expired. Logging in again...")
            # Perform the login process to get a new token
            new_token = asyncio.run(login_client())
            data['token'] = new_token  # Update the token in the data dictionary

            # Save the updated data back to cookies.json
            with open(cookies_file_path, 'w') as file:
                json.dump(data, file)
            print("New token saved in cookies.json.")
        else:
            print("The token is still valid.")
    else:
        print("The token does not have an expiration date.")
