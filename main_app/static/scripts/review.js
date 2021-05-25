const $ratingInput = $('#id_rating');

function createStars() {
    $ratingInput.hide();
    currentRating = $ratingInput.val();
    for (let i=0; i<5; i++) {
        $star = $('<i class="fas fa-star rating"></i>');
        $star.attr('id', `star${i}`);
        if (i<currentRating) {
            $star.addClass('filled');
        };
        $star.insertBefore($ratingInput);
        $star.on('click', colorStars)
    };
};

function colorStars(e) {
    for (let i=0; i<5; i++) {
        $star = $(`#star${i}`);
        $star.removeClass('filled');
    };
    selectedStar = $(e.target);
    selectedStarId = Number(selectedStar.attr('id').slice(4));
    for (let i=0; i<=selectedStarId; i++) {
        $star = $(`#star${i}`);
        $star.addClass('filled');
    };
    rating = selectedStarId+1;
    $ratingInput.val(rating);
};

createStars();