ymaps.ready(init)

function init() {

    let myMap = new ymaps.Map('map', {
        center: position,
        zoom: 15
    }),
        objectManager = new ymaps.ObjectManager(
        );
    objectManager.objects.options.set('preset', 'islands#redDotIcon');
    objectManager.clusters.options.set('preset', 'islands#redClusterIcons');
    myMap.geoObjects.add(objectManager);
    objectManager.add(point_data);
}

function create_volume_table() {
    let vectors_block = document.querySelector('.vectors')
    fetch(get_vector_url, {
        method: 'POST',
        headers: {"X-CSRFToken": csrf},
        body: JSON.stringify({'census_id': Number(census_id)}),
    }).then((res)=> {
        res.json().then((data) => {
            data.data.forEach((item)=>{
                let volume_item = document.createElement('div')
                volume_item.classList.add('vector-item')

                let table = document.createElement('table')
                table.classList.add('table', 'table-striped')
                table.style.width = '200px'

                let thead = document.createElement('thead')
                let tr = document.createElement('tr')
                let th = document.createElement('th')
                th.setAttribute('scope', 'col')
                th.innerHTML = item.vectors
                tr.append(th)
                thead.append(tr)
                table.append(thead)
                // vectors_block.append(table)

                item.value.forEach((value) => {
                    let tbody = document.createElement('tbody')
                    let tbody_tr = document.createElement('tr')
                    let tbody_th = document.createElement('th')
                    tbody_th.setAttribute('scope', 'col')
                    tbody_th.innerHTML = value
                    tbody_tr.append(tbody_th)
                    tbody.append(tbody_tr)
                    table.append(tbody)
                })
                vectors_block.append(table)
            })
        })
    })
}

create_volume_table()

