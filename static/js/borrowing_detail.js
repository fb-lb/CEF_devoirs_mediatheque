document.addEventListener("DOMContentLoaded", function() {
    // Add event listener on media_id field in BorrowingMediaForm form
    const mediaInputBorrow = document.getElementById("media-id-borrow");
    const mediaInfoBorrow = document.getElementById("media-info-borrow");
    const mediaChoiceBorrow = document.getElementById("media-type-borrow")

    mediaInputBorrow.addEventListener("input", function() {
        const mediaId = this.value;
        const mediaType = mediaChoiceBorrow.value

        if (mediaId) {
            fetch(`/bibliothecaire/get-media-details/?media_id=${mediaId}&media_type=${mediaType}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        mediaInfoBorrow.innerHTML = `<p style="color:red;">${data.error}</p>`;
                    } else {
                        mediaInfoBorrow.innerHTML = `<p>${data.title} par ${data.author}</p>`;
                    }
                });
        } else {
            mediaInfoBorrow.innerHTML = "";
        }
    });

    // Add event listener on member_id field in BorrowingMediaForm form
    const memberInputBorrow = document.getElementById("member-id-borrow");
    const memberInfoBorrow = document.getElementById("member-info-borrow");

    memberInputBorrow.addEventListener("input", function() {
        memberId = this.value;
        if (memberId) {
            fetch(`/bibliothecaire/get-member-details/?member_id=${memberId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error){
                        memberInfoBorrow.innerHTML = `<p style="color:red;">${data.error}</p>`;
                   } else {
                        memberInfoBorrow.innerHTML = `<p>${data.first_name} ${data.last_name}</p>`;
                    }
                })

        } else {
            memberInfoBorrow.innerHTML = "";
        }
    })

    // Add event listener on member_id field in ReturnMediaForm form
    memberInputReturn = document.getElementById('member-id-return');
    memberInfoReturn = document.getElementById('member-info-return');
    mediaSelectReturn = document.getElementById('media-select-return');
    mediaTypeReturn = document.getElementById('media-type-return')
    noMediaReturn = document.getElementById('no-media-return')

    memberInputReturn.addEventListener('input', function() {
        memberId = this.value;
        if (memberId) {
            fetch(`/bibliothecaire/get-borrowed-media/?member_id=${memberId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        memberInfoReturn.innerHTML = `<p>${data.error}</p>`;
                        mediaSelectReturn.innerHTML = ""
                        mediaTypeReturn.value = ""
                    } else if (data.empty) {
                        memberInfoReturn.innerHTML = `<p>${data.member_data.name}</p>`
                        mediaSelectReturn.innerHTML = ""
                        noMediaReturn.innerHTML = `<p>${data.empty}</p>`
                        mediaTypeReturn.value = ""
                    } else {
                        memberInfoReturn.innerHTML = `<p>${data.member_data.name}</p>`
                        noMediaReturn.innerHTML = "";
                        mediaSelectReturn.innerHTML = "";
                        data.media_choices.forEach(media => {
                            const option = document.createElement('option');
                            option.value = media.id;
                            option.dataset.type = media.type
                            option.textContent = media.id + ' - ' + media.name + ' par ' + media.author + ' (' + media.type + ')';
                            mediaSelectReturn.appendChild(option);
                        mediaTypeSelected = mediaSelectReturn.options[mediaSelectReturn.selectedIndex]
                        mediaTypeReturn.value = mediaTypeSelected.dataset.type
                        })
                    }
                })
        } else {
            memberInfoReturn.innerHTML = "";
            mediaSelectReturn.innerHTML = "";
            mediaTypeReturn.value = ""
            noMediaReturn.innerHTML = "";
        }
    })

    // Add event listener on media_id field in ReturnMediaForm form
    mediaSelectReturn.addEventListener("change", function() {
        mediaTypeSelected = this.options[this.selectedIndex]
        mediaTypeReturn.value = mediaTypeSelected.dataset.type
    })
});