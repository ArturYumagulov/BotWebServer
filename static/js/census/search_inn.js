let inn = document.getElementById('innId')
let innDiv = document.getElementById('innDivId')
let active_check = document.getElementById('workCheckbox')
let searchBlock = document.getElementById('innSearchUl')
let out = document.querySelector('.out')
let orgNameDiv = document.getElementById('organizationsNameDivId')
const closeCheckbox = document.getElementById('closeCheckbox')
const workCheckbox = document.getElementById('workCheckbox')
const communicateCheckbox = document.getElementById('communicateCheckbox')
let orgNameInput = document.getElementById('organizationsNameId')

let partnersInn = inn.getAttribute('data-url')

function cleanSearchBlock(searchBlock) {
    for (let i = 1; i < searchBlock.children.length; i++) {
        searchBlock.children[i].remove()
    }
}
function createFloatDiv(element, category_name, text="", sub_text="") {
    return `<div class="form-floating mb-3" id="${category_name}${element.id}DivId">
            <input class="form-control" name="${category_name}_${element.id}" id="${category_name}_${element.id}" 
            type="text" placeholder="${text} ${element.text} ${sub_text}" aria-describedby="${category_name}IdFeedback" required>
            <label for="${category_name}Id">${text} ${element.text} ${sub_text}</label>
            <div id="${category_name}IdFeedback" class="invalid-feedback">Укажите ${text} ${element.text}</div>
            </div>`
        }
function LoadMultiDivData(element, url) {
    return fetch(url, {
        headers: {"X-CSRFToken": csrf},
        method: "POST",
        body: JSON.stringify({department: depart})
    }).then((res) => res.json())
        .then((data) => {
            return data})
        }

function LengthValue(item, event, data) {
    let inn_value = item.value
    if (inn_value.length !== 10 && inn_value.length !== 12){
        inn.classList.add('is-invalid')
        inn.classList.remove('mb-3', 'is-valid')
        document.getElementById('innIdFeedback').innerHTML = 'Длина ИНН должна содержать 10 или 12 символов'
        document.getElementById('organizationsNameId').value = ''
    }  else if (data.length <= 0) {
        inn.classList.add('is-invalid')
        inn.classList.remove('mb-3', 'is-valid')
        innDiv.classList.add('is-invalid')
        document.getElementById('innIdFeedback').innerHTML = 'Проверьте правильность введенного ИНН'
        inn.setAttribute('required', '')
    } else {
        item.classList.remove('is-invalid')
        item.classList.add('is-valid')
    }
}

function HideSearchBlock(hide=false) {
    if (hide) {
        searchBlock.style.display = 'none'
        inn.classList.add('mb-3')
    } else {
        inn.classList.remove('mb-3')
        searchBlock.style.display = 'block'
    }
}

function createSearchElem(searchBlock, item, source) {
    let li = document.createElement('li')
    li.classList.add('result-inn')
    li.style.cursor = 'pointer'
    li.innerHTML = `${item.name}`
    li.setAttribute('data-inn', item.inn)
    li.setAttribute('data-name', item.name)
    li.setAttribute('data-source', item.source)
    searchBlock.append(li)
}

