// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('canvas'), antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);

// Store the original camera position for resetting
const originalCameraPosition = new THREE.Vector3(0, 50, 100);
camera.position.copy(originalCameraPosition);
camera.lookAt(0, 0, 0);

// Lighting
const sunLight = new THREE.PointLight(0xffffff, 1.5, 500);
sunLight.position.set(0, 0, 0);
scene.add(sunLight);
const ambientLight = new THREE.AmbientLight(0x404040, 0.2);
scene.add(ambientLight);

// Planet data
const planets = [
    { name: 'Mercury', radius: 0.5, distance: 10, speed: 0.02, color: 0xaaaaaa },
    { name: 'Venus', radius: 0.8, distance: 15, speed: 0.015, color: 0xffcc00 },
    { name: 'Earth', radius: 1, distance: 20, speed: 0.01, color: 0x0000ff },
    { name: 'Mars', radius: 0.7, distance: 25, speed: 0.008, color: 0xff0000 },
    { name: 'Jupiter', radius: 2, distance: 35, speed: 0.005, color: 0xffa500 },
    { name: 'Saturn', radius: 1.8, distance: 45, speed: 0.004, color: 0xdeb887 },
    { name: 'Uranus', radius: 1.5, distance: 55, speed: 0.003, color: 0x00ffff },
    { name: 'Neptune', radius: 1.5, distance: 65, speed: 0.002, color: 0x00008b }
];

// Create planets and labels
const planetMeshes = [];
const labels = [];
planets.forEach(planet => {
    const geometry = new THREE.SphereGeometry(planet.radius, 32, 32);
    const material = new THREE.MeshPhongMaterial({ color: planet.color });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.x = planet.distance;
    mesh.userData = { ...planet, angle: 0 };
    scene.add(mesh);
    planetMeshes.push(mesh);

    // Create label
    const canvas = document.createElement('canvas');
    canvas.width = 128;
    canvas.height = 32;
    const context = canvas.getContext('2d');
    context.fillStyle = 'white';
    context.font = '20px Arial';
    context.fillText(planet.name, 0, 20);
    const texture = new THREE.CanvasTexture(canvas);
    const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
    const sprite = new THREE.Sprite(spriteMaterial);
    sprite.scale.set(5, 1.25, 1);
    sprite.position.set(planet.distance, planet.radius + 2, 0);
    scene.add(sprite);
    labels.push(sprite);
});

// Create Sun
const sunGeometry = new THREE.SphereGeometry(5, 32, 32);
const sunMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00 });
const sun = new THREE.Mesh(sunGeometry, sunMaterial);
scene.add(sun);

// Background stars
const starGeometry = new THREE.BufferGeometry();
const starCount = 1000;
const starPositions = new Float32Array(starCount * 3);
for (let i = 0; i < starCount * 3; i++) {
    starPositions[i] = (Math.random() - 0.5) * 1000;
}
starGeometry.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
const starMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 0.5 });
const stars = new THREE.Points(starGeometry, starMaterial);
scene.add(stars);

// Animation and speed control
const clock = new THREE.Clock();
let isPaused = false;
const slidersContainer = document.getElementById('sliders');
planets.forEach((planet, index) => {
    const container = document.createElement('div');
    container.className = 'slider-container';
    container.innerHTML = `
        <label>${planet.name} Speed: <span id="speed${planet.name}">${planet.speed.toFixed(3)}</span></label>
        <input type="range" min="0" max="0.05" step="0.001" value="${planet.speed}" id="slider${planet.name}">
    `;
    slidersContainer.appendChild(container);
    document.getElementById(`slider${planet.name}`).addEventListener('input', (e) => {
        planetMeshes[index].userData.speed = parseFloat(e.target.value);
        document.getElementById(`speed${planet.name}`).textContent = e.target.value;
    });
});

// Pause/Resume button
document.getElementById('pauseResume').addEventListener('click', () => {
    isPaused = !isPaused;
    document.getElementById('pauseResume').textContent = isPaused ? 'Resume' : 'Pause';
});

// Raycaster for detecting clicks on planets
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

// Zoom animation state
let targetCameraPosition = null;
let isZooming = false;
const zoomSpeed = 0.05; // Controls how fast the camera zooms

// Click event to zoom in on a planet
document.getElementById('canvas').addEventListener('click', (event) => {
    // Calculate mouse position in normalized device coordinates (-1 to +1)
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    // Update the raycaster with the camera and mouse position
    raycaster.setFromCamera(mouse, camera);

    // Check for intersections with planet meshes
    const intersects = raycaster.intersectObjects(planetMeshes);
    if (intersects.length > 0) {
        const clickedPlanet = intersects[0].object;
        // Set the target camera position to zoom in (slightly above the planet to see the label)
        const planetPos = clickedPlanet.position.clone();
        targetCameraPosition = new THREE.Vector3(
            planetPos.x,
            planetPos.y + clickedPlanet.userData.radius + 5, // Position above the planet
            planetPos.z + 10 // Zoom in close, but not too close
        );
        isZooming = true;
    }
});

// Double-click to reset camera position
document.getElementById('canvas').addEventListener('dblclick', () => {
    targetCameraPosition = originalCameraPosition.clone();
    isZooming = true;
});

// Animation loop with camera zoom
function animate() {
    requestAnimationFrame(animate);

    // Handle camera zoom animation
    if (isZooming && targetCameraPosition) {
        camera.position.lerp(targetCameraPosition, zoomSpeed);
        camera.lookAt(0, 0, 0); // Keep looking at the center (Sun) for a natural feel
        // Stop zooming when close enough to the target
        if (camera.position.distanceTo(targetCameraPosition) < 0.1) {
            isZooming = false;
        }
    }

    if (!isPaused) {
        const delta = clock.getDelta();
        planetMeshes.forEach((mesh, index) => {
            mesh.userData.angle += mesh.userData.speed * delta * 60;
            mesh.position.x = mesh.userData.distance * Math.cos(mesh.userData.angle);
            mesh.position.z = mesh.userData.distance * Math.sin(mesh.userData.angle);

            // Update label position to follow the planet
            labels[index].position.set(
                mesh.position.x,
                mesh.position.y + mesh.userData.radius + 2,
                mesh.position.z
            );
        });
    }
    renderer.render(scene, camera);
}
animate();

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});