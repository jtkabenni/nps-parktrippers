const updateVisitButton = document.querySelector("#update-visit");

async function updateVisit(e) {
  const visitId = document.querySelector('input[name="visit-id"]').value;
  const username = document.querySelector('input[name="user-username"]').value;
  try {
    const form = document.getElementById("update-visit"); // Get the form element
    const formData = new FormData(form); // Create a FormData object

    const csrfToken = formData.get("csrf_token");
    await axios.post(
      `/${username}/visits/${visitId}/update-visit`,
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
if (updateVisitButton) {
  updateVisitButton.addEventListener("submit", async (e) => {
    e.preventDefault();
    updateVisit(e);
  });
}