function LoadInnSearchBlock(url, event) {
    fetch(url, {
        headers: {"X-CSRFToken": csrf},
        body: JSON.stringify({searchInn: event.target.value}),
        method: "POST",
    }).then((res) => res.json()).then(
        (data) => {
            // if (window.location.pathname !== '/census/census-template/') {  // Выключил проверку ИНН
            LengthValue(inn, event, data)
            // } else
            {
                if (data.length > 0) {
                data.forEach((item) => {
                    if (item.source === "out") {
                        HideSearchBlock(false)
                        out.innerHTML = "Данный ИНН существует в 1С"
                        innDiv.classList.remove('mb-3')
                        createSearchElem(searchBlock, item)

                        let results_list = document.querySelectorAll('.result-inn')
                        let contragent = document.getElementById('searchClient')
                        // let orgDiv = document.getElementById('organizationsNameDivId')

                        results_list.forEach((item) => {
                            item.addEventListener('click', () => {
                                active_check.checked = true
                                try {
                                    document.getElementById('communicateCheckbox').setAttribute('disabled', '')
                                } catch (TypeError) {}
                                document.getElementById('closeCheckbox').setAttribute('disabled', '')
                                HideSearchBlock(true)
                                let items = document.querySelectorAll('.result-inn')
                                items.forEach((item) => {
                                    item.remove()
                                })
                                contragent.style.display = 'block'
                                contragent.value = item.getAttribute('data-inn')
                                contragent.classList.add('is-valid')
                                contragent.setAttribute('required', '')
                                // inn.value = ''
                                inn.removeAttribute('required')
                                inn.classList.remove('is-valid')
                                innDiv.style.display = 'none'
                                orgNameDiv.style.display = 'none'
                                orgNameDiv.children[0].removeAttribute('required')
                                orgNameDiv.children[0].classList.remove('is-invalid')
                            })
                        })

                    } else {
                        HideSearchBlock(false)
                        out.innerHTML = ''
                        innDiv.classList.remove('mb-3')
                        createSearchElem(searchBlock, item)

                        let results_list = document.querySelectorAll('.result-inn')
                        results_list.forEach((item) => {
                            item.addEventListener('click', () => {
                                // HideSearchBlock(true)
                                let orgName = document.getElementById('organizationsNameId')
                                orgName.value = item.getAttribute('data-name')
                                orgName.classList.remove('is-invalid')
                                orgName.classList.add('is-valid')
                                inn.value = item.getAttribute('data-inn')
                                HideSearchBlock(searchBlock)
                            })
                        })
                    }
                })
            }
            }
            // LengthValue(inn, event, data)

        })
}

function loadValidPartners() {
    let search = document.getElementById('searchClient')
    let partners = document.getElementById('todo-app').dataset.search
    let dataList = document.getElementById('contragentsListOptions')

        // Поиск контрагентов
    search.addEventListener('keyup', function (e) {
        let searchValue = e.target.value;
        if (searchValue.trim().length > 0) {
            fetch(partners,
                {
                    headers: {"X-CSRFToken": csrf},
                    body: JSON.stringify({searchText: searchValue}),
                    method: "POST",
                }).then((res) => res.json())
                .then((data) => {
                    if (data.length === 0) {
                        dataList.style.display = 'block'
                        search.classList.remove('mb-3')
                        dataList.innerHTML = '<li class="list-group-item">Ничего не найдено</li>'
                    } else {
                        dataList.style.display = 'block'
                        dataList.innerHTML = ''
                        search.classList.remove('mb-3')
                        data.forEach((i) => {
                            let item = document.createElement('li')
                            item.setAttribute('id', 'result')
                            item.setAttribute('data-inn', i.inn)
                            item.classList.add('list-group-item')
                            item.style.cursor = 'pointer'
                            item.innerHTML = i.name + ' - ' + i.inn
                            dataList.append(item)
                        })
                        let find_item = document.querySelectorAll('#result')
                        find_item.forEach((ii) => {
                            ii.addEventListener('click', function (){
                                ii.classList.add('bg-secondary')
                                search.value = ii.dataset.inn
                                inn.value = ii.dataset.inn
                                if (search.value.length > 0) {
                                    search.classList.remove('is-invalid')
                                    search.classList.add('is-valid')
                                }
                                dataList.style.display = 'none'
                                search.classList.add('mb-3')
                                ii.style.display = 'none'
                            })
                        })

                        // закрытие окна при клике не в поле окна
                        window.onclick = function (e) {
                            if (!Array.from(e.target.classList).includes('list-group-item')) {
                                dataList.style.display = 'none'
                                dataList.innerHTML = '';
                            }
                        }

                    }
                })
        } else {
            dataList.innerHTML = '';
        }
    })
}

inn.addEventListener('blur', (e) => {
    LoadInnSearchBlock(partnersInn, e)
    cleanSearchBlock(searchBlock)
    HideSearchBlock(true)
})

