document.addEventListener("DOMContentLoaded", function () {
    const addToFavoritesButtons = document.querySelectorAll(".add-to-favorites");
    const removeFromFavoritesButtons = document.querySelectorAll(".remove-from-favorites");

    addToFavoritesButtons.forEach(button => {
        button.addEventListener("click", function () {
            const itemId = this.getAttribute("data-item-id");
            const itemType = this.getAttribute("data-item-type");
            fetch(addToFavoritesUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({
                    item_id: itemId,
                    item_type: itemType
                })
            })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    console.error("Failed to add to favorites:", response.statusText);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });

    removeFromFavoritesButtons.forEach(button => {
        button.addEventListener("click", function () {
            const itemId = this.getAttribute("data-item-id");
            const itemType = this.getAttribute("data-item-type");
            fetch(removeFromFavoritesUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({
                    item_id: itemId,
                    item_type: itemType
                })
            })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    console.error("Failed to remove from favorites:", response.statusText);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
