var map;
const getNotesApi = '/api/notes'  // urls
window.onload = () => {
    initializeMap()
    getAllNotes()
}


function getAllNotes() {
    $.ajax({
        type: "GET",
        url: getNotesApi,
        success: function (data) {
            console.log({ data });

            notes = data;
            for (let index = 0; index < notes.length; index++) {
                const note = notes[index]
                addMarker(note)
            }
        }
    })
}

function addMarker(note) {
    // add marker
    const { lat, lng } = note
    const marker = L.marker([lat, lng]).addTo(map);

    marker.on('click', event => {
        selectedMarkerLatLng = event.latlng
        showDetailModal(event)
    })

}


function initializeMap() {
    console.log("Initialize Map Function")
    map = new MapmyIndia.Map(
        "map",
        {
            center: [20.5937, 78.9629],
            zoomControl: true,
            zoom: 5,
            hybrid: true
        }
    );
}