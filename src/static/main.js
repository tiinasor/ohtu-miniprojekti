// form type handling
const typeSelect = document.getElementById("citation_type");
const fieldBlocks = document.querySelectorAll(".citation-fields");
const formElement = document.querySelector(".form-panel form");
const saveButton = document.getElementById("save_button");
const cancelEditBtn = document.getElementById("cancel_edit");

function updateFields() {
    if (!typeSelect) return;
    const selected = typeSelect.value;
    fieldBlocks.forEach(b => {
        const isSelected = b.dataset.type === selected;
        b.style.display = isSelected ? "block" : "none";
        b.querySelectorAll("input, select, textarea").forEach(input => {
            input.disabled = !isSelected;
        });
    });
}

function enterCreateMode() {
    if (saveButton) saveButton.textContent = "Save citation";
    if (cancelEditBtn) cancelEditBtn.style.display = "none";
    if (formElement) formElement.action = "/create_citation";
    if (typeSelect) {
        typeSelect.value = "article";
        updateFields();
    }
}

function enterEditMode() {
    if (saveButton) saveButton.textContent = "Update citation";
    if (cancelEditBtn) cancelEditBtn.style.display = "inline-block";
    if (formElement) formElement.action = "/create_citation";
}

if (typeSelect) {
    updateFields();
    typeSelect.addEventListener("change", updateFields);
    enterCreateMode();
}

// selection + global edit/delete
let selectedCitation = null;

const rows = document.querySelectorAll(".list-panel tbody tr");
const editBtn = document.getElementById("edit_selected");
const deleteBtn = document.getElementById("delete_selected");
const deleteForm = document.getElementById("delete_selected_form");


// global Delete: confirm, then submit the form
if (deleteForm) {
    deleteForm.addEventListener("submit", function (event) {
        if (!selectedCitation) {
            event.preventDefault();
            return;
        }
        const name = selectedCitation.name || "this citation";
        const ok = window.confirm(`Are you sure you want to remove "${name}"?`);
        if (!ok) {
            event.preventDefault();
        }
    });
}

// search functionality
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search");
    if (!searchInput) return;

    searchInput.addEventListener("input", () => {
        const filter = searchInput.value.toLowerCase();
        const rows = document.querySelectorAll(".citation");

        rows.forEach(row => {
            // this makes all data inserted in any ref field one string for searching.
            const values = Object.values(row.dataset).map(v => v.toLowerCase());
            const text = values.join(" ");
            row.style.display = text.includes(filter) ? "" : "none";
        });
    });
});

// validate selection for generating bibtex
function validateSelection(event) {
    const checkboxes = document.querySelectorAll('input[name="selected[]"]:checked');
    if (checkboxes.length === 0) {
        event.preventDefault();
        alert("Please select at least one citation");
        return false;
    }
    return true;
}

let originalRows = null;
let lastCol = null;
let lastDir = null;

function sortColumn(col, direction) {
    const table = document.getElementById("sortable");
    const tbody = table.querySelector("tbody");
    let rows = Array.from(tbody.querySelectorAll("tr"));

    if (!originalRows) {
        originalRows = rows.map(r => r.cloneNode(true));
    }

    if (col === lastCol && direction === lastDir) {
        resetSorting();
        return;
    }

    lastCol = col;
    lastDir = direction;

    rows.sort((a, b) => {
        let A = a.children[col].innerText.trim();
        let B = b.children[col].innerText.trim();

        const nA = parseFloat(A);
        const nB = parseFloat(B);

        if (!isNaN(nA) && !isNaN(nB)) {
            return direction === "asc" ? nA - nB : nB - nA;
        }

        return direction === "asc"
            ? A.localeCompare(B)
            : B.localeCompare(A);
    });

    tbody.innerHTML = "";
    rows.forEach(r => tbody.appendChild(r));

    highlightArrows(col, direction);
}

function resetSorting() {
    const tbody = document.querySelector("#sortable tbody");
    tbody.innerHTML = "";
    originalRows.forEach(r => tbody.appendChild(r.cloneNode(true)));

    lastCol = null;
    lastDir = null;

    highlightArrows(null, null);
}

function highlightArrows(col, direction) {
    const ups = document.querySelectorAll(".sort-up");
    const downs = document.querySelectorAll(".sort-down");

    ups.forEach(el => el.style.opacity = "0.3");
    downs.forEach(el => el.style.opacity = "0.3");

    if (col === null) return;

    if (direction === "asc") {
        document.querySelectorAll(".sort-up")[col].style.opacity = "1";
    } else if (direction === "desc") {
        document.querySelectorAll(".sort-down")[col].style.opacity = "1";
    }
}

function showNotification(message, isError = false) {
    const notification = document.getElementById("download-notification");
    if (notification) {
        notification.textContent = message;
        notification.style.backgroundColor = isError ? "#f8d7da" : "#d4edda";
        notification.style.borderColor = isError ? "#f5c6cb" : "#c3e6cb";
        notification.style.color = isError ? "#721c24" : "#155724";
        notification.style.display = "block";
        
        setTimeout(() => {
            notification.style.display = "none";
        }, 3000);
    }
}

function downloadBibTexSelected(event) {
    event.preventDefault();
    
    // Validate selection
    const checkboxes = document.querySelectorAll('input[name="selected[]"]:checked');
    if (checkboxes.length === 0) {
        alert("Please select at least one citation");
        return false;
    }
    
    // Get selected IDs
    const formData = new FormData();
    checkboxes.forEach(cb => {
        formData.append("selected[]", cb.value);
    });
    
    // Make AJAX request
    fetch("/generate_bibtex_selected", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(text || "Failed to generate BibTeX file");
            });
        }
        return response.blob();
    })
    .then(blob => {
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "selected_citations.bib";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        // Show success notification
        showNotification("File downloaded successfully");
    })
    .catch(error => {
        showNotification("Error: " + error.message, true);
    });
    
    return false;
}

function downloadBibTexAll(event) {
    event.preventDefault();
    
    // Make AJAX request
    fetch("/generate_bibtex", {
        method: "POST"
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(text || "Failed to generate BibTeX file");
            });
        }
        return response.blob();
    })
    .then(blob => {
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "citations.bib";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        // Show success notification
        showNotification("File downloaded successfully");
    })
    .catch(error => {
        showNotification("Error: " + error.message, true);
    });
    
    return false;
}