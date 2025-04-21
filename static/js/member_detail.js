// Add event listener on id field in UpdateMember form
document.addEventListener("DOMContentLoaded", function () {
    const memberInput = document.getElementById("member-id-update");
    const memberError = document.getElementById("member-error-update");
    const memberLastName = document.getElementById("member-last-name-update");
    const memberFirstName = document.getElementById("member-first-name-update");

    memberInput.addEventListener("input", function () {
        const memberId = this.value;

        if (memberId) {
            fetch(`/bibliothecaire/get-member-details/?member_id=${memberId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        memberError.innerHTML = `<p style="color:red">${data.error}</p>`;
                        memberLastName.value = "";
                        memberFirstName.value = "";
                    } else {
                        memberLastName.value = data.last_name;
                        memberFirstName.value = data.first_name;
                    }
                });
        } else {
            memberError.innerHTML = "";
            memberLastName.value = "";
            memberFirstName.value = "";
        }
    })
})

// Add event listener on id field in DeleteMember form
document.addEventListener("DOMContentLoaded", function () {
    const memberInput = document.getElementById("member-id-delete");
    const memberInfo = document.getElementById("member-info-delete");

    memberInput.addEventListener("input", function () {
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