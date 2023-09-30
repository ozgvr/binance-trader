var favorites = JSON.parse(localStorage.getItem('favorites')) || [];

function handleResponse(res){
    const favorites = JSON.parse(localStorage.getItem('favorites')) || [];
    
    return res.map(item => {
        const newItem = {...item};
        newItem.favorite = favorites.includes(item.name);
        return newItem;
    });

}

function formatName(value, row){
    return value;
}

function formatPrice(value, row){
    return parseFloat(value).toString();
}

function formatFavorite(value, row){
    return "★"
}

function styleFavorite(value, row, index) {
    if (value==true) {
      return {
        classes: "text-warning", css: { cursor: "pointer"}
      }
    }
    return {
        classes: "text-body-tertiary", css: { cursor: "pointer"}
    }
  }

function formatChange(value, row){
    value = parseFloat(value).toFixed(2);

    if(value>0){
        return '<span class="text-success">'+ "+" + value + "%" + '</span>'
    }
    else if(value<0){
        return '<span class="text-danger">' + value + "%" + '</span>'
    }
    return '<span class="text-secondary">' + "-" + value + "%" + '</span>'
}

function addToFavorites(symbol) {
    if(!favorites.includes(item.name))
    favorites.push(symbol);
    localStorage.setItem('favorites', JSON.stringify(favorites));
    favorites = JSON.parse(localStorage.getItem('favorites'));
}

function removeFromFavorites(index) {
    favorites.splice(index, 1);
    localStorage.setItem('favorites', JSON.stringify(favorites));
    favorites = JSON.parse(localStorage.getItem('favorites'));
}

function addToFavorites(symbol) {
    if (!favorites.includes(symbol)) {
        favorites.push(symbol);
        localStorage.setItem('favorites', JSON.stringify(favorites));
    }
}

function removeFromFavorites(symbol) {
    const index = favorites.indexOf(symbol);
    if (index !== -1) {
        favorites.splice(index, 1);
        localStorage.setItem('favorites', JSON.stringify(favorites));
    }
}

$('#list').on('click-cell.bs.table', function (e, field, value, row, element) {
    if (field == "favorite") {
        if (!value) {
            addToFavorites(row.name);
            $('#list').bootstrapTable('load', handleResponse($('#list').bootstrapTable('getData')));
        } else {
            removeFromFavorites(row.name);
            $('#list').bootstrapTable('load', handleResponse($('#list').bootstrapTable('getData')));
        }
    } else {
        location.hash = row.name.slice(0, -4);
        $('#watchlist-offcanvas').offcanvas('hide');
    }
});