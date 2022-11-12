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

    $("#btn_cerrar_caja").click(function(evt){
        evt.preventDefault();
        let url_cerrar_caja = $("#url_cerrar_caja").val();
        let id_apertura=$("#id_apertura").val();
        const csrftoken=getCookie('csrftoken');
        let datos = {
            csrfmiddlewaretoken:csrftoken,
            'id_apertura':id_apertura,
        };
        console.log(datos);
        $.ajax({
            url:url_cerrar_caja,
            type:'POST',
            data:datos,
            dataType:'json',
            success:function(data){
                console.log(data)
                let res=data.res;
                if(res==true){
                    toastr['success']("Cierre realizado correctamente!!");
                    let list_apertura_corte = $("#list_apertura_corte").val();
                    console.log(list_apertura_corte)
                    window.open(list_apertura_corte, '_parent');
                }
            }
        });
        
    });

})