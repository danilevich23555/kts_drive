function UUIDv4() {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

const rawApiUrl = document.getElementById('api-host').attributes['data-host'].value
const apiUrl = rawApiUrl !== '{{API_HOST}}' ? rawApiUrl : 'http://0.0.0.0:8888';


const request = async ({uri, method = 'GET', data = null, headers = {}, is_json = false}) => { // TODO: сделать объект, добавить async
    if (is_json) {
        headers['Content-Type'] = 'application/json';
    }

    const resp = await fetch(
        `${apiUrl}/${uri}`,
        {
            method,
            body: is_json && !!data ? JSON.stringify(data) : data,
            headers,
        },
    )
    if (!resp.ok) {
        alert(`Request failed: ${method} ${uri} -> ${resp.status} ${await resp.text()}`);
        return null
    }
    return await resp.json();
}


const createElement = ({tag = 'div', id = null, classnames = [], attributes = {}, text = null}) => {
    let elem = document.createElement(tag);
    if (id !== null) {
        elem.id = id;
    }
    if (classnames?.length) {
        elem.classList.add(...classnames);
    }
    if (attributes) {
        for (const key in attributes) {
            elem.attributes[key] = attributes[key];
        }
    }
    if (text !== null) {
        elem.innerText = text;
    }
    return elem;
}


const formatDate = (date) => {
    if (typeof date == 'string') {
        date = new Date(Date.parse(date));
    }
    return `${date.toLocaleTimeString()} ${date.toLocaleDateString()}`
}

const formatSize = (size) => {
    const sizes = ['Б', 'Кб', 'Мб', 'Гб'];
    for (let i = 0; i < sizes.length; i++) {
        if (size < 1024) {
            return `${size.toFixed(2)} ${sizes[i]}`;
        }
        size /= 1024;
    }
    return 'вы серьезно?'
}
