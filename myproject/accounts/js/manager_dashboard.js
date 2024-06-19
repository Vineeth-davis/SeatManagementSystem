document.addEventListener("DOMContentLoaded", function() {
    const addMemberForm = document.getElementById("addMemberForm");
    const bookSeatForm = document.getElementById("bookSeatForm");
    const cancelBookingForm = document.getElementById("cancelBookingForm");

    if (addMemberForm) {
        addMemberForm.addEventListener("submit", function(e) {
            e.preventDefault();
            const usernames = document.getElementById("usernames").value;
            fetch(addMemberForm.action, {
                method: "POST",
                body: new URLSearchParams(new FormData(addMemberForm)),
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("Members added successfully");
                        location.reload();
                    } else {
                        alert("Error: " + data.message);
                    }
                });
        });
    }

    // Similar handlers can be added for bookSeatForm and cancelBookingForm
});