function checkHiddenSearchObjects(check_obj_id, hidden_id, input_id=null, org_hidden=false) {
    let item = document.getElementById(check_obj_id)
    let hidden_item = document.getElementById(hidden_id)
    let search_place = document.getElementById('contragentsListOptions')
    // let orgNameInput = document.getElementById('organizationsNameId')
    let communicate =document.getElementById('communicateCheckbox')
    let closing = document.getElementById('closeCheckbox')


    item.addEventListener('change', function () {
        if (this.checked) {
            // console.log(communicate)
            try {
                communicate.setAttribute('disabled', '')
            } catch (TypeError) {}

            closing.setAttribute('disabled', '')
            hidden_item.style.display = 'block'
            hidden_item.setAttribute('required', '')

            if (org_hidden === true) {
                innDiv.style.display = 'none'
                orgNameDiv.style.display = 'none'
                inn.removeAttribute('required')
                inn.classList.remove('is-invalid')
                orgNameInput.removeAttribute('required')
            }
            inn.classList.remove('is-valid')

            if (input_id !== null) {
                let input = document.getElementById(input_id)
                input.setAttribute('required', '')
            }
            hidden_item.classList.add('mb-3')
            hidden_item.addEventListener('keyup', (e) => {
                if (e.target.value.length === 0) {
                    hidden_item.classList.add('is-invalid')
                }
            })
        } else {
            try {
                communicate.removeAttribute('disabled')
            } catch (TypeError) {}
            closing.removeAttribute('disabled')
            hidden_item.style.display = 'none'
            // document.querySelector('.search .invalid-feedback').style.display = 'none'
            search_place.style.display = 'none'
            hidden_item.removeAttribute('required')
            hidden_item.value = ''
            hidden_item.classList.remove('is-valid')
            hidden_item.classList.remove('is-invalid')
            inn.classList.remove('is-valid', 'is-invalid')
            inn.value = ''
            if (org_hidden === true) {
                innDiv.style.display = 'block'
                orgNameDiv.style.display = 'block'
                inn.setAttribute('required', '')
                orgNameInput.setAttribute('required', '')
            }

            if (input_id !== null) {
                let input = document.getElementById(input_id)
                input.removeAttribute('required')
                input.value = ''
                input.classList.remove('is-valid')
                input.classList.remove('is-invalid')
            }
        }
    });
}

checkHiddenSearchObjects('workCheckbox', 'searchClient', null, true);

async function createMultiSelectOption(select, category_id, valuesList) {
    valuesList.forEach((value) => {
        let option = document.createElement('option')
        option.setAttribute('value', value.id)
        option.setAttribute('data-slug', value.slug)
        option.innerHTML = value.name
        select.append(option)
    })
}

async function createSelectMulti(select_id) {
    let select = document.getElementById(select_id)
    let url = select.dataset.url
    let data = await loadData(url)
    await createMultiSelectOption(select, '', data)
}

async function loadData(url){

    let response = await fetch(url, {
        headers: {"X-CSRFToken": csrf},
        method: "POST",
        body: JSON.stringify({department: depart})
    });
    if (response.ok) {
        let json = await response.json()
        return json
    } else {
        alert("Ошибка: " + response.status);
    }
}

let super_inn = document.getElementById('hidden_inn')

window.addEventListener('load', (e) => {
    if (super_inn.value !== 'None') {
    inn.value = super_inn.value
    fetch('/census/get-inn/', {
        method: 'POST',
        headers: {"X-CSRFToken": csrf},
        body: JSON.stringify({searchInn: super_inn.value})
    }).then(response=>response.json()).then(data=> {
        LengthValue(inn, e, data)
        if (data.length > 0) {
            orgNameInput.value = data[0].name
            inn.setAttribute('disabled', '')
            orgNameInput.setAttribute('disabled', '')
        }
    })
}
})


function isInteger(num) {
        return /^\d+$/.test(num);
    }

function floatFormValid(input_id, hidden=true, is_integer=false, is_string=true) {
        let input = document.getElementById(input_id)

        input.addEventListener('keyup', function (e) {
            if (e.target.value === '' ) {
                input.classList.add('is-invalid')
            } else if (e.target.value.length > 0) {
                input.classList.remove('is-invalid')
                input.classList.add('is-valid')
                if (is_integer === true){
                    if(isInteger(e.target.value)) {
                        input.classList.remove('is-invalid')
                        input.classList.add('is-valid')
                    } else {
                        input.classList.remove('is-valid')
                        input.classList.add('is-invalid')
                    }
                } else if (is_string) {
                    if(isInteger(e.target.value)) {
                        input.classList.remove('is-valid')
                        input.classList.add('is-invalid')
                    } else if (typeof e.target.value === 'string') {
                        input.classList.remove('is-invalid')
                        input.classList.add('is-valid')
                    }
                }
            }
        })
    }

floatFormValid('searchClient', true, false, true)
