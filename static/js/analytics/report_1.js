let table = document.querySelector('.report-1')
let filters_block = document.getElementById('filters')
let loader = document.querySelector('.loader')
let head_load = document.getElementById('head-load')
let footer_load = document.getElementById('footer-load')


function fetchVolume(url) {
   return fetch(url, {
          method: "POST",
          headers: {"X-CSRFToken": csrf},
          body: JSON.stringify({depart: depart}),
      }
  ).then((res) => res.json())
        .then((data) => {
            return data})
}


let volumes = fetchVolume(volume_url)
let elements = []
let limits = new Map()

async function load_data(limit, skip) {
  const [reports_data, volumes_data, length_data, volumes_sum_data] = await Promise.all([
      fetch(`${report_1}?limit=100&skip=0`, {
          method: "POST",
          headers: {"X-CSRFToken": csrf},
          body: JSON.stringify({depart: depart}),
      }),
      fetch(volume_url, {
          method: "POST",
          headers: {"X-CSRFToken": csrf},
          body: JSON.stringify({depart: depart}),
      }),
      fetch(get_length, {
          method: "POST",
          headers: {"X-CSRFToken": csrf},
          body: JSON.stringify({depart: depart}),
      }),
      fetch(volumes_sum_url, {
          method: "POST",
          headers: {"X-CSRFToken": csrf},
          body: JSON.stringify({depart: depart}),
      })
  ]);
  const reports = await reports_data.json();
  const volumes = await volumes_data.json();
  const length = await length_data.json();
  const volumes_sum = await volumes_sum_data.json();
  return [reports, volumes, length, volumes_sum];
}

function create_filter_bottom(category_name, items) {
    let button_div = document.createElement('div')
    button_div.classList.add('btn-group', 'm-1')
    button_div.setAttribute('id', category_name.id)
    let button = document.createElement('button')
    button.id = `dropdownMenu${category_name.id}_id`
    let dropdown_menu = document.createElement('ul')
    dropdown_menu.classList.add('dropdown-menu')
    dropdown_menu.setAttribute('aria-labelledby', `dropdownMenu${category_name.id}_id`)

    items.forEach((item) => {
        if (item !== null) {
            if (typeof item === 'object') {
                for (let i = 0; i < item.length; i++) {
                    let item_li = document.createElement('li')
                    let item_a = document.createElement('a')
                    item_a.classList.add('dropdown-item', 'filter')
                    item_a.setAttribute('category', category_name.id)
                    item_a.innerHTML = item[i]
                    item_li.append(item_a)
                    dropdown_menu.append(item_li)
                }
            } else {
                let item_li = document.createElement('li')
                let item_a = document.createElement('a')
                item_a.classList.add('dropdown-item', 'filter')
                item_a.setAttribute('category', category_name.id)
                item_a.innerHTML = item
                item_li.append(item_a)
                dropdown_menu.append(item_li)
            }
        }
    })


    button.classList.add('btn', 'btn-secondary', 'dropdown-toggle')
    button.setAttribute('type', 'button')
    button.setAttribute('data-bs-toggle', 'dropdown')
    // button.setAttribute('data-bs-auto-close', 'false')
    button.setAttribute('aria-expanded', 'false')
    button.innerHTML = category_name.name
    button_div.append(button)
    button_div.append(dropdown_menu)
    return button_div
}

