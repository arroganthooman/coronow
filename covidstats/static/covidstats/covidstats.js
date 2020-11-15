let margin = ({top: 0, right: 0, bottom: 10, left: 0})
let height = 500
let width = 4000
let form = $("#form-daerah")
let formInput = $("#input-daerah")
let csrftoken = $('[name="csrfmiddlewaretoken"]').attr("value")
let url = $('[name="url"]').attr("value")
let provDaerah = $("#prov-daerah")
let tippy_prov_not_found = tippy("#input-daerah", {
    arrow: tippy.roundArrow,
    content: "Nama provinsi tidak ditemukan",
    theme: "light",
    animation: "shift-toward",
    trigger: "manual"
})[0]

function tippyShow (t) {
    t.show()
    window.setTimeout(() => {
        t.hide()
    }, 3000)
}

function generateChart(provinsi){
    $.ajax({
        url: url,
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        dataType: "json",
        data: {
            prov: provinsi,
            post_type: "POST_PROV"
        }
    }).done(function(response) {
        createSVG(response)
        formInput.val('')
        provinsi = provinsi.toLowerCase()
        if (provinsi.includes("dki")){
            provinsi = "DKI Jakarta"
        }
        provDaerah.html(provinsi)
    }).fail(function (error) {
        if(error.responseJSON['not-found'] == true){
            tippyShow(tippy_prov_not_found)
        } else{
            console.log(error);
        }
    });
}

function createSVG(data){
    let m = data.length
    
    //Rerepresent data as stacked
    dataStacked = d3.transpose(
        d3.stack()
        .keys(["MENINGGAL", "KASUS", "SEMBUH"])
        .order(d3.stackOrderNone)
        .offset(d3.stackOffsetNone)(data))
        .map((d, i) => d.map(([y0, y1]) => [y0, y1, i]))

    let y1Max = d3.max(dataStacked, y => d3.max(y, d => d[1]))

    //Function of relation between x axis and element's width
    let x = d3.scaleBand()
        .domain(d3.range(m))
        .rangeRound([margin.left, width - margin.right])
        .padding(0.08)

    //Function of relation between y axis and element's height
    let y = d3.scaleLinear()
        .domain([0, y1Max])
        .range([height - margin.bottom, margin.top])
        
    //Function of color representation of data based on category
    let z = function(i){
        switch (i) {
            case 0:
                return "#C8312A" 
            case 1:
                return "#FBD46D"
            case 2:
                return "#4F8A8B"
        }
    }

    //Function to create x Axis g element
    function xAxis (svg){
        svg.append("g")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x).tickSizeOuter(0).tickFormat(() => ""))
    }

    //Create SVG element container
    svg = d3.select("#chart-container")
        .html("")
        .append("svg")
        .attr("viewBox", [0, 0, width, height])
        .attr("xmlns", "http://www.w3.org/2000/svg")
        .attr("preserveAspectRatio", "none")
        .attr("width", "80vw")
        .style("height", "clamp(450px, 80vw, 530px)")

    //Create all stacked bars
    rect = svg.selectAll("g")
        .data(dataStacked)
        .join("g")
        .selectAll("rect")
        .data(d => d)
        .join("rect")
          .attr("fill", (d, i) => z(i))
          .attr("x", (d) => x(d[2]))
          .attr("y", height - margin.bottom)
          .attr("width", x.bandwidth())
          .attr("height", 0);

    //Create x Axis
    svg.append("g")
        .call(xAxis)
        .attr("class", "stroke-black")

    //Transition Animation
    function transitionStacked() {
        y.domain([0, y1Max]);
    
        rect.transition()
            .ease(d3.easeExpInOut)  
            .duration(700)
            //.delay((d, i) => i * 50)
            .attr("y", d => y(d[1]))
            .attr("height", d => y(d[0]) - y(d[1]))
            .transition()
            .attr("x", (d, i) => x(d[2]))
            .attr("width", x.bandwidth());
    }

    transitionStacked()
}


(() => {
    let list_daerah = ['DKI Jakarta', 'Jawa Timur', 'Jawa Barat', 'Jawa Tengah', 'Sulawesi Selatan', 'Sumatera Barat', 'Kalimantan Timur', 'Riau', 'Sumatera Utara', 'Bali', 'Kalimantan Selatan', 'Banten', 'Papua', 'Sumatera Selatan', 'Aceh', 'Sulawesi Utara', 'Sulawesi Tenggara', 'Kalimantan Tengah', 'Kepulauan Riau', 'Papua Barat', 'Daerah Istimewa Yogyakarta', 'Nusa Tenggara Barat', 'Maluku', 'Gorontalo', 'Lampung', 'Maluku Utara', 'Kalimantan Barat', 'Jambi', 'Bengkulu', 'Sulawesi Barat', 'Sulawesi Tengah', 'Kalimantan Utara', 'Nusa Tenggara Timur', 'Kepulauan Bangka Belitung', 'Indonesia']
    $("#input-daerah")
        .autocomplete({ source: list_daerah })    
})()

window.onload = () => {
    $("#form-daerah").on('submit', () => {
        let prov = formInput.val()
        generateChart(prov)

        return false
    })
    generateChart("INDONESIA")
}