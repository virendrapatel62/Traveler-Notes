

var map; // Map main object
var noteModalHtmlElement; // Note Modal Div Html Element Obbject
var noteModal // Bootstrap Model Object
var title, comment, lat, lng // form values
var form  // html form elemtn model form

const createNoteApi = '/api/notes' // urls
const getNotesApi = '/api/notes'  // urls
const deleteNotesApi = '/api/notes/'  // urls
const searchPlacesApi = '/api/map/search/places?address='  // urls
const elocApi = '/api/map/eloc/'  // urls

var detailModal // Bootstrap Object
var selectedMarkerLatLng

const PLACE_LIST_ID = 'places'


var notes = [];


//IDS
var noteDetailModalBodyId = 'noteDetailModalBody'
var noteDetailCardTemplateId = 'noteDetailCardTemplate'

window.onload = () => {
    console.log("On Load Function", CSRF_TOKEN)
    initializeMap()
    handleMapClick()
    modalSetup()
    handleNoteFormSubmission()
    getAllNotes()
    setupAddMore()
    handleSearchInputFieldKeyUpEvent()

}

function handlePlaceListItemClick() {
    const className = 'place-list-item'
    const placesElements = document.getElementsByClassName(className)

    for (let i = 0; i < placesElements.length; i++) {
        const placeElm = placesElements[i]
        placeElm.onclick = (event) => {
            address = JSON.parse(event.target.dataset.address)
            const { eLoc } = address
            console.log({ eLoc });

            $.ajax({
                url: elocApi + eLoc,
                type: "GET",
                beforeSend: () => {
                    document.getElementById(PLACE_LIST_ID).innerHTML = ""
                },
                success: (response) => {
                    const { results } = response
                    if (results.length > 0) {
                        const { longitude, latitude } = results[0]
                        console.log(latitude, longitude);
                        changeMapView(latitude, longitude)
                    }
                }
            })
        }
    }
}


function changeMapView(latitude, longitude) {
    map.setView({ lat: latitude, lng: longitude })
    map.setZoom(10)
}



// search Input Field Key Up Hanlde
function handleSearchInputFieldKeyUpEvent() {
    const searchInput = document.getElementById("searchInput")
    console.log({ searchInput });
    var request;
    searchInput.onkeyup = () => {
        const value = searchInput.value
        console.log({ search: value });
        // 
        if (request)
            request.abort()

        request = $.ajax({
            type: "GET",
            url: searchPlacesApi + value,
            success: function (data) {
                var addresses = []
                addresses = data.copResults

                var html = addresses.map(address => {
                    return `<li data-address='${JSON.stringify(address)}' class='list-group-item place-list-item'>${address.formattedAddress}</li>`
                }).join('')

                const listHtmlElement = document.getElementById(PLACE_LIST_ID)
                listHtmlElement.innerHTML = html

                handlePlaceListItemClick()

            }
        })


    }
}

function setupAddMore() {
    document.getElementById('addmore')
        .onclick = () => {
            lat = selectedMarkerLatLng.lat
            lng = selectedMarkerLatLng.lng
            detailModal.hide()
            noteModal.show()
        }
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


function afterSaveNote(note) {
    console.log({ note });

    notes.push(note)

    addMarker(note)
    noteModal.hide()
    form.reset()
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

function showDetailModal(event) {
    template = document.getElementById(noteDetailCardTemplateId)
    modalBody = document.getElementById(noteDetailModalBodyId)

    // clearing body
    while (modalBody.firstChild) {
        modalBody.removeChild(modalBody.firstChild)
    }

    filteredNotes = notes.filter(
        (note) => {
            if (note.lat == selectedMarkerLatLng.lat && note.lng == selectedMarkerLatLng.lng) return true

            return false
        }
    )

    console.log(filteredNotes)

    filteredNotes.forEach(note => {
        const card = template.cloneNode(true)
        card.hidden = false
        card.querySelector('.title').textContent = note.title
        card.querySelector('.comment').textContent = note.comment

        // delete Card Button Handle
        card.querySelector('.deleteNoteButton').onclick = () => {

            $.ajax({
                type: "DELETE",
                url: deleteNotesApi + note.id,
                beforeSend: (xhr) => {
                    xhr.setRequestHeader('X-CSRFTOKEN', CSRF_TOKEN)
                },
                success: () => {
                    detailModal.hide()
                    const index = notes.findIndex((value) => note.id == value.id)
                    if (index >= 0) {
                        notes.splice(index, 1)
                    }
                }
            });
        }

        modalBody.appendChild(card)
    })

    detailModal.show()
}

function saveNote() {
    const data = { lat, lng, title, comment, csrfmiddlewaretoken: CSRF_TOKEN }
    $.ajax({
        type: "POST",
        url: createNoteApi,
        data: data,
        success: afterSaveNote
    });
}

function handleNoteFormSubmission() {
    form = document.getElementById('noteForm')
    // handling form submission
    form.onsubmit = (event) => {

        event.preventDefault()
        const { title: titleInput, comment: commentInput } = form.elements

        title = titleInput.value
        comment = commentInput.value
        saveNote()
    }
}

function modalSetup() {
    console.log("Doing Modal Setup")
    noteModalHtmlElement = document.getElementById('noteModal')
    const detailModalDiv = document.getElementById('detailModal')
    noteModal = new bootstrap.Modal(noteModalHtmlElement)
    detailModal = new bootstrap.Modal(detailModalDiv)

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

function handleMapClick() {
    map.on('click', (event) => {
        const { latlng } = event
        // assigning to global variables
        lat = latlng.lat
        lng = latlng.lng
        noteModal.show()
    })
}


