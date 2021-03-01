# Flight Finder Web Application

This is a Flask application that allows the user to search for the cheapest available flights and receive booking links. It is designed to simplify the process of finding flight deals by asking for limited input from the user and allowing a range of destinations to be searched for at once.

## How the Application Works
1. The homepage of the application includes a form in which the user can enter flight details (departure city, arrival cities and a range of possible departure dates).   
1. The application searches for the cheapest flights that match those specifications using the Tequila flight search API (URL provided below).  
1. A results page containing details of the cheapest flights (and booking links) is rendered and passed back to the user.
<br>

|                          Homepage:                      |                  Search Results:                 |
| ------------------------------------------------------- | ------------------------------------------------ |
| <img src="/images/flight-finder-search.png">             |<img src="/images/flight-results.png">             |

## Using the Application
The application has been deployed on Heroku and can be accessed here:  
* https://cheap-flight-finder-app.herokuapp.com/


## Supporting Libraries and APIs
* Flask (backend): https://flask.palletsprojects.com/en/1.1.x/quickstart/  
* Bootstrap (frontend): https://getbootstrap.com/  
* The Tequila flight search API (for flight data): https://tequila.kiwi.com/portal/login  

## Future Development  
I do not have any immediate plans to change the application. However, it is likely that small improvements to functionality and appearance (through CSS) will be made in the future.
