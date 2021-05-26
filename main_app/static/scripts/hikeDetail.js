$allPhotos = $('.detail-photo');

function left() {
    changePhoto(-1);
};
function right() {
    changePhoto(1);
};

function changePhoto(direction) {
    const currentIndex = Number($('.selected-img').attr('id').slice(5));
    let nextIndex = direction + currentIndex;
    if (nextIndex > $allPhotos.length - 1) {
        nextIndex = 0;
    } else if (nextIndex < 0) {
        nextIndex = $allPhotos.length - 1;
    }
    $nextPhoto = $allPhotos.eq(nextIndex);
    nextURL = $nextPhoto.attr('src');
    $('.selected-img').attr('src', nextURL);
    $('.selected-img').attr('id', `photo${nextIndex}`);
};

function displayPhoto(e) {
    const $selectedPhoto = $(e.target);
    const currentIndex = $selectedPhoto.index();
    const imageURL = $selectedPhoto.attr('src');
    const $photoModal = $('#photo-modal');
    $('.selected-img').attr('src', imageURL);
    $('.selected-img').attr('id', `photo${currentIndex}`);
    $photoModal.show();
    window.addEventListener('click', (e) => {
        if (e.target == document.getElementById('modal-content')) {
            $photoModal.hide();
        };
    });
};

$allPhotos.on('click', displayPhoto);
$('#left').on('click', left);
$('#right').on('click', right);