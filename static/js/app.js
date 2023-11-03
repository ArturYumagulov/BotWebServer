(function (qualifiedName) {
    function isInteger(num) {
        if (num < '0' || num > '9') {
            return false;
        } else {
            return true;
        }
    }
    function floatFormValid(div_id, input_id, label_id, hidden=true, is_integer=false) {
        let div = document.getElementById(div_id)
        let input = document.getElementById(input_id)
        let label = document.getElementById(label_id)



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
            // headers: {"X-CSRFToken": csrf},
            method: "GET"});
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
            {headers: {"X-CSRFToken": csrf}, method: "GET"});
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
        let oilDebt = document.getElementById('debitId')
        let oilDebtInput = document.getElementById('iolDebitId')

        let lukoilDebt = document.getElementById('lukDebitId')
        let lukoilDebtInput = document.getElementById('lukoilDebitId')

        let roweDebt = document.getElementById('RowDebitId')
        let roweDebtInput = document.getElementById('RoweDebitId')

        let motulDebt = document.getElementById('motDebitId')
        let motulDebtInput = document.getElementById('motulDebitId')

        let oilsDiv = document.getElementById('oilsDiv')
        let oilsSelect = document.getElementById('oils')

        let filters = document.getElementById('filtersDiv')
        let filtersInput = document.getElementById('filters')

        let accessDiv = document.getElementById('accessDiv')
        let accessInput = document.getElementById('accessId')

        let akbDiv = document.getElementById('akbDiv')
        let akbInput = document.getElementById('akbId')

        let otherVectorDiv = document.getElementById('otherVectorId')
        let otherVectorInput = document.getElementById('otherVectorInputId')


        $('#vectorMulti').on('select2:select', function (e) {
            if(e.params.data.text === 'Масло') {
                oilDebt.style.display = 'block'
                oilDebtInput.setAttribute('required', '')
                roweDebt.style.display = 'block'
                roweDebtInput.setAttribute('required', '')
                motulDebt.style.display = 'block'
                motulDebtInput.setAttribute('required', '')
                lukoilDebt.style.display = 'block'
                lukoilDebtInput.setAttribute('required', '')
                oilsDiv.style.display = 'block'
                oilsSelect.setAttribute('required', '')
                oilsDiv.classList.add('was-validated')
            }
            else if(e.params.data.text === 'Фильтры') {
                filters.style.display = 'block'
                filters.classList.add('was-validated')
                filtersInput.setAttribute('required', '')
            }
            else if(e.params.data.text === 'Аксессуары') {
                accessDiv.style.display = 'block'
                accessInput.setAttribute('required', '')
            }
            else if(e.params.data.text === 'АКБ') {
                akbDiv.style.display = 'block'
                akbInput.setAttribute('required', '')

            }
            else if(e.params.data.text === 'Другое') {
                otherVectorDiv.style.display = 'block'
                otherVectorInput.setAttribute('required', '')

            }
        })
        $('#vectorMulti').on('select2:unselect', function (e) {
            if(e.params.data.text === 'Масло') {
                oilDebt.style.display = 'none'
                oilDebtInput.removeAttribute('required')
                roweDebt.style.display = 'none'
                roweDebtInput.removeAttribute('required')
                motulDebt.style.display = 'none'
                motulDebtInput.removeAttribute('required')
                lukoilDebt.style.display = 'none'
                lukoilDebtInput.removeAttribute('required')
                oilsDiv.style.display = 'none'
                oilsSelect.removeAttribute('required')
                oilsDiv.classList.remove('was-validated')
            }
            else if(e.params.data.text === 'Фильтры') {
                filters.style.display = 'none'
                filters.classList.remove('was-validated')
                filtersInput.removeAttribute('required')
            }
            else if(e.params.data.text === 'Аксессуары') {
                accessDiv.style.display = 'none'
                accessInput.removeAttribute('required')
                accessInput.value = ''
                let other = document.getElementById('otherDivId')
                let access_select = document.getElementById('accessId')
                let access_select_items = document.querySelectorAll('.acc_div')
                let access_list = document.querySelectorAll('.access')
                other.style.display = 'none'
                access_select.value = ''
                access_select.classList.remove('is-valid')
                access_select_items.forEach((item) => {
                    item.style.display = 'none'
                    item.removeAttribute('required')
                })
                access_list.forEach((item) => {
                    item.style.display = 'none'
                    item.removeAttribute('required')
                })
            }
            else if(e.params.data.text === 'АКБ') {
                akbDiv.style.display = 'none'
                akbInput.removeAttribute('required')
                akbInput.value = ''
                akbInput.classList.remove('is-valid', 'is-invalid')
            }
            else if(e.params.data.text === 'Другое') {
                otherVectorDiv.style.display = 'none'
                otherVectorInput.removeAttribute('required')
                otherVectorInput.value = ''
                otherVectorInput.classList.remove('is-valid', 'is-invalid')

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
            if(i.id !== 'closeCheckbox' && i.type !== 'hidden' && i.id !== 'resultCommentId' && i.id !== 'formFileMultiple') {
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
    }

    async function CreateApp(container) {
        loadValidPartners();
        checkHiddenSearchObjects('workCheckbox', 'searchClient', null, true);
        floatFormValid('boardId', 'signboardId', 'signboardId', true)
        await createOption('pointTypeID')
        await createOption('shopCategoryId')
        await createOption('stoTypeId')
        // await createOption('pointVectorId')
        await createOption('accessId')
        HideMultiSelectItem(document.getElementById('accessId'))
        await createSelectMulti('cars')
        await createSelectMulti('oils')
        await createSelectMulti('filters')
        await createControlOption('controlId')
        await createSelectMulti('providers')
        await createSelectMulti('vectorMulti')

        // checkHiddenSearchObjects('decisionCheckboxId', 'fioId', 'decisionMakerId');
        // checkHiddenSearchObjects('decisionCheckboxId', 'emailId', 'decisionMakerEmailId');
        // checkHiddenSearchObjects('decisionCheckboxId', 'phoneId', 'decisionMakerPhoneId');

        await validSelect('typeId')
        await validSelect('shopCategoryId')
        await validSelect('pointTypeID')
        // await validSelect('pointVectorId')
        await validSelect('stoTypeId')
        await validSelect('accessId')
        await validSelect('controlId')
        await validSelect('akbId')

        floatFormValid('fioId', 'decisionMakerId', 'fioIdFeedback', false)
        floatFormValid('emailId', 'decisionMakerEmailId', 'decisionMakerEmailIdFeedback', false)
        floatFormValid('phoneId', 'decisionMakerPhoneId', 'decisionMakerPhoneIdFeedback', false)
        floatFormValid('functionId', 'decisionMakerFunctionId', 'functionIdFeedback', false)
        floatFormValid('elevatorId', 'elevatorCountId', 'elevatorCountIdFeedback', false,
            true)
        floatFormValid('debitId', 'iolDebitId', 'iolDebitIdFeedback', false, true)
        floatFormValid('lukDebitId', 'lukoilDebitId', 'lukoilDebitIdFeedback', false, true)
        floatFormValid('RowDebitId', 'RoweDebitId', 'RoweDebitIdFeedback', false, true)
        floatFormValid('motDebitId', 'motulDebitId', 'motulDebitIdFeedback', false, true)
        floatFormValid('otherDivId', 'otherId', 'otherIdFeedback', false)
        floatFormValid('otherProvDivId', 'otherProvId', 'otherProvIdFeedback', false)
        floatFormValid('otherVectorId', 'otherVectorInputId', 'otherVectorFeedback', false)
        floatFormValid('resultCommentDivId', 'resultCommentId', 'resultCommentFeedback', false)
        floatFormValid('innDivId', 'innId', 'innIdFeedback', false)
        // Автосервис
        await hideChangeFloatElem('pointTypeID', 'elevatorId', 'elevatorCountId','Автосервис')
        await hideChangeSelectElem('pointTypeID', 'stoTypeDiv', 'stoTypeId', 'Автосервис')
        await hideSelectMultiElement('pointTypeID', 'carsDiv', 'cars', 'Автосервис')

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
        let date_cursor = document.querySelector('.input-group-text')
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
        let contacts_div = document.getElementById('contactDivId')
        let contact_select = document.getElementById('ContactId')
        inn.addEventListener('blur', function (e) {
            let searchInn = e.target.value
            let partnersInn = inn.getAttribute('data-url')
            let org_name_div = document.getElementById('organizationsNameDivId')
            let org_name = document.getElementById('organizationsNameId')
                if (searchInn.trim().length > 0) {
                        fetch(partnersInn,
                    {
                        headers: {"X-CSRFToken": csrf},
                        body: JSON.stringify({searchInn: searchInn}),
                        method: "POST",
                        }).then((res) => res.json())
                    .then((data) => {
                        if (data.length > 0) {
                            innDiv.classList.remove('mb-3')
                            searchBlock.style.display = 'block'
                            data.forEach((item) => {
                                let li = document.createElement('li')
                                li.classList.add('list-group-item', 'result-inn')
                                li.style.cursor = 'pointer'
                                li.innerHTML = `${item.name}`
                                li.setAttribute('data-inn', item.name)
                                searchBlock.append(li)
                            })
                            let result_item = document.querySelectorAll('.list-group-item.result-inn')
                            result_item.forEach((i) => {
                                i.addEventListener('click', function () {
                                    active_check.checked = true
                                    let contragent = document.getElementById('searchClient')
                                    contragent.value = i.getAttribute('data-inn')
                                    contragent.style.display = 'block'
                                    contragent.classList.add('is-valid')
                                    innDiv.style.display = 'none'
                                    inn.innerHTML = ''
                                    searchBlock.style.display = 'none'
                                    org_name_div.style.display = 'none'
                                    org_name.removeAttribute('required')
                                })
                            })
                        } else {
                            searchBlock.style.display = 'none'
                            innDiv.classList.add('mb-3')

                        }
                    })
            }
        })
        active_check.addEventListener('change', function () {
            inn.classList.add('mb-3')
            document.getElementById('innId').value = ''
            for (let i = 1; i < searchBlock.children.length; i++) {
                searchBlock.children[i].remove()
            }
        })
        inn.addEventListener('focus', function () {
            for (let i = 1; i < searchBlock.children.length; i++) {
                searchBlock.children[i].remove()
            }
        })

    }
    window.CreateApp = CreateApp;

})();
