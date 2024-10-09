document.addEventListener('DOMContentLoaded', function () {
    const userModal = document.getElementById('userModal');

    userModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // Кнопка, которая открыла модальное окно
        const geekData = JSON.parse(button.getAttribute('data-geek')); // Получаем данные о пользователе

        // Заполняем модальное окно данными
        const modalTitle = userModal.querySelector('.modal-title');
        const modalBody = userModal.querySelector('#userModalContent');

        modalTitle.textContent = `Details for ${geekData.username}`;
        modalBody.innerHTML = `
            <p><strong>Username:</strong> ${geekData.username}</p>
            <p><strong>Friends:</strong> ${geekData.friends} friend${geekData.friends !== 1 ? 's' : ''}</p>
        `;
    });
});
