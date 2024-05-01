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
    {'id': 'author', 'name': "Родитель"},
    {'id': 'inn', 'name': "ИНН"},
    {'id': 'name', 'name': "Наименование"},
    {'id': 'contact', 'name': "Контактное лицо"},
    {'id': 'phone', 'name': "Телефон"},
    {'id': 'category', 'name': "Сегмент"},
    {'id': 'result', 'name': "Результат"},
    {'id': 'elevators', 'name': "Подъемники"},
    {'id': 'cars', 'name': "Автомобили"},
    // {'id': 'across_oil', 'name': "Количество"},
    {'id': 'volume_census', 'name': "Объем потребления масел (сенсус)"},
    {'id': 'volume_oil', 'name': "Общее потребления масел"},
    {'id': 'working', 'name': "Действующий"},
    {'id': 'diff', 'name': "Разница"},
    {'id': 'start_category', 'name': "Категория клиента начальная"},
    {'id': 'now_category', 'name': "Категория клиента действующая"},
    {'id': 'potential', 'name': "Потенциал"},
    {'id': 'frequency', 'name': "Частота заказа"}
]

let b2b_column_list = [
    {'id': 'author', 'name': "Родитель"},
    {'id': 'inn', 'name': "ИНН"},
    {'id': 'name', 'name': "Наименование"},
    {'id': 'contact', 'name': "Контактное лицо"},
    {'id': 'phone', 'name': "Телефон"},
    {'id': 'category', 'name': "Сегмент"},
    {'id': 'result', 'name': "Результат"},
    {'id': 'equipment', 'name': "Парк техники"},
    {'id': 'across_oil', 'name': "Количество"},
    {'id': 'volume_census', 'name': "Объем потребления масел (сенсус)"},
    {'id': 'volume_oil', 'name': "Общее потребления масел"},
    {'id': 'working', 'name': "Действующий"},
    {'id': 'diff', 'name': "Разница"},
    {'id': 'start_category', 'name': "Категория клиента начальная"},
    {'id': 'now_category', 'name': "Категория клиента действующая"},
    {'id': 'potential', 'name': "Потенциал"},
    {'id': 'frequency', 'name': "Частота заказа"}
]
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
            else if (i === 10) {
                create_volume_sum(report.volumes, tr)
            }
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


