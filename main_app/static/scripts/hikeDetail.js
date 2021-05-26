$allPhotos = $('.detail-photo');

function displayPhoto(e) {
    console.log('clicked');
    const $selectedPhoto = $(e.target);
    const imageURL = $selectedPhoto.attr('src');
    const $photoModal = $('#photo-modal');
    $('#selected-img').attr('src', imageURL);
    $photoModal.show();
    window.addEventListener('click', (e) => {
        if (e.target == document.getElementById('modal-content')) {
            $photoModal.hide();
        };
    });
};

$allPhotos.on('click',displayPhoto);