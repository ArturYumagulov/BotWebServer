let table = document.querySelector('.report-1')
let loader = document.querySelector('.loader')
let head_load = document.getElementById('head-load')
let footer_load = document.getElementById('footer-load')

async function load_data() {
  const [reports_data, volumes_data] = await Promise.all([
    fetch(report_1, {
        method: "POST",
        headers: {"X-CSRFToken": csrf},
        body: JSON.stringify({depart: depart}),
    }),
    fetch(volume_url, {
        method: "POST",
        headers: {"X-CSRFToken": csrf},
        body: JSON.stringify({depart: depart}),
    })
  ]);
  const reports = await reports_data.json();
  const volumes = await volumes_data.json();
  return [reports, volumes];
}
let b2c_column_list = [
    {'id': 'author', 'name': "Родитель", 'filter': true},
    {'id': 'inn', 'name': "ИНН", 'filter': false},
    {'id': 'name', 'name': "Наименование", 'filter': false},
    {'id': 'contact', 'name': "Контактное лицо", 'filter': false},
    {'id': 'phone', 'name': "Телефон", 'filter': false},
    {'id': 'category', 'name': "Сегмент", 'filter': true},
    {'id': 'result', 'name': "Результат", 'filter': true},
    {'id': 'elevators', 'name': "Подъемники", 'filter': true},
    {'id': 'cars', 'name': "Автомобили", 'filter': true},
    // {'id': 'across_oil', 'name': "Количество"},
    {'id': 'volume_census', 'name': "Объем потребления масел (сенсус)", 'filter': false},
    // {'id': 'volume_oil', 'name': "Общее потребления масел"},
    {'id': 'working', 'name': "Действующий", 'filter': true},
    {'id': 'diff', 'name': "Разница", 'filter': false},
    // {'id': 'start_category', 'name': "Категория клиента начальная", 'filter': false},
    {'id': 'now_category', 'name': "Категория клиента действующая", 'filter': false},
    {'id': 'potential', 'name': "Потенциал", 'filter': true},
    // {'id': 'frequency', 'name': "Частота заказа", 'filter': false}
]

let b2b_column_list = [
    {'id': 'author', 'name': "Родитель", 'filter': true},
    {'id': 'inn', 'name': "ИНН", 'filter': false},
    {'id': 'name', 'name': "Наименование", 'filter': false},
    {'id': 'contact', 'name': "Контактное лицо", 'filter': false},
    {'id': 'phone', 'name': "Телефон", 'filter': false},
    {'id': 'category', 'name': "Сегмент", 'filter': false},
    {'id': 'result', 'name': "Результат", 'filter': false},
    {'id': 'equipment', 'name': "Парк техники", 'filter': false},
    {'id': 'across_oil', 'name': "Количество", 'filter': false},
    {'id': 'volume_census', 'name': "Объем потребления масел (сенсус)", 'filter': false},
    {'id': 'volume_oil', 'name': "Общее потребления масел", 'filter': false},
    {'id': 'working', 'name': "Действующий", 'filter': false},
    {'id': 'diff', 'name': "Разница", 'filter': false},
    {'id': 'start_category', 'name': "Категория клиента начальная", 'filter': false},
    {'id': 'now_category', 'name': "Категория клиента действующая", 'filter': false},
    {'id': 'potential', 'name': "Потенциал", 'filter': false},
    {'id': 'frequency', 'name': "Частота заказа", 'filter': false}
]

function create_filter_bottom(category_name, items) {
    let button_div = document.createElement('div')
    button_div.classList.add('btn-group', 'm-1')
    button_div.setAttribute('id', category_name.id)
    let button = document.createElement('button')
    let dropdown_menu = document.createElement('ul')
    dropdown_menu.classList.add('dropdown-menu')

    items.forEach((item) => {
        let item_li = document.createElement('li')
        let item_a = document.createElement('a')
        item_a.classList.add('dropdown-item')
        item_a.innerHTML = item
        item_li.append(item_a)
        dropdown_menu.append(item_li)
    })


    button.classList.add('btn', 'btn-secondary', 'dropdown-toggle')
    button.setAttribute('type', 'button')
    button.setAttribute('data-bs-toggle', 'dropdown')
    button.setAttribute('data-bs-auto-close', 'false')
    button.setAttribute('aria-expanded', 'false')
    button.innerHTML = category_name.name
    button_div.append(button)
    button_div.append(dropdown_menu)
    return button_div
}

