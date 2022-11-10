function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(document).ready(function(){
    $("#btn_crear_venta").click(function(evt){
        let url_verificar_apertura_activa_usuario=$("#url_verificar_apertura_activa_usuario").val();
        const csrftoken=getCookie("csrftoken");
        $.ajax({
            url:url_verificar_apertura_activa_usuario,
            type:"POST",
            data:{
                csrfmiddlewaretoken:csrftoken,
            },
            dataType:'json',
            success:function(data){
              let res=data.res;
              console.log(typeof(res))
              console.log(data);
              //si res lanza true entonces es que existe una apertura vigente
              if(res==1){
                let url_crear_venta=$("#url_crear_venta").val();
                window.open(url_crear_venta, '_parent')
              }else if(res==2){
                console.log("Hola Entro aqui");
                let nombre_usuario_de_la_apertura_responsable=data.nombre_usuario;
                toastr['warning']("Hay una apertura activa a cargo de "+nombre_usuario_de_la_apertura_responsable+" para que usted pueda seguir vendiendo es necesario que este usuario se cuadre y haga corte");
              }
              
            }
        })
    });
});