const NPSBaseUrl = "https://developer.nps.gov/api/v1";
const suggestions = document.querySelector("#park-list");
const parkSearch = document.querySelector("#search-park");
const apiKey = "S7cm7RqypBs9MQKwodrODT5NBiv5oGDjOdaH1nVf";
const searchActivitiesButton = document.querySelector("#search-activities");
const updateActivitiesButton = document.querySelector("#update-activities");
const activitiesSection = document.querySelector(".available-activities");
const selectedActivitiesSection = document.querySelector(
  ".selected-activities"
);
const selectedActivitiesList = document.querySelector(
  ".selected-activities ul"
);
const startDateInput = document.getElementById("start-date");
const endDateInput = document.getElementById("end-date");
let parks = {};
let parkData = {};
let parkActivities = {};
let selectedActivities = [];
let visit = {};
let searchStatus = null;

async function fetchParks() {
  if (searchStatus === "Add ") {
    try {
      const response = await axios.get(
        `${NPSBaseUrl}/parks?api_key=${apiKey}&limit=500`
      );
      parks = response.data.data;
      displayParkSuggestions(parks);
      console.log(parks);
    } catch (err) {
      console.log(err);
    }
  } else if (searchStatus === "Update") {
    const parkId = document.querySelector('input[name="park-id"]').value;
    try {
      const response = await axios.get(
        `${NPSBaseUrl}/parks?api_key=${apiKey}&parkCode=${parkId}`
      );
      parks = response.data.data;
      displayParkSuggestions(parks);
      console.log(parks);
    } catch (err) {
      console.log(err);
    }
  }
}

function displayParkSuggestions(parks) {
  suggestions.innerHTML = "";
  for (let park of parks) {
    let option = document.createElement("option");
    option.innerHTML = park.fullName;
    suggestions.append(option);
  }
}

function validateDates() {
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
  parkData = parks.find((park) => park.fullName === parkSearch.value);
  if (parkData) {
    await Promise.all([
      getParkActivities("campgrounds"),
      getParkActivities("events"),
      getParkActivities("thingstodo"),
    ]);
  }
  visit = {
    park_code: parkData.parkCode,
    start_date: startDateInput.value,
    end_date: endDateInput.value,
  };
}
// Get park activities based on given endpoint
async function getParkActivities(endpoint) {
  try {
    const response = await axios.get(
      `https://developer.nps.gov/api/v1/${endpoint}?api_key=${apiKey}&limit=500&parkCode=${parkData.parkCode}`
    );
    parkActivities[endpoint] = response.data.data;
  } catch (err) {
    console.log(err);
  }
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
    selectedActivitiesSection.classList.remove("hide");
    const div = document.createElement("div");
    div.innerHTML = `<h3>${activity.title}</h3><p ><i class = "activity-type">${activity.activities[0].name}</i> </p><p>${activity.shortDescription}</p>${location}${duration}`;
    div.addEventListener("click", (e) => {
      addActivityToSelected(e, activity), addSelectedActivityLis();
    });
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
  } else {
    const indexToRemove = selectedActivities.findIndex(
      (item) => item.name === activity.title
    );
    if (indexToRemove !== -1) {
      selectedActivities.splice(indexToRemove, 1);
      console.log("Removed:", activity.name);
    }
  }
}

function addSelectedActivityLis() {
  for (activity of selectedActivities) {
    const li = document.createElement("li");
    li.innerHTML = activity.name;
    selectedActivitiesList.append(li);
  }
}

if (searchActivitiesButton) {
  searchStatus = "Add";
  fetchParks();
  searchActivitiesButton.addEventListener("click", async () => {
    await submitPark();
    displayParkActivities();
  });
} else if (updateActivitiesButton) {
  searchStatus = "Update";
  fetchParks();
  updateActivitiesButton.addEventListener("click", async () => {
    await submitPark();
    displayParkActivities();
  });
}
