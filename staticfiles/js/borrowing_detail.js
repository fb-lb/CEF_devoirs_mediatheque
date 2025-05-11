document.addEventListener("DOMContentLoaded", function() {
    // Add event listener on media_id field in BorrowingMediaForm form
    const mediaInputBorrow = document.getElementById("media-id-borrow");
    const mediaInfoBorrow = document.getElementById("media-info-borrow");

    mediaInputBorrow.addEventListener("input", function() {
        const mediaId = this.value;

        if (mediaId) {
            fetch(`/bibliothecaire/get-media-details-borrowing/?media_id=${mediaId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        mediaInfoBorrow.innerHTML = `<p class="error">${data.error}</p>`;
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
                        memberInfoBorrow.innerHTML = `<p class="error">${data.error}</p>`;
                   } else {
                        memberInfoBorrow.innerHTML = `<p>${data.first_name} ${data.last_name}</p>`;
                        if (data.is_blocked == true) {
                            blockedParagraph = document.createElement('p');
                            blockedTextNode = document.createTextNode("Ce membre ne peut pas emprunter car il est interdit d'emprunt (il est en retard sur un emprunt à son nom)");
                            blockedParagraph.appendChild(blockedTextNode);
                            blockedParagraph.classList.add('error');
                            memberInfoBorrow.appendChild(blockedParagraph);
                        } else if (data.nb_current_borrowings >= 3) {
                            tooMuchParagraph = document.createElement('p');
                            tooMuchTextNode = document.createTextNode("Ce membre ne peut pas emprunter car il a déjà 3 emprunts enregistrés à son nom");
                            tooMuchParagraph.appendChild(tooMuchTextNode);
                            tooMuchParagraph.classList.add('error');
                            memberInfoBorrow.appendChild(tooMuchParagraph);
                        }
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
    noMediaReturn = document.getElementById('no-media-return');

    memberInputReturn.addEventListener('input', function() {
        memberId = this.value;
        if (memberId) {
            fetch(`/bibliothecaire/get-borrowed-media/?member_id=${memberId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        memberInfoReturn.innerHTML = `<p class='error'>${data.error}</p>`;
                        mediaSelectReturn.innerHTML = "";
                    } else if (data.empty) {
                        memberInfoReturn.innerHTML = `<p>${data.member_data.name}</p>`;
                        mediaSelectReturn.innerHTML = "";
                        noMediaReturn.innerHTML = `<p>${data.empty}</p>`;
                    } else {
                        memberInfoReturn.innerHTML = `<p>${data.member_data.name}</p>`;
                        noMediaReturn.innerHTML = "";
                        mediaSelectReturn.innerHTML = "";
                        data.media_choices.forEach(media => {
                            const option = document.createElement('option');
                            option.value = media.id;
                            option.dataset.type = media.type;
                            option.textContent = media.id + ' - ' + media.name + ' par ' + media.author + ' (' + media.type + ')';
                            mediaSelectReturn.appendChild(option);
                            today_date = new Date().toISOString().split('T')[0];
                            if (media.return_date < today_date) {
                                late_paragraph = document.createElement('p');
                                late_text = document.createTextNode("En retard pour le retour de l'emprunt : " + media.id + " - " + media.name + " par " + media.author + " (" + media.type + ")");
                                late_paragraph.appendChild(late_text);
                                late_paragraph.classList.add('error');
                                memberInfoReturn.appendChild(late_paragraph);
                            }
                        })
                    }
                })
        } else {
            memberInfoReturn.innerHTML = "";
            mediaSelectReturn.innerHTML = "";
            noMediaReturn.innerHTML = "";
        }
    })


    // Add event listener on search bar input which filter each line by their content
    const inputElement = document.getElementById('borrowing-search-bar');
    let debounceTimeout;

    inputElement.addEventListener("input", (event) => {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            const searchValue = event.target.value.toLowerCase();
            const allTrElements = document.querySelectorAll('tr');
            for (const tr of allTrElements) {
                tr.classList.remove('hidden-search');
                if (tr.classList.length == 0) {
                    continue;
                } else if (!tr.innerText.toLowerCase().includes(searchValue)) {
                    tr.classList.add('hidden-search');
                }
            }
        }, 500)
    });
});