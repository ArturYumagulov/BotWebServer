(function (qualifiedName) {
    function cleanSearchBlock(searchBlock) {
            for (let i = 1; i < searchBlock.children.length; i++) {
                searchBlock.children[i].remove()
            }
        }
    function isInteger(num) {
        if (num < '0' || num > '9') {
            return false;
        } else {
            return true;
        }
    }
    function floatFormValid(div_id, input_id, label_id, hidden=true, is_integer=false) {
        // let div = document.getElementById(div_id)
        let input = document.getElementById(input_id)
        // let label = document.getElementById(label_id)


        input.addEventListener('keyup', function (e) {
            if (e.target.value === '' ) {
                input.classList.add('is-invalid')
            } else if (e.target.value.length > 0){
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

            }
            }
        })
    }
    function checkHiddenSearchObjects(check_obj_id, hidden_id, input_id=null, org_hidden=false) {
        let item = document.getElementById(check_obj_id)
        let hidden_item = document.getElementById(hidden_id)
        let search_place = document.getElementById('contragentsListOptions')
        let innDiv = document.getElementById('innDivId')
        let innInput = document.getElementById('innId')
        let orgNameDiv = document.getElementById('organizationsNameDivId')
        let orgNameInput = document.getElementById('organizationsNameId')

        item.addEventListener('change', function () {
            if (this.checked) {
                hidden_item.style.display = 'block'
                hidden_item.setAttribute('required', '')
                if (org_hidden === true) {
                    innDiv.style.display = 'none'
                    orgNameDiv.style.display = 'none'
                    innInput.removeAttribute('required')
                    orgNameInput.removeAttribute('required')
                }
                innInput.classList.remove('is-valid')
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
                    hidden_item.style.display = 'none'
                    search_place.style.display = 'none'
                    hidden_item.removeAttribute('required')
                    hidden_item.value = ''
                    hidden_item.classList.remove('is-valid')
                    innInput.classList.remove('is-valid', 'is-invalid')
                    if (org_hidden === true) {
                        innDiv.style.display = 'block'
                        orgNameDiv.style.display = 'block'
                        innInput.setAttribute('required', '')
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
    async function createOption(item_id) {
        let item = document.getElementById(item_id)
        let url = item.dataset.url
        let data = await loadData(url)

        data.forEach((i) => {
            let option = document.createElement("option")
            option.setAttribute('value', i.id)
            option.setAttribute('data-slug', i.slug)
            option.innerHTML = i.name
            item.append(option)
        })
    }
    async function createControlOption(item_id) {

        let item = document.getElementById(item_id)
        let url = item.dataset.url
        let data = await loadData(url)


        data.forEach((i) => {
            let option = document.createElement("option")
            option.setAttribute('value', i.id)
            option.dataset.control = i.control_data
            option.innerHTML = i.name
            item.append(option)
        })
    }
    async function loadData(url){

        let response = await fetch(url, {
            headers: {"X-CSRFToken": csrf},
            method: "POST",
            body: JSON.stringify({department: 'b2b'})
        });
        if (response.ok) {
            let json = await response.json()
            return json
        } else {
            alert("Ошибка: " + response.status);
        }
    }
    async function loadDataCategory(item, category_id){
        let url = item.dataset.url + '/' + category_id
        let response = await fetch(url,
            {
                headers: {"X-CSRFToken": csrf},
                method: "POST"
            });
        if (response.ok) {
            let json = await response.json()
            return json
        } else {
            alert("Ошибка: " + response.status);
        }
    }
    async function createMultiSelectOption(select, category_id, valuesList) {
        valuesList.forEach((value) => {
            let option = document.createElement('option')
            option.setAttribute('value', value.id)
            option.setAttribute('data-slug', value.slug)
            option.innerHTML = value.name
            select.append(option)
        })
    }
    function HideMultiSelectItem(access) {
        access.addEventListener('change', function () {
            let value = access.value
            let text = access.options[access.selectedIndex].innerHTML
            let divs = document.querySelectorAll('.acc_div')
            let other = document.getElementById('otherDivId')
            divs.forEach((item) => {
                let clean_id = item.id.split('_')[1]
                if (value === clean_id) {
                    item.style.display = 'block'
                    item.classList.add('was-validated')
                    item.children[0].setAttribute('required', '')
                    other.style.display = 'none'
                } else if (text === 'Другое') {
                    other.style.display = 'block'
                    item.style.display = 'none'
                    item.children[0].removeAttribute('required')
                    item.classList.remove('was-validated')
                } else {
                    item.style.display = 'none'
                    item.children[0].removeAttribute('required')
                    item.classList.remove('was-validated')
                    other.style.display = 'none'
                }
            })
            $(`#category_${value}`).val(null).trigger('change')
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
                                item.classList.add('list-group-item')
                                item.style.cursor = 'pointer'
                                item.innerHTML = i.name
                                dataList.append(item)
                            })
                            let find_item = document.querySelectorAll('#result')
                            find_item.forEach((ii) => {
                                ii.addEventListener('click', function (){
                                    ii.classList.add('bg-secondary')
                                    search.value = ii.innerHTML
                                    if (search.value.length > 0) {
                                        search.classList.remove('is-invalid')
                                        search.classList.add('is-valid')
                                    }
                                    dataList.style.display = 'none'
                                    search.classList.add('mb-3')
                                    ii.style.display = 'none'
                                })
                            })
                        }
                    })
            } else {
                dataList.innerHTML = '';
            }
        })
    }
    async function createSelectMulti(select_id) {
        let select = document.getElementById(select_id)
        let url = select.dataset.url
        let data = await loadData(url)
        await createMultiSelectOption(select, '', data)
    }
    async function validSelect(select_id) {
        let select = document.getElementById(select_id)
        select.addEventListener('change', function () {
            if (select.selectedIndex !== 0) {
            select.classList.add('is-valid')
            }
        })
    }
    async function hideChangeFloatElem(elem_id, hidden_id, input_id, value) {
        let elem = document.getElementById(elem_id)
        let input = document.getElementById(input_id)
        let hidden_item = document.getElementById(hidden_id)
        elem.addEventListener('change', function () {
            if (elem.options[elem.selectedIndex].innerHTML === value) {
                hidden_item.style.display = 'block'
                input.setAttribute('required', '')
            } else {
                hidden_item.style.display = 'none'
                input.removeAttribute('required')
                input.value = ''
                input.classList.remove('is-valid')
                input.classList.remove('is-invalid')
            }
        })
    }
    async function hideChangeSelectElem(elem_id, hidden_id, select_id, value) {
        let item = document.getElementById(elem_id)
        let div = document.getElementById(hidden_id)
        let select = document.getElementById(select_id)

        item.addEventListener('change', function () {
            if (item.options[item.selectedIndex].innerHTML === value) {
                div.style.display = 'block'
                select.setAttribute('required', '')
            } else {
                div.style.display = 'none'
                select.removeAttribute('required')
            }
        })
    }
    async function hideSelectMultiElement(elem_id, hidden_id, select_id, value) {
        let item = document.getElementById(elem_id)
        let div = document.getElementById(hidden_id)
        let select = document.getElementById(select_id)
        item.addEventListener('change', function () {
            if (item.options[item.selectedIndex].innerHTML === value) {
                div.style.display = 'block'
                div.classList.add('was-validated')
                select.setAttribute('required', '')
            } else {
                div.style.display = 'none'
                div.classList.remove('was-validated')
                select.removeAttribute('required')
            }
            $(`#${select_id}`).val(null).trigger('change')
        })
    }
    function vectorHideBlock(){
        function createFloatDiv(element, category_name, text="") {
            return `<div class="form-floating mb-3" id="${category_name}${element.id}DivId">
            <input class="form-control" name="${category_name}_${element.id}" id="${category_name}_${element.id}" 
            type="text" placeholder="${text} ${element.text}" aria-describedby="${category_name}IdFeedback" required>
            <label for="${category_name}Id">${text} ${element.text}</label>
            <div id="${category_name}IdFeedback" class="invalid-feedback">Укажите ${text} ${element.text}</div>
            </div>`
        }
        function LoadMultiDivData(element, url) {
            return fetch(url, {
                headers: {"X-CSRFToken": csrf},
                method: "POST",
                body: JSON.stringify({department: 'b2b'})
            }).then((res) => res.json())
                    .then((data) => {
                        return data})
        }

        $('#vectorMulti').on('select2:select', function (e) {
            let element = e.params.data
            let category = e.params.data.element.dataset.slug
            // let select = document.getElementById(`${category}_load`).children[1]
            // let url = select.dataset.url
            // let data = LoadMultiDivData(element, url)


            if (element.text === "Другое") {
                let other = document.getElementById('otherVectorId')
                other.style.display = 'block'
                other.children[0].setAttribute('required', '')
            } else if (element.text !== "Другое") {
                let select = document.getElementById(`${category}_load`).children[1]
                let url = select.dataset.url
                let data = LoadMultiDivData(element, url)
                data.then((result)=>{
                    result.forEach((item) => {

                        let option = document.createElement('option')
                        option.setAttribute('value', item.id)
                        option.innerHTML = item.name
                        select.append(option)

                    })
                });
                select.parentNode.style.display = 'block'
            }

        })

        $('#vectorMulti').on('select2:unselect', function (e) {
            let element = e.params.data
            let category = e.params.data.element.dataset.slug

            if (element.text === "Другое") {
                let other = document.getElementById('otherVectorId')
                other.children[0].removeAttribute('required')
                other.children[0].value = ""
                other.style.display = 'none'
            } else if (element.text !== "Другое") {

                let select = document.getElementById(`${category}_load`).children[1]
                select.parentNode.style.display = 'block'
                for (let i = select.options.length - 1; i >= 0; i--) {
                    console.log(select.options[i])
                    select.options[i].remove()
                }
                select.removeAttribute('required')
                select.parentNode.style.display = 'none'
            }

        })

        $('#equipmentId').on('select2:select', function (e) {
            let element = e.params.data
            let category_name = this.name
            if (element.text === "Другое"){
                let div = createFloatDiv(element, category_name, 'Техника')
                this.parentNode.insertAdjacentHTML("afterend", div)
                            floatFormValid(`${category_name}${element.id}DivId`,
                          `${category_name}_${element.id}`, `${category_name}Id`, false,
                false)
            }
        })

        $('#equipmentId').on('select2:unselect', function (e) {
            let element = e.params.data
            let category_name = this.name
            let item = document.getElementById(`${category_name}${element.id}DivId`)
            item.remove()
        })

        $('#volumeMultiDiv').on('select2:select', function (e) {
            let category_name = this.children[0].name
            let element = e.params.data
            let div = createFloatDiv(element, category_name, 'Объем потребления масла')
            this.insertAdjacentHTML("afterend", div)
            floatFormValid(`${category_name}${element.id}DivId`,
                          `${category_name}_${element.id}`, `${category_name}Id`, false,
                true)
            if (element.text === "Другое") {
                category_name = 'other_volume_name'
                let div = createFloatDiv(element, category_name, 'Какое масло')
                this.insertAdjacentHTML("afterend", div)
                floatFormValid(`${category_name}${element.id}DivId`,
                          `${category_name}_${element.id}`, `${category_name}Id`, false,
                false)
            }
        })

        $('#volumeMultiDiv').on('select2:unselect', function (e) {
            let element = e.params.data
            let category_name = 'other_volume_name'
            if (element.text !== "Другое") {
                document.getElementById(`${this.children[0].name}_${e.params.data.id}`).parentNode.remove()
            } else {
                document.getElementById(`${category_name}${element.id}DivId`).remove()
                document.getElementById(`${this.children[0].name}_${e.params.data.id}`).parentNode.remove()
            }
        })
    }

    function otherProviders(){

            // Другие поставщики

            $('#providers').on('select2:select', function (e) {
                let other_prov_div = document.getElementById('otherProvDivId')
                let other_input = document.getElementById('otherProvId')
                if (e.params.data.text === "Другое") {
                    other_prov_div.style.display = 'block'
                    other_input.setAttribute('required', '')
                }

            })
            $('#providers').on('select2:unselect', function (e) {
                let other_prov_div = document.getElementById('otherProvDivId')
                let other_input = document.getElementById('otherProvId')
                if (e.params.data.text === "Другое") {
                    other_prov_div.style.display = 'none'
                    other_input.removeAttribute('required')
                    other_input.value = ''
                    other_input.classList.remove('is-valid', 'is-invalid')
                }
            })
        }

    function FilesFormValid(form_id) {
        let item = document.getElementById(form_id)
        item.classList.add('is-invalid')
        item.addEventListener('change', function () {
            if (item.files.length === 0) {
            item.classList.add('is-invalid')
        } else {
            item.classList.remove('is-invalid')
            item.classList.add('is-valid')
        }
        })
    }

    function delAddReqCheckbox(){
        let selects = document.querySelectorAll('select')
        let inputs = document.querySelectorAll('input')
        let elements = []
        let ids = []
        inputs.forEach((i) => {
            if(i.id !== 'closeCheckbox' && i.type !== 'hidden' && i.id !== 'resultCommentId'
                && i.id !== 'formFileMultiple' && i.id !== 'communicateCheckbox') {
                elements.push(i)
            }
        })
        selects.forEach((i) => {
            elements.push(i)
        })
        elements.forEach((elem) => {
            if ('required' in elem.attributes) {
                ids.push(elem.id)
            }
        })

        let closing_checkbox = document.getElementById('closeCheckbox')

        closing_checkbox.addEventListener('change', function () {
            if (this.checked) {
                elements.slice(1)
                elements.forEach((item) => {
                    item.setAttribute('disabled', '')
                })
                function removeReq(iterElem) {
                    iterElem.forEach((elem) => {
                        let el = document.getElementById(elem)
                        el.removeAttribute('required')
                    })
                }
                removeReq(ids);
            } else {
                elements.forEach((item) => {
                    item.removeAttribute('disabled')
                })
                function addReq(iterElem) {
                    iterElem.forEach((elem) => {
                        let el = document.getElementById(elem)
                        el.setAttribute('required', '')
                    })
                }
                addReq(ids)
            }
        })

        let communicate = document.getElementById('communicateCheckbox')

        communicate.addEventListener('change', function () {
            if (this.checked) {
                elements.slice(1)
                elements.forEach((item) => {
                    item.setAttribute('disabled', '')
                })
                function removeReq(iterElem) {
                    iterElem.forEach((elem) => {
                        let el = document.getElementById(elem)
                        el.removeAttribute('required')
                    })
                }
                removeReq(ids);
            } else {
                elements.forEach((item) => {
                    item.removeAttribute('disabled')
                })
                function addReq(iterElem) {
                    iterElem.forEach((elem) => {
                        let el = document.getElementById(elem)
                        el.setAttribute('required', '')
                    })
                }
                addReq(ids)
            }
        })
    }

    async function CreateApp(container) {
        loadValidPartners();
        checkHiddenSearchObjects('workCheckbox', 'searchClient', null, true);
        floatFormValid('boardId', 'signboardId', 'signboardId', true)
        await createOption('shopCategoryId')
        // await createSelectMulti('oils')
        // await createSelectMulti('filters')
        await createControlOption('controlId')
        await createSelectMulti('providers')
        await createSelectMulti('vectorMulti')
        await createSelectMulti('volumeId')
        await createSelectMulti('equipmentId')
        await validSelect('shopCategoryId')
        await validSelect('controlId')

        floatFormValid('fioId', 'decisionMakerId', 'fioIdFeedback', false)
        floatFormValid('emailId', 'decisionMakerEmailId', 'decisionMakerEmailIdFeedback', false)
        floatFormValid('phoneId', 'decisionMakerPhoneId', 'decisionMakerPhoneIdFeedback', false)
        floatFormValid('functionId', 'decisionMakerFunctionId', 'functionIdFeedback', false)
        floatFormValid('otherProvDivId', 'otherProvId', 'otherProvIdFeedback', false)
        floatFormValid('otherVectorId', 'otherVectorInputId', 'otherVectorFeedback', false)
        floatFormValid('resultCommentDivId', 'resultCommentId', 'resultCommentFeedback', false)


        let access_items = document.querySelectorAll('.access')

        for (let i = 1; i < access_items.length + 1; i++) {
            let div = document.getElementById('category_' + i + '_div')
            let item = document.getElementById('category_' + i)
            let item_id = item.getAttribute('id').split('_')[1]
            let data = await loadDataCategory(item, item_id)
            await createMultiSelectOption(item, item_id, data)
            div.style.display = 'none'
        }

        let control = document.getElementById('controlId')
        let date = document.getElementById('dateDiv')
        let date_input = document.getElementById('date')
        control.addEventListener('change', function () {
            if (control.options[control.selectedIndex].dataset.control === 'true') {
                date.style.display = 'block'
                date_input.setAttribute('required', '')
            } else {
                date.style.display = 'none'
                date_input.removeAttribute('required')
            }
        })

        let other_multi_selects = document.querySelectorAll('.multi')
        other_multi_selects.forEach((item) => {
            item.style.display = 'none'
        })

        vectorHideBlock();
        otherProviders();
        delAddReqCheckbox();
        FilesFormValid('formFileMultiple')

        let inn = document.getElementById('innId')
        let innDiv = document.getElementById('innDivId')
        let active_check = document.getElementById('workCheckbox')
        let searchBlock = document.getElementById('innSearchUl')
        let out = document.querySelector('.out')

        function LengthValue(item, event) {
            let inn_value = item.value

                if (inn_value.length !== 10 && inn_value.length !== 12){
                document.getElementById('innId').classList.add('is-invalid')
                inn.classList.remove('mb-3', 'is-valid')
                document.getElementById('innIdFeedback').innerHTML = 'Длина ИНН должна содержать 10 или 12 символов'
                document.getElementById('organizationsNameId').value = ''
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
            li.classList.add('list-group-item', 'result-inn')
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
                    if (data.length > 0) {
                        data.forEach((item) => {
                            if (item.source === "out") {
                                HideSearchBlock(false)
                                out.innerHTML = "Данный ИНН существует в 1С"
                                innDiv.classList.remove('mb-3')
                                createSearchElem(searchBlock, item)

                                let results_list = document.querySelectorAll('.list-group-item.result-inn')
                                let contragent = document.getElementById('searchClient')
                                let orgDiv = document.getElementById('organizationsNameDivId')
                                results_list.forEach((item) => {
                                    item.addEventListener('click', () => {
                                        active_check.checked = true
                                        HideSearchBlock(true)
                                        let items = document.querySelectorAll('.list-group-item.result-inn')
                                        items.forEach((item) => {
                                            item.remove()
                                        })
                                        contragent.style.display = 'block'
                                        contragent.value = item.getAttribute('data-name')
                                        contragent.classList.add('is-valid')
                                        contragent.setAttribute('required', '')
                                        inn.value = ''
                                        inn.removeAttribute('required')
                                        inn.classList.remove('is-valid')
                                        innDiv.style.display = 'none'
                                        orgDiv.style.display = 'none'
                                        orgDiv.children[0].removeAttribute('required')
                                    })
                                })

                            } else {
                                HideSearchBlock(false)
                                out.innerHTML = ''
                                innDiv.classList.remove('mb-3')
                                createSearchElem(searchBlock, item)

                                let results_list = document.querySelectorAll('.list-group-item.result-inn')
                                results_list.forEach((item) => {
                                    item.addEventListener('click', () => {
                                        // HideSearchBlock(true)
                                        let orgName = document.getElementById('organizationsNameId')
                                        orgName.value = item.getAttribute('data-name')
                                        inn.value = item.getAttribute('data-inn')
                                        HideSearchBlock(searchBlock)
                                    })
                                })
                            }

                        })
                    }
                }
            )
        }
        let partnersInn = inn.getAttribute('data-url')
        inn.addEventListener('focus', (e) => {
            LengthValue(inn, e)
        })
        inn.addEventListener('blur', (e) => {
            LengthValue(inn, e)
            LoadInnSearchBlock(partnersInn, e)
            cleanSearchBlock(searchBlock)
            HideSearchBlock(true)
        })
    }
    window.CreateApp = CreateApp;
})();
