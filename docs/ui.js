document
.getElementById("playerSearch")
.addEventListener("input",function(){

 const name = this.value.toLowerCase()

 scene.children.forEach(o=>{

  if(!o.userData) return

  if(!name || (o.userData.player||"")
      .toLowerCase()
      .includes(name))
        o.visible = true
  else
        o.visible = false

 })

})
