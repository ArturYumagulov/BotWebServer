(function() {

    function create_volume_data(volumes, tr) {
    volumes.forEach((volume) => {
        let td = document.createElement('td')
        td.innerHTML = volume.value
        td.style.textAlign = 'center'
        tr.append(td)
    })
}

    let elements = new Set()
    let limits = new Map()
    let update = document.getElementById('update')


    function create_volume_sum(volumes, tr) {
        let volumes_sum = 0

        volumes.forEach((num) => {
            volumes_sum += Number(num.value)
        })
        let td = document.createElement('td')
        td.innerHTML = volumes_sum
        td.style.textAlign = 'center'
        tr.append(td)
    }


    function create_eq_or_cars_rows(report, tbody) {

        if (report.cars.length > 0) {
            report.cars.slice(1).forEach((car) => {
                let tr = document.createElement('tr')
                let cars_td = document.createElement('td')
                cars_td.style.textAlign = 'center'
                cars_td.innerHTML = car
                tr.append(cars_td)
                tbody.append(tr)
            })
        } else if (report.equipments.length > 0) {
            report.equipments.slice(1).forEach((car) => {
                let tr = document.createElement('tr')
                let cars_td = document.createElement('td')
                cars_td.style.textAlign = 'center'
                cars_td.innerHTML = car
                tr.append(cars_td)
                tbody.append(tr)
            })
        }
    }

    function create_director_filter_bottom_item(data, block_id) {
        let item_set = new Set()
        if (data.data.length >= 1) {
            data.data.forEach((item) => {
                if (item[block_id] !== undefined) {
                    item_set.add(item[block_id])
                }
            })
        }

        return item_set
    }

    async function create_director_filters(filters_buttons_list, data) {
        filters_buttons_list.forEach((button) => {
            if (button.filter) {
                let filter_items = create_director_filter_bottom_item(data, button.id)
                if (filter_items.size > 0) {
                    filters_block.append(create_filter_bottom(button, filter_items))
                }
            }
        })
    }

    async function create_director_buttons() {
        let main = document.getElementById('main')
        let div = document.createElement('div')
        let b2c_but = document.createElement("button")
        let b2b_but = document.createElement("button")
        let industrial_but = document.createElement("button")
        let filters = document.getElementById('filters')


        // filters.style.display = 'none'
        update.style.display = 'none'

        // div.classList.add()
        div.id = 'buttons'
        window.addEventListener('resize', () => {

            if (window.innerWidth < 468) {
                div.classList.remove('position-absolute', 'top-50', 'start-50')
                div.classList.add('w-100')
            }

        })
        b2b_but.classList.add('btn', 'btn-outline-secondary', 'me-1', 'mb-1')
        b2c_but.classList.add('btn', 'btn-outline-secondary', 'me-1', 'mb-1')
        industrial_but.classList.add('btn', 'btn-outline-secondary', 'me-1', 'mb-1')

        b2b_but.setAttribute('id', 'b2b')
        b2c_but.setAttribute('id', 'b2c')
        industrial_but.setAttribute('id', 'industrial')

        b2c_but.innerHTML = 'B2C'
        b2b_but.innerHTML = 'B2B'
        industrial_but.innerHTML = 'Industrial'
        div.append(b2c_but, b2b_but, industrial_but)
        main.append(div)
    }


    async function create_director_table_row(report, columns_list, depart) {
        let tbody = document.createElement('tbody')
        tbody.setAttribute('id', 'values')
        let tr = document.createElement('tr')
        let eq_rowspan_len = rowspan_count(report)
        for (let i = 0; i < columns_list.length; i++) {
            let td = document.createElement('td')
            if (depart === 'b2c') {
                if (i < 8) {
                    td.setAttribute('rowspan', eq_rowspan_len)
                    td.innerHTML = report[`${columns_list[i].id}`]
                    td.style.textAlign = 'center'
                    tr.append(td)
                } else if (i === 8) {    // cars
                    td.innerHTML = report[`${columns_list[i].id}`][0]
                    td.style.textAlign = 'center'
                    tr.append(td)
                } else if (i === 9) {  // volumes
                    create_volume_data(report.volumes, tr)
                } else {
                    td.setAttribute('rowspan', eq_rowspan_len)
                    td.innerHTML = report[`${columns_list[i].id}`]
                    td.style.textAlign = 'center'
                    tr.append(td)
                }
            } else {
                if (i < 7) {
                    td.setAttribute('rowspan', eq_rowspan_len)
                    td.innerHTML = report[`${columns_list[i].id}`]
                    td.style.textAlign = 'center'
                    tr.append(td)
                } else if (i === 7) {
                    td.innerHTML = report[`${columns_list[i].id}`][0]
                    td.style.textAlign = 'center'
                    tr.append(td)
                } else if (i === 8) {  // volumes
                    create_volume_data(report.volumes, tr)
                } else {
                    td.setAttribute('rowspan', eq_rowspan_len)
                    td.innerHTML = report[`${columns_list[i].id}`]
                    td.style.textAlign = 'center'
                    tr.append(td)
                }
            }

        }
        tbody.append(tr)
        create_eq_or_cars_rows(report, tbody)
        table.append(tbody)
    }

    async function DirectorFilterReport(url, limit = 100, skip = 0, filters, res_depart) {
        return fetch(`${url}?limit=${limit}&skip=${skip}`, {
                method: "POST",
                headers: {"X-CSRFToken": csrf},
                body: JSON.stringify({depart: res_depart, filters: filters}),
            }
        ).then((res) => res.json())
            .then((data) => {
                return data
            })
    }

    async function filters_control_director(column_lists, depart) {

        let filters_list = document.querySelectorAll('.filter')
        filters_list.forEach((filter_item) => {
            filter_item.addEventListener('click', () => {
                console.log(depart, 'dep')
                table.innerHTML = ''

                let new_set = new Map()
                new_set.set('filter_category', filter_item.getAttribute('category'))
                elements.add(`${filter_item.getAttribute('category')}_${filter_item.innerHTML}`)

                let data = DirectorFilterReport(filter_report_1, limits.limit, limits.skip, Array.from(elements), depart)
                data.then((reports) => {

                    clean_duplicate_filters()

                    if (depart === 'b2c') {
                        create_table_head(column_lists, b2c_volume_list)
                    } else if (depart === 'b2b') {
                        create_table_head(column_lists, b2b_volume_list)
                    } else if (depart === 'industrial') {
                        create_table_head(column_lists, industrial_volume_list)
                    }

                    reports.data.forEach((report) => {
                            create_director_table_row(report, column_lists, depart)
                        })
                })
            })
        })
    }

    function clean_duplicate_director_filters() {
        // очистка дубликатов в фильтрах

        let filters = document.getElementById('filters')

        filters.childNodes.forEach((filter) => {
            if (filter.childNodes[1] !== undefined) {
                if (filter.childNodes[1].childNodes.length > 1) {
                    let filter_list = []
                    for (let i = 0; i < filter.childNodes[1].childNodes.length; i++) {
                        if (!filter_list.includes(filter.childNodes[1].childNodes[i].innerText)) {
                            filter_list.push(filter.childNodes[1].childNodes[i].innerText)
                        } else {
                            filter.childNodes[1].childNodes[i].remove()
                        }
                    }
                }
            }
        })
    }


    async function create_director_report_1(depart, column_list, volume_list) {
        fetch(`${report_1}?limit=100&skip=0`, {
            method: "POST",
            headers: {"X-CSRFToken": csrf},
            body: JSON.stringify({depart: depart}),
        }).then((res) => res.json()).then((data) => {
            console.log(data.data.length)
            if (data.data.length === 0) {
                update.style.display = 'none'
                console.log(table)
                table.innerHTML = '<p class="text-center text-secondary m-5">Нет данных</p>'
            }
            else {
                create_director_filters(column_list, data)
                clean_duplicate_director_filters()
                create_table_head(column_list, volume_list)
                data.data.forEach((report) => {
                    create_director_table_row(report, column_list, depart)
                })
                filters_control_director(column_list, depart)
            }
        })
    }

    async function createTable(table) {

        await create_director_buttons()

        let buttons = document.querySelectorAll('.btn')
        let main = document.getElementById('main')
        let div = document.getElementById('buttons')
        buttons.forEach((button) => {
            button.addEventListener('click', () => {
                update.style.display = 'block'
                table.innerHTML = ''
                filters_block.innerHTML = ''
                div.style.position = 'relative'
                div.style.display = 'flex'
                div.style.flexDirection = 'column'
                div.style.top = '0'
                div.style.left = '0'
                if (button.id === 'b2c') {
                    create_director_report_1(button.id, b2c_column_list, b2c_volume_list)
                } else if (button.id === 'b2b') {
                    create_director_report_1(button.id, b2b_column_list, b2b_volume_list)
                } else if (button.id === 'industrial') {
                    create_director_report_1(button.id, industrial_column_list, industrial_volume_list)
                }
            })
        })
    }

    window.createTable = createTable;
})();
