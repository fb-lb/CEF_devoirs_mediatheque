// Add event listener on id field in UpdateMember form
document.addEventListener("DOMContentLoaded", function() {
    const memberInput = document.getElementById("member-id-update");
    const memberError = document.getElementById("member-error-update");
    const memberLastName = document.getElementById("member-last-name-update");
    const memberFirstName = document.getElementById("member-first-name-update");
    const memberIsBlocked = document.getElementById("member-is-blocked-update");

    memberInput.addEventListener("input", function() {
        const memberId = this.value;

        if (memberId) {
            fetch(`/bibliothecaire/get-member-details/?member_id=${memberId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        memberError.innerHTML = `<p style="color:red">${data.error}</p>`;
                        memberLastName.value = "";
                        memberFirstName.value = "";
                        memberIsBlocked.innerHTML = ""
                    } else {
                        memberLastName.value = data.last_name;
                        memberFirstName.value = data.first_name;
                        true_option = document.createElement('option');
                        true_option.value = "true";
                        true_option.textContent = "Oui";
                        memberIsBlocked.appendChild(true_option);
                        false_option = document.createElement('option');
                        false_option.value = "false";
                        false_option.textContent = "Non";
                        memberIsBlocked.appendChild(false_option);
                        if (data.is_blocked == true) {
                            memberIsBlocked.value = "true";
                        } else if (data.is_blocked == false) {
                            memberIsBlocked.value = "false";
                        }

                    }
                });
        } else {
            memberError.innerHTML = "";
            memberLastName.value = "";
            memberFirstName.value = "";
            memberIsBlocked.innerHTML = ""
        }
    })
})

// Add event listener on id field in DeleteMember form
document.addEventListener("DOMContentLoaded", function() {
    const memberInput = document.getElementById("member-id-delete");
    const memberInfo = document.getElementById("member-info-delete");

    memberInput.addEventListener("input", function() {
        const memberId = this.value;

        if (memberId) {
            fetch(`/bibliothecaire/get-member-details/?member_id=${memberId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        memberInfo.innerHTML = `<p style="color:red">${data.error}</p>`;
                    } else {
                        memberInfo.innerHTML = `<p>${data.last_name} ${data.first_name}</p>`;
                    }
                });
        } else {
            memberInfo.innerHTML = "";
        }
    })
})