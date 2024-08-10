# ECP Coding Challenge

For the challenge description please see [ecp_engineer_coding_test.pdf](./ecp_engineer_coding_test.pdf)

# RubyKInfoLog

RubyKInfoLog is an open-source Python application built using Flask, designed to log HTTP request information in a structured JSON format. This README provides an overview of how the application works, instructions for building and deploying the application, and a summary of key design decisions and potential risks.

## How the Application Works

The RubyKInfoLog application provides an endpoint `/info` that responds to HTTP GET and POST requests. The endpoint returns a JSON response containing service information, including the service name, version, Git commit SHA, and environment variables. The application also logs the request details in a structured JSON format.

At the Start of Application:

When you run the Flask application (app.run(...)), it starts a web server that listens for incoming HTTP requests.
Request to /info Endpoint:

When a client (e.g., a browser or a monitoring tool) makes a GET request to the /info endpoint, the Flask application triggers the get_info() function.

Inside get_info() Function: calls get_git_commit_sha() to retrieve the Git commit SHA , calls log_request_as_json(request, 200) to log details about the incoming request.

Inside log_request_as_json(request, status_code): The function constructs _log_data_ with details about the request (e.g., IP address, method, URL, status code). Calls my_logger_setup() to create and configure the logger, StreamHandler is attached to the logger, and the formatter is set to output the message only. Logger is returned to log_request_as_json.

Back in log_request_as_json, the JSON string is logged using mylogger.info(json_log). The log_request_as_json function completes and returns to get_info().

The get_info() function sends a JSON response back to the client, containing the infoResult dictionary

### Key Features

- **Logging**: Logs requests in JSON format with details such as IP address, request method, URL, and timestamp.
- **Endpoint**: Provides an `/info` endpoint that returns service metadata.
- **Environment Variables**: Configurable through environment variables for service port and log level.

## How to Build

### Prerequisites

- Docker installed on your machine.
- Correct permissions to build the docker image from the repo directory.

### Builder Docker Image

You can use the provided Dockerfile to build the application. The Dockerfile sets up the environment, installs dependencies, and starts the Flask application.

```Dockerfile
#UsetheofficialPythonimagefromtheDockerHub
FROMpython:3.11-slim

#Createandsettheworkingdirectory
WORKDIR/app

#Copytheapplicationfilestothecontainer
COPY./app

#defineargumenttoreceivegitshaidwhilethedockerisrun
ARGCOMMIT_SHA

#storethegitshaidintothefile
RUNecho${COMMIT_SHA}>commit_sha.txt

#Installdependencies
RUNpipinstall--no-cache-dir-rrequirements.txt

#Commandtoruntheapplication
CMD["python3","RubyKInfoLog.py"]


# Command to run the application
CMD ["python", "app.py"]
```

### Building the Docker Image

```sh
sudo docker build -t ruby-info-log-build --build-arg  COMMIT_SHA=$(git rev-parse HEAD) .
```

## How to Deploy

### Running the Docker Container

After building the Docker image, you can run the container using the following command:

```sh
sudo docker run --env-file .env --name rubytest -p 5000:5000   ruby-info-log-build
```

### Accessing the Application

Once the container is running, you can access the application at `http://localhost:5000/info`.

## Key Design Decisions/Risks

### Design Decisions

1. **Structured Logging**: The application logs request details in a structured JSON format for easier parsing and analysis.
2. **Environment Variables**: Key configuration options, such as service port and log level, are configurable through environment variables to enhance flexibility and portability. The Environment variables are stored in .env file of this repo.
3. **Git Commit SHA**: The application reads the Git commit SHA from a file (`commit_sha.txt`) . This SHA id is provided to the docker image while building the image.
4. **Using Flask**. This application uses flask framework in python to create a /info endpoint.
5. **Application Version maintenance** This application assumes that the current version is 1.0.0  . Futher enhancements can be made to take version as an input variable. However it is hardcoded at present.
6. **The app is listening on 0.0.0.0** : To make the application available outside the container below code is used
	
	```sh
		app.run(host="0.0.0.0",debug=True,port=myport)
	```
	Above makes the flask app listen to all the requests that can reach this server.
7. **stdout** in python stdout is the default value of logging.StreamHandler().
8. **HTTP server default logs 200 disabled** The default logs are disabled to get rid of any redundancies in logs.
	```sh
	    	log.setLevel(logging.INFO)
    		# Add a lambda filter to exclude HTTP 200 logs
    		log.addFilter(lambda record: '200' not in record.getMessage())
 	```
	
### Risks

1. **Not running the application from correct path might lead to incorrect SHA id being displayed**: 
2. **Security**: The application currently logs incoming request details, which may include sensitive information. Ensure that no sensitive data is logged, and secure the `/info` endpoint if necessary.
3. **Environment Variable Management**: Proper management of environment variables is crucial. Ensure that sensitive information is not exposed and environment variables are set securely.

## Conclusion

RubyKInfoLog is a simple yet flexible logging service that can be easily built and deployed using Docker. By following this README, you should be able to set up and run the application, as well as understand the key design decisions and risks involved. Contributions and improvements to the project are welcome.

