

function get_product(clicked_product_id) {
    var selected_product = clicked_product_id.replace("button_id_", "");
    localStorage.setItem("selected_product", selected_product);

}



if (window.location.pathname == "/category/1") {
    $("#cat_1").addClass("selected");
}
else if (window.location.pathname == "/category/2") {
    $("#cat_2").addClass("selected");
}
else if (window.location.pathname == "/category/3") {
    $("#cat_3").addClass("selected");
}
else if (window.location.pathname == "/category/4") {
    $("#cat_4").addClass("selected");
}
else if (window.location.pathname == "/category/5") {
    $("#cat_5").addClass("selected");
}
else if (window.location.pathname == "/category/6") {
    $("#cat_6").addClass("selected");
}
