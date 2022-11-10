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
    $("#monto_real_en_caja").on('input', function(){
        this.value=this.value.replace(/[^0-9,.]/g, '').replace(/,/g, '.');
    });
    alert($("#monto_que_debe_haber_en_caja").val())
    $("#monto_real_en_caja").keyup(function(){
        let monto_real_en_caja= parseFloat($(this).val());
        console.log(monto_real_en_caja)
        let monto_que_debe_haber_en_caja= parseFloat($("#monto_que_debe_haber_en_caja").val().replace(',', '.'));
        console.log(monto_que_debe_haber_en_caja)
        let diferencia=monto_que_debe_haber_en_caja-monto_real_en_caja;
        if(!isNaN(diferencia)){
            if(diferencia==0){
                $("#mostrar_cuadratura").text("La diferencia es "+redondear(diferencia)+" usted esta cuadrado!");
            }else if (diferencia>0){
                $("#mostrar_cuadratura").text("Hay un faltante de "+redondear(diferencia)+" no esta cuadrado");
            }else if(diferencia<0){
                $("#mostrar_cuadratura").text("Hay un sobrante de "+redondear(diferencia)+" no esta cuadrado");  
            }
        }
        
    });

    function redondear(num) {
        var m = Number((Math.abs(num) * 100).toPrecision(15));
        return Math.round(m) / 100 * Math.sign(num);
    }
});