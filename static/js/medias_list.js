document.addEventListener("DOMContentLoaded", () => {
    // Add event listener on select element which filter each line by their type
    const selectElement = document.getElementById('media-filter');
    selectElement.addEventListener("change", (event) => {
        const optionSelected = event.target.value;
        const allTrElements = document.querySelectorAll('tr');
        for (const tr of allTrElements) {
            tr.classList.remove('hidden-select');
            if (tr.classList.length == 0) {
                continue;
            } else if (optionSelected == 'all') {
                continue
            } else if (tr.classList.contains(optionSelected)) {
                continue
            } else {
                tr.classList.add('hidden-select');
            }
        }
    });

    // Add event listener on search bar input which filter each line by their content
    const inputElement = document.getElementById('media-search-bar');
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
})