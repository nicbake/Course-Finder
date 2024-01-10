const cardgen = (courseName, courseDescription, coursePreReq, courseCredits, courseSem) => {
        
    // Column adds left and right lines
    let column = document.createElement('div');
    
    // Card elements, the card, its header, and its text content inside body
    let card = document.createElement('div');
    let header = document.createElement('div');  
    let body = document.createElement('div');
    let text = document.createElement('div');

    //Extra stuff 
    let preText = document.createElement('div');
    let creditText = document.createElement('div');
    let semText = document.createElement('div');

    // Add classes to the divs
    column.classList.add("col");
    column.classList.add("card-padding");
    card.classList.add("card");
    header.classList.add("card-header");
    body.classList.add("card-body");
    text.classList.add("card-text");

    preText.classList.add("card-text");
    creditText.classList.add("card-text");
    semText.classList.add("card-text");

    header.textContent = courseName;
    text.textContent = courseDescription;

    preText.textContent = coursePreReq;
    creditText.textContent = courseCredits;
    semText.textContent = courseSem;

    // Append order
    card.append(header);
    body.append(text);
    if (preText.textContent != "Prerequisites: ") {
        body.append(preText);
    }
    body.append(creditText);
    body.append(semText);
    card.append(body);
    column.append(card);
    return (column);
}

export default cardgen