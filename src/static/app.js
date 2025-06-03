document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const attendanceActivitySelect = document.getElementById("attendance-activity");
  const categoryFilter = document.getElementById("category-filter");
  const signupForm = document.getElementById("signup-form");
  const attendanceForm = document.getElementById("attendance-form");
  const reportForm = document.getElementById("report-form");
  const messageDiv = document.getElementById("message");
  const attendanceMessageDiv = document.getElementById("attendance-message");
  const reportResults = document.getElementById("report-results");
  const reportContent = document.getElementById("report-content");
  const reportSummary = document.getElementById("report-summary");
  
  // Current selected category
  let currentCategory = "All";

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      // Get activities (possibly filtered by category)
      const endpoint = currentCategory === "All" 
        ? "/activities" 
        : `/activities/filter?category=${encodeURIComponent(currentCategory)}`;
      
      const response = await fetch(endpoint);
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft =
          details.max_participants - details.participants.length;

        // Create participants HTML with delete icons instead of bullet points
        const participantsHTML =
          details.participants.length > 0
            ? `<div class="participants-section">
              <h5>Participants:</h5>
              <ul class="participants-list">
                ${details.participants
                  .map(
                    (email) =>
                      `<li><span class="participant-email">${email}</span><button class="delete-btn" data-activity="${name}" data-email="${email}">❌</button></li>`
                  )
                  .join("")}
              </ul>
            </div>`
            : `<p><em>No participants yet</em></p>`;

        activityCard.innerHTML = `
          <h4>${name} <span class="category-badge category-${details.category}">${details.category}</span></h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <p class="duration-info">Session Duration: ${details.duration_per_session} hour${details.duration_per_session !== 1 ? 's' : ''}</p>
          <div class="participants-container">
            ${participantsHTML}
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdowns if not already there
        if (!Array.from(activitySelect.options).some(option => option.value === name)) {
          const option = document.createElement("option");
          option.value = name;
          option.textContent = name;
          activitySelect.appendChild(option);
          
          const attendanceOption = document.createElement("option");
          attendanceOption.value = name;
          attendanceOption.textContent = name;
          attendanceActivitySelect.appendChild(attendanceOption);
        }
      });

      // Add event listeners to delete buttons
      document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", handleUnregister);
      });
    } catch (error) {
      activitiesList.innerHTML =
        "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Function to fetch categories from API
  async function fetchCategories() {
    try {
      const response = await fetch("/activities/categories");
      const categories = await response.json();

      // Add categories to filter dropdown
      categories.forEach(category => {
        const option = document.createElement("option");
        option.value = category;
        option.textContent = category;
        categoryFilter.appendChild(option);
      });
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  }

  // Handle category filter change
  categoryFilter.addEventListener("change", (event) => {
    currentCategory = event.target.value;
    fetchActivities();
  });

  // Handle unregister functionality
  async function handleUnregister(event) {
    const button = event.target;
    const activity = button.getAttribute("data-activity");
    const email = button.getAttribute("data-email");

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(
          activity
        )}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";

        // Refresh activities list to show updated participants
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to unregister. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error unregistering:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(
          activity
        )}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();

        // Refresh activities list to show updated participants
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Handle attendance form submission
  attendanceForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("attendance-email").value;
    const activity = document.getElementById("attendance-activity").value;
    const date = document.getElementById("attendance-date").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/record-attendance?email=${encodeURIComponent(email)}&date=${encodeURIComponent(date)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        attendanceMessageDiv.textContent = result.message;
        attendanceMessageDiv.className = "success";
        attendanceForm.reset();
      } else {
        attendanceMessageDiv.textContent = result.detail || "An error occurred";
        attendanceMessageDiv.className = "error";
      }

      attendanceMessageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        attendanceMessageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      attendanceMessageDiv.textContent = "Failed to record attendance. Please try again.";
      attendanceMessageDiv.className = "error";
      attendanceMessageDiv.classList.remove("hidden");
      console.error("Error recording attendance:", error);
    }
  });

  // Handle report form submission
  reportForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("report-email").value;

    try {
      const response = await fetch(`/students/${encodeURIComponent(email)}/activity-report`);
      const report = await response.json();

      if (response.ok) {
        // Display the report
        reportContent.innerHTML = "";
        
        if (Object.keys(report.activities).length === 0) {
          reportContent.innerHTML = "<p>No activities found for this student.</p>";
        } else {
          // Create HTML for each activity
          Object.entries(report.activities).forEach(([name, details]) => {
            const activityElement = document.createElement("div");
            activityElement.className = "report-activity";
            
            activityElement.innerHTML = `
              <h5>
                ${name}
                <span class="category-badge category-${details.category}">${details.category}</span>
              </h5>
              <p class="attendance-stat">Attended Sessions: ${details.attended_sessions}</p>
              <p class="attendance-stat">Total Hours: ${details.hours}</p>
            `;
            
            reportContent.appendChild(activityElement);
          });
        }
        
        // Add summary
        reportSummary.innerHTML = `
          <p>Total Activities: ${report.total_activities}</p>
          <p>Total Hours: ${report.total_hours}</p>
        `;
        
        reportResults.classList.remove("hidden");
      } else {
        alert(report.detail || "An error occurred");
      }
    } catch (error) {
      alert("Failed to generate report. Please try again.");
      console.error("Error generating report:", error);
    }
  });

  // Initialize app
  fetchCategories();
  fetchActivities();
});
