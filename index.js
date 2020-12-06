mapboxgl.accessToken = "pk.eyJ1IjoibmFubzAxIiwiYSI6ImNraHVlYjQ4aDFidzYyeHBiemZlZ2d3d20ifQ.P6e2_ZATNHTAb6BWuadxFw";
/**
 * @typedef {{
 * dinosaur: string,
 * zone: string,
 * diet: string,
 * size: string,
 * weight: string,
 * speed: string,
 * lived: string,
 * price: string
 * }} dinosaur
 * 
 * @typedef {{
 * id: number,
 * name: string,
 * rank: string,
 * early_interval: string,
 * late_interval: string,
 * latitude: number,
 * longitude: number,
 * old_latitude: number,
 * old_longitude: number,
 * country: string,
 * state: string,
 * county: string,
 * formation: string,
 * lithology: string,
 * lithology_description: string,
 * comment: string
 * }} fossil
 * 
 * @typedef {{
 * name: string,
 * type: string,
 * start: number,
 * end: number,
 * color_rgb: string,
 * color_hex: string,
 * children: time[]
 * }} time
 */


//Variables globales
//J'ai mis des doc pour les types pour améliorer l'autocomplete
/** 
 * @type {Array<dinosaur>} 
*/
let dinos;
let map;
/**
 * @type {Array<fossil>}
 */
let fossils;
let fossilMarkers = [];
let popup = new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: true,
    closeOnMove: true,
    anchor: "left"
});
/**
 * @type {time}
 */
let timeline;
/**
 * @type {Object.<string, time>}
 */
let flatTimeline = {};

let icicle;

/** @type {Promise<Array<dinosaur>>} */
let dinoLoader = d3.csv("data/dinosaurs.csv");
/** @type {Promise<Array<fossil>>} */
let fossilLoader = d3.json("data/fossils.json");
/** @type {Promise<Array<time>>} */
let timelineLoader = d3.json("data/gts_tree.json");

Promise.all([dinoLoader, fossilLoader, timelineLoader]).then(([dinoData, fossilData, timelineData]) => {
    dinos = dinoData;
    fossils = fossilData;
    timeline = timelineData;
    /* flatTimeline */ buildTimeLineDict(timelineData);

    //Chargement et traitement des données
    loadDinos(dinoData);
    loadMap(fossilData);
    loadTimeline(timelineData);

    showDinoList("A");
    showDinoCard("Allosaurus");
}).catch((error) => {
    console.log(error);
    //alert("Une erreur a eu lieu lors du chargement des données.");
});

/**
 * @param {dinos} data 
 */
function loadDinos(data) {
    let initials = [];
    data.map((dino) => {
        let firstLetter = dino.dinosaur[0];
        //éviter les doublons
        if (!initials.includes(firstLetter)){
            initials.push(firstLetter);
        }
    });

    let btnGroup = document.getElementById("letter-slider");
    initials.map((letter) => {
        let btn = document.createElement("button");
        btn.classList.add("btn", "btn-info", "dino-letter");
        btn.textContent = letter.toUpperCase();
        btn.addEventListener("click", (ev) => {
            showDinoList(letter);
        });
        btnGroup.append(btn);
    })
    let btnReset = document.createElement("button");
    btnReset.classList.add("btn", "btn-dark", "dino-letter");
    btnReset.id = "reset-btn";
    btnReset.textContent = "Reset";
    btnReset.style.marginLeft = "10px";
    btnGroup.append(btnReset);

    btnReset.addEventListener("click", () => {
        /** @type {HTMLImageElement} */
        let img = document.getElementById("dino-image");
        img.src = `img/jurassicworld.png`;
        document.getElementById("dino-name").textContent = "No dinosaur selected";
        document.getElementById("dino-feature-zone").textContent = "-";
        document.getElementById("dino-feature-diet").textContent = "-";
        document.getElementById("dino-feature-size").textContent = "-";
        document.getElementById("dino-feature-weight").textContent = "-";
        document.getElementById("dino-feature-speed").textContent = "-";
        document.getElementById("dino-feature-price").textContent = "-";
        fossilMarkers.forEach((marker) => {
            marker.addTo(map);
        });
    });

};

/**
 * @param {fossils} fossilData
 */
