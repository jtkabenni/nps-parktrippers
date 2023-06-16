const addVisitButton = document.querySelector("#add-visit");

async function addVisit(e) {
  try {
    const form = document.getElementById("add-visit"); // Get the form element
    const formData = new FormData(form); // Create a FormData object

    const csrfToken = formData.get("csrf_token");
    await axios.post(
      "/add-visit",
      {
        visit: visit,
        activities: selectedActivities,
        park: {
          park_code: selectedParkData.parkCode,
          park_name: selectedParkData.fullName,
        },
      },
      {
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
      }
    );
    window.location.href = "/";
  } catch (err) {
    console.log(err);
  }
}

if (addVisitButton) {
  addVisitButton.addEventListener("submit", async (e) => {
    e.preventDefault();
    addVisit(e);
  });
}
