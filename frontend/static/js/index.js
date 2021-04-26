function call_click() {
    console.log('click')
    const counter = document.getElementById('counter')
    counter.textContent = (parseInt(counter.innerText) + 1) + " $"
    var x = new XMLHttpRequest();
    x.open("GET", "api/call_click/", true);
    x.send();
}