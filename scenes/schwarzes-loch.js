// Folge 1: "Was passiert, wenn du in ein Schwarzes Loch fällst?"
let disk, stars, glow, ring, cam;

export default {
  duration: 23,
  fps: 30,
  highlightFirst: false,
  captions: [
    { t0: 0.4, t1: 4.0, text: 'Was passiert, wenn du in ein Schwarzes Loch fällst?' },
    { t0: 4.0, t1: 8.0, text: 'Seine Schwerkraft ist so stark, dass nicht einmal Licht entkommt.' },
    { t0: 8.0, t1: 12.0, text: 'Das Gas um das Loch rast mit fast Lichtgeschwindigkeit.' },
    { t0: 12.0, t1: 16.0, text: 'Je näher du kommst, desto langsamer vergeht deine Zeit …' },
    { t0: 16.0, t1: 19.8, text: '… und dein Körper wird lang gezogen wie Spaghetti.' },
    { t0: 19.8, t1: 23.0, text: 'Folge für mehr 3D-Mysterien!' },
  ],

  setup({ THREE, scene, camera }) {
    cam = camera;
    // Sterne
    const N = 7000, sp = new Float32Array(N * 3), sc = new Float32Array(N * 3);
    let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    for (let i = 0; i < N; i++) {
      const u = rnd() * 2 - 1, th = rnd() * Math.PI * 2, r = 400 + rnd() * 400, s = Math.sqrt(1 - u * u);
      sp.set([r * s * Math.cos(th), r * u, r * s * Math.sin(th)], i * 3);
      const k = 0.5 + rnd() * 0.5, blue = rnd();
      sc.set([k * (0.8 + 0.2 * (1 - blue)), k * 0.9, k * (0.8 + 0.2 * blue)], i * 3);
    }
    const sg = new THREE.BufferGeometry();
    sg.setAttribute('position', new THREE.BufferAttribute(sp, 3));
    sg.setAttribute('color', new THREE.BufferAttribute(sc, 3));
    stars = new THREE.Points(sg, new THREE.PointsMaterial({ size: 1.6, vertexColors: true, sizeAttenuation: false }));
    scene.add(stars);

    // Ereignishorizont
    scene.add(new THREE.Mesh(new THREE.SphereGeometry(1, 64, 64), new THREE.MeshBasicMaterial({ color: 0x000000 })));

    // Photonenring
    ring = new THREE.Mesh(new THREE.TorusGeometry(1.08, 0.025, 16, 200),
      new THREE.MeshBasicMaterial({ color: 0xffe2a8 }));
    scene.add(ring);

    // Glühender Halo (Sprite)
    const c = document.createElement('canvas'); c.width = c.height = 256;
    const g = c.getContext('2d'), grad = g.createRadialGradient(128, 128, 40, 128, 128, 128);
    grad.addColorStop(0, 'rgba(255,170,80,0.0)'); grad.addColorStop(0.32, 'rgba(255,150,60,0.55)');
    grad.addColorStop(0.5, 'rgba(255,90,20,0.18)'); grad.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = grad; g.fillRect(0, 0, 256, 256);
    glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true }));
    glow.scale.set(5, 5, 1); glow.material.opacity = 0.6; glow.renderOrder = -1;
    scene.add(glow);

    // Akkretionsscheibe: Partikel, Kepler-Rotation im Shader
    const M = 60000, rad = new Float32Array(M), ang = new Float32Array(M), hgt = new Float32Array(M), rnds = new Float32Array(M);
    for (let i = 0; i < M; i++) {
      const r = 1.5 + Math.pow(rnd(), 1.8) * 6.5;
      rad[i] = r; ang[i] = rnd() * Math.PI * 2;
      hgt[i] = (rnd() - 0.5) * 0.06 * r * (rnd() < 0.1 ? 3 : 1); rnds[i] = rnd();
    }
    const dg = new THREE.BufferGeometry();
    dg.setAttribute('position', new THREE.BufferAttribute(new Float32Array(M * 3), 3));
    dg.setAttribute('aR', new THREE.BufferAttribute(rad, 1));
    dg.setAttribute('aA', new THREE.BufferAttribute(ang, 1));
    dg.setAttribute('aH', new THREE.BufferAttribute(hgt, 1));
    dg.setAttribute('aRnd', new THREE.BufferAttribute(rnds, 1));
    disk = new THREE.Points(dg, new THREE.ShaderMaterial({
      uniforms: { uTime: { value: 0 }, uScale: { value: 1920.0 }, uDim: { value: 1 } },
      transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
      vertexShader: `
        attribute float aR, aA, aH, aRnd; uniform float uTime, uScale; varying vec3 vCol; varying float vA;
        void main(){
          float a = aA + uTime * 2.6 * pow(aR, -1.5) * 3.0;
          vec3 p = vec3(cos(a)*aR, aH, sin(a)*aR);
          vec4 mv = modelViewMatrix * vec4(p,1.0);
          gl_Position = projectionMatrix * mv;
          gl_PointSize = (0.012 + 0.014*aRnd) * uScale / -mv.z;
          float heat = clamp(1.0 - (aR-1.5)/6.0, 0.0, 1.0);
          // Doppler-Effekt: zum Betrachter hin heller/blauer
          vec3 vel = normalize(vec3(-sin(a), 0.0, cos(a)));
          vec3 toCam = normalize(-mv.xyz);
          float dop = dot(normalize((modelViewMatrix*vec4(vel,0.0)).xyz), toCam);
          vCol = mix(vec3(0.9,0.25,0.05), vec3(1.0,0.85,0.55), heat) * (1.0 + 0.9*dop);
          vCol = mix(vCol, vec3(0.7,0.8,1.0), max(dop,0.0)*0.25*heat);
          vA = 0.35 + 0.65*heat;
        }`,
      fragmentShader: `
        varying vec3 vCol; varying float vA; uniform float uDim;
        void main(){ vec2 d = gl_PointCoord-0.5; float f = smoothstep(0.5,0.0,length(d)); gl_FragColor = vec4(vCol*f*vA*0.45*uDim, f); }`,
    }));
    disk.rotation.z = 0.12;
    ring.rotation.x = Math.PI / 2; ring.rotation.y = 0.12;
    scene.add(disk);
  },

  update(t, { bloom }) {
    disk.material.uniforms.uTime.value = t;
    // Kamerafahrt: von weit weg bis an den Horizont
    const p = Math.min(1, t / 21);
    const ease = p * p * (3 - 2 * p);
    const dist = 16 * Math.pow(1 - ease, 1.3) + 2.2;
    const elev = 0.55 - 0.42 * ease + 0.05 * Math.sin(t * 0.7);
    const az = t * 0.12;
    cam.position.set(Math.sin(az) * dist * Math.cos(elev), Math.sin(elev) * dist, Math.cos(az) * dist * Math.cos(elev));
    cam.lookAt(0, 0, 0);
    // Spaghettifizierung: Sichtfeld weitet sich, Bild streckt sich
    const sp = Math.max(0, (t - 16) / 5);
    cam.fov = 50 + sp * sp * 40;
    cam.scale.set(1, 1 + sp * sp * 0.8, 1);
    cam.updateProjectionMatrix();
    ring.lookAt(cam.position); // Photonenring immer zum Betrachter (Linseneffekt)
    bloom.strength = 0.55 + 0.25 * ease;
    disk.material.uniforms.uDim.value = 1 - 0.85 * Math.min(1, sp);
    stars.rotation.y = t * 0.004;
  },
};
