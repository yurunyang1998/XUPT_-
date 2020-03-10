let logout = document.getElementById('logout')
logout.onclick = function () {
    let xhr = new XMLHttpRequest;
    xhr.onreadystatechange = function () {
        if (xhr.status === 200 && xhr.readyState === 4) {

            window.location.href = "/index"

        }
    }
    xhr.open('GET', '/LogOut')
    xhr.send()
}