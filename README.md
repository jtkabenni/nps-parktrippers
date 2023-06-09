# Parktrippers

Parktrippers is an application that allows you to create the perfect itinerary for a trip to a US national park. With Parktrippers you can select a park and browse what events and activities are available during the dates of your stay, and add them to a daily or multi-day itinerary.

## API used

This project uses the [National Park Service API](https://www.nps.gov/subjects/developer/api-documentation.htm).
A different background image will display for every new session. I used the [Unsplash APi](https://unsplash.com/documentation) with a national parks filter to get these images.

## Deployment

Parktrippers is deployed using [Render](https://render.com/) at [Parktrippers](https://parktrippers.onrender.com/)

## Features

- **Search parks and activities:** Enter park and date information for your visit, and select activities for that park, including hiking trails, campgrounds, ranger programs, and other events to add to your visit.
- **View Visit and activities:** View details and activities for each park visit.
- **Add notes for each activity:** Add, update, and delete notes for each visit activity.
- **National park background image:** Fetch a new national park image as the background image every session.
- **Secure authentication**: Securely sign up or login with password encryption

## Standard user flow

- Sign up or log into the Parktrippers app.
- Click on **Add visit**, and enter a national park (US only for now!) and start and end date. Click **Search activities** to retrieve all available activities for that park.
- Select the activities you want to add to your visit and click **Add visit** button to save the visit.
- Click on **Profile** in the navigation to view all of your visits.
- Click each visit to see the details of the visit and activities. From here you can add and update notes for each activity, delete activities, delete the visit, and add new activities to your visit.

## Stack used

- Flask
- Python 3.10.8
- Javascript
- CSS
- Jinja
- WTForms
- Axios

## Feedback?

Reach out to jennytakahara@gmail.com with any questions or feedback!
