const updateVisitButton = document.querySelector("#update-visit");

async function updateVisit(e) {
  e.preventDefault();
  const visitId = document.querySelector('input[name="visit-id"]').value;
  const username = document.querySelector('input[name="user-username"]').value;
  console.log("clicked update visit");
  try {
    await axios.post(
      `/${username}/visits/${visitId}/update-visit`,
      {
        visit: visit,
        activities: selectedActivities,
        park: { park_code: parkData.parkCode, park_name: parkData.fullName },
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    console.log("success!");
    window.location.href = "/";
  } catch (err) {
    console.log(err);
  }
}

updateVisitButton.addEventListener("click", async (e) => {
  updateVisit(e);
});
