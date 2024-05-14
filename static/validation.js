function validateform()
{
    
    var amount = document.getElementById("amount").value;
    var description = document.getElementById("description").value;
    var date = document.getElementById("date").value;
    var category = document.getElementById("category").value;

    if (amount == "" || description == "" || date == "" || category == "")
        {
            alert("Please enter all fields");
            return false;
        }
    return true;
}


function search()
{
    var form = document.getElementById("search_form");
    var query = document.getElementById("query").value;
    if (query == null || query == "") 
    {
        alert("Please enter search criteria");
        return false; // Prevent further execution
    }
    var xhr = new Htt
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/search', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
    if (xhr.readyState == 4 && xhr.status == 200) {
        document.getElementById('resultsBody').innerHTML = xhr.responseText;
    }
    };
    xhr.send('query=' + query);
    return false; // Prevent form submission
}


function toggleEditSave(button) {
    const row = button.closest('tr');
    const inputs = row.querySelectorAll('input');
    if (button.textContent === 'Edit') {
        inputs.forEach(input => input.removeAttribute('disabled'));
        button.textContent = 'Save';
    } else {
        inputs.forEach(input => input.removeAttribute('disabled'));
        // Add a hidden form to handle the save operation
        const form = document.createElement('form');
        form.action = '/edit';
        form.method = 'post';
        inputs.forEach(input => {
            const clone = input.cloneNode();
            clone.removeAttribute('disabled');
            form.appendChild(clone);
        });
        document.body.appendChild(form);
        form.submit();
    }
}