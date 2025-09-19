/* === File: background_3d.js === */

document.addEventListener('DOMContentLoaded', () => {
    // Ensure three.js is loaded
    if (typeof THREE === 'undefined') {
        console.error('Three.js has not been loaded. Make sure to include it in your HTML.');
        return;
    }

    const canvas = document.getElementById('bg-canvas');
    if (!canvas) {
        console.error('Canvas element with id "bg-canvas" not found.');
        return;
    }

    // Scene setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 15;

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);

    // Earth
    const sphereGeometry = new THREE.SphereGeometry(5, 32, 32);
    // Using a simple, beautiful blue material instead of a texture for reliability and style
    const sphereMaterial = new THREE.MeshStandardMaterial({
        color: 0x0077ff,
        metalness: 0.3,
        roughness: 0.6,
    });
    const earth = new THREE.Mesh(sphereGeometry, sphereMaterial);
    scene.add(earth);

    // Stars
    const starVertices = [];
    for (let i = 0; i < 10000; i++) {
        const x = (Math.random() - 0.5) * 2000;
        const y = (Math.random() - 0.5) * 2000;
        const z = (Math.random() - 0.5) * 2000;
        starVertices.push(x, y, z);
    }
    const starGeometry = new THREE.BufferGeometry();
    starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
    const starMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 0.1 });
    const stars = new THREE.Points(starGeometry, starMaterial);
    scene.add(stars);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
    scene.add(ambientLight);
    const pointLight = new THREE.PointLight(0xffffff, 1.5);
    pointLight.position.set(5, 10, 15);
    scene.add(pointLight);

    // Mouse interaction
    let mouseX = 0;
    let mouseY = 0;
    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX / window.innerWidth) * 2 - 1;
        mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
    });

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);

        // Gentle rotation
        earth.rotation.y += 0.0005;
        stars.rotation.y += 0.0001;

        // Interactive rotation based on mouse position
        earth.rotation.y += mouseX * 0.001;
        earth.rotation.x += mouseY * 0.001;

        renderer.render(scene, camera);
    }
    animate();

    // Handle window resizing
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
});
