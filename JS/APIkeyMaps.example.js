const GOOGLE_MAPS_KEY = "TU_API_KEY_AQUI";  // tu clave real

const script = document.createElement('script');
script.src = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_KEY}`
script.async = true;
script.defer = true;
document.head.appendChild(script);