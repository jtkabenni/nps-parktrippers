const suggestions = document.querySelector("#parks-list ul");
const suggestions2 = document.querySelector("#park-list");
const parkSearch = document.querySelector("#search-park");
const apiKey = "S7cm7RqypBs9MQKwodrODT5NBiv5oGDjOdaH1nVf";
const addParkButton = document.querySelector("#submit-park");
const activitiesSection = document.querySelector(".available-activities");
const selectedActivitiesSection = document.querySelector(
  ".selected-activities"
);
const selectedActivitiesList = document.querySelector(
  ".selected-activities ul"
);
const startDate = document.querySelector("#start-date");
const endDate = document.querySelector("#end-date");

let parks = [];
let parkData = {};
let parkActivities = {};
let selectedActivities = [];
let visit = {};

async function fetchParks() {
  try {
    const response = await axios.get(
      `https://developer.nps.gov/api/v1/parks?api_key=${apiKey}&limit=500`
    );
    console.log(response.data.data);
    parks = response.data.data;
    displayParksuggestions();
  } catch (err) {
    console.log(err);
  }
}

function displayParksuggestions() {
  suggestions.innerHTML = "";
  for (let park of parks) {
    let option = document.createElement("option");
    option.innerHTML = park.fullName;
    suggestions2.append(option);
  }
}

function validateDates() {
  // e.preventDefault();
  const startDateInput = document.getElementById("start-date");
  const endDateInput = document.getElementById("end-date");
  console.log(startDateInput.value, endDateInput.value);
  const searchContainer = document.querySelector(".search-container p");
  if (startDateInput.value > endDateInput.value) {
    p = document.createElement("p");
    p.innerHTML = "The start date cannot be greater than the end date.";
    searchContainer.append(p);
    return;
  } else if (startDateInput.value === "" || endDateInput.value === "") {
    p = document.createElement("p");
    p.innerHTML = "Please enter a date.";
    searchContainer.append(p);
    return;
  }
}

async function submitPark(e) {
  validateDates();
  const getParkData = async (endpoint, activityKey) => {
    try {
      const response = await axios.get(
        `https://developer.nps.gov/api/v1/${endpoint}?api_key=${apiKey}&limit=500&parkCode=${parkData.parkCode}`
      );

      parkActivities[activityKey] = response.data.data;
    } catch (err) {
      console.log(err);
    }
  };
  parkData = parks.find((park) => park.fullName === parkSearch.value);
  if (parkData) {
    await Promise.all([
      getParkData("campgrounds", "campgrounds"),
      getParkData("events", "events"),
      getParkData("thingstodo", "thingstodo"),
    ]);
  }
  (visit = {
    park_code: parkData.parkCode,
    start_date: startDate.value,
    end_date: endDate.value,
  }),
    console.log(parkActivities);
}

function displayParkActivities() {
  activitiesSection.innerHTML = "";
  for (let activity of parkActivities.thingstodo) {
    const location = activity.location
      ? `<p>
        <b>Location:</b>${activity.location}
      </p>`
      : "";

    const duration = activity.duration
      ? `<p>
        <b>Duration:</b>${activity.duration}
      </p>`
      : "";

    const div = document.createElement("div");

    selectedActivitiesSection.classList.remove("hide");
    div.innerHTML = `<h3>${activity.title}</h3><p ><i class = "activity-type">${activity.activities[0].name}</i> </p><p>${activity.shortDescription}</p>${location}${duration}`;
    div.addEventListener("click", (e) => addActivityToSelected(e, activity));
    activitiesSection.append(div);
  }
}

function addActivityToSelected(e, activity) {
  selectedActivitiesList.innerHTML = "";
  const closestDiv = e.target.closest("div");
  closestDiv.classList.toggle("selected");

  if (closestDiv.classList.contains("selected")) {
    selectedActivities.push({
      name: activity.title,
      description: activity.shortDescription,
      activity_type: activity.activities[0].name,
      location: activity.location,
      duration: activity.duration,
    });
    console.log(selectedActivities);
  } else {
    const indexToRemove = selectedActivities.findIndex(
      (item) => item.name === activity.title
    );
    if (indexToRemove !== -1) {
      selectedActivities.splice(indexToRemove, 1);
      console.log("Removed item from selectedActivities:", activity.name);
    }
    console.log(selectedActivities);
  }

  for (activity of selectedActivities) {
    const li = document.createElement("li");
    li.innerHTML = activity.name;
    selectedActivitiesList.append(li);
  }
}

addParkButton.addEventListener("click", async () => {
  await submitPark();
  displayParkActivities();
});

fetchParks();