function create__filter_bottom_item(data, block_id) {
    let item_set = new Set()
    data.data.forEach((item) => {
        if (item[block_id] !== undefined) {
            item_set.add(item[block_id])
        }
    })
    return item_set
}

function create__filter_bottom_many_item(data) {
    let item_set = new Set()
    data.data.forEach((item) => {
        item_set.add(item.category)
    })
    return item_set
}

function create_filters(filters_buttons_list, data) {
    let filters_block = document.getElementById('filters')
    filters_buttons_list.forEach((button)=>{
        if (button.filter) {
            let filter_items = create__filter_bottom_item(data, button.id)
            if (filter_items.size > 0) {
                filters_block.append(create_filter_bottom(button, filter_items))
            }
        }
    })
}
function create_table_head(column_list, volumes) {
    let t_head = document.createElement('thead')
    let tr = document.createElement('tr')
    let volume_tr = document.createElement('tr')
    let volume_count = 0
    volume_tr.setAttribute('id', 'oil_volume')
    volumes.forEach((volume) => {
        let volume_th = document.createElement('th')
        volume_th.classList.add('table-head-item')
        volume_th.setAttribute('scope', 'col')
        volume_th.setAttribute('id', volume.slug)
        volume_th.innerHTML = volume.name
        volume_tr.append(volume_th)
        })
    column_list.forEach((column) => {
        let th = document.createElement('th')
        th.classList.add('table-head-item')
        th.setAttribute('id', column.id)
        th.setAttribute('scope', 'col')
        th.innerHTML = column.name
        if (column.id !== 'volume_census') {
            th.setAttribute('rowspan', '2')
        } else {
            th.setAttribute('colspan', `${volumes.length}`)
        }

        tr.append(th)
    })
    t_head.append(tr)
    t_head.append(volume_tr)
    table.append(t_head)
}

function create_volume_data(volumes, tr) {
    volumes.forEach((volume) => {
        let td = document.createElement('td')
        td.innerHTML = volume.value
        td.style.textAlign = 'center'
        tr.append(td)
    })
}

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

function rowspan_count(report) {
    if (report.equipments.length > 0) {
        return report.equipments.length
    } else if (report.cars.length > 0) {
        return report.cars.length
    }
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
    }
}


function create_table_row(report, columns_list) {
    let tbody = document.createElement('tbody')
    tbody.setAttribute('id', 'values')
    let tr = document.createElement('tr')

    // reports_list.forEach((report) => {
        let  eq_rowspan_len = rowspan_count(report)
        for (let i = 0; i < columns_list.length; i++) {
            let td = document.createElement('td')
            if (i < 8) {
                td.setAttribute('rowspan', eq_rowspan_len)
                td.innerHTML = report[`${columns_list[i].id}`]
                td.style.textAlign = 'center'
                tr.append(td)
            }
            else if (i === 8) {
                td.innerHTML = report[`${columns_list[i].id}`][0]
                td.style.textAlign = 'center'
                tr.append(td)
            }
            else if (i === 9) {
                create_volume_data(report.volumes, tr)
            }
            // else if (i === 10) {
            //     create_volume_sum(report.volumes, tr)
            // }
            else {
                td.setAttribute('rowspan', eq_rowspan_len)
                td.innerHTML = report[`${columns_list[i].id}`]
                tr.append(td)
            }
        }
        tbody.append(tr)
        create_eq_or_cars_rows(report, tbody)
        table.append(tbody)
    // })
}


load_data().then(([reports, volumes]) => {
    console.log(reports)
    // create__filter_bottom_item(reports, 'category')
    create_filters(b2c_column_list, reports)
    if (depart === 'b2c') {
        create_table_head(b2c_column_list, volumes)
        reports.data.forEach((report) => {
            create_table_row(report, b2c_column_list, volumes)
        })
    } else if (depart === 'industrial' || depart === 'b2b') {
        create_table_head(b2b_column_list, volumes)
        reports.data.forEach((report) => {
            create_table_row(report, b2c_column_list, volumes)
        })
    }

}).finally(() => {
    head_load.style.height = '0'
    footer_load.style.height = '0'
    loader.style.display = 'none'
})

// create_filters(b2c_column_list)