function loadMap(fossilData) {
    map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        zoom: 1
    });

    fossilData.forEach((fossil) => {
        let color = flatTimeline[fossil.early_interval];
        let el = createMarker(color !== undefined ? {color: color.color_hex} : {});
        el.addEventListener("mouseenter", () => { 
            showFossilData(fossil); 
        });
        el.addEventListener("mouseleave", () => {
            popup.remove();
        })
        el.addEventListener("click", () => {
            //console.log(fossil.early_interval);
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
    });

    map.zoomTo(1);
    map.setCenter([0,30]);

};

function loadTimeline(data) {
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
        .excludeRoot(true)
        .tooltipContent((d) => `From -${d.start} to -${d.end} Mil. years ago`)
        .minSegmentWidth(3)
        (timelineEl);

};

/**
 * Construit un dictionnaire non-récursif des ères pour un accès facile
 * @param {time} time 
 */
function buildTimeLineDict(time) {
    let name = time.name.toLowerCase();
    flatTimeline[name] = time;

    time.children.forEach((child) => {
        buildTimeLineDict(child);
    });
}

function createMarker(options = {}) {
    let defaultOptions = {
        width: 15,
        height: 15,
        color: "#4040D0",//"rgba(60,60,220,0.8)"//
        opacity: 0.6
    };
    options = Object.assign(defaultOptions, options);
    let el = document.createElement("div");
    el.classList.add("marker");
    el.style.width = `${options.width}px`;
    el.style.height = `${options.height}px`;
    el.style.borderRadius = "100%";
    el.style.borderWidth = "1px";
    el.style.borderStyle = "solid";
    el.style.backgroundColor = options.color;
    el.style.opacity = options.opacity;

    return el;
}

function showDinoList(letter) {
    let dinoSelector = document.getElementById("dino-selector");

    //Vider l'élément HTML
    while (dinoSelector.hasChildNodes()){
        dinoSelector.removeChild(dinoSelector.firstChild);
    }

    let validDinos = dinos.filter((dino) => dino.dinosaur[0].toLowerCase() === letter.toLowerCase());

    let btnGroup = document.getElementById("dino-selector");
    validDinos.map((dino) => {
        let btn = document.createElement("button");
        btn.classList.add("btn", "btn-light", "dino-button");
        btn.textContent = dino.dinosaur;
        btn.addEventListener("click", (ev) => {
            showDinoCard(dino.dinosaur)
        });
        btnGroup.append(btn);
    })
}

/**
 * @param {string} dinoname 
 */
function showDinoCard(dinoname) {
    let dinoData = dinos.find((dino) => {
        return dino.dinosaur.toLowerCase() === dinoname.toLowerCase();
    });

    /** @type {HTMLImageElement} */
    let img = document.getElementById("dino-image");
    img.src = `img/${dinoData.dinosaur}.png`;
    document.getElementById("dino-name").textContent = dinoData.dinosaur;
    document.getElementById("dino-feature-zone").textContent = dinoData.zone;
    document.getElementById("dino-feature-diet").textContent = dinoData.diet;
    document.getElementById("dino-feature-size").textContent = dinoData.size;
    document.getElementById("dino-feature-weight").textContent = dinoData.weight;
    document.getElementById("dino-feature-speed").textContent = dinoData.speed;
    document.getElementById("dino-feature-price").textContent = dinoData.price;

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

/**
 * @param {fossil} fossil 
 */
function showFossilData(fossil) {
    popup
        .setLngLat([fossil.longitude, fossil.latitude])
        .setHTML(`<div>
        ${fossil.name} <br />
        Current pos.: (${fossil.latitude}, ${fossil.longitude}) <br />
        Old pos.: (${fossil.old_latitude}, ${fossil.old_longitude}) <br />
        </div>`)
        .addTo(map);
}

function zoomToInterval(intervalName) {
    let intervalData = flatTimeline[intervalName];
    //console.log(intervalData);
    if (intervalData !== undefined) {
        icicle.zoomToNode(intervalData);
    }
}

/*
 * Cherche récursivement l'intervalle demandé dans la ligne du temps
 * @param {time} data 
 * @param {string} intervalName 
 * @returns {time}
 */
/*function findIntervalIn(data, intervalName){
    if (data.name.toLowerCase() === intervalName.toLowerCase()) {
        return data;
    } else {
        let result = data.children.map((child) => findIntervalIn(child, intervalName));
        //console.log(result);
        return result.find((value) => value !== undefined);
    }
}*/