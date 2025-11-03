/**
 * API Client for communicating with the Django REST API
 * 
 * This object contains functions to fetch data from the backend API endpoints.
 * All functions are async (return Promises) and use the Fetch API.
 */
const Api = {
    /**
     * Fetch all businesses from the API
     * @returns {Promise<Array>} Array of business objects
     */
    async fetchBusinesses() {
        const response = await fetch("/api/businesses/");
        if (!response.ok) throw new Error("Failed to fetch businesses");
        const data = await response.json();
        // Handle both paginated responses (data.results) and direct arrays (data)
        return data.results || data;
    },
    
    /**
     * Fetch businesses within a radius (Spatial Query #1: Proximity Search)
     * @param {number} lat - Latitude of the search center
     * @param {number} lon - Longitude of the search center
     * @param {number} radius - Search radius in meters
     * @returns {Promise<Array>} Array of nearby business objects
     */
    async fetchNearby(lat, lon, radius) {
        const url = `/api/businesses/nearby/?lat=${lat}&lon=${lon}&radius=${radius}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch nearby businesses");
        return response.json();
    },
    
    /**
     * Fetch the N nearest businesses (Spatial Query #2: Nearest Neighbor)
     * @param {number} lat - Latitude of the search center
     * @param {number} lon - Longitude of the search center
     * @param {number} limit - Number of results to return (default: 3)
     * @returns {Promise<Array>} Array of nearest business objects
     */
    async fetchNearest(lat, lon, limit = 3) {
        const url = `/api/businesses/nearest/?lat=${lat}&lon=${lon}&limit=${limit}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch nearest businesses");
        return response.json();
    },
    
    /**
     * Fetch businesses within a specific service area (Spatial Query #3: Containment)
     * @param {string} areaName - Name of the service area
     * @returns {Promise<Array>} Array of businesses in the area
     */
    async fetchWithinArea(areaName) {
        const url = `/api/businesses/within-area/?name=${areaName}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch businesses in area");
        return response.json();
    },
    
    /**
     * Search businesses by name or description
     * @param {string} name - Search term to find in business names or descriptions
     * @returns {Promise<Array>} Array of matching business objects
     */
    async searchByName(name) {
        const url = `/api/businesses/?search=${encodeURIComponent(name)}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to search businesses");
        const data = await response.json();
        // Handle both paginated responses (data.results) and direct arrays (data)
        return data.results || data;
    }
};