var data = {}


$("#link-btn").click(e => {
    e.preventDefault()
    data = {}
    const url = $("#link").val()
    const jsonData = {
        "url": url
    }
    fetch("/compete", {
        method: "POST",
        headers: {
            "Content-Type": 'application/json; charset=UTF-8'
        },
        body: JSON.stringify(jsonData)
    }).then(
        response => response.json()
    ).then(
        json => {
            if (json.status === "success") {
                copyData(json)
                console.log(data)
                buildTable(json.table)
            } else {
                window.alert("網址不正確")
                $("#link").val("")
            }
        }
    )
})


const copyData = json => {
    for (const key in json) {
        data[key] = json[key]
    }
}


const writeTableHeader = name => {
    return `<th>${name}</th>`
}


const writeTableCell = (h1, h2, number) => {
    return `<td><a class='link' onclick="getVersusData('${h1}', '${h2}') ">${number}</a></td>`
}


const buildTable = table => {   

    console.log(table)

    let n = table.length
    let tableHTML = ""

    for (let i = 0; i < n; i++) {
        tableHTML += "<tr>"
        for (let j = 0; j < n; j++) {
            if (i == 0 || j == 0) {
                tableHTML += writeTableHeader(table[i][j])
            } else {
                tableHTML += writeTableCell(table[i][0], table[0][j], table[i][j])
            }
        }
        tableHTML += "</tr>"
    }

    $("#result > table").html(tableHTML)
}


const getVersusData = (h1, h2) => {
    let versusKey = `${h1}, ${h2}`

    let row1 = `<tr><th>場次</th>`
    let row2 = `<tr><th>${h1}</th>`
    let row3 = `<tr><th>${h2}</th>`

    data[versusKey].forEach(it => {
        console.log(it)
        if (it.highQuality) {
            row1 += `<td class="highlighted"><a href="${it.url}" target="_blank">${it.id}</a></td>`
        } else {
            row1 += `<td><a href="${it.url}" target="_blank">${it.id}</a></td>`
        }
        row2 += `<td>${it.h1}</td>`
        row3 += `<td>${it.h2}</td>`
    })
    
    let tableHTML = row1 + row2 + row3
    $("#versus-tbl").html(tableHTML)
}
