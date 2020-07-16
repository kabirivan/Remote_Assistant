const assist = document.getElementById("assist")

function call_assist(event) {
    event.preventDefault();
    console.log("boton presionado")
    var promisse = new Promise ((resolve,reject) =>{
        fetch('/chat_assis/', {
            method: 'POST',
            body: 'Poner pantalla asistente'
        }).then(doc=>{
            resolve()
        }).catch(
            ()=>{
                reject()
            }
        )
    })

}

assist.addEventListener('click', call_assist)

