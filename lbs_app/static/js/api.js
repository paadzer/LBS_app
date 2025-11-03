const Api = {
    async fetchBusinesses() {
        const response = await fetch("/api/businesses/");
        if (!response.ok) throw new Error("Failed to fetch businesses");
        const data = await response.json();
        return data.results || data; // Handle paginated or non-paginated responses
    },
    
    async fetchNearby(lat, lon, radius) {
        const url = `/api/businesses/nearby/?lat=${lat}&lon=${lon}&radius=${radius}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch nearby businesses");
        return response.json();
    },
    
    async fetchNearest(lat, lon, limit = 3) {
        const url = `/api/businesses/nearest/?lat=${lat}&lon=${lon}&limit=${limit}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch nearest businesses");
        return response.json();
    },
    
    async fetchWithinArea(areaName) {
        const url = `/api/businesses/within-area/?name=${areaName}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch businesses in area");
        return response.json();
    },
    
    async searchByName(name) {
        const url = `/api/businesses/?search=${encodeURIComponent(name)}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to search businesses");
        const data = await response.json();
        return data.results || data; // Handle paginated or non-paginated responses
    }
};