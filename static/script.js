function showAlert(message, type) {
  const alert = document.getElementById("alert");
  alert.className = `alert alert-${type}`;
  alert.textContent = message;
  alert.style.display = "block";
  setTimeout(() => {
    alert.style.display = "none";
  }, 3000);
}

document.getElementById("studentForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const studentData = {
    name: document.getElementById("name").value,
    age: parseInt(document.getElementById("age").value),
    grade: document.getElementById("grade").value,
    api_key: document.getElementById("api_key").value,
  };

  try {
    const response = await fetch("/api/students", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(studentData),
    });

    const result = await response.json();

    if (response.ok) {
      showAlert("Student registered successfully", "success");
      document.getElementById("studentForm").reset();
      viewStudents();
    } else {
      showAlert(result.error || result.message, "error");
    }
  } catch (error) {
    showAlert("Error registering student", "error");
  }
});

async function viewStudents() {
  try {
    const response = await fetch("/api/students/view", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        api_key: document.getElementById("api_key").value,
      }),
    });

    const data = await response.json();
    const studentList = document.getElementById("studentList");

    if (response.ok && data.students) {
      let tableHTML = `
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Age</th>
                                    <th>Grade</th>
                                    <th>Created At</th>
                                </tr>
                            </thead>
                            <tbody>
                    `;

      data.students.forEach((student) => {
        tableHTML += `
                            <tr>
                                <td>${student.id}</td>
                                <td>${student.name}</td>
                                <td>${student.age}</td>
                                <td>${student.grade}</td>
                                <td>${new Date(
                                  student.created_at
                                ).toLocaleString()}</td>
                            </tr>
                        `;
      });

      tableHTML += `</tbody></table>`;
      studentList.innerHTML = tableHTML;
    } else {
      studentList.innerHTML = "";
      showAlert(data.error || data.message, "error");
    }
  } catch (error) {
    showAlert("Error fetching students", "error");
  }
}
