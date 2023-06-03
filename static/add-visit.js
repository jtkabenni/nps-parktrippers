const addVisitButton = document.querySelector("#add-visit");

async function addVisit(e) {
  console.log("clicked add visit");
  try {
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
        },
      }
    );
    console.log("success!");
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
