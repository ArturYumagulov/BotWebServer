function create_director_buttons() {
    let main = document.getElementById('main')
    let div = document.createElement('div')
    let b2c_but = document.createElement("button")
    let b2b_but = document.createElement("button")
    let industrial_but = document.createElement("button")
    let filters = document.getElementById('filters')
    let update = document.getElementById('update')


    filters.style.display = 'none'
    update.style.display = 'none'

    // div.classList.add()
    div.id = 'buttons'
    window.addEventListener('resize', ()=> {

        if (window.innerWidth < 468) {
            div.classList.remove('position-absolute', 'top-50', 'start-50')
            div.classList.add('w-100')
    }

    })
    b2b_but.classList.add('btn', 'btn-outline-secondary', 'me-1')
    b2c_but.classList.add('btn', 'btn-outline-secondary', 'me-1')
    industrial_but.classList.add('btn', 'btn-outline-secondary', 'me-1')

    b2b_but.setAttribute('id', 'b2b')
    b2c_but.setAttribute('id', 'b2c')
    industrial_but.setAttribute('id', 'industrial')

    b2c_but.innerHTML = 'B2C'
    b2b_but.innerHTML = 'B2B'
    industrial_but.innerHTML = 'Industrial'
    div.append(b2c_but, b2b_but, industrial_but)
    main.append(div)
}


function create_director_table_row(report, columns_list, depart) {
    let tbody = document.createElement('tbody')
    tbody.setAttribute('id', 'values')
    let tr = document.createElement('tr')
    let eq_rowspan_len = rowspan_count(report)
    // if (depart === 'b2c') {} else {}
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
            } else if (i === 7 ){
                td.innerHTML = report[`${columns_list[i].id}`][0]
                td.style.textAlign = 'center'
                tr.append(td)
            }   else if (i === 8) {  // volumes
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

function DirectorFilterReport(url, limit=100, skip=0, filters, depart) {
   return fetch(`${url}?limit=${limit}&skip=${skip}`, {
          method: "POST",
          headers: {"X-CSRFToken": csrf},
          body: JSON.stringify({depart: depart, filters: filters}),
      }
  ).then((res) => res.json())
        .then((data) => {
            return data})
}

function create_filters_director_table(filter_item, column_lists, depart) {
    let new_set = new Map()
    new_set.set('filter_category', filter_item.getAttribute('category'))

    elements.push(`${filter_item.getAttribute('category')}_${filter_item.innerHTML}`)
    let data = DirectorFilterReport(filter_report_1, limits.limit, limits.skip, elements, depart)
    table.innerHTML = ''
    filters_block.innerHTML = ''
    data.then((reports) => {
        create_filters(column_lists, reports)
        clean_duplicate_filters()
        volumes.then((volumes) => {
            create_table_head(column_lists, volumes)
            reports.data.forEach((report) => {
                create_table_row(report, column_lists, volumes)
            })
            filters_control(column_lists, reports)
        })
    })
}

function filters_control_director(column_lists, depart) {

    let filters_list = document.querySelectorAll('.filter')
    filters_list.forEach((filter_item) => {
        filter_item.addEventListener('click', () => {
            create_filters_director_table(filter_item, column_lists, depart)
        })
    })
}

function create_director_report_1(depart, column_list, volume_list) {

    fetch(`${report_1}?limit=100&skip=0`, {
        method: "POST",
        headers: {"X-CSRFToken": csrf},
        body: JSON.stringify({depart: depart}),
    }).then((res) => res.json()).then((data) => {
        create_filters(column_list, data)
        clean_duplicate_filters()
        create_table_head(column_list, volume_list)
        data.data.forEach((report) => {
            create_director_table_row(report, column_list, depart)
        })
        filters_control_director(column_list, depart)
    })
}