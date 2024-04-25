let map;

document.addEventListener('DOMContentLoaded', () => {
    const launchSiteElement = document.getElementById('launch-site');
    const spaceRocketElement = document.getElementById('space-rocket');
    const spacesuitElement = document.getElementById('spacesuit');
    const fuelTypeElement = document.getElementById('fuel-type');
    const fuelQuantityElement = document.getElementById('fuel-quantity');
    const foodSuppliesElement = document.getElementById('food-supplies');
    const estimatedCostElement = document.getElementById('estimated-cost');
    const launchButton = document.getElementById('launch-button');
    const rocketAnimationElement = document.getElementById('rocket-animation');
    const rocketElement = document.querySelector('.rocket');
    const statusElement = document.getElementById('status');

    let previousState = {};

    function initializeMap() {
        map = L.map('map').setView([0, 0], 1);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
            maxZoom: 18,
        }).addTo(map);
    }

    function updateMap(launchSite) {
        const locations = {
            "Guiana Space Centre, French Guiana": { latitude: 5.239, longitude: -52.768 },
            "Baikonur Cosmodrome, Kazakhstan": { latitude: 45.965, longitude: 63.305 },
            "Vandenberg Space Force Base, USA": { latitude: 34.759, longitude: -120.554 },
            "Rocket Lab Launch Complex 1, New Zealand": { latitude: -39.262, longitude: 177.864 },
            "Cape Canaveral Space Launch Complex, Florida": { latitude: 28.396, longitude: -80.605 }
        };

        if (launchSite && locations[launchSite]) {
            const location = locations[launchSite];
            const latlng = [location.latitude, location.longitude];
            map.setView(latlng, 8);

            const marker = L.marker(latlng).addTo(map);
            marker.bindPopup(launchSite).openPopup();
        } else {
            map.setView([0, 0], 1);
            map.eachLayer(layer => {
                if (layer instanceof L.Marker) {
                    map.removeLayer(layer);
                }
            });
        }
    }

    function updateElement(element, value, previousValue) {
        if (value !== previousValue) {
            element.textContent = value || 'Not selected';
            element.classList.add('updated');
            setTimeout(() => {
                element.classList.remove('updated');
            }, 1000);
        }
    }

    function updateState() {
        fetch('/api/state')
            .then(response => response.json())
            .then(state => {
                updateElement(launchSiteElement, state.selected_launch_site, previousState.selected_launch_site);
                updateMap(state.selected_launch_site);
                updateElement(spaceRocketElement, state.selected_rocket, previousState.selected_rocket);
                updateElement(spacesuitElement, state.selected_suit, previousState.selected_suit);
                updateElement(fuelTypeElement, state.fuel_type, previousState.fuel_type);
                updateElement(fuelQuantityElement, state.fuel_quantity, previousState.fuel_quantity);
                updateElement(foodSuppliesElement, state.food_supplies, previousState.food_supplies);
                updateElement(estimatedCostElement, state.estimated_cost, previousState.estimated_cost);
                previousState = state;
            });
    }

    function launchRocket() {
        launchButton.disabled = true;
        fetch('/launch', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                statusElement.textContent = data.message;
                rocketAnimationElement.classList.add('launch');
                setTimeout(() => {
                    rocketAnimationElement.classList.remove('launch');
                    rocketElement.style.opacity = '0';
                    launchButton.disabled = false;
                    showCrewTransmissionPopup();
                }, 3000);
            });
    }

    function showCrewTransmissionPopup() {
        const popup = document.getElementById('crew-transmission-popup');
        const viewTransmissionButton = document.getElementById('view-transmission-button');
        const closePopupButton = document.getElementById('close-popup-button');
        const crewPhotoContainer = document.getElementById('crew-photo-container');
        const loadingIndicator = document.getElementById('loading-indicator');

        viewTransmissionButton.addEventListener('click', () => {
            loadingIndicator.style.display = 'block';
            fetch('/api/crew-photo')
                .then(response => response.json())
                .then(data => {
                    const imageUrl = data.image_url;
                    const crewPhoto = document.createElement('img');
                    crewPhoto.src = imageUrl;
                    crewPhoto.onload = () => {
                        loadingIndicator.style.display = 'none';
                        crewPhotoContainer.innerHTML = '';
                        crewPhotoContainer.appendChild(crewPhoto);
                    };
                });
        });

        closePopupButton.addEventListener('click', () => {
            popup.style.display = 'none';
        });

        setTimeout(() => {
            popup.style.display = 'block';
        }, 5000);
    }

    function pollState() {
        updateState();
        setTimeout(pollState, 1000);
    }

    initializeMap();
    launchButton.addEventListener('click', launchRocket);
    pollState();
});