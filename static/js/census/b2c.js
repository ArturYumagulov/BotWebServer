(function (qualifiedName) {

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

    async function validSelect(select_id) {
        let select = document.getElementById(select_id)
        select.addEventListener('change', function () {
            if (select.selectedIndex !== 0) {
            select.classList.add('is-valid');
            select.style.color = 'black'
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

        let debits = document.querySelectorAll('.volume')
        let elevator = document.getElementById('elevatorId')

        let akbDiv = document.getElementById('akbDiv')
        let akbInput = document.getElementById('akbId')

        let otherVectorDiv = document.getElementById('otherVectorId')
        let otherVectorInput = document.getElementById('otherVectorInputId')

        const package_div = document.getElementById('packagesMultiDiv')
        const package_input = document.getElementById('packagesMulti')

        const lukoil_multi_div = document.getElementById('lukoilMultiDiv')
        const lukoil_multi_input = document.getElementById('lukoilMulti')


        $('#vectorMulti').on('select2:select', function (e) {

            let element = e.params.data
            let category = e.params.data.element.dataset.slug
            const kpp = document.getElementById('kpp')

            if(e.params.data.text === 'Масло') {

                elevator.style.display = 'block'
                elevator.setAttribute('required', '')
                floatFormValid(elevator.children[0].id, true, true)

                debits.forEach((debit) => {
                    debit.style.display = 'block';
                    debit.children[0].setAttribute('required', '')
                    floatFormValid(debit.children[0].id, true, true)
                })

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

                // Фасовка
                package_div.style.display = 'block'
                package_input.setAttribute('required', '')

                // Коробка
                kpp.parentNode.style.display = "block";
                kpp.setAttribute('required', '')
            }

            else if(e.params.data.text === 'Другое') {
                otherVectorDiv.style.display = 'block'
                otherVectorInput.setAttribute('required', '')
            }
            else if (e.params.data.text === 'АКБ'){
                akbDiv.style.display = 'block'
                akbInput.setAttribute('required', '')

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

            } else {

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
                select.setAttribute('required', '')
            }
        })

        $('#vectorMulti').on('select2:unselect', function (e) {
            let category = e.params.data.element.dataset.slug
            console.log(e.params.data.text)
            if(e.params.data.text === 'Масло') {
                let element = document.getElementById(`maslo`)
                element.style.display = 'none'
                element.removeAttribute('required')

                elevator.style.display = 'none'
                elevator.removeAttribute('required')
                elevator.classList.remove('is-invalid')

                debits.forEach((debit) => {
                    debit.style.display = 'none';
                    debit.children[0].removeAttribute('required')
                    debit.children[0].classList.remove('is-invalid')
                })

                let select = document.getElementById(`${category}_load`)
                let options = select.children[1].options

                for (let i = options.length - 1; i >= 0; i--) {
                    options[i].remove()
                }
                select.style.display = 'none'
                select.removeAttribute('required')

                // Фасовка
                package_div.style.display = 'none'
                package_input.removeAttribute('required')

                // Удаление фасовки
                for (let i = 0; i < package_input.options.length; i++) {
                    package_input.options[i].remove()
                }
                // Коробка
                kpp.parentNode.style.display = "none";
                kpp.removeAttribute('required')
            }
            else if (e.params.data.text === 'АКБ'){
                akbDiv.style.display = 'none'
                akbInput.removeAttribute('required')

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

        function lukoil_brands(){
            const lukoil_div = document.getElementById('lukoilMultiDiv')
            const lukoil_input = document.getElementById('lukoilMulti')
            $('#maslo').on('select2:select', function (e) {
                let txt = e.params.data.text
                if (txt === "ЛУКОЙЛ") {
                    lukoil_div.style.display = 'block'
                    lukoil_input.setAttribute('required', '')
                }
            })
            $('#maslo').on('select2:unselect', function (e) {
                lukoil_div.style.display = 'none'
                lukoil_input.removeAttribute('required')
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
                    item.classList.remove('is-invalid')
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
        FilesFormValid('formFileMultiple')
        checkHiddenSearchObjects('workCheckbox', 'searchClient', null, true);
        await createOption('pointTypeID')
        await createOption('shopCategoryId')
        await createOption('stoTypeId')
        await createSelectMulti('cars')
        // await createControlOption('controlId')
        await createSelectMulti('bonusMulti')
        await createSelectMulti('providers')
        await createSelectMulti('vectorMulti')
        await createSelectMulti('lukoilMulti')
        await createSelectMulti('packagesMulti')

        await validSelect('kpp')
        await validSelect('typeId')
        await validSelect('federal')
        await validSelect('shopCategoryId')
        await validSelect('pointTypeID')
        await validSelect('stoTypeId')
        // await validSelect('controlId')
        await validSelect('akbId')

        floatFormValid('signboardId', true)
        floatFormValid('lastnameMakerId', false, false, true)
        floatFormValid('firstnameMakerId', false, false, true)
        floatFormValid('surnameMakerId', false, false, true)
        floatFormValid( 'decisionMakerEmailId',  false)
        floatFormValid('decisionMakerPhoneId',  false, true, false)
        floatFormValid('decisionMakerFunctionId', false)

        floatFormValid('otherProvId', true, false)
        floatFormValid('otherVectorInputId', true, false)
        floatFormValid('resultCommentId', true, false)
        floatFormValid('elevatorCountId', true, true, false)

        // Автосервис
        await hideChangeFloatElem('pointTypeID', 'elevatorId', 'elevatorCountId','Автосервис')
        await hideChangeSelectElem('pointTypeID', 'stoTypeDiv', 'stoTypeId', 'Автосервис')
        await hideSelectMultiElement('pointTypeID', 'carsDiv', 'cars', 'Автосервис')

        // let access_items = document.querySelectorAll('.access')
        //
        // for (let i = 1; i < access_items.length + 1; i++) {
        //     let div = document.getElementById('category_' + i + '_div')
        //     let item = document.getElementById('category_' + i)
        //     let item_id = item.getAttribute('id').split('_')[1]
        //     let data = await loadDataCategory(item, item_id)
        //     await createMultiSelectOption(item, item_id, data)
        //     div.style.display = 'none'
        // }

        let other_multi_selects = document.querySelectorAll('.multi')
        other_multi_selects.forEach((item) => {
            item.style.display = 'none'
        })

        vectorHideBlock();
        otherProviders();
        delAddReqCheckbox();
        lukoil_brands()
        loadValidPartners();

        closeCheckbox.removeAttribute('disabled');
        workCheckbox.removeAttribute('disabled');
    }
    window.CreateApp = CreateApp;
})();
