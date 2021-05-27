function moveCheckboxes() {
    const $routeTypeUL = $('#id_route_type');
    const $difficultyUL = $('#id_difficulty');
    const $filterForm = $('#filter-form');
    const $formChildren = $filterForm.children();
    const $routeTypeP = $formChildren.eq(3);
    const $difficultyP = $formChildren.eq(6);
    $routeTypeUL.appendTo($routeTypeP);
    $difficultyUL.appendTo($difficultyP);
}

function displayStars() {
    const $ratingInput = $('#id_rating_gte');
    $ratingInput.hide();
    currentRating = $ratingInput.val();
    const $starDiv = $('<div class="star-div">');
    $starDiv.insertBefore($ratingInput);
    for (let i=0; i<5; i++) {
        $star = $('<i class="fas fa-star rating"></i>');
        $star.attr('id', `star${i}`);
        if (i<currentRating) {
            $star.addClass('filled');
        };
        $star.appendTo($starDiv);
        $star.on('click', colorStars)
    };
    const $starText = $('<p id="star-text">');
    $starText.appendTo($starDiv);
};

function colorStars(e) {
    const $ratingInput = $('#id_rating_gte');
    const $starText = $('#star-text');
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
    $starText.text(`${rating} and up`);
};

function addPlaceholder() {
    const $minLength = $('#id_length_0');
    const $maxLength = $('#id_length_1');
    $minLength.attr('placeholder','Min (miles)');
    $maxLength.attr('placeholder','Max (miles)');
}
moveCheckboxes();
displayStars();
addPlaceholder();
