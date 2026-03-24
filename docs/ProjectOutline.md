# **Carbon Commute Web App – Project Outline**

## **1\. System Description and Vision**

Our project is a **Carbon Commute Calculator**, designed to help users estimate CO2 emissions for their daily trips and make more sustainable transportation choices. Our goal is to make a **web application** with a user-friendly interface that clearly guides users through entering their trip and vehicle data.

We aim for the web app to:

* Let users **input vehicle information** (make, model, year)  
* Let users **input trip information** (origin, destination, frequency, passengers)  
* Provide **CO2 emission estimates** for single trips and rolled-up summaries (weekly, monthly, yearly)  
* Allow users to **save and select vehicle and trip presets**

**Intended Users:**

* Students, faculty, and community members interested in sustainable commuting  
* Transportation planners or researchers who want data on commuting emission

**The web application will provide the following functionality:**

* The application will allow users to input vehicle details and save them as reusable presets.  
* Output correct fuel type based on vehicle details.  
* Input trip details, including origin, destination, and number of passengers  
* Compute CO2 emissions.  
* Fetch realistic route distances from the **Google Routes API**  
* Display calculated emissions in a readable format  
* Offer a clean, interactive user interface with HTML forms and CSS styling

## **2\. Application Domain Data Sets**

The application relies on two main sources of data to calculate emissions accurately: fuel economy data and route distances.

**Fuel Economy Dataset:** 

* Source: United States Department of Energy/ [fueleconomy.gov](http://fueleconomy.gov)  
* Format: CSV (Zipped or Unzipped), XML also available  
* Content: Vehicle data includes make, model, year, fuel type, and MPG (city, highway, combined). Emissions data is provided in a separate file, linked to vehicles via vehicle ID.  
* Usage: Used to look up vehicle fuel efficiency and emissions factors when calculating CO2 for trips.

**Trip/Route Data:** 

* Source: User input (addresses) and Google Routes API  
* Format: JSON from API or text input  
* Content   
  * Origin address  
  * Destination Address  
  * Distance of the route (Calculated by Google)  
* Usage  
  * Users enter the origin and destination addresses (e.g., street, city, zip code).  
  * The app sends these to the **Google Routes API**, which returns the actual route distance.  
  * The app uses this distance with the vehicle’s fuel efficiency and fuel type to compute CO₂ emissions per trip.


**Conceptual Entities:**

* **Vehicle:** make, model, year, fuel type, MPG  
* **Route:** origin, destination, distance  
* **Trip:** vehicle \+ route \+ frequency \+ occurrence \+ passengers  
* **User Presets:** saved vehicles and trips for repeated use

**3\. Development Environment Overview**

* **GitHub Repository:** [https://github.com/2026-spring-comp-705-805/project-bella-bhargavi.git](https://github.com/2026-spring-comp-705-805/project-bella-bhargavi.git)  
* **Project Board:** GitHub Project for tracking tasks and responsibilities  
* **Local Development Environment:**  
  * Python 3.12   
  * Poetry/venv for environment   
  * Flask framework for routing and serving HTML pages(jinja2 templates)  
  * HTML/CSS for frontend  
  * SQLAlchemy for persistent storage if needed

## **4\. Development Activities, Deliverables, and Ownership Responsibilities**

**WEEK 7 (Mar 04 – Mar 10\)**  
- Understand the source code structure and flow of the application and run the existing Python application. Assignee: Bella, Bhargavi  
- Test the source code application to understand how vehicles, routes, and trips are working. Assignee: Bella, Bhargavi  
- Submit the project outline for the team project. Assignee: Bella, Bhargavi  
- Initialize the GitHub repository for the project. Assignee: Bhargavi  
- Create a Google Cloud account and generate the Google Routes API key and configure it in the .env file. Assignee: Bella

**WEEK 8 (Mar 11 – Mar 24\)**  
- Create the Flask project structure with app.py, templates, static, and src folders and organize the project files. Assignee: Bhargavi  
- Install required dependencies and create the requirements.txt file. Assignee: Bhargavi  
- Initialize SQLAlchemy models for trip, vehicle, and summary. Assignee: Bhargavi  
- Create index.html with a header, middle section, and footer. Assignee: Bella  
- Create style.css and apply basic styling for the header, body layout, and footer. Assignee: Bella

**WEEK 9 (Mar 25 – Mar 31\)**  
- Create add\_vehicle.html with a form that includes Make, Model, and Year fields and a submit button. Assignee: Bhargavi  
- Implement a Flask route to display the form using GET request and capture Make, Model, and Year values using POST request and integrate them with the HTML form. Assignee: Bella

**WEEK 10 (Apr 01 – Apr 07\)**  
- Create add\_trip.html with a form that includes origin, destination, frequency, and passengers fields and a submit button. Assignee: Bella  
- Implement a Flask route to display the form using GET request and capture input values using POST request and integrate them with the HTML form. Assignee: Bhargavi

**WEEK 11 (Apr 08 – Apr 14\)**  
- Create summary.html to display the summary of the calculated carbon dioxide emissions for the trips. Assignee: Bhargavi  
- Implement the Flask route to send trip data to summary.html and display the emissions results. Assignee: Bella

**WEEK 12 (Apr 15 – Apr 21\)**  
- Create dashboard.html to display the vehicles list and trip history in the form of lists. Assignee: Bella  
- Implement and Integrate Flask route to display the vehicles list and trip history. Assignee: Bhargavi

**WEEK 13 (Apr 22 – Apr 28\)**  
- Perform testing and bug fixing for the application features. Assignee: Bella, Bhargavi  
- Improve the UI styling using CSS. Assignee: Bella, Bhargavi

**WEEK 14 (Apr 29 – May 5\)**  
- Prepare the final project presentation and demo of the web application. Assignee: Bella, Bhargavi

 

   
