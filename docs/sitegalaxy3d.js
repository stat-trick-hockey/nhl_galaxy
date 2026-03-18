const scene = new THREE.Scene()

const camera = new THREE.PerspectiveCamera(
75,
window.innerWidth / 800,
0.1,
1000
)

const renderer = new THREE.WebGLRenderer()

renderer.setSize(window.innerWidth,800)

document
.getElementById("viewer")
.appendChild(renderer.domElement)

camera.position.z = 60

fetch("embedded_goals.json")
.then(r=>r.json())
.then(goals=>{

window.goals = goals

goals.forEach(g=>{

 const geometry = new THREE.SphereGeometry(.2)

 const color = new THREE.Color(
   `hsl(${g.cluster*40},80%,60%)`
 )

 const material = new THREE.MeshBasicMaterial({color})

 const star = new THREE.Mesh(geometry,material)

 star.position.x = g.gx*3
 star.position.y = g.gy*3
 star.position.z = g.gz*3

 star.userData = g

 scene.add(star)

})

})

function animate(){

 requestAnimationFrame(animate)

 scene.rotation.y += 0.0008

 renderer.render(scene,camera)

}

animate()
