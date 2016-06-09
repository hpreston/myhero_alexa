# IN DEVELOPMENT NOT READY FOR WIDESPREAD USE YET

# MyHero Alexa Service

This is the code and details for an Alexa Skill as part of a basic microservice demo application.
This provides a voice interface for a voting system where users can vote for their favorite movie superhero.

Details on deploying the entire demo to a Mantl cluster can be found at
* MyHero Demo - [hpreston/myhero_demo](https://github.com/hpreston/myhero_demo)

The application was designed to provide a simple demo for Cisco Mantl.  It is written as a simple Python Flask application and deployed as a docker container.

Other services are:
* Data - [hpreston/myhero_data](https://github.com/hpreston/myhero_data)
* App - [hpreston/myhero_app](https://github.com/hpreston/myhero_app)
* Web - [hpreston/myhero_web](https://github.com/hpreston/myhero_web)
* Ernst - [hpreston/myhero_ernst](https://github.com/hpreston/myhero_ernst)
  * Optional Service used along with an MQTT server when App is in "queue" mode
* Spark Bot - [hpreston/myhero_spark](https://github.com/hpreston/myhero_spark)
  * Optional Service that allows voting through IM/Chat with a Cisco Spark Bot
* Tropo App - [hpreston/myhero_tropo](https://github.com/hpreston/myhero_tropo)
  * Optional Service that allows voting through TXT/SMS messaging
* Alexa Skill - [hpreston/myhero_alexa](https://github.com/hpreston/myhero_alexa)
  * Optional Serice that allows voting through a Amazon Alexa voice interface


The docker containers are available at
* Data - [hpreston/myhero_data](https://hub.docker.com/r/hpreston/myhero_data)
* App - [hpreston/myhero_app](https://hub.docker.com/r/hpreston/myhero_app)
* Web - [hpreston/myhero_web](https://hub.docker.com/r/hpreston/myhero_web)
* Ernst - [hpreston/myhero_ernst](https://hub.docker.com/r/hpreston/myhero_ernst)
  * Optional Service used along with an MQTT server when App is in "queue" mode
* Spark Bot - [hpreston/myhero_spark](https://hub.docker.com/r/hpreston/myhero_spark)
  * Optional Service that allows voting through IM/Chat with a Cisco Spark Bot
* Tropo App - [hpreston/myhero_tropo](https://hub.docker.com/r/hpreston/myhero_tropo)
  * Optional Service that allows voting through TXT/SMS messaging
* Alexa Skill - [hpreston/myhero_alexa](https://hub.docker.com/r/hpreston/myhero_alexa)
  * Optional Serice that allows voting through a Amazon Alexa voice interface


## Alexa Skill Details
This repo contains the Python code for an AWS Lambda function that can be linked to an Alexa Skill through Amazon's Developer Site.  Also included are files with the utterances and intents source needed to fully install the function.

_You will need to replace the URL for your myhero_app service in the code prior to uploading to AWS Lambda_

## Skill Installation Steps

...

## Using the Skill

...

