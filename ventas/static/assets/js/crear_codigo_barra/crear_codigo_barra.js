$(document).ready(function(){
    $("#frm_codigo_barra").submit(function(evt){
        
        let codigo=$("#codigo").val();

        if(codigo.length>0){

        }else{
            toastr['warning']("Debe de ingresar el codigo a generar")
            evt.preventDefault();
        }



    })
})