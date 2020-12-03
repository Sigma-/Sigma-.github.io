mapboxgl.accessToken = "pk.eyJ1IjoibmFubzAxIiwiYSI6ImNraHVlYjQ4aDFidzYyeHBiemZlZ2d3d20ifQ.P6e2_ZATNHTAb6BWuadxFw";

//Variables globales
/** 
 * @type {any[]} 
 * Attributs de chaque élément dans dino: dinosaur,zone,diet,size,weight,speed,lived
*/
let dinos;
let map;
/**
 * Attributs de chaque élément dans fossils: 
 * id, name (génome + espèce), rank (species/genus), early_interval, late_interval, 
 * latitude, longitude, old_latitude, old_longtitude, 
 * country, state, county,
 * formation, lithology, lithology_description, comment
 */
let fossils;
let fossilMarkers = [];
let popup = new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: false
});
let timeline;
let icicle;

d3.csv("data/dinosaurs.csv").then(function(data) {
    console.log(data);

    let initials = [];
    data.map((dino) => {
        let firstLetter = dino.dinosaur[0];
        //éviter les doublons
        if (!initials.includes(firstLetter)){
            initials.push(firstLetter);
        }
    });

    dinos = data;

    let btnGroup = document.getElementById("letter-slider");
    initials.map((letter) => {
        let btn = document.createElement("button");
        btn.classList.add("btn", "btn-secondary", "dino-letter");
        btn.textContent = letter;
        btn.addEventListener("click", (ev) => {
            showDinoList(letter);
        });
        btnGroup.append(btn);
    })

});

d3.json("data/fossils.json").then(function(data) {
    console.log(data);
    map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11'
    });

    data.forEach((fossil) => {
        let el = createMarker();
        el.addEventListener("mouseenter", () => { showFossilData(fossil); });
        el.addEventListener("click", () => {
            console.log(fossil.early_interval);
            zoomToInterval(fossil.early_interval);
        })
        //el.addEventListener("mouseleave", (thisEl) => {});
        let marker = new mapboxgl.Marker({
            element: el
        })
            .setLngLat([fossil.longitude, fossil.latitude])
            .addTo(map);
        //Lier les données de fossile au marqueur
        marker.fossil = fossil;
        fossilMarkers.push(marker);
    })
    fossils = data;


});

d3.json("data/gts_tree.json").then(function(data) {
    console.log(data);

    let timelineEl = document.getElementById("timeline");
    let elSize = timelineEl.getBoundingClientRect();
    let width = elSize.width;
    let height = elSize.height;

    //https://github.com/vasturiano/icicle-chart
    icicle = Icicle();
    icicle.data(data)
        .orientation("td") //top-down
        .width(width)
        .height(height)
        .size((d) => {
            if (d.children.length === 0) {
                return d.start - d.end
            } else {
                return 0
            }
        })
        .label((d) => `${d.name} ${d.type}`)
        .color("color_hex")
        //.excludeRoot(true)
        .tooltipContent((d) => `From ${d.start} to ${d.end}`)
        .minSegmentWidth(3)
        (timelineEl);

    timeline = data;
});

function createMarker(options = {}) {
    let defaultOptions = {
        width: 8,
        height: 8,
        color: "#4040D0"
    };
    options = Object.assign(defaultOptions, options);
    let el = document.createElement("div");
    el.classList.add("marker");
    el.style.width = `${options.width}px`;
    el.style.height = `${options.height}px`;
    el.style.borderRadius = "100%";
    el.style.backgroundColor = options.color;

    return el;
}

function showDinoList(letter) {
    let dinoSelector = document.getElementById("dino-selector");

    //Vider l'élément HTML
    while (dinoSelector.hasChildNodes()){
        dinoSelector.removeChild(dinoSelector.firstChild);
    }

    let validDinos = dinos.filter((dino) => dino.dinosaur[0] === letter);

    let btnGroup = document.getElementById("dino-selector");
    validDinos.map((dino) => {
        let btn = document.createElement("button");
        btn.classList.add("btn", "btn-secondary", "dino-button");
        btn.textContent = dino.dinosaur;
        btn.addEventListener("click", (ev) => {
            showDinoCard(dino.dinosaur)
        });
        btnGroup.append(btn);
    })
}

function showDinoCard(dinoname) {
    let dinoData = dinos.find((dino) => {
        return dino.dinosaur === dinoname;
    });

    /** @type {HTMLImageElement} */
    let img = document.getElementById("dino-image");
    img.src = `img/${dinoData.dinosaur}.png`;
    document.getElementById("dino-feature-zone").textContent = dinoData.zone;
    document.getElementById("dino-feature-diet").textContent = dinoData.diet;
    document.getElementById("dino-feature-size").textContent = dinoData.size;
    document.getElementById("dino-feature-weight").textContent = dinoData.weight;
    document.getElementById("dino-feature-speed").textContent = dinoData.speed;

    fossilMarkers.forEach((marker) => {
        //Récupérer le nom du génus
        let markerDinoName = marker.fossil.name.split(" ")[0];
        //Si le marqueur correspond au dino choisi
        if (markerDinoName.toLowerCase() === dinoname.toLowerCase()) {
            marker.addTo(map);
        } else {
            marker.remove();
        }
    });
}

function showFossilData(fossil) {
    popup
        .setLngLat([fossil.longitude, fossil.latitude])
        .setHTML(`<div>
        ${fossil.old_latitude}, ${fossil.old_longtitude}
        </div>`)
        .addTo(map);
}

function zoomToInterval(intervalName) {
    let intervalData = findIntervalIn(timeline, intervalName);
    console.log(intervalData);
    if (intervalData !== undefined) {
        icicle.zoomToNode(intervalData);
    }
}

function findIntervalIn(data, intervalName){
    if (data.name.toLowerCase() === intervalName.toLowerCase()) {
        return data;
    } else {
        let result = data.children.map((child) => findIntervalIn(child, intervalName));
        console.log(result);
        return result.find((value) => value !== undefined);
    }
}