let addresses = new Set()

function closeAnotherClick(not_include_class, close_object) {
    window.onclick = function (e) {
        if (!Array.from(e.target.classList).includes(not_include_class)) {
            close_object.style.display = 'none'
        }
    }
}

function create_result_item(result_lst, data) {
    result_lst.style.display = 'block'
    if (!Array.from(addresses).includes(data[0].result)) {
        let li = document.createElement('li')
        li.classList.add('list-group-item')
        addresses.add(data[0].result)
        li.innerHTML = data[0].result
        result_lst.append(li)
    }
}

function load_address(address) {
    return fetch(address_url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': "{{ csrf_token }}"
        },
        body: JSON.stringify({
            "address": address
        })
    })
}

let result_list = document.querySelector('.address-result')
let address_input = document.getElementById('address-input')

address_input.addEventListener('keyup', (e) => {
    let clean_address = load_address(e.target.value)
    clean_address.then((res) => res.json().then((data) => {
            if (data) {
                if (data.length === 1 || data) {
                    create_result_item(result_list, data)
                } else {
                    result_list.style.display = 'none'
                    result_list.innerHTML = ''
                }
            } else {
                result_list.style.display = 'none'
                result_list.innerHTML = ''
            }
        })
    )

    closeAnotherClick('list-group-item', result_list)

    result_list.childNodes.forEach((result) => {
        result.addEventListener('click', () => {
            address_input.value = result.innerHTML
            result_list.innerHTML = ''
            let new_address = load_address(result.innerHTML)
            new_address.then((res) => res.json().then((address) => {
                if (address) {
                    if (address.length > 0) {
                        create_result_item(result_list, address)
                    }
                }
            }))
        })
    })
})

result_list.addEventListener('mouseover', () => {
    result_list.childNodes.forEach((result) => {
        result.addEventListener('click', () => {
            address_input.value = result.innerHTML
            result_list.innerHTML = ''
            let new_address = load_address(result.innerHTML)
            new_address.then((res) => res.json().then((address) => {
                if (address) {
                    if (address.length > 0) {
                        create_result_item(result_list, address)
                    }
                }
            }))
        })
    })
})
