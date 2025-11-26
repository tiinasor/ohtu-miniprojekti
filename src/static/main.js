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

function clearSelection() {
    rows.forEach(r => r.classList.remove("selected-row"));
    selectedCitation = null;
    if (editBtn) editBtn.disabled = true;
    if (deleteBtn) deleteBtn.disabled = true;
    if (deleteForm) deleteForm.action = "";
}

rows.forEach(row => {
    row.addEventListener("click", function () {
        rows.forEach(r => r.classList.remove("selected-row"));
        this.classList.add("selected-row");

        selectedCitation = {
            id: this.dataset.id,
            name: this.dataset.name,
            type: this.dataset.type
        };

        if (editBtn) editBtn.disabled = false;
        if (deleteBtn) deleteBtn.disabled = false;
        if (deleteForm && selectedCitation.id) {
            deleteForm.action = `/remove/${selectedCitation.id}`;
        }
    });
});

// click outside table should clear selection
document.addEventListener("click", function (event) {
    const listPanel = document.querySelector(".list-panel");
    if (!listPanel) return;

    const table = listPanel.querySelector("table");
    const actions = listPanel.querySelector(".list-actions");

    // if click is inside table or inside the edit/delete button row, keep selection
    if ((table && table.contains(event.target)) ||
        (actions && actions.contains(event.target))) {
        return;
    }

    clearSelection();
});

// global Edit: switch to correct form type and change button text
if (editBtn) {
    editBtn.addEventListener("click", function () {
        if (!selectedCitation || !typeSelect) return;

        typeSelect.value = selectedCitation.type || "article";
        updateFields();

        enterEditMode();

        const formPanel = document.querySelector(".form-panel");
        if (formPanel) {
            formPanel.scrollIntoView({ behavior: "smooth" });
        }
    });
}

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

// cancel edit: reset form and selection
if (cancelEditBtn) {
    cancelEditBtn.addEventListener("click", function () {
        if (formElement) formElement.reset();
        enterCreateMode();
        clearSelection();
    });
}
