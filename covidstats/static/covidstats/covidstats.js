let margin = ({top: 0, right: 0, bottom: 10, left: 0})
let height = 550
let tickW = 0.9
let width
let transitionDuration =  500
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

String.prototype.format = String.prototype.f = function() {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

function tippyShow (t) {
    t.show()
    window.setTimeout(() => {
        t.hide()
    }, 3000)
}

let provData
let format = "harian"

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
        provData = response
        generateSVG()

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

function generateSVG(){
    m = provData.length
    
    svg = d3.select("#chart")
            .each((d, i, node) => {
                $(node[0]).hover(
                    function() {$(this).children().not(":last").toggleClass("svg-hover", true)},
                    function() {$(this).children().not(":last").toggleClass("svg-hover", false)}
                )
            })

    // tanggal = data.map((d) => (new Date(d.tanggal)).toISOString().slice(0,10))
    tanggal_obj = provData.map((d) => (new Date(d.tanggal)))

    $("#update-terakhir-chart").html("Update terakhir<br>" + tanggal_obj[tanggal_obj.length - 1].toLocaleDateString("id-ID", {day: 'numeric', month: 'short', year:'numeric'}))

    let keys
    if(format == "harian"){
        keys = ["MENINGGAL", "KASUS", "SEMBUH"]
    } else {
        keys = ["AKUMULASI_MENINGGAL", "AKUMULASI_KASUS", "AKUMULASI_SEMBUH"]
    }
    
    //Rerepresent data as stacked
    dataStacked = d3.transpose(
        d3.stack()
        .keys(keys)
        .order(d3.stackOrderNone)
        .offset(d3.stackOffsetNone)(provData))
        .map((d, i) => d.map(([y0, y1]) => [y0, y1, i]))

    let y1Max = d3.max(dataStacked, y => d3.max(y, d => d[1]))

    dataStacked = dataStacked.map((d,i) => d.concat([[0, d[2][1] + 1, i], [0, y1Max, i]]))

    x = d3.scaleUtc()
        // .domain([Math.floor(-(m * 0.05)), Math.ceil(m * 1.05)])
        .domain([
                new Date(tanggal_obj[0].valueOf() - (10 * 86400000)),
                new Date(tanggal_obj[tanggal_obj.length - 1].valueOf() + (10 * 86400000))
        ])

    //Function of relation between y axis and element's height
    y = d3.scaleLinear()
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
            default:
                return "#ffffff00"
        }
    }

    //Create all stacked bars
    rect = svg.selectAll("g")
        .data(dataStacked)
        .join(
          enter => enter.append("g"),
          update => update,
          exit => exit
            .selectAll("rect")
                .transition()
                .ease(d3.easeExpInOut)  
                .duration(transitionDuration)
                .attr("x", ((width - margin.right) - ((width - margin.right) / m * tickW) * 10))
                .attr("width", 0)
                .attr("y", height - margin.bottom)
                .attr("height", 0)
                .remove()
            .remove()
        )
        .selectAll("rect")
        .data(d => d)
        .join(
          enter => enter.append('rect')
            .attr("fill", (d, i) => z(i))
            .attr("y", height - margin.bottom)
            .attr('width', 0)
            .attr("height", 0)
            .each((d, i, node) => {
                if(i == 4){
                    $(node[4]).parent().hover(
                        function() {$(this).toggleClass("svg-hover", false)},
                        function() {$(this).toggleClass("svg-hover", true)}
                    );
                    tippy(node[3], {
                        triggerTarget: node[4],
                        content: `  <div class="d-flex flex-column">
                                        <p class="tooltip-tanggal">{3}</p>
                                        <p class="tooltip-box-sembuh">{0}</p>
                                        <p class="tooltip-box-positif">{1}</p>
                                        <p class="tooltip-box-meninggal">{2}</p>
                                    </div>`.format(node[2].__data__[1] - node[2].__data__[0], 
                                        node[1].__data__[1] - node[1].__data__[0], 
                                        node[0].__data__[1] - node[0].__data__[0],
                                        tanggal_obj[node[0].__data__[2]]
                                            .toLocaleDateString(
                                                "id-ID", 
                                                {
                                                    day: 'numeric', 
                                                    month: 'short', year:'numeric'
                                                })),
                        placement: "bottom",
                        allowHTML: true,
                        theme: "light",
                        duration: 0,
                        popperOptions: {
                            modifiers: [
                                {
                                    name: 'flip',
                                    options: {
                                        fallbackPlacements: ['bottom', 'top'],
                                        padding: -50
                                    }
                                }
                            ]
                        }
                    })
                }
            }),
          update => update
            .each((d, i, node) => {
                if(i == 3){
                    node[i]._tippy.setProps({
                        content: `  <div class="d-flex flex-column">
                                        <p class="tooltip-tanggal">{3}</p>
                                        <p class="tooltip-box-sembuh">{0}</p>
                                        <p class="tooltip-box-positif">{1}</p>
                                        <p class="tooltip-box-meninggal">{2}</p>
                                    </div>`.format(node[2].__data__[1] - node[2].__data__[0], 
                                        node[1].__data__[1] - node[1].__data__[0], 
                                        node[0].__data__[1] - node[0].__data__[0],
                                        tanggal_obj[node[0].__data__[2]]
                                            .toLocaleDateString(
                                                "id-ID", 
                                                {
                                                    day: 'numeric', 
                                                    month: 'short', year:'numeric'
                                                }))
                    })
                }
            }),
            exit => exit.remove()
        )

    //Create x Axis
    if(typeof xAxis === "undefined"){
        xAxis = svg.append("g")
            .attr("transform", `translate(0,${height - margin.bottom})`)
    }

    function updateX() {
        width = parseInt(svg.style("width"), 10)
        x.range([margin.left, width - margin.right])
        tickStep = Math.ceil(m / (width / 200))
        xAxis.call(d3.axisBottom(x)
            .tickValues(d3.timeDay.range(
                new Date(tanggal_obj[0].valueOf()),
                new Date(tanggal_obj[tanggal_obj.length - 1].valueOf()), //+ (tickStep * 86400000)),
                tickStep)
            )
            .tickFormat(d3.utcFormat("%d %b"))
            .tickSizeOuter(0))
    }

    function updateWidth() {
        rect.attr("x", d => x(tanggal_obj[d[2]]))
            .attr("width", (width - margin.right) / m * tickW)
    }

    //Transition Animation
    async function transitionStacked() {
        y.domain([0, y1Max]);

        //Run animation in rect simultaniously
        if(rect._groups[0][0].getAttribute('x') != null){
            rect.call(async function() {
                await d3.select({})
                    .transition()
                    .duration(transitionDuration)
                    .tween(
                        "attr:x",
                        function() {
                            interpX = rect._groups.map(
                                (el, i) => {
                                    let initX = parseFloat(el[3].getAttribute('x'))
                                    let nextX = x(tanggal_obj[i])
                                    
                                    return isNaN(initX) ? d3.interpolateNumber(((width - margin.right) - ((width - margin.right) / m * tickW) * 10), nextX) : d3.interpolateNumber(initX, nextX)
                                }
                            )
                            rectW = rect._groups[0][0].getAttribute('width')
                            expectedW = (width - margin.right) / m * tickW
                            interpWidth = rectW == 0 ? d3.interpolateNumber(expectedW, expectedW) : d3.interpolateNumber(rectW, expectedW)
                            return function(t) {
                                rect.each((d, i, node) => {
                                    d3.select(node[i])
                                    .attr("x", interpX[d[2]](t))
                                    .attr("width", interpWidth(t))
                                })
                            }
                        }
                    )
            })
        } else {
            updateWidth()
        }
        
        rect.transition()
            .ease(d3.easeExpInOut)  
            .duration(transitionDuration)
                .attr("y", d => y(d[1]))
                .attr("height", d => y(d[0]) - y(d[1]))
    }

    updateX()
    transitionStacked()

    if($("#chart:hover").length > 0){
        document.querySelector("#chart").dispatchEvent(new MouseEvent("mouseover"))
    }

    window.addEventListener('resize', function() {
        updateX()
        updateWidth()
    })
}


