const parkSearch = document.querySelector("#search-park");
const startDateInput = document.getElementById("start-date");
const endDateInput = document.getElementById("end-date");
const parkSuggestions = document.querySelector("#park-list");
const searchActivitiesButton = document.querySelector("#search-activities");
const updateActivitiesButton = document.querySelector("#update-activities");
const availableActivitiesSection = document.querySelector(
  ".available-activities"
);
const selectedActivitiesSection = document.querySelector(
  ".selected-activities"
);
const selectedActivitiesList = document.querySelector(
  ".selected-activities ul"
);
let parks = {};
let selectedParkData = {};
let parkActivities = {};
let selectedActivities = [];
let visit = {};
let searchStatus = null;

// Fetch parks based on add visit or update visit status
async function fetchParks() {
  if (searchStatus === "Add") {
    try {
      const response = await axios.get("/fetch-parks");
      parks = response.data.data;
      displayParkSuggestions(parks);
    } catch (err) {
      console.log(err);
    }
  } else if (searchStatus === "Update") {
    const parkId = document.querySelector('input[name="park-id"]').value;
    console.log(parkId);
    try {
      const response = await axios.get("/fetch-updated-park", {
        params: { parkId: parkId },
      });
      parks = response.data.data;
    } catch (err) {
      console.log(err);
    }
  }
}

// Add park names to datalist input as dropdown/search options
function displayParkSuggestions(parks) {
  parkSuggestions.innerHTML = "";
  for (let park of parks) {
    let option = document.createElement("option");
    option.innerHTML = park.fullName;
    parkSuggestions.append(option);
  }
}

// search for park, validate DataTransfer, and call requests to get all park activities for given endpoints
async function submitPark(e) {
  validateDates();
  selectedParkData = parks.find((park) => park.fullName === parkSearch.value);
  if (selectedParkData) {
    await Promise.all([
      getParkActivities("campgrounds"),
      getParkActivities("events"),
      getParkActivities("thingstodo"),
    ]);
  }
  visit = {
    park_code: selectedParkData.parkCode,
    start_date: startDateInput.value,
    end_date: endDateInput.value,
  };
}

// Add date input validation to search park function
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

// Get park activities based on given endpoint and save to parkActivities
async function getParkActivities(endpoint) {
  try {
    const response = await axios.get("/fetch-park-activities", {
      params: {
        endpoint: endpoint,
        parkId: selectedParkData.parkCode,
      },
    });

    console.log(response);
    parkActivities[endpoint] = response.data.data;
  } catch (err) {
    console.log(err);
  }
}

// add activity div for each park activity
function displayParkActivities() {
  availableActivitiesSection.innerHTML = "";
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
    availableActivitiesSection.append(div);
  }
}

// manage adding and removing selected activities
function addActivityToSelected(e, activity) {
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
      console.log("Removed:", activity.title);
    }
  }
}

// add activity li for each selected activity
function addSelectedActivityLis() {
  selectedActivitiesList.innerHTML = "";
  console.log(selectedActivities);
  for (activity of selectedActivities) {
    const li = document.createElement("li");
    li.innerHTML = activity.name;
    selectedActivitiesList.append(li);
  }
}

// update search status and add event listener based on which template is rendered
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
