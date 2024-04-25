(function (qualifiedName) {
    function isInteger(num) {
        if (num < '0' || num > '9') {
            return false;
        } else {
            return true;
        }
    }
    function floatFormValid(input_id, hidden=true, is_integer=false, is_string=true) {
        let input = document.getElementById(input_id)


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
    function checkHiddenSearchObjects(check_obj_id, hidden_id, input_id=null, org_hidden=false) {
        let item = document.getElementById(check_obj_id)
        let hidden_item = document.getElementById(hidden_id)
        let search_place = document.getElementById('contragentsListOptions')
        let innDiv = document.getElementById('innDivId')
        let innInput = document.getElementById('innId')
        let orgNameDiv = document.getElementById('organizationsNameDivId')
        let orgNameInput = document.getElementById('organizationsNameId')
        let communicate =document.getElementById('communicateCheckbox')
        let closing = document.getElementById('closeCheckbox')


        item.addEventListener('change', function () {
            if (this.checked) {
                // console.log(communicate)
                communicate.setAttribute('disabled', '')
                closing.setAttribute('disabled', '')

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
                    communicate.removeAttribute('disabled')
                    closing.removeAttribute('disabled')
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
    // async function createControlOption(item_id) {
    //
    //     let item = document.getElementById(item_id)
    //     let url = item.dataset.url
    //     let data = await loadData(url)
    //
    //
    //     data.forEach((i) => {
    //         let option = document.createElement("option")
    //         option.setAttribute('value', i.id)
    //         option.dataset.control = i.control_data
    //         option.innerHTML = i.name
    //         item.append(option)
    //     })
    // }
    // async function loadData(url){
    //
    //     let response = await fetch(url, {
    //         headers: {"X-CSRFToken": csrf},
    //         method: "POST",
    //         body: JSON.stringify({department: depart})
    //     });
    //     if (response.ok) {
    //         let json = await response.json()
    //         return json
    //     } else {
    //         alert("Ошибка: " + response.status);
    //     }
    // }

    // async function createMultiSelectOption(select, category_id, valuesList) {
    //     valuesList.forEach((value) => {
    //         let option = document.createElement('option')
    //         option.setAttribute('value', value.id)
    //         option.setAttribute('data-slug', value.slug)
    //         option.innerHTML = value.name
    //         select.append(option)
    //     })
    // }

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
            select.classList.add('is-valid');
            select.style.color = 'black'
            }
        })
    }

    function vectorHideBlock(){

        $('#vectorMulti').on('select2:select', function (e) {
            let element = e.params.data
            let category = e.params.data.element.dataset.slug

            if (element.text === "Другое") {
                let other = document.getElementById('otherVectorId')
                other.style.display = 'block'
                other.children[0].setAttribute('required', '')
                other.children[0].classList.remove('is-valid')
                other.children[0].classList.add('is-invalid')
            } else if (element.text !== "Другое") {
                let select = document.getElementById(`${category}_load`).children[1]
                select.setAttribute('required', '')
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
                other.children[0].classList.remove('is-valid')
                other.children[0].classList.add('is-invalid')
                other.children[0].value = ""
                other.style.display = 'none'
            } else if (element.text !== "Другое") {

                let select = document.getElementById(`${category}_load`).children[1]
                select.parentNode.style.display = 'block'
                for (let i = select.options.length - 1; i >= 0; i--) {
                    select.options[i].remove()
                }
                select.removeAttribute('required')
                select.parentNode.style.display = 'none'
            }

        })

        $('#equipmentId').on('select2:select', function (e) {
            let element = e.params.data
            let category_name = this.name
            if (element.text !== "Другое"){
            let div = createFloatDiv(element, category_name, 'Количество')
            this.parentNode.insertAdjacentHTML("afterend", div)
            floatFormValid(`${category_name}_${element.id}`, false, true)
            }
            if (element.text === "Другое") {
                let div_name = createFloatDiv(element, `${category_name}_other_name`, 'Какая техника')
                let div = createFloatDiv(element, `${category_name}`, 'Количество')
                this.parentNode.insertAdjacentHTML("afterend", div)
                this.parentNode.insertAdjacentHTML("afterend", div_name)
                floatFormValid(`${category_name}_${element.id}`, false, true)
                floatFormValid(`${category_name}_other_name_${element.id}`, false, false)
            }

        })

        $('#equipmentId').on('select2:unselect', function (e) {
            let element = e.params.data
            let category_name = this.name
            let item = document.getElementById(`${category_name}${element.id}DivId`)
            item.remove()
            //
            if (element.text === "Другое") {
                let other_name = document.getElementById(`${category_name}_other_name${element.id}DivId`)
                other_name.remove()
            }
        })

        $('#volumeIdDiv').on('select2:select', function (e) {
            let category_name = this.children[0].name
            let element = e.params.data
            let div = createFloatDiv(element, category_name, 'Объем потребления масла', 'в месяц в литрах')
            this.insertAdjacentHTML("afterend", div)
            floatFormValid(`${category_name}_${element.id}`,false, true)
            if (element.text === "Другое") {
                category_name = 'other_volume_name'
                let div = createFloatDiv(element, category_name, 'Какое масло')
                this.insertAdjacentHTML("afterend", div)
                floatFormValid(
                          `${category_name}_${element.id}`, false,
                false)
            }
        })

        $('#volumeIdDiv').on('select2:unselect', function (e) {
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
        loadValidPartners();
        // checkHiddenSearchObjects('workCheckbox', 'searchClient', null, true);
        floatFormValid('signboardId', true)
        await createOption('shopCategoryId')
        // await createControlOption('controlId')
        await createSelectMulti('providers')
        await createSelectMulti('vectorMulti')
        await createSelectMulti('volumeId')
        await createSelectMulti('equipmentId')
        await validSelect('shopCategoryId')
        // await validSelect('controlId')
        await validSelect('tenderId')

        floatFormValid('lastnameMakerId', false, false, true)
        floatFormValid('firstnameMakerId', false, false, true)
        floatFormValid('surnameMakerId', false, false, true)
        floatFormValid( 'decisionMakerEmailId',  false)
        floatFormValid('decisionMakerPhoneId',  false, true, false)
        floatFormValid('decisionMakerFunctionId', false)

        floatFormValid('otherProvId', false)
        floatFormValid( 'otherVectorInputId', true)
        floatFormValid('resultCommentId', false)


        // let control = document.getElementById('controlId')
        // let date = document.getElementById('dateDiv')
        // let date_input = document.getElementById('date')
        // control.addEventListener('change', function () {
        //     if (control.options[control.selectedIndex].dataset.control === 'true') {
        //         date.style.display = 'block'
        //         date_input.setAttribute('required', '')
        //     } else {
        //         date.style.display = 'none'
        //         date_input.removeAttribute('required')
        //     }
        // })

        let other_multi_selects = document.querySelectorAll('.multi')
        other_multi_selects.forEach((item) => {
            item.style.display = 'none'
        })

        vectorHideBlock();
        otherProviders();
        delAddReqCheckbox();
        FilesFormValid('formFileMultiple')

        let form = document.getElementsByTagName('form')[0]
        form.addEventListener('submit', function (e) {
            let inputs = document.getElementsByTagName('input')
            let valid_list = []
            for (let i = 0; i < inputs.length; i++) {
                if (Array.prototype.slice.call(inputs[i].classList).includes('is-invalid')) {
                    valid_list.push(inputs[i])
                }
            }

            if (valid_list.length > 0) {
                console.log('invalid')
                console.log(valid_list)
                e.preventDefault()
            } else {
                console.log('valid')
                form.submit()
            }
        })
    }
    window.CreateApp = CreateApp;
})();
