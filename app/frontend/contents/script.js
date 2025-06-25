// Set the base URL for the API (using the Docker Compose service name if applicable)
const apiBaseUrl = window.env.apiBaseUrl;

// Load and display pets from the given URL (default is all pets)
async function loadPets(url = `${apiBaseUrl}/pets`) {
  try {
    const response = await fetch(url);
    if (response.ok) {
      const pets = await response.json();
      const petsList = document.getElementById("petsList");
      petsList.innerHTML = "";
      pets.forEach((pet) => {
        const li = document.createElement("li");
        li.className = "pet-item";
        li.innerHTML = `
          <strong>ID:</strong> ${pet.id} <br>
          <strong>Name:</strong> ${pet.name} <br>
          <strong>Species:</strong> ${pet.species} <br>
          <strong>Age:</strong> ${pet.age} <br>
          <strong>Breed:</strong> ${pet.breed ? pet.breed : 'N/A'} <br>
          <strong>Guardian:</strong> ${pet.guardian} <br>
          <strong>Created:</strong> ${pet.creation_date}
        `;
        // Create a Delete button
        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";
        deleteBtn.addEventListener("click", () => deletePet(pet.id));
        li.appendChild(deleteBtn);
        // Create an Update button
        const updateBtn = document.createElement("button");
        updateBtn.textContent = "Update";
        updateBtn.addEventListener("click", () => showUpdateForm(pet));
        li.appendChild(updateBtn);
        petsList.appendChild(li);
      });
    } else {
      alert("Error loading pets");
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

// Delete pet by ID
async function deletePet(petId) {
  try {
    const response = await fetch(`${apiBaseUrl}/pets/${petId}`, {
      method: "DELETE",
    });
    if (response.ok) {
      loadPets();
    } else {
      alert("Error deleting pet");
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

// Show the update form pre-filled with the pet data
function showUpdateForm(pet) {
  document.getElementById("updatePetId").value = pet.id;
  document.getElementById("updateName").value = pet.name;
  document.getElementById("updateSpecies").value = pet.species;
  document.getElementById("updateAge").value = pet.age;
  document.getElementById("updateBreed").value = pet.breed || "";
  document.getElementById("updateGuardian").value = pet.guardian;
  document.getElementById("updateSection").style.display = "block";
}

// Update pet data via PUT request
async function updatePet(petId, petData) {
  try {
    const response = await fetch(`${apiBaseUrl}/pets/${petId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(petData),
    });
    if (response.ok) {
      document.getElementById("updateSection").style.display = "none";
      loadPets();
    } else {
      alert("Error updating pet");
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

// Event listener for the "Add Pet" form submission
document.getElementById("addPetForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const name = document.getElementById("name").value;
  const species = document.getElementById("species").value;
  const age = parseInt(document.getElementById("age").value);
  const breed = document.getElementById("breed").value;
  const guardian = document.getElementById("guardian").value;

  const petData = { name, species, age, breed, guardian };

  try {
    const response = await fetch(`${apiBaseUrl}/pets`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(petData),
    });
    if (response.ok) {
      document.getElementById("addPetForm").reset();
      loadPets();
    } else {
      alert("Error adding pet");
    }
  } catch (error) {
    console.error("Error:", error);
  }
});

// Event listener for the "Update Pet" form submission
document.getElementById("updatePetForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const petId = document.getElementById("updatePetId").value;
  const name = document.getElementById("updateName").value;
  const species = document.getElementById("updateSpecies").value;
  const age = parseInt(document.getElementById("updateAge").value);
  const breed = document.getElementById("updateBreed").value;
  const guardian = document.getElementById("updateGuardian").value;

  const petData = { name, species, age, breed, guardian };

  updatePet(petId, petData);
});

// Cancel the update operation and hide the update form
document.getElementById("cancelUpdate").addEventListener("click", () => {
  document.getElementById("updateSection").style.display = "none";
});

// Event listeners for filtering buttons
document.getElementById("loadAll").addEventListener("click", () => loadPets(`${apiBaseUrl}/pets`));
document.getElementById("loadCats").addEventListener("click", () => loadPets(`${apiBaseUrl}/pets/cats`));
document.getElementById("loadDogs").addEventListener("click", () => loadPets(`${apiBaseUrl}/pets/dogs`));

// Load all pets on initial page load
loadPets();
