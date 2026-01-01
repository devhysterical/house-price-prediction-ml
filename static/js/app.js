/**
 * House Price Prediction - Frontend JavaScript
 */

document.addEventListener("DOMContentLoaded", function () {
  initializeApp();
});

function initializeApp() {
  setupRangeInputs();
  setupPredictionForm();
}

/**
 * Setup range input value displays
 */
function setupRangeInputs() {
  const rangeInputs = document.querySelectorAll('input[type="range"]');

  rangeInputs.forEach((input) => {
    const valueDisplay = document.getElementById(`${input.id}-value`);

    // Update display on input
    input.addEventListener("input", function () {
      updateRangeValue(this, valueDisplay);
    });

    // Initialize display
    updateRangeValue(input, valueDisplay);
  });
}

/**
 * Update range value display
 */
function updateRangeValue(input, display) {
  let value = parseFloat(input.value);

  // Format based on input type
  switch (input.id) {
    case "Population":
      display.textContent = value.toLocaleString();
      break;
    case "HouseAge":
      display.textContent = Math.round(value);
      break;
    default:
      display.textContent = value.toFixed(1);
  }

  // Update slider background gradient
  const percent = ((value - input.min) / (input.max - input.min)) * 100;
  input.style.background = `linear-gradient(to right, 
        rgba(99, 102, 241, 0.5) 0%, 
        rgba(99, 102, 241, 0.5) ${percent}%, 
        rgba(255, 255, 255, 0.1) ${percent}%, 
        rgba(255, 255, 255, 0.1) 100%)`;
}

/**
 * Setup prediction form submission
 */
function setupPredictionForm() {
  const form = document.getElementById("prediction-form");
  const predictBtn = document.getElementById("predict-btn");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    // Get form data
    const formData = getFormData();

    // Set loading state
    setLoadingState(true);

    try {
      // Make prediction request
      const result = await makePrediction(formData);

      if (result.success) {
        showResult(result.prediction);
      } else {
        showError(result.error || "Prediction failed");
      }
    } catch (error) {
      console.error("Prediction error:", error);
      showError("Failed to connect to server. Please try again.");
    } finally {
      setLoadingState(false);
    }
  });
}

/**
 * Get form data
 */
function getFormData() {
  return {
    MedInc: parseFloat(document.getElementById("MedInc").value),
    HouseAge: parseFloat(document.getElementById("HouseAge").value),
    AveRooms: parseFloat(document.getElementById("AveRooms").value),
    AveBedrms: parseFloat(document.getElementById("AveBedrms").value),
    Population: parseFloat(document.getElementById("Population").value),
    AveOccup: parseFloat(document.getElementById("AveOccup").value),
    Latitude: parseFloat(document.getElementById("Latitude").value),
    Longitude: parseFloat(document.getElementById("Longitude").value),
  };
}

/**
 * Make prediction API request
 */
async function makePrediction(data) {
  const response = await fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return await response.json();
}

/**
 * Set loading state
 */
function setLoadingState(isLoading) {
  const predictBtn = document.getElementById("predict-btn");

  if (isLoading) {
    predictBtn.classList.add("loading");
    predictBtn.disabled = true;
  } else {
    predictBtn.classList.remove("loading");
    predictBtn.disabled = false;
  }
}

/**
 * Show prediction result
 */
function showResult(prediction) {
  const placeholder = document.getElementById("result-placeholder");
  const resultData = document.getElementById("result-data");
  const resultError = document.getElementById("result-error");

  // Hide placeholder and error
  placeholder.style.display = "none";
  resultError.style.display = "none";

  // Update values
  document.getElementById("price-value").textContent =
    prediction.price_formatted;
  document.getElementById("price-100k").textContent = prediction.price_100k;

  // Show result with animation
  resultData.style.display = "block";
  resultData.style.animation = "none";
  resultData.offsetHeight; // Trigger reflow
  resultData.style.animation = "fadeIn 0.5s ease";

  // Scroll to result on mobile
  if (window.innerWidth <= 900) {
    document.getElementById("result-card").scrollIntoView({
      behavior: "smooth",
      block: "center",
    });
  }
}

/**
 * Show error message
 */
function showError(message) {
  const placeholder = document.getElementById("result-placeholder");
  const resultData = document.getElementById("result-data");
  const resultError = document.getElementById("result-error");
  const errorMessage = document.getElementById("error-message");

  // Hide placeholder and result
  placeholder.style.display = "none";
  resultData.style.display = "none";

  // Show error
  errorMessage.textContent = message;
  resultError.style.display = "block";
}

/**
 * Format currency
 */
function formatCurrency(amount) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}