(() => {
    let list_daerah = ['DKI Jakarta', 'Jawa Timur', 'Jawa Barat', 'Jawa Tengah', 'Sulawesi Selatan', 'Sumatera Barat', 'Kalimantan Timur', 'Riau', 'Sumatera Utara', 'Bali', 'Kalimantan Selatan', 'Banten', 'Papua', 'Sumatera Selatan', 'Aceh', 'Sulawesi Utara', 'Sulawesi Tenggara', 'Kalimantan Tengah', 'Kepulauan Riau', 'Papua Barat', 'Daerah Istimewa Yogyakarta', 'Nusa Tenggara Barat', 'Maluku', 'Gorontalo', 'Lampung', 'Maluku Utara', 'Kalimantan Barat', 'Jambi', 'Bengkulu', 'Sulawesi Barat', 'Sulawesi Tengah', 'Kalimantan Utara', 'Nusa Tenggara Timur', 'Kepulauan Bangka Belitung', 'Indonesia']
    $("#input-daerah")
        .autocomplete({ source: list_daerah })    

    tippy('[data-tippy-content]', {
        placement: 'bottom',
        interactive: true,
        appendTo: document.body
    })

    let btnTgle = $("#buttonToggle")
    let tgl = btnTgle.parent()
    let logo = btnTgle.children()

    btnTgle[0].state = 0

    btnTgle.draggable({
        containment: "#toggle",
        axis: "y",
        drag: (event, ui) => {
            let child = $(ui.helper).children()
            let el = $(ui.helper)
            elH = el.height()
            elY = el.position().top
            child.css("top", -ui.position.top)
            //console.log((elH / 2 + elY) < (el.parent().height() / 2))
        },
        stop: (event, ui) => {
            let el = $(ui.helper)
            let child = el.children()
            elH = el.height()
            elY = el.position().top
    
            
            if((elH / 2 + elY) < (el.parent().height() / 2)){
                el[0].state = 0
                el.css("top", 0)
                child.css("top", 0)

                if(format != "harian"){
                    format = "harian"
                    generateSVG()
                }
            } else {
                el[0].state = 1
                el.css("top", el.parent().height() - elH)
                child.css("top", -(el.parent().height() - elH))

                if(format != "kumulatif"){
                    format = "kumulatif"
                    generateSVG()
                }
            }
        }
    })

    btnTgle.parent()
        .on("mousedown", (e) => {
            btnTgle.parent().on("mouseup mousemove", function handler(e) {
                if (e.type === "mouseup"){
                    if (btnTgle[0].state == 0){
                        btnTgle[0].state = 1
                        btnTgle.css("top", tgl.height() - btnTgle.height())
                        logo.css("top", -(tgl.height() - btnTgle.height()))

                        format = "kumulatif"
                        generateSVG()
                    } else {
                        btnTgle[0].state = 0
                        btnTgle.css("top", 0)
                        logo.css("top", 0)

                        format = "harian"
                        generateSVG()
                    }
                }
                btnTgle.parent().off('mouseup mousemove', handler);
            })
            
        })
})()


window.onload = () => {
    $("#form-daerah").on('submit', () => {
        let prov = formInput.val()
        generateChart(prov)

        return false
    })
    generateChart("INDONESIA")
}