//index de prueba ya que no funciono y lo tuve que poner en el html de agregar_item
var apiUrl ='http://localhost:7777/api/cliente';
var apiUrl2 ='http://localhost:5000/api/producto';

// obtener selector  cliente 
fetch(apiUrl).then(function(result){
    if(result.ok){
        return result.json();
    }

}).then(function(data){
    data.forEach(function(element){
        console.log(element);
        let cboCliente=document.getElementById("cboCliente");
        let opt =document.createElement("option");
        opt.appendChild( document.createTextNode(element.razonSocial));
        opt.value=element.id;

        cboCliente.appendChild(opt);

    })
})

//obtener selector productos

fetch(apiUrl2).then(function(result){
    if(result.ok){
        return result.json();
    }

}).then(function(data){
    data.forEach(function(element){
        console.log(element);
        let cboProducto=document.getElementById("cboProducto");
        let opt =document.createElement("option");
        opt.appendChild( document.createTextNode(element.nombreproducto));
        opt.value=element.id;

        cboProducto.appendChild(opt);

    })

})




