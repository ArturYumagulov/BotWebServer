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
            headers: {"X-CSRFToken": csrf},
            method: "POST",
            body: JSON.stringify({department: depart})
            })
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
    // async function createMultiSelectOption(select, category_id, valuesList) {
    //
    //     valuesList.forEach((value) => {
    //         let option = document.createElement('option')
    //         option.setAttribute('value', value.id)
    //         option.innerHTML = value.name
    //         select.append(option)
    //     })
    // }
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
    // async function createSelectMulti(select_id) {
    //     let select = document.getElementById(select_id)
    //     let url = select.dataset.url
    //     let data = await loadData(url)
    //     await createMultiSelectOption(select, '', data)
    // }
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

        let vitexDebt = document.getElementById('vitDebitId')
        let vitexDebtInput = document.getElementById('vitexDebitId')

        let accessDiv = document.getElementById('accessDiv')
        let accessInput = document.getElementById('accessId')

        let akbDiv = document.getElementById('akbDiv')
        let akbInput = document.getElementById('akbId')

        let otherVectorDiv = document.getElementById('otherVectorId')
        let otherVectorInput = document.getElementById('otherVectorInputId')


        $('#vectorMulti').on('select2:select', function (e) {

            let element = e.params.data
            let category = e.params.data.element.dataset.slug

            if(e.params.data.text === 'Масло') {
                oilDebt.style.display = 'block'
                oilDebtInput.setAttribute('required', '')
                roweDebt.style.display = 'block'
                roweDebtInput.setAttribute('required', '')
                motulDebt.style.display = 'block'
                motulDebtInput.setAttribute('required', '')
                lukoilDebt.style.display = 'block'
                lukoilDebtInput.setAttribute('required', '')
                vitexDebt.style.display = 'block'
                vitexDebtInput.setAttribute('required', '')

                let select = document.getElementById(`${category}_load`).children[1]
                let url = select.dataset.url
                let data = LoadMultiDivData(element, url)

                data.then((result)=> {
                    result.forEach((item) => {

                        let option = document.createElement('option')
                        option.setAttribute('value', item.id)
                        option.innerHTML = item.name
                        select.append(option)

                    })
                });
                select.parentNode.style.display = 'block'
                select.setAttribute('required', '')
            }

            else if(e.params.data.text === 'Другое') {
                otherVectorDiv.style.display = 'block'
                otherVectorInput.setAttribute('required', '')

            } else {

                let select = document.getElementById(`${category}_load`).children[1]
                let url = select.dataset.url
                let data = LoadMultiDivData(element, url)
                console.log(category)

                data.then((result)=> {
                    result.forEach((item) => {

                        let option = document.createElement('option')
                        option.setAttribute('value', item.id)
                        option.innerHTML = item.name
                        select.append(option)

                    })
                });
                select.parentNode.style.display = 'block'
                select.setAttribute('required', '')
            }
        })

        $('#vectorMulti').on('select2:unselect', function (e) {
            let category = e.params.data.element.dataset.slug

            if(e.params.data.text === 'Масло') {
                let element = document.getElementById(`maslo_load`)
                element.style.display = 'none'
                element.removeAttribute('required')
                oilDebt.style.display = 'none'
                oilDebtInput.removeAttribute('required')
                roweDebt.style.display = 'none'
                roweDebtInput.removeAttribute('required')
                motulDebt.style.display = 'none'
                motulDebtInput.removeAttribute('required')
                lukoilDebt.style.display = 'none'
                lukoilDebtInput.removeAttribute('required')
                vitexDebt.style.display = 'none'
                vitexDebtInput.removeAttribute('required')


                let select = document.getElementById(`${category}_load`)
                let options = select.children[1].options
                for (let i = options.length - 1; i >= 0; i--) {
                    options[i].remove()
                }
                select.style.display = 'none'
                select.removeAttribute('required')
            }

            else if(e.params.data.text === 'Другое') {
                otherVectorDiv.style.display = 'none'
                otherVectorInput.removeAttribute('required')
                otherVectorInput.value = ''
                otherVectorInput.classList.remove('is-valid', 'is-invalid')

            } else {
                let select = document.getElementById(`${category}_load`)
                let options = select.children[1].options
                for (let i = options.length - 1; i >= 0; i--) {
                    options[i].remove()
                }
                select.style.display = 'none'
                select.removeAttribute('required')
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
                        el.classList.remove('is-invalid')
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
        checkHiddenSearchObjects('workCheckbox', 'searchClient', null, true);
        floatFormValid('boardId', 'signboardId', 'signboardId', true)
        await createOption('pointTypeID')
        await createOption('shopCategoryId')
        await createOption('stoTypeId')
        await createOption('accessId')
        HideMultiSelectItem(document.getElementById('accessId'))
        await createSelectMulti('cars')
        await createControlOption('controlId')
        await createSelectMulti('providers')
        await createSelectMulti('vectorMulti')
        await validSelect('typeId')
        await validSelect('shopCategoryId')
        await validSelect('pointTypeID')
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
        floatFormValid('vitDebitId', 'vitexDebitId', 'vitexDebitIdFeedback', false, true)
        floatFormValid('otherProvDivId', 'otherProvId', 'otherProvIdFeedback', false)
        floatFormValid('otherVectorId', 'otherVectorInputId', 'otherVectorFeedback', false)
        floatFormValid('resultCommentDivId', 'resultCommentId', 'resultCommentFeedback', false)
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
    }
    window.CreateApp = CreateApp;
})();
