function count_item(item) {  
    $.ajax({
        type: "get",
        url: "count.php",
        data: "item="+item,
        success: function (response) {
        }
    });
}