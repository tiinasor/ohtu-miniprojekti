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