document.addEventListener("DOMContentLoaded", function () {
    // Add event listener on media_id field in BorrowingMediaForm form
    const mediaInputBorrow = document.getElementById("media-id-borrow");
    const mediaInfoBorrow = document.getElementById("media-info-borrow");
    const mediaChoiceBorrow = document.getElementById("media-type-borrow")

    mediaInputBorrow.addEventListener("input", function () {
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

    memberInputBorrow.addEventListener("input", function () {
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
});