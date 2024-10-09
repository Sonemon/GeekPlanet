document.addEventListener('DOMContentLoaded', function () {
    const userModal = document.getElementById('userModal');

    userModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const geekData = JSON.parse(button.getAttribute('data-geek'));

        // modal content
        const modalTitle = userModal.querySelector('.modal-title');
        const modalBody = userModal.querySelector('#userModalContent');

        modalTitle.textContent = `Details for ${geekData.username}`;
        modalBody.innerHTML = `
            <p><strong>Username:</strong> ${geekData.username}</p>
            <p><strong>Friends:</strong> ${geekData.friends} friend${geekData.friends !== 1 ? 's' : ''}</p>
        `;

        const viewProfileButton = document.getElementById("viewProfileButton");
        viewProfileButton.href = `/geeks/${geekData.id}/`;
        viewProfileButton.style.display = "inline";
    });
});
