const updateVisitButton = document.querySelector("#update-visit");

async function updateVisit(e) {
  const visitId = document.querySelector('input[name="visit-id"]').value;
  const username = document.querySelector('input[name="user-username"]').value;
  try {
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
