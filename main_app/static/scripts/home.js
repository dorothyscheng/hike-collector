homePhotoArr=[
    'https://images.unsplash.com/photo-1594376764040-6bf8f76b47e4?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=2064&q=80',
    'https://images.unsplash.com/photo-1559010766-cfdb07342084?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=2071&q=80',
    'https://images.unsplash.com/photo-1605999212840-4c6e2c4f8d57?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1994&q=80',
]

function changePhoto() {
    const $homeHead = $('#home-head');
    let photoIndex = 0;
    let photoInterval = setInterval(()=>{
        photoIndex++;
        if (photoIndex > homePhotoArr.length-1) {
            photoIndex = 0;
        };
        $homeHead.css('background-image',`url("${homePhotoArr[photoIndex]}")`);
    }, 5000);
}

changePhoto()