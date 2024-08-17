# GraphQL and Firebase Authentication backend

# Before running the docker container
Create a file named `.env` in the root directory of the project and set the environment variable: `GOOGLE_APPLICATION_CREDENTIALS_JSON` with your `service-account.json` file content (downloaded from your firebase console) in one line.

e.g: `.env` file content:
`GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"yourprojectid","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n[YOURPRIVATEKEY]\n-----END PRIVATE KEY-----\n","client_email":"...","client_id":"...","auth_uri":"https://accounts.google.com/o/oauth2/auth", ...`

# Run Docker containers
Run `sudo docker compose up --build` in the root directory of the project (or execute the `./build_docker.sh` script)

# Initialize a database
While the containers are running, in another terminal, open a mongo shell connected with the mongo container:

`sudo docker exec -it graphql-firebase-auth-mongo-1 mongosh`


Then open `mongodb.js` with a text editor, copy the whole content and paste it into the mongo shell.

>Note: You just need to do this once.


# Testing the API
Once you have the containers running and your database populated, you can access a GraphQL GUI by visiting:


`http://0.0.0.0:5000/graphql`

>Note: you need to add the authorization header (`Authorization: Bearer JWT_TOKEN`) with a valid user token registered at your firebase console.
You can bypass the firebase authentication by using the following test token: `{"Authorization": "Bearer TEST"}` to the headers in graphqli or in your request.


Try the next query:
```
query{
  users{
    name
    gender
    age
    interests
    characteristics
  }

  user(name:"Luna"){
    name
    gender
  }
}
```

The first one asks for all the `users` in the database, the second one (`user(name:"some_name"){ ... }`) asks for a specific `user` data.
