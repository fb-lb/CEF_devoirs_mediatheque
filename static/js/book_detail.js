// Add event listener on id field in DeleteBook form
document.addEventListener("DOMContentLoaded", function () {
    const bookInput = document.getElementById("book-id-delete");
    const bookInfo = document.getElementById("book-info-delete");

    bookInput.addEventListener("input", function () {
        const bookId = this.value;

        if (bookId) {
            fetch(`/bibliothecaire/get-book-details/?book_id=${bookId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        bookInfo.innerHTML = `<p style="color:red;">${data.error}</p>`;
                    } else {
                        bookInfo.innerHTML = `<p>${data.title} par ${data.author}</p>`;
                    }
                });
        } else {
            bookInfo.innerHTML = "";
        }
    });
});

// Add event listener on id field in UpdateBook form
document.addEventListener("DOMContentLoaded", function () {
    const bookInput = document.getElementById("book-id-update");
    const bookInfo = document.getElementById("book-error-update");
    const bookName = document.getElementById("book-name-update");
    const bookAuthor = document.getElementById("book-author-update");

    bookInput.addEventListener("input", function () {
        const bookId = this.value;

        if (bookId) {
            fetch(`/bibliothecaire/get-book-details/?book_id=${bookId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        bookInfo.innerHTML = `<p style="color:red;">${data.error}</p>`;
                        bookName.value = '';
                        bookAuthor.value = '';
                    } else {
                        bookInfo.innerHTML = "";
                        bookName.value = data.title;
                        bookAuthor.value = data.author;
                    }
                });
        } else {
            bookInfo.innerHTML = "";
            bookName.value = '';
            bookAuthor.value = '';
        }
    });
});