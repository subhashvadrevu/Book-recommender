const userInput = document.getElementById('user-input');
const suggestionList = document.querySelector('.show-suggestions')

userInput.addEventListener('input', async() => {
    let query = userInput.value.trim();
    if(query.length < 3)  {
        suggestionList.innerHTML = "";
        return;
    }

    try {
        const response = await fetch(`/suggestions?query=${query}`);
        const data = await response.json();
        
        suggestionList.innerHTML = "";   
        data.forEach(book => {
            let div = document.createElement('div');
            div.classList.add('suggestion-item');
            div.innerHTML = book ;
            div.onclick = function() {
                userInput.value = book;
                suggestionList.innerHTML = "";
            };

            suggestionList.appendChild(div);

        });


    } catch (error) {
        console.log('error fetching books', error)
    }

});