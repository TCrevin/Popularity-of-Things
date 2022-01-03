# Popularity-of-Things

The purpose of this tool is to find and quantify the popularity of software used in cybersecurity.

The following repository contains the source code for two Docker images "embed" and "api" which are available from the following
Docker repositories.

The tool uses various third party API keys to access Twitter, Google and Reddit.
Said keys will be deactivated by maintainers of this repository if found in violation of the terms of service of the API.

To pull and run the latest version of the images,

'''

docker pull juandockerpot/embed:latest
docker pull juandockerpot/api:latest

docker run -v ~/docker:/var/lib/output juandockerpot/embed:latest
docker run -v ~/docker:/var/lib/output juandockerpot/api:latest

'''