function create_filter_bottom_item(data, block_id) {
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

function create_filters(filters_buttons_list, data) {
    filters_buttons_list.forEach((button)=>{
        if (button.filter) {
            let filter_items = create_filter_bottom_item(data, button.id)
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
    else if (report.equipments.length > 0) {
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


function create_table_row(report, columns_list) {
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


function clean_duplicate_filters() {
    // очистка дубликатов в фильтрах

    let filters = document.getElementById('filters')

    filters.childNodes.forEach((filter)=>{
        if (filter.childNodes[1] !== undefined) {
            if (filter.childNodes[1].childNodes.length > 1) {
                let filter_list = []
                for (let i = 0; i < filter.childNodes[1].childNodes.length; i++) {
                    if (!filter_list.includes(filter.childNodes[1].childNodes[i].innerText)) {
                        filter_list.push(filter.childNodes[1].childNodes[i].innerText)
                    }
                    else {
                        filter.childNodes[1].childNodes[i].remove()
                    }
                    // filter_list.push(filter.childNodes[1].childNodes[i].innerText)
                }
            }
        }
    })
}

function create_paginator(pages_count, peer_count) {
    let paginator_ul = document.querySelector('.pagination')
    let prev = document.querySelector('previous')
    let pages =  Math.ceil(pages_count/ peer_count)
    let next_li = document.createElement('li')
    let next_div = document.createElement('div')
    next_div.classList.add('page-link')
    next_li.classList.add('page-item')
    next_div.setAttribute('id', 'next')
    next_div.innerHTML = 'Далее'
    next_li.append(next_div)
    for (let i = 1; i < pages + 1; i++) {
        let li = document.createElement('li')
        let li_div = document.createElement('div')
        li.classList.add('page-item')
        li.setAttribute('id', `page-${i}`)
        li_div.classList.add('page-link')
        if (i === 1) {
            li_div.setAttribute('limit', peer_count)
            li.classList.add('active')
            li_div.setAttribute('skip', 0)
            li.setAttribute('id', `page-1`)
        } else {
            li_div.setAttribute('limit', Number(peer_count) * i)
            li_div.setAttribute('skip', Number((peer_count) * i) - peer_count)
        }
        li_div.innerHTML = i
        li.append(li_div)
        paginator_ul.append(li)
    }
    paginator_ul.append(next_li)

}

function filterReport(url, limit=100, skip=0, filters) {
   return fetch(`${url}?limit=${limit}&skip=${skip}`, {
          method: "POST",
          headers: {"X-CSRFToken": csrf},
          body: JSON.stringify({depart: depart, filters: filters}),
      }
  ).then((res) => res.json())
        .then((data) => {
            return data})
}

function create_filters_table(filter_item, column_lists) {
    let new_set = new Map()
    new_set.set('filter_category', filter_item.getAttribute('category'))

    elements.push(`${filter_item.getAttribute('category')}_${filter_item.innerHTML}`)
    if (depart === 'director') {
        let data = filterReport(filter_report_1, limits.limit, limits.skip, elements)
    }
    let data = filterReport(filter_report_1, limits.limit, limits.skip, elements)
    table.innerHTML = ''
    filters_block.innerHTML = ''
    console.log(elements)
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

function filters_control(column_lists) {

    let filters_list = document.querySelectorAll('.filter')
    filters_list.forEach((filter_item) => {
        filter_item.addEventListener('click', () => {
            create_filters_table(filter_item, column_lists)
        })
    })
}


function links_control(column_lists, volumes) {
    let links = document.querySelectorAll('.page-link')

    links.forEach((link => {
        link.addEventListener('click', () => {
            console.log(elements)
            if (link.getAttribute('id') !== 'next') {
                link.parentNode.classList.add('active')
                let limit = link.getAttribute('limit')
                let skip = link.getAttribute('skip')
                limits.set('limit', limit)
                if (limit > 0) {
                    let nxt_btn = document.getElementById(`page-${(limit / 100) - 1}`)
                    let prv_btn = document.getElementById(`page-${(limit / 100) + 1}`)

                    if (nxt_btn != null) {
                        nxt_btn.classList.remove('active')
                    } else if (prv_btn != null) {
                        prv_btn.classList.remove('active')
                    }

                }
                limits.set('skip', skip)
                table.innerHTML = ''
                filters_block.innerHTML = ''
                let data = filterReport(filter_report_1, Number(limits.get('limit')), Number(limits.get('skip')), elements)
                data.then((data) => {
                    create_filters(column_lists, data)
                    clean_duplicate_filters()
                    create_table_head(column_lists, volumes)
                    data.data.forEach((report) => {
                        create_table_row(report, column_lists, volumes)
                    })
                    filters_control(column_lists, data)
                })
            } else {
                console.log('click')
            }
        })
    }))

}




// Первоначальная загрузка
load_data(100, 0).then(([reports, volumes, length, volumes_sum]) => {

     if (window.location.search.length > 0) {
         let filter_mask = window.location.search.slice(1).split('&')
         let worker = decodeURI(filter_mask[0].split('=')[1])
         let author = decodeURI(filter_mask[1].split('=')[1])
         let dep = decodeURI(filter_mask[2].split('=')[1])
         let filters = [`worker_${worker}`, `author_${author}`, 'working_Нет']

         let response = fetch(`${filter_report_1}?limit=100&skip=0`, {
             method: 'POST',
             headers: {"X-CSRFToken": csrf},
             body: JSON.stringify({depart: dep, 'filters': filters}),
         })
         response.then((res) => res.json()).then((data) => {
             if (dep === 'b2c') {
                 // create_filters(b2c_column_list, data)
                 // clean_duplicate_filters()
                 create_table_head(b2c_column_list, volumes)
                 data.data.forEach((report) => {
                     create_table_row(report, b2c_column_list, volumes, volumes_sum)
                 })
                 // filters_control(b2c_column_list, reports)

             } else if (depart === 'industrial' || depart === 'b2b' || 'director') {
                 // create_filters(industrial_column_list, data)
                 // clean_duplicate_filters()
                 create_table_head(industrial_column_list, volumes)
                 data.data.forEach((report) => {
                     create_table_row(report, industrial_column_list, volumes, volumes_sum)
                 })
                 // filters_control(industrial_column_list, reports)
             }
         })
     } else {

         if (depart === 'b2c') {
             // filters_control(b2c_column_list)
             create_filters(b2c_column_list, reports)
             clean_duplicate_filters()
             create_table_head(b2c_column_list, volumes)
             reports.data.forEach((report) => {
                 create_table_row(report, b2c_column_list, volumes, volumes_sum)
             })
             // create_paginator(length.count, 100)
             filters_control(b2c_column_list, reports)
         } else if (depart === 'industrial' || depart === 'b2b') {
             create_filters(industrial_column_list, reports)
             clean_duplicate_filters()
             create_table_head(industrial_column_list, volumes)
             reports.data.forEach((report) => {
                 create_table_row(report, industrial_column_list, volumes, volumes_sum)
             })
             // create_paginator(length.count, 100)
             filters_control(industrial_column_list, reports)
             links_control(industrial_column_list, volumes)

         } else if (depart === 'director') {

            create_director_buttons()

            let buttons = document.querySelectorAll('.btn')
            let main = document.getElementById('main')
            let div = document.getElementById('buttons')
            buttons.forEach((button) => {
                button.addEventListener('click', ()=>{
                    table.innerHTML = ''
                    div.style.position = 'relative'
                    div.style.top = '0'
                    div.style.left = '0'
                    if (button.id === 'b2c') {
                        create_director_report_1(button.id, b2c_column_list, b2c_volume_list)
                    }
                    else if (button.id === 'b2b') {
                        create_director_report_1(button.id, b2b_column_list, b2b_volume_list)
                    } else if (button.id === 'industrial') {
                        create_director_report_1(button.id, industrial_column_list, industrial_volume_list)
                    }
                })
            })

         }
     }
}).finally(() => {
    head_load.style.height = '0'
    footer_load.style.height = '0'
    loader.style.display = 'none'
})
