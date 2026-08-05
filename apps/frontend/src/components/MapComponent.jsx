import { useEffect, useRef } from 'react';
import L from 'leaflet';

export default function MapComponent({ geojson }) {
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);
  const geojsonLayerRef = useRef(null);

  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (!mapRef.current) {
      mapRef.current = L.map(mapContainerRef.current).setView([-15.7801, -47.9292], 4);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(mapRef.current);
    }

    const map = mapRef.current;

    if (geojsonLayerRef.current) {
      map.removeLayer(geojsonLayerRef.current);
    }

    if (geojson) {
      const customIcon = L.divIcon({
        html: `
          <svg width="24" height="40" viewBox="0 0 24 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 0C5.37 0 0 5.37 0 12C0 21 12 40 12 40C12 40 24 21 24 12C24 5.37 18.63 0 12 0ZM12 18C8.685 18 6 15.315 6 12C6 8.685 8.685 6 12 6C15.315 6 18 8.685 18 12C18 15.315 15.315 18 12 18Z" fill="#0d6efd"/>
          </svg>
        `,
        className: 'custom-leaflet-marker',
        iconSize: [24, 40],
        iconAnchor: [12, 40],
        popupAnchor: [0, -36]
      });

      const layer = L.geoJSON(geojson, {
        pointToLayer: (geoJsonPoint, latlng) => {
          return L.marker(latlng, { icon: customIcon });
        },
        onEachFeature: (feature, layer) => {
          if (feature.properties && feature.properties.local) {
            layer.bindPopup(
              `<strong>${feature.properties.local}</strong><br/>${feature.properties.descricao}`
            );
          }
        }
      }).addTo(map);

      geojsonLayerRef.current = layer;

      try {
        const bounds = layer.getBounds();
        if (bounds.isValid()) {
          map.fitBounds(bounds, { padding: [40, 40] });
        }
      } catch (e) {
        console.error("Erro ao ajustar zoom", e);
      }
    }
  }, [geojson]);

  return (
    <div className="card shadow-sm border-0 mt-4">
      <div className="card-header bg-dark text-white fw-bold">
        Currículo: Locais de atuação
      </div>
      <div className="card-body p-0">
        <div 
          ref={mapContainerRef} 
          style={{ height: '350px', width: '100%', borderRadius: '0 0 4px 4px' }} 
        />
      </div>
    </div>
  );
}
