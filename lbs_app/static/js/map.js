document.addEventListener("DOMContentLoaded", async function() {
    // Initialize map centered on Dublin, Ireland
    const map = L.map("map").setView([53.3498, -6.2603], 6);
    
    // Add OpenStreetMap tiles
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);
    
    // Marker layer group and marker store
    const markers = L.layerGroup().addTo(map);
    const markerStore = new Map(); // Store markers by business ID
    let searchLocationMarker = null; // Marker for search location
    
    // Custom icon colors based on category
    const iconColors = {
        'Restaurant': '#f5576c',
        'Retail': '#667eea',
        'Services': '#4facfe'
    };
    
    function createCustomIcon(color, index = null) {
        const badge = index !== null ? `<div style="position: absolute; top: -8px; right: -8px; background: white; color: ${color}; width: 24px; height: 24px; border-radius: 50%; border: 2px solid ${color}; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px;">${index}</div>` : '';
        return L.divIcon({
            className: 'custom-marker',
            html: `
                <div style="position: relative; background-color: ${color}; width: 35px; height: 35px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>
                ${badge}
            `,
            iconSize: [35, 35]
        });
    }
    
    // Create custom icon for search location
    function createSearchLocationIcon() {
        return L.divIcon({
            className: 'search-location-marker',
            html: `
                <div style="position: relative;">
                    <div style="background-color: #ff6b6b; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 8px; height: 8px; background: white; border-radius: 50%;"></div>
                </div>
            `,
            iconSize: [20, 20]
        });
    }
    
    // Function to calculate zoom level based on radius (meters)
    function getZoomLevelForRadius(radius) {
        // Approximate zoom levels for different radius
        if (radius <= 500) return 16;
        if (radius <= 1000) return 15;
        if (radius <= 2000) return 14;
        if (radius <= 5000) return 13;
        if (radius <= 10000) return 12;
        if (radius <= 20000) return 11;
        return 10;
    }
    
    // Load all businesses on initial load
    async function loadInitialBusinesses() {
        try {
            const businesses = await Api.fetchBusinesses();
            refreshMarkers(businesses);
        } catch (error) {
            console.error("Error loading businesses:", error);
        }
    }
    
    // Refresh map markers with businesses - supports numbered markers
    function refreshMarkers(businesses, highlightBusinesses = null) {
        markers.clearLayers();
        markerStore.clear();
        
        // Safety check: ensure businesses is an array
        if (!businesses || !Array.isArray(businesses)) {
            console.error("Invalid businesses data:", businesses);
            return;
        }
        
        businesses.forEach(business => {
            const [lon, lat] = business.location.coordinates;
            const color = iconColors[business.category.name] || '#667eea';
            
            // Check if this business should have a number
            let number = null;
            if (highlightBusinesses) {
                const index = highlightBusinesses.findIndex(b => b.id === business.id);
                if (index !== -1) {
                    number = index + 1;
                }
            }
            
            const marker = L.marker([lat, lon], {
                icon: createCustomIcon(color, number),
                isHighlighted: number !== null
            }).addTo(markers);
            
            // Store marker for clicking from list
            markerStore.set(business.id, marker);
            
            // Create enhanced popup
            const prefix = number ? `#${number}: ` : '';
            const popup = `
                <div class="popup-content">
                    <h6 class="fw-bold mb-2" style="color: ${color};">${prefix}${business.name}</h6>
                    <p class="mb-2"><span class="badge" style="background-color: ${color};">${business.category.name}</span></p>
                    ${business.description ? `<p class="small mb-2 text-muted">${business.description}</p>` : ""}
                    ${business.phone ? `<p class="small mb-1"><i class="bi bi-telephone"></i> ${business.phone}</p>` : ""}
                    ${business.website ? `<p class="small mb-0"><a href="${business.website}" target="_blank" class="text-decoration-none"><i class="bi bi-globe"></i> Visit Website</a></p>` : ""}
                </div>
            `;
            
            marker.bindPopup(popup);
        });
    }
    
    // Update nearest businesses list with enhanced styling and click handlers
    async function updateNearestList(lat, lon) {
        const listElement = document.getElementById("nearest-list");
        listElement.innerHTML = `
            <div class="text-center py-3">
                <div class="spinner-border spinner-border-sm text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2 text-muted mb-0">Finding businesses...</p>
            </div>
        `;
        
        try {
            const businesses = await Api.fetchNearest(lat, lon, 10);
            
            if (businesses.length === 0) {
                listElement.innerHTML = `
                    <div class="text-center text-muted py-3">
                        <i class="bi bi-exclamation-circle fs-4"></i>
                        <p class="mt-2 mb-0">No businesses found</p>
                    </div>
                `;
                return businesses;
            }
            
            listElement.innerHTML = "";
            businesses.forEach((business, index) => {
                const color = iconColors[business.category.name] || '#667eea';
                const div = document.createElement("div");
                div.className = "business-item";
                div.innerHTML = `
                    <div class="d-flex align-items-start">
                        <div class="me-3">
                            <div class="fw-bold text-center" style="width: 40px; height: 40px; line-height: 40px; border-radius: 50%; background-color: ${color}; color: white; border: 3px solid white; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">${index + 1}</div>
                        </div>
                        <div class="flex-grow-1">
                            <div class="fw-bold mb-1">${business.name}</div>
                            <div class="badge mb-1" style="background-color: ${color}; font-size: 0.7rem;">${business.category.name}</div>
                            ${business.description ? `<div class="small text-muted">${business.description.substring(0, 60)}${business.description.length > 60 ? '...' : ''}</div>` : ''}
                        </div>
                    </div>
                `;
                
                // Click handler to zoom to business and open popup
                div.addEventListener('click', () => {
                    const marker = markerStore.get(business.id);
                    if (marker) {
                        map.setView([business.location.coordinates[1], business.location.coordinates[0]], 15);
                        marker.openPopup();
                    }
                });
                
                listElement.appendChild(div);
            });
            
            return businesses;
        } catch (error) {
            console.error("Error updating nearest list:", error);
            listElement.innerHTML = `
                <div class="text-center text-danger py-3">
                    <i class="bi bi-exclamation-triangle fs-4"></i>
                    <p class="mt-2 mb-0">Error loading results</p>
                </div>
            `;
            return [];
        }
    }
    
    // Handle search form submission - zoom to radius and show numbered markers
    const searchForm = document.getElementById("search-form");
    searchForm.addEventListener("submit", async function(event) {
        event.preventDefault();
        
        const lat = parseFloat(document.getElementById("latitude").value);
        const lon = parseFloat(document.getElementById("longitude").value);
        const radius = parseInt(document.getElementById("radius").value) || 5000;
        
        try {
            // Get businesses within radius
            const businesses = await Api.fetchNearby(lat, lon, radius);
            
            // Get nearest 10 for numbering
            const nearestBusinesses = await updateNearestList(lat, lon);
            
            // Show all businesses within radius, with numbers on nearest 10
            refreshMarkers(businesses, nearestBusinesses);
            
            // Add or update search location marker
            if (searchLocationMarker) {
                map.removeLayer(searchLocationMarker);
            }
            searchLocationMarker = L.marker([lat, lon], {
                icon: createSearchLocationIcon()
            }).addTo(map);
            searchLocationMarker.bindPopup("<strong>Search Location</strong>");
            
            // Zoom to location based on radius
            const zoomLevel = getZoomLevelForRadius(radius);
            map.setView([lat, lon], zoomLevel);
        } catch (error) {
            console.error("Error searching:", error);
            alert("Error searching for businesses. Please try again.");
        }
    });
    
    // Handle name search form submission
    const nameSearchForm = document.getElementById("name-search-form");
    nameSearchForm.addEventListener("submit", async function(event) {
        event.preventDefault();
        
        const name = document.getElementById("business-name").value.trim();
        if (!name) {
            alert("Please enter a business name to search");
            return;
        }
        
        try {
            const businesses = await Api.searchByName(name);
            
            if (businesses.length === 0) {
                alert("No businesses found with that name");
                return;
            }
            
            // Clear previous search location marker
            if (searchLocationMarker) {
                map.removeLayer(searchLocationMarker);
            }
            
            // Show all matching businesses
            refreshMarkers(businesses);
            
            // Update results list
            const listElement = document.getElementById("nearest-list");
            listElement.innerHTML = "";
            businesses.forEach((business, index) => {
                const color = iconColors[business.category.name] || '#667eea';
                const div = document.createElement("div");
                div.className = "business-item";
                div.innerHTML = `
                    <div class="d-flex align-items-start">
                        <div class="me-3">
                            <div class="fw-bold text-center" style="width: 40px; height: 40px; line-height: 40px; border-radius: 50%; background-color: ${color}; color: white; border: 3px solid white; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">${index + 1}</div>
                        </div>
                        <div class="flex-grow-1">
                            <div class="fw-bold mb-1">${business.name}</div>
                            <div class="badge mb-1" style="background-color: ${color}; font-size: 0.7rem;">${business.category.name}</div>
                            ${business.description ? `<div class="small text-muted">${business.description.substring(0, 60)}${business.description.length > 60 ? '...' : ''}</div>` : ''}
                        </div>
                    </div>
                `;
                
                // Click handler to zoom to business and open popup
                div.addEventListener('click', () => {
                    const marker = markerStore.get(business.id);
                    if (marker) {
                        map.setView([business.location.coordinates[1], business.location.coordinates[0]], 15);
                        marker.openPopup();
                    }
                });
                
                listElement.appendChild(div);
            });
            
            // Zoom to show all results
            if (businesses.length > 0) {
                const bounds = L.latLngBounds(
                    businesses.map(b => [b.location.coordinates[1], b.location.coordinates[0]])
                );
                map.fitBounds(bounds, { padding: [50, 50] });
            }
        } catch (error) {
            console.error("Error searching:", error);
            alert("Error searching for businesses. Please try again.");
        }
    });
    
    // Map click to populate search form
    map.on("click", function(e) {
        document.getElementById("latitude").value = e.latlng.lat.toFixed(6);
        document.getElementById("longitude").value = e.latlng.lng.toFixed(6);
    });
    
    // Load initial data
    loadInitialBusinesses();
});