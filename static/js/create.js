// ─────────────────────────────────────────────
//  create.js  —  Form validation + live preview
// ─────────────────────────────────────────────

// Sample data sets
const SAMPLES = {
  sales: "North America, 420000\nEurope, 310000\nAsia Pacific, 280000\nLatin America, 190000\nMiddle East, 145000",
  survey: "Excellent, 312\nGood, 285\nAverage, 198\nBelow Average, 87\nPoor, 34",
  monthly: "January, 18200\nFebruary, 21400\nMarch, 19800\nApril, 24100\nMay, 28700\nJune, 31200"
};

// Load a sample into the textarea
function loadSample(key) {
  $("#raw_data").val(SAMPLES[key]).trigger("input");
}

// ── PARSE TEXTAREA INTO ROWS ──
function parseRows(text) {
  const rows = [];
  text.split("\n").forEach(function (line) {
    line = line.trim();
    if (!line) return;

    let parts;
    if (line.includes(","))      parts = line.split(",", 2);
    else if (line.includes(":")) parts = line.split(":", 2);
    else return;

    const val = parseFloat(parts[1]);
    if (!isNaN(val)) {
      rows.push({ label: parts[0].trim(), value: val });
    }
  });
  return rows;
}

// Colour palette for charts
const COLORS = [
  "#f0ad4e","#2ecc71","#e74c3c","#3498db",
  "#9b59b6","#1abc9c","#e67e22","#34495e"
];

let previewChart = null;

// ── RENDER LIVE PREVIEW CHART ──
function renderPreview() {
  const rows      = parseRows($("#raw_data").val());
  const chartType = $("input[name='chart_type']:checked").val();

  // Not enough data yet
  if (rows.length < 2) {
    $("#preview-empty").show();
    $("#previewChart").hide();
    if (previewChart) { previewChart.destroy(); previewChart = null; }
    return;
  }

  // Show canvas, hide placeholder
  $("#preview-empty").hide();
  $("#previewChart").show();

  const labels   = rows.map(r => r.label);
  const values   = rows.map(r => r.value);
  const bgColors = labels.map((_, i) => COLORS[i % COLORS.length]);
  const isMulti  = ["pie", "doughnut", "radar"].includes(chartType);

  // Destroy old chart before making new one
  if (previewChart) previewChart.destroy();

  previewChart = new Chart(
    document.getElementById("previewChart").getContext("2d"),
    {
      type: chartType,
      data: {
        labels: labels,
        datasets: [{
          data: values,
          backgroundColor: bgColors,
          borderColor: isMulti ? "#fff" : bgColors,
          borderWidth: isMulti ? 2 : 0,
          borderRadius: chartType === "bar" ? 6 : 0,
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: isMulti, position: "bottom" }
        }
      }
    }
  );
}

// ── FORM VALIDATION ──
function validateForm() {
  let isValid = true;

  // Clear old errors
  $(".text-danger").text("");

  // 1. Check title
  const title = $("#title").val().trim();
  if (!title) {
    $("#title-error").text("Please enter a story title.");
    isValid = false;
  } else if (title.length < 4) {
    $("#title-error").text("Title must be at least 4 characters.");
    isValid = false;
  }

  // 2. Check category
  if (!$("#category").val()) {
    $("#category-error").text("Please select a category.");
    isValid = false;
  }

  // 3. Check data rows
  const rows = parseRows($("#raw_data").val());
  if (rows.length < 2) {
    $("#data-error").text("Please enter at least 2 valid rows (Label, Value).");
    isValid = false;
  }

  return isValid;
}

// ── EVENT LISTENERS ──
$(document).ready(function () {

  // Live preview when user types
  $("#raw_data").on("input", function () {
    const rows = parseRows($(this).val());
    // Show row count
    $("#row-count").text(rows.length + " row(s) detected");
    renderPreview();
  });

  // Re-render when chart type changes
  $("input[name='chart_type']").on("change", function () {
    renderPreview();
  });

  // Validate on submit
  $("#storyForm").on("submit", function (e) {
    if (!validateForm()) {
      e.preventDefault(); // Stop form if invalid
      return;
    }
    // Show loading state
    $("#submitBtn")
      .prop("disabled", true)
      .html('<span class="spinner-border spinner-border-sm me-2"></span>Generating…');
  });

  // Initial render if textarea already has data (browser back button)
  if ($("#raw_data").val()) {
    renderPreview();
  }

});
