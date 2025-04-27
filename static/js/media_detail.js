document.addEventListener("DOMContentLoaded", function() {
    // Add event listener on id field in DeleteMedia form
    const mediaInputDelete = document.getElementById("media-id-delete");
    const mediaInfoDelete = document.getElementById("media-info-delete");

    mediaInputDelete.addEventListener("input", function() {
        const mediaId = this.value;
        const mediaTypeElement = document.getElementById("media-type-delete");
        const mediaType = mediaTypeElement.value;

        if (mediaId) {
            fetch(`/bibliothecaire/get-media-details-management/?media_id=${mediaId}&media_type=${mediaType}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        mediaInfoDelete.innerHTML = `<p style="color:red;">${data.error}</p>`;
                    } else {
                        mediaInfoDelete.innerHTML = `<p>${data.title} par ${data.author}</p>`;
                    }
                });
        } else {
            mediaInfoDelete.innerHTML = "";
        }
    });


    // Add event listener on id field in UpdateMedia form
    const mediaInputUpdate = document.getElementById("media-id-update");
    const mediaInfoUpdate = document.getElementById("media-error-update");
    const mediaNameUpdate = document.getElementById("media-name-update");
    const mediaAuthorUpdate = document.getElementById("media-author-update");

    mediaInputUpdate.addEventListener("input", function() {
        const mediaId = this.value;
        const mediaTypeElement = document.getElementById("media-type-update");
        const mediaType = mediaTypeElement.value;

        if (mediaId) {
            fetch(`/bibliothecaire/get-media-details-management/?media_id=${mediaId}&media_type=${mediaType}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        mediaInfoUpdate.innerHTML = `<p style="color:red;">${data.error}</p>`;
                        mediaNameUpdate.value = "";
                        mediaAuthorUpdate.value = "";
                    } else {
                        mediaInfoUpdate.innerHTML = "";
                        mediaNameUpdate.value = data.title;
                        mediaAuthorUpdate.value = data.author;
                    }
                });
        } else {
            mediaInfoUpdate.innerHTML = "";
            mediaNameUpdate.value = "";
            mediaAuthorUpdate.value = "";
        }
    });
